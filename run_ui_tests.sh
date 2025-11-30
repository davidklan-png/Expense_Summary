#!/bin/bash
# Quick start script for UI/UX cross-browser tests

set -e

echo "🧪 Saison Transform UI/UX Test Runner"
echo "======================================"
echo ""

# Check if virtual environment is activated
if [[ -z "$VIRTUAL_ENV" ]]; then
    if [ -f ".venv/bin/activate" ]; then
        echo "📦 Activating virtual environment..."
        source .venv/bin/activate
    else
        echo "⚠️  Warning: No virtual environment found"
    fi
fi

# Check if Playwright is installed
if ! command -v playwright &> /dev/null; then
    echo "📥 Installing Playwright..."
    pip install pytest pytest-playwright
    playwright install
fi

# Parse arguments
BROWSER="${1:-chromium}"
MODE="${2:-all}"

echo "🌐 Browser: $BROWSER"
echo "📋 Test mode: $MODE"
echo ""

# Start Streamlit app in background
echo "🚀 Starting Streamlit app..."
export SAISONXFORM_SKIP_GIT_VALIDATION=1
streamlit run web_app.py --server.port 8502 --server.headless true > /dev/null 2>&1 &
STREAMLIT_PID=$!

# Wait for app to start
echo "⏳ Waiting for app to start (10 seconds)..."
sleep 10

# Check if app is running
if ! curl -s http://localhost:8502 > /dev/null; then
    echo "❌ Failed to start Streamlit app"
    kill $STREAMLIT_PID 2>/dev/null || true
    exit 1
fi

echo "✅ Streamlit app is running (PID: $STREAMLIT_PID)"
echo ""

# Run tests based on mode
case $MODE in
    all)
        echo "🧪 Running all UI tests..."
        pytest tests/ui_tests/ -v --browser $BROWSER
        ;;
    safari)
        echo "🧪 Running Safari-specific tests..."
        pytest tests/ui_tests/test_cross_browser.py::TestSafariSpecific -v --browser webkit
        ;;
    devices)
        echo "🧪 Running device emulation tests..."
        pytest tests/ui_tests/test_cross_browser.py::TestDeviceEmulation -v --browser $BROWSER
        ;;
    core)
        echo "🧪 Running core functionality tests..."
        pytest tests/ui_tests/test_cross_browser.py::TestCrossBrowserCore -v --browser $BROWSER
        ;;
    *)
        echo "❌ Unknown mode: $MODE"
        echo "Available modes: all, safari, devices, core"
        kill $STREAMLIT_PID
        exit 1
        ;;
esac

TEST_EXIT_CODE=$?

# Cleanup
echo ""
echo "🧹 Cleaning up..."
kill $STREAMLIT_PID 2>/dev/null || true
wait $STREAMLIT_PID 2>/dev/null || true

# Summary
echo ""
echo "======================================"
if [ $TEST_EXIT_CODE -eq 0 ]; then
    echo "✅ All tests passed!"
else
    echo "❌ Some tests failed (exit code: $TEST_EXIT_CODE)"
    echo ""
    echo "📸 Screenshots saved to: tests/ui_tests/screenshots/"
    echo "📼 Traces saved to: tests/ui_tests/traces/"
    echo ""
    echo "View traces with:"
    echo "  playwright show-trace tests/ui_tests/traces/<test_name>.zip"
fi
echo "======================================"

exit $TEST_EXIT_CODE
