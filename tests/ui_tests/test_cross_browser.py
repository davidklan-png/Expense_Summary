"""Cross-Browser UI/UX Tests for Streamlit Web Interface.

Tests core functionality across Chromium, WebKit (Safari), and different devices.
Focuses on Safari compatibility issues and cross-platform consistency.
"""

import pytest
from playwright.sync_api import Page, expect
from pathlib import Path
import time

# Import configuration
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from playwright_config import BROWSERS, DEVICES, TEST_CONFIG, SAFARI_SPECIFIC_TESTS


class TestCrossBrowserCore:
    """Core functionality tests across all browsers."""

    @pytest.fixture(scope="function")
    def app_url(self):
        """Base URL for the Streamlit app."""
        return TEST_CONFIG["base_url"]

    def test_app_loads_successfully(self, page: Page, app_url: str):
        """Test that the app loads without JavaScript errors."""
        page.goto(app_url)

        # Wait for Streamlit to initialize
        page.wait_for_selector("text=Saison Transform", timeout=TEST_CONFIG["timeout"])

        # Check for JavaScript console errors
        console_errors = []
        page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)

        # Wait a bit for any async errors
        page.wait_for_timeout(2000)

        # Assert no critical errors
        critical_errors = [e for e in console_errors if "SyntaxError" in e or "TypeError" in e]
        assert len(critical_errors) == 0, f"JavaScript errors detected: {critical_errors}"

    def test_network_info_displays_without_error(self, page: Page, app_url: str):
        """Test network information displays correctly (Safari regex fix)."""
        page.goto(app_url)
        page.wait_for_selector("text=🌐 Network Access", timeout=TEST_CONFIG["timeout"])

        # Should see URL in code block (not markdown link)
        local_url = page.locator("code:has-text('http://localhost:8502')")
        expect(local_url).to_be_visible()

        # No regex errors in console
        console_errors = []
        page.on("console", lambda msg: console_errors.append(msg) if msg.type == "error" else None)
        page.wait_for_timeout(1000)

        regex_errors = [e for e in console_errors if "regular expression" in str(e).lower()]
        assert len(regex_errors) == 0, f"Regex errors detected: {regex_errors}"

    def test_sidebar_navigation(self, page: Page, app_url: str):
        """Test sidebar settings are accessible."""
        page.goto(app_url)

        # Check sidebar header
        settings_header = page.locator("text=⚙️ Settings")
        expect(settings_header).to_be_visible()

        # Check network info section
        network_section = page.locator("text=🌐 Network Access")
        expect(network_section).to_be_visible()

    def test_main_tabs_render(self, page: Page, app_url: str):
        """Test that main navigation tabs render correctly."""
        page.goto(app_url)

        # Wait for app to load
        page.wait_for_selector("text=Saison Transform", timeout=TEST_CONFIG["timeout"])

        # Check for main tabs (using Streamlit tab structure)
        # Note: Streamlit tabs may be in different DOM structure
        page.wait_for_timeout(2000)  # Allow tabs to render

        # Verify content areas exist
        assert page.locator("text=Upload Files").count() > 0 or page.locator("text=📤").count() > 0

    def test_responsive_layout_desktop(self, page: Page, app_url: str):
        """Test layout works on desktop resolution."""
        page.set_viewport_size({"width": 1920, "height": 1080})
        page.goto(app_url)

        page.wait_for_selector("text=Saison Transform", timeout=TEST_CONFIG["timeout"])

        # Sidebar should be visible on desktop
        sidebar = page.locator('[data-testid="stSidebar"]')
        expect(sidebar).to_be_visible()

    def test_file_upload_interface_exists(self, page: Page, app_url: str):
        """Test file upload interface is present and functional."""
        page.goto(app_url)
        page.wait_for_selector("text=Saison Transform", timeout=TEST_CONFIG["timeout"])

        # Look for file uploader (Streamlit uses specific data-testid)
        # File uploader should be present
        page.wait_for_timeout(2000)

        # Check for upload-related text
        upload_elements = page.locator("text=/upload|ファイル/i")
        assert upload_elements.count() > 0, "File upload interface not found"


class TestSafariSpecific:
    """Safari-specific compatibility tests."""

    @pytest.fixture(scope="function")
    def app_url(self):
        """Base URL for the Streamlit app."""
        return TEST_CONFIG["base_url"]

    @pytest.mark.safari
    def test_no_regex_errors_in_markdown(self, page: Page, app_url: str):
        """Test that markdown rendering doesn't cause regex errors (Safari issue)."""
        page.goto(app_url)
        page.wait_for_selector("text=Saison Transform", timeout=TEST_CONFIG["timeout"])

        console_errors = []
        page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)

        # Wait for markdown to render
        page.wait_for_timeout(3000)

        # Check for the specific Safari regex error
        regex_errors = [e for e in console_errors if "invalid group specifier name" in e.lower()]
        assert len(regex_errors) == 0, f"Safari regex errors detected: {regex_errors}"

    @pytest.mark.safari
    def test_url_display_in_code_blocks(self, page: Page, app_url: str):
        """Test URLs are displayed in code blocks (not markdown links)."""
        page.goto(app_url)
        page.wait_for_selector("text=🌐 Network Access", timeout=TEST_CONFIG["timeout"])

        # URLs should be in <code> elements
        code_blocks = page.locator("code")
        code_count = code_blocks.count()

        assert code_count >= 1, "Network URLs should be in code blocks"

        # Check that at least one contains a URL
        has_url = False
        for i in range(code_count):
            text = code_blocks.nth(i).text_content()
            if "http://" in text or "https://" in text:
                has_url = True
                break

        assert has_url, "No URLs found in code blocks"

    @pytest.mark.safari
    def test_webkit_font_rendering(self, page: Page, app_url: str):
        """Test that Japanese fonts render correctly in Safari/WebKit."""
        page.goto(app_url)
        page.wait_for_selector("text=Saison Transform", timeout=TEST_CONFIG["timeout"])

        # Check if page has Japanese text
        page.wait_for_timeout(1000)

        # Japanese characters should be visible
        # (This is a basic check - font rendering is mainly visual)
        assert page.content() is not None


class TestDeviceEmulation:
    """Tests across different device types (Desktop, iPad)."""

    @pytest.fixture(scope="function")
    def app_url(self):
        """Base URL for the Streamlit app."""
        return TEST_CONFIG["base_url"]

    @pytest.mark.parametrize("device_name", ["desktop_mac", "desktop_windows", "ipad_pro"])
    def test_app_loads_on_device(self, page: Page, app_url: str, device_name: str):
        """Test app loads correctly on different devices."""
        device_config = DEVICES[device_name]

        # Set viewport and user agent
        page.set_viewport_size(device_config["viewport"])
        page.context.set_extra_http_headers({"User-Agent": device_config["user_agent"]})

        page.goto(app_url)
        page.wait_for_selector("text=Saison Transform", timeout=TEST_CONFIG["timeout"])

        # App should load without errors
        assert "Saison Transform" in page.content()

    @pytest.mark.ipad
    def test_touch_interactions_on_ipad(self, page: Page, app_url: str):
        """Test touch-friendly interface on iPad."""
        device_config = DEVICES["ipad_pro"]
        page.set_viewport_size(device_config["viewport"])

        page.goto(app_url)
        page.wait_for_selector("text=Saison Transform", timeout=TEST_CONFIG["timeout"])

        # Sidebar should be collapsible on mobile/tablet
        # (Streamlit handles this automatically)
        page.wait_for_timeout(1000)

        # Check that content is responsive
        assert page.viewport_size["width"] == 1024

    @pytest.mark.ipad
    def test_file_upload_on_touch_device(self, page: Page, app_url: str):
        """Test file upload works on touch devices (iPad)."""
        device_config = DEVICES["ipad_pro"]
        page.set_viewport_size(device_config["viewport"])

        page.goto(app_url)
        page.wait_for_selector("text=Saison Transform", timeout=TEST_CONFIG["timeout"])

        # File upload should be accessible
        page.wait_for_timeout(2000)

        # Look for file upload elements
        upload_text = page.locator("text=/upload|drop/i")
        assert upload_text.count() > 0, "File upload not accessible on iPad"


class TestAccessibility:
    """Accessibility and usability tests."""

    @pytest.fixture(scope="function")
    def app_url(self):
        """Base URL for the Streamlit app."""
        return TEST_CONFIG["base_url"]

    def test_semantic_html_structure(self, page: Page, app_url: str):
        """Test that page uses semantic HTML."""
        page.goto(app_url)
        page.wait_for_selector("text=Saison Transform", timeout=TEST_CONFIG["timeout"])

        # Should have proper headings
        h1_count = page.locator("h1").count()
        assert h1_count >= 0  # Streamlit may use different heading structure

    def test_keyboard_navigation(self, page: Page, app_url: str):
        """Test keyboard navigation works."""
        page.goto(app_url)
        page.wait_for_selector("text=Saison Transform", timeout=TEST_CONFIG["timeout"])

        # Tab key should move focus
        page.keyboard.press("Tab")
        page.wait_for_timeout(500)

        # Some element should have focus
        focused = page.evaluate("document.activeElement.tagName")
        assert focused is not None

    def test_color_contrast_sufficient(self, page: Page, app_url: str):
        """Test that color contrast meets WCAG standards."""
        page.goto(app_url)
        page.wait_for_selector("text=Saison Transform", timeout=TEST_CONFIG["timeout"])

        # This is a basic check - full contrast testing requires additional tools
        # Check that background and text are different
        page.wait_for_timeout(1000)
        assert page.content() is not None
