# UI/UX Cross-Browser Testing Suite

Comprehensive automated testing for the Streamlit web interface across different browsers and devices.

## Overview

This testing suite ensures consistent functionality and user experience across:
- **Browsers**: Chromium, WebKit (Safari), Firefox
- **Devices**: Desktop (Mac/Windows), iPad Pro, iPad Air
- **Platforms**: macOS, Windows, Linux

## Why Cross-Browser Testing?

The Streamlit app has specific compatibility requirements:
- **Safari**: Older JavaScript engine requires special handling (regex issues)
- **WebKit**: Different rendering engine than Chromium
- **Touch Devices**: iPad requires touch-friendly UI testing

## Test Categories

### 1. Core Functionality Tests
- App loading and initialization
- Network information display (Safari regex fix)
- Sidebar navigation
- Tab rendering
- Responsive layout

### 2. Safari-Specific Tests
- No regex errors in markdown rendering
- URL display in code blocks (not markdown links)
- WebKit font rendering for Japanese text

### 3. Device Emulation Tests
- Desktop Mac (1920x1080, Retina)
- Desktop Windows (1920x1080)
- iPad Pro 12.9" (1024x1366, touch)
- iPad Air (820x1180, touch)

### 4. Accessibility Tests
- Semantic HTML structure
- Keyboard navigation
- Color contrast (WCAG compliance)

## Setup

### Install Dependencies

```bash
# Install Python dependencies
pip install -r requirements.txt

# Install Playwright and browsers
pip install pytest pytest-playwright
playwright install
```

### Install Specific Browsers

```bash
# Install only Chromium
playwright install chromium

# Install WebKit (Safari engine)
playwright install webkit

# Install all browsers
playwright install
```

## Running Tests

### Run All Tests (Chromium)

```bash
pytest tests/ui_tests/ -v
```

### Run Safari/WebKit Tests

```bash
pytest tests/ui_tests/ -v --browser webkit
```

### Run Safari-Specific Tests Only

```bash
pytest tests/ui_tests/test_cross_browser.py::TestSafariSpecific -v
```

### Run Device Emulation Tests

```bash
pytest tests/ui_tests/test_cross_browser.py::TestDeviceEmulation -v
```

### Run with Specific Device

```bash
# iPad Pro tests
pytest tests/ui_tests/ -v -m ipad

# Desktop Mac tests
pytest tests/ui_tests/ -v -m desktop_mac
```

### Run Tests in Headed Mode (See Browser)

```bash
pytest tests/ui_tests/ -v --headed
```

## Test Configuration

### Browser Configuration (`playwright_config.py`)

```python
BROWSERS = {
    "chromium": {...},
    "webkit": {...},      # Safari engine
    "firefox": {...}
}
```

### Device Profiles

```python
DEVICES = {
    "desktop_mac": {
        "viewport": {"width": 1920, "height": 1080},
        "device_scale_factor": 2,  # Retina display
        ...
    },
    "ipad_pro": {
        "viewport": {"width": 1024, "height": 1366},
        "has_touch": True,
        ...
    }
}
```

## Debugging Failed Tests

### Screenshots

Screenshots are automatically saved on test failure:

```
tests/ui_tests/screenshots/
└── test_name.png
```

### Traces

Playwright traces are saved for debugging:

```
tests/ui_tests/traces/
└── test_name.zip
```

View traces with:

```bash
playwright show-trace tests/ui_tests/traces/test_name.zip
```

### Console Logs

Tests capture JavaScript console errors:

```python
console_errors = []
page.on("console", lambda msg: console_errors.append(msg))
```

## CI/CD Integration

### GitHub Actions Workflow

Tests run automatically on:
- Push to `develop` or `main` branches
- Pull requests
- Changes to frontend files:
  - `web_app.py`
  - `src/saisonxform/ui/**`
  - `src/saisonxform/templates/**`
  - `.streamlit/**`

### Workflow Jobs

1. **ui-tests-chromium**: Chromium/Chrome tests on Ubuntu
2. **ui-tests-webkit**: WebKit/Safari tests on macOS
3. **ui-tests-devices**: Device emulation tests (all devices)

### Viewing Results

- ✅ Green checkmark: All tests passed
- ❌ Red X: Tests failed
- Click "Details" to see logs and download artifacts (screenshots, traces)

## Common Issues & Solutions

### Safari Regex Errors

**Problem**: `SyntaxError: Invalid regular expression: invalid group specifier name`

**Solution**: Use `st.code()` instead of markdown links for URLs

```python
# ❌ Causes Safari error
st.markdown(f"[{url}]({url})")

# ✅ Safari compatible
st.code(url, language="")
```

### Streamlit App Not Starting

**Problem**: Tests fail because app isn't ready

**Solution**: Increase startup wait time

```bash
streamlit run web_app.py &
sleep 10  # Wait for app to start
```

### WebKit Not Installed on macOS

**Problem**: `webkit` binary not found

**Solution**: Install with Playwright

```bash
playwright install webkit
```

## Writing New Tests

### Test Structure

```python
class TestNewFeature:
    """Tests for new feature."""

    @pytest.fixture(scope="class")
    def base_url(self):
        return TEST_CONFIG["base_url"]

    def test_feature_works(self, page: Page, base_url: str):
        """Test description."""
        page.goto(base_url)
        page.wait_for_selector("text=Expected Text")
        # Assertions here
```

### Using Markers

```python
@pytest.mark.safari  # Safari-specific test
@pytest.mark.ipad    # iPad device emulation
@pytest.mark.webkit  # Run on WebKit browser
def test_example(page: Page):
    ...
```

### Best Practices

1. **Use Explicit Waits**: `page.wait_for_selector()` instead of `time.sleep()`
2. **Check Console Errors**: Capture JavaScript errors in tests
3. **Test Responsiveness**: Test on multiple viewport sizes
4. **Screenshot on Failure**: Already configured automatically
5. **Use Semantic Selectors**: Prefer text content over CSS selectors

## Test Markers

- `@pytest.mark.webkit`: Run on WebKit (Safari)
- `@pytest.mark.firefox`: Run on Firefox
- `@pytest.mark.safari`: Safari-specific functionality
- `@pytest.mark.ipad`: iPad device emulation
- `@pytest.mark.desktop_mac`: Mac desktop emulation
- `@pytest.mark.desktop_windows`: Windows desktop emulation

## Performance

### Test Execution Time

- Chromium tests: ~2-3 minutes
- WebKit tests: ~3-4 minutes (macOS only)
- Device emulation: ~2 minutes per device

### Parallel Execution

Run tests in parallel for faster execution:

```bash
pytest tests/ui_tests/ -n auto  # Requires pytest-xdist
```

## Maintenance

### Updating Browser Versions

```bash
playwright install --with-deps
```

### Adding New Device Profiles

Edit `playwright_config.py`:

```python
DEVICES = {
    "new_device": {
        "name": "Device Name",
        "viewport": {"width": ..., "height": ...},
        "user_agent": "...",
        ...
    }
}
```

### Adding New Test Scenarios

1. Add test to `test_cross_browser.py`
2. Use appropriate class (`TestCrossBrowserCore`, `TestSafariSpecific`, etc.)
3. Add markers if needed
4. Run locally before pushing

## Resources

- [Playwright Documentation](https://playwright.dev/python/)
- [Streamlit Testing Guide](https://docs.streamlit.io/library/advanced-features/testing)
- [pytest Documentation](https://docs.pytest.org/)

## Support

For issues with UI tests:
1. Check test logs and screenshots
2. View Playwright traces
3. Run tests locally with `--headed` to see browser
4. Open GitHub issue with test failure details

---

**Last Updated**: 2025-11-29
**Playwright Version**: 1.40+
**Python Version**: 3.10+
