# 🔥 Allow Backend Server Through Firewall (Windows)

# This script allows Python to accept connections from your local network
# Run this in PowerShell as Administrator

Write-Host "Checking firewall rules for Python..." -ForegroundColor Cyan

# Find Python executable
$pythonPath = (Get-Command python).Source

Write-Host "Python location: $pythonPath" -ForegroundColor Yellow

# Create firewall rule
$ruleName = "TalimBot Backend Server"

# Check if rule already exists
$existingRule = Get-NetFirewallRule -DisplayName $ruleName -ErrorAction SilentlyContinue

if ($existingRule) {
    Write-Host "Firewall rule already exists. Removing old rule..." -ForegroundColor Yellow
    Remove-NetFirewallRule -DisplayName $ruleName
}

# Create new rule
Write-Host "Creating firewall rule to allow Python server..." -ForegroundColor Cyan

New-NetFirewallRule -DisplayName $ruleName `
    -Direction Inbound `
    -Program $pythonPath `
    -Action Allow `
    -Protocol TCP `
    -LocalPort 8000 `
    -Profile Any `
    -Description "Allows TalimBot backend server to accept connections on port 8000"

Write-Host "✅ Firewall rule created successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "Now your server at http://192.168.114.1:8000 should be accessible from your phone!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Make sure your laptop and phone are on the same Wi-Fi"
Write-Host "2. Server must be running: python main.py"
Write-Host "3. On phone, visit: http://192.168.114.1:8000/api/students"
