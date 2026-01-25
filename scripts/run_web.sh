#!/bin/bash
# Launch Saison Transform Web Interface

# Get Windows host IP (works for WSL2)
WINDOWS_IP=$(cat /etc/resolv.conf | grep nameserver | awk '{print $2}')
# Get WSL2 internal IP as fallback
WSL_IP=$(hostname -I | awk '{print $1}')

echo "🚀 Starting Saison Transform Web Interface..."
echo ""
echo "📱 Access from other devices on your WiFi:"
echo "  → http://${WINDOWS_IP}:8502"
echo ""
echo "The web interface is also accessible at:"
echo "  Local (this machine):  http://localhost:8502"
echo "  WSL2 internal:         http://${WSL_IP}:8502"
echo "  Windows host:          http://${WINDOWS_IP}:8502"
echo ""
echo "Features:"
echo "  📤 Drag & drop CSV files for upload"
echo "  ⚙️  Configure processing parameters"
echo "  ✏️  Edit data interactively in tables"
echo "  💾 Download processed CSV and HTML reports"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Activate virtual environment and run streamlit
cd "$(dirname "$0")/.."
.venv/bin/python -m streamlit run web_app.py \
  --server.port 8502 \
  --server.address 0.0.0.0 \
  --server.headless true \
  --server.enableWebsocketCompression false
