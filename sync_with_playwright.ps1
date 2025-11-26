# PowerShell script for easy Playwright sync operations
# Usage examples:
#   .\sync_with_playwright.ps1 -Action test -Player "Lewandowski"
#   .\sync_with_playwright.ps1 -Action sync -Players "Lewandowski","Zielinski"
#   .\sync_with_playwright.ps1 -Action syncall -Limit 10

param(
    [Parameter(Mandatory=$true)]
    [ValidateSet('test', 'sync', 'syncall', 'compare', 'install')]
    [string]$Action,
    
    [string]$Player = "",
    [string[]]$Players = @(),
    [int]$Limit = 0,
    [switch]$Visible = $false,
    [switch]$UseId = $false
)

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  PLAYWRIGHT SYNC TOOL" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Change to script directory
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptPath

switch ($Action) {
    'install' {
        Write-Host "📦 Installing Playwright..." -ForegroundColor Yellow
        Write-Host ""
        
        python -m pip install playwright
        if ($LASTEXITCODE -ne 0) {
            Write-Host "❌ Failed to install playwright package" -ForegroundColor Red
            exit 1
        }
        
        Write-Host ""
        Write-Host "📦 Installing Chromium browser..." -ForegroundColor Yellow
        playwright install chromium
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host ""
            Write-Host "✅ Playwright installed successfully!" -ForegroundColor Green
        } else {
            Write-Host "❌ Failed to install Chromium browser" -ForegroundColor Red
            exit 1
        }
    }
    
    'test' {
        if (-not $Player) {
            Write-Host "❌ Error: -Player parameter required for test action" -ForegroundColor Red
            Write-Host "Usage: .\sync_with_playwright.ps1 -Action test -Player 'Robert Lewandowski'" -ForegroundColor Yellow
            exit 1
        }
        
        Write-Host "🧪 Testing single player sync: $Player" -ForegroundColor Yellow
        Write-Host ""
        
        python sync_playwright_single.py $Player
    }
    
    'sync' {
        if (-not $Player -and $Players.Count -eq 0) {
            Write-Host "❌ Error: -Player or -Players parameter required for sync action" -ForegroundColor Red
            Write-Host "Usage: .\sync_with_playwright.ps1 -Action sync -Player 'Robert Lewandowski'" -ForegroundColor Yellow
            Write-Host "   or: .\sync_with_playwright.ps1 -Action sync -Players 'Lewandowski','Zielinski'" -ForegroundColor Yellow
            exit 1
        }
        
        $args = @()
        
        if ($Player) {
            Write-Host "🔄 Syncing player: $Player" -ForegroundColor Yellow
            $args += $Player
        } else {
            Write-Host "🔄 Syncing $($Players.Count) player(s)" -ForegroundColor Yellow
            $args += $Players
        }
        
        if ($Visible) {
            $args += "--visible"
            Write-Host "👁️ Running in visible mode" -ForegroundColor Cyan
        }
        
        if ($UseId) {
            $args += "--use-id"
            Write-Host "🆔 Using FBref IDs (faster)" -ForegroundColor Cyan
        }
        
        Write-Host ""
        
        python sync_playwright.py @args
    }
    
    'syncall' {
        Write-Host "🔄 Syncing ALL players in database" -ForegroundColor Yellow
        
        $args = @()
        
        if ($Limit -gt 0) {
            $args += "--limit=$Limit"
            Write-Host "📊 Limit: $Limit players" -ForegroundColor Cyan
        } else {
            Write-Host "⚠️ No limit - will sync ALL players!" -ForegroundColor Red
        }
        
        if ($Visible) {
            $args += "--visible"
            Write-Host "👁️ Running in visible mode" -ForegroundColor Cyan
        }
        
        Write-Host ""
        
        python sync_all_playwright.py @args
    }
    
    'compare' {
        Write-Host "📊 Comparing old vs new scraper" -ForegroundColor Yellow
        Write-Host "⚠️ This will take ~30 seconds" -ForegroundColor Yellow
        Write-Host ""
        
        python tmp_rovodev_compare_scrapers.py
    }
}

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  Done!" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Cyan
