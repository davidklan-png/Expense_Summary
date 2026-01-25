# Network Access Guide

This guide explains how to access the Saison Transform web interface from other devices on your local network.

## Quick Start

### For Linux/Mac Users

Simply run:
```bash
./run_web.sh
```

The script will automatically configure the server to accept connections from your local network and display both local and network URLs.

### For WSL2/Windows Users

WSL2 runs in a virtualized network, so additional setup is required for network access.

## Step-by-Step Setup for WSL2

### Step 1: Start the Server

In your WSL2 terminal:
```bash
cd /path/to/saisonxform
./run_web_network.sh
```

Note the WSL2 internal IP shown (e.g., `172.22.94.242`)

### Step 2: Setup Port Forwarding

You only need to do this once (or after restarting Windows).

#### Option A: Automated Setup (Recommended)

1. Open PowerShell as **Administrator** on Windows
2. Navigate to your project directory:
   ```powershell
   cd C:\path\to\saisonxform
   ```
3. Run the setup script:
   ```powershell
   .\setup_port_forward.ps1
   ```

#### Option B: Manual Setup

1. Get your WSL2 IP address (from Step 1 output)
2. Open PowerShell as **Administrator**
3. Run these commands:
   ```powershell
   # Remove old rule if exists
   netsh interface portproxy delete v4tov4 listenport=8502 listenaddress=0.0.0.0

   # Add new port forwarding rule (replace <WSL_IP> with actual IP)
   netsh interface portproxy add v4tov4 listenport=8502 listenaddress=0.0.0.0 connectport=8502 connectaddress=<WSL_IP>

   # Configure Windows Firewall
   New-NetFirewallRule -DisplayName "WSL2 Streamlit 8502" -Direction Inbound -LocalPort 8502 -Protocol TCP -Action Allow
   ```

### Step 3: Find Your Windows IP Address

In PowerShell or Command Prompt:
```powershell
ipconfig
```

Look for:
```
Wireless LAN adapter Wi-Fi:
   IPv4 Address. . . . . . . . . . . : 192.168.1.9
```

### Step 4: Access from Other Devices

On any device connected to the same WiFi network:

1. Open a web browser
2. Navigate to: `http://YOUR_WINDOWS_IP:8502`
3. Example: `http://192.168.1.9:8502`

## Troubleshooting

### Cannot Connect from Other Devices

1. **Verify the server is running:**
   ```bash
   # In WSL2
   curl http://localhost:8502
   ```

2. **Check port forwarding rules:**
   ```powershell
   # In PowerShell
   netsh interface portproxy show v4tov4
   ```

3. **Check Windows Firewall:**
   ```powershell
   Get-NetFirewallRule -DisplayName "WSL2 Streamlit 8502"
   ```

4. **Test from Windows host first:**
   ```powershell
   # In PowerShell
   curl http://localhost:8502
   ```

### Port Forwarding Not Working After Restart

Windows resets port forwarding rules after restart. Re-run the setup script or manual commands from Step 2.

### WSL2 IP Changed

The WSL2 IP address can change. If connection stops working:

1. Check current WSL2 IP:
   ```bash
   hostname -I | awk '{print $1}'
   ```

2. Update port forwarding rule with new IP (re-run setup script)

## Removing Port Forwarding

When you no longer need network access:

```powershell
# Remove port forwarding
netsh interface portproxy delete v4tov4 listenport=8502 listenaddress=0.0.0.0

# Remove firewall rule
Remove-NetFirewallRule -DisplayName "WSL2 Streamlit 8502"
```

## Security Notes

- The web interface is accessible to **anyone on your local network**
- Do not expose this to the public internet
- Use only on trusted networks (home/office WiFi)
- Stop the server when not in use (Ctrl+C)

## URLs Summary

| Access Point | URL | Notes |
|-------------|-----|-------|
| Local (WSL2) | `http://localhost:8502` | Access from WSL2 terminal/browser |
| Windows Host | `http://localhost:8502` | After port forwarding setup |
| Network Devices | `http://192.168.1.9:8502` | Use your actual Windows IP |
| WSL2 Direct | `http://172.22.x.x:8502` | WSL2 internal IP (not accessible from other devices) |

## Related Documentation

- [WEB_INTERFACE_GUIDE.md](docs/guides/WEB_INTERFACE_GUIDE.md) - Complete web interface usage guide
- [README.md](README.md) - Main project documentation
- [setup_port_forward.ps1](setup_port_forward.ps1) - Automated port forwarding script
