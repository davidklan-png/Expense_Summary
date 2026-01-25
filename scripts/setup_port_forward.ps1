# PowerShell Script to Setup Port Forwarding for WSL2
# Run this in PowerShell as Administrator

Write-Host "Setting up port forwarding for Saison Transform Web Interface..." -ForegroundColor Green
Write-Host ""

# Get WSL2 IP address
$wslIP = bash.exe -c "hostname -I | awk '{print `$1}'"
$wslIP = $wslIP.Trim()

Write-Host "WSL2 IP Address: $wslIP" -ForegroundColor Cyan

# Remove existing port proxy if it exists
Write-Host "Removing existing port forwarding rules (if any)..." -ForegroundColor Yellow
netsh interface portproxy delete v4tov4 listenport=8502 listenaddress=0.0.0.0 2>$null

# Add new port proxy rule
Write-Host "Adding port forwarding rule..." -ForegroundColor Yellow
netsh interface portproxy add v4tov4 listenport=8502 listenaddress=0.0.0.0 connectport=8502 connectaddress=$wslIP

# Configure Windows Firewall
Write-Host "Configuring Windows Firewall..." -ForegroundColor Yellow
$ruleName = "WSL2 Streamlit 8502"
Remove-NetFirewallRule -DisplayName $ruleName 2>$null
New-NetFirewallRule -DisplayName $ruleName -Direction Inbound -LocalPort 8502 -Protocol TCP -Action Allow

Write-Host ""
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host ""
Write-Host "You can now access the web interface from other devices using:" -ForegroundColor Cyan
Write-Host "  http://YOUR_WINDOWS_IP:8502" -ForegroundColor White
Write-Host ""
Write-Host "To find your Windows IP:" -ForegroundColor Yellow
Write-Host "  ipconfig" -ForegroundColor White
Write-Host "  Look for 'Wireless LAN adapter Wi-Fi' -> 'IPv4 Address'" -ForegroundColor White
Write-Host ""
Write-Host "Current port forwarding rules:" -ForegroundColor Cyan
netsh interface portproxy show v4tov4
Write-Host ""
Write-Host "To remove port forwarding later, run:" -ForegroundColor Yellow
Write-Host "  netsh interface portproxy delete v4tov4 listenport=8502 listenaddress=0.0.0.0" -ForegroundColor White
