"""Playwright Configuration for Cross-Browser Testing.

Defines browser configurations, devices, and test settings for
comprehensive UI/UX testing across platforms.
"""

from typing import Dict

# Browser configurations
BROWSERS = {
    "chromium": {
        "name": "Chromium",
        "headless": True,
        "args": ["--disable-dev-shm-usage"],
    },
    "webkit": {
        "name": "WebKit (Safari)",
        "headless": True,
        "args": [],
    },
    "firefox": {
        "name": "Firefox",
        "headless": True,
        "args": [],
    },
}

# Device emulation configurations
DEVICES = {
    "desktop_mac": {
        "name": "Desktop Mac",
        "viewport": {"width": 1920, "height": 1080},
        "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
        "device_scale_factor": 2,
        "is_mobile": False,
        "has_touch": False,
    },
    "desktop_windows": {
        "name": "Desktop Windows",
        "viewport": {"width": 1920, "height": 1080},
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "device_scale_factor": 1,
        "is_mobile": False,
        "has_touch": False,
    },
    "ipad_pro": {
        "name": "iPad Pro 12.9",
        "viewport": {"width": 1024, "height": 1366},
        "user_agent": "Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
        "device_scale_factor": 2,
        "is_mobile": True,
        "has_touch": True,
    },
    "ipad_air": {
        "name": "iPad Air",
        "viewport": {"width": 820, "height": 1180},
        "user_agent": "Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
        "device_scale_factor": 2,
        "is_mobile": True,
        "has_touch": True,
    },
}

# Test configuration
TEST_CONFIG = {
    "base_url": "http://localhost:8502",
    "timeout": 30000,  # 30 seconds
    "screenshot_on_failure": True,
    "screenshot_dir": "tests/ui_tests/screenshots",
    "video_on_failure": True,
    "video_dir": "tests/ui_tests/videos",
    "trace_on_failure": True,
    "trace_dir": "tests/ui_tests/traces",
}

# Critical user flows to test
USER_FLOWS = [
    "file_upload",
    "preview_edit",
    "attendee_management",
    "batch_download",
    "settings_configuration",
]

# Safari-specific tests (regex issues, webkit quirks)
SAFARI_SPECIFIC_TESTS = [
    "network_url_display",
    "markdown_rendering",
    "file_download",
    "clipboard_operations",
]
