"""Pytest Configuration for UI Tests.

Provides fixtures and configuration for Playwright-based UI testing.
"""

import pytest
from pathlib import Path
import sys

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Conditional import - only available when playwright is installed
try:
    from playwright.sync_api import sync_playwright, Browser, Page, BrowserContext
    from playwright_config import BROWSERS, DEVICES, TEST_CONFIG

    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    # Skip this entire conftest if playwright is not available
    pytest.skip("Playwright not installed - skipping UI tests", allow_module_level=True)


@pytest.fixture(scope="session")
def browser_type_name(request):
    """Get browser type from pytest markers or default to chromium."""
    # Check for browser markers
    if request.node.get_closest_marker("webkit"):
        return "webkit"
    elif request.node.get_closest_marker("firefox"):
        return "firefox"
    else:
        return "chromium"


@pytest.fixture(scope="session")
def playwright():
    """Start Playwright."""
    with sync_playwright() as p:
        yield p


@pytest.fixture(scope="session")
def browser(playwright, browser_type_name):
    """Launch browser for the session."""
    browser_config = BROWSERS.get(browser_type_name, BROWSERS["chromium"])

    if browser_type_name == "chromium":
        browser = playwright.chromium.launch(headless=browser_config["headless"], args=browser_config["args"])
    elif browser_type_name == "webkit":
        browser = playwright.webkit.launch(headless=browser_config["headless"], args=browser_config["args"])
    elif browser_type_name == "firefox":
        browser = playwright.firefox.launch(headless=browser_config["headless"], args=browser_config["args"])
    else:
        browser = playwright.chromium.launch()

    yield browser
    browser.close()


@pytest.fixture(scope="function")
def context(browser, request):
    """Create a new browser context for each test."""
    # Check if test has device marker
    device_name = None
    if request.node.get_closest_marker("ipad"):
        device_name = "ipad_pro"
    elif request.node.get_closest_marker("desktop_mac"):
        device_name = "desktop_mac"
    elif request.node.get_closest_marker("desktop_windows"):
        device_name = "desktop_windows"

    # Create context with device emulation if specified
    if device_name and device_name in DEVICES:
        device_config = DEVICES[device_name]
        context = browser.new_context(
            viewport=device_config["viewport"],
            user_agent=device_config["user_agent"],
            device_scale_factor=device_config["device_scale_factor"],
            is_mobile=device_config["is_mobile"],
            has_touch=device_config["has_touch"],
        )
    else:
        context = browser.new_context()

    # Enable tracing for debugging
    if TEST_CONFIG.get("trace_on_failure"):
        context.tracing.start(screenshots=True, snapshots=True)

    yield context

    # Save trace on failure
    if TEST_CONFIG.get("trace_on_failure") and request.node.rep_call.failed:
        trace_dir = Path(TEST_CONFIG["trace_dir"])
        trace_dir.mkdir(parents=True, exist_ok=True)
        trace_path = trace_dir / f"{request.node.name}.zip"
        context.tracing.stop(path=str(trace_path))
    else:
        context.tracing.stop()

    context.close()


@pytest.fixture(scope="function")
def page(context, request):
    """Create a new page for each test."""
    page = context.new_page()

    # Set default timeout
    page.set_default_timeout(TEST_CONFIG["timeout"])

    yield page

    # Screenshot on failure
    if TEST_CONFIG.get("screenshot_on_failure") and hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        screenshot_dir = Path(TEST_CONFIG["screenshot_dir"])
        screenshot_dir.mkdir(parents=True, exist_ok=True)
        screenshot_path = screenshot_dir / f"{request.node.name}.png"
        page.screenshot(path=str(screenshot_path))

    page.close()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Make test result available to fixtures."""
    outcome = yield
    rep = outcome.get_result()

    # Store the result in the item for fixture access
    setattr(item, f"rep_{rep.when}", rep)


def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line("markers", "webkit: mark test to run on WebKit (Safari)")
    config.addinivalue_line("markers", "firefox: mark test to run on Firefox")
    config.addinivalue_line("markers", "safari: mark test for Safari-specific functionality")
    config.addinivalue_line("markers", "ipad: mark test for iPad device emulation")
    config.addinivalue_line("markers", "desktop_mac: mark test for Mac desktop")
    config.addinivalue_line("markers", "desktop_windows: mark test for Windows desktop")
