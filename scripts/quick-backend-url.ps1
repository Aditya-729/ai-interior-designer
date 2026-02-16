# Quick Backend URL Setup Script
# This helps you get your backend URL for Vercel environment variables

Write-Host "🚀 Quick Backend URL Setup" -ForegroundColor Cyan
Write-Host ""

# Check if backend is running locally
Write-Host "Checking if backend is running locally..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/api/v1/system/health" -TimeoutSec 2 -ErrorAction Stop
    Write-Host "✅ Backend is running on http://localhost:8000" -ForegroundColor Green
    $backendRunning = $true
} catch {
    Write-Host "⚠️  Backend is not running on localhost:8000" -ForegroundColor Yellow
    $backendRunning = $false
}

Write-Host ""
Write-Host "Choose an option:" -ForegroundColor Cyan
Write-Host "1. Use ngrok (if backend is running locally)" -ForegroundColor White
Write-Host "2. I have a deployed backend URL" -ForegroundColor White
Write-Host "3. I need to deploy my backend first" -ForegroundColor White
Write-Host ""

$choice = Read-Host "Enter choice (1-3)"

switch ($choice) {
    "1" {
        if (-not $backendRunning) {
            Write-Host ""
            Write-Host "⚠️  Backend is not running. Please start it first:" -ForegroundColor Yellow
            Write-Host "   cd backend" -ForegroundColor Gray
            Write-Host "   python main.py" -ForegroundColor Gray
            Write-Host ""
            $continue = Read-Host "Press Enter after starting backend, or type 'skip' to continue anyway"
            if ($continue -eq "skip") {
                Write-Host "Continuing with ngrok setup..." -ForegroundColor Yellow
            }
        }
        
        Write-Host ""
        Write-Host "📦 Setting up ngrok..." -ForegroundColor Yellow
        
        # Check if ngrok is installed
        $ngrokInstalled = Get-Command ngrok -ErrorAction SilentlyContinue
        if (-not $ngrokInstalled) {
            Write-Host "❌ ngrok is not installed!" -ForegroundColor Red
            Write-Host ""
            Write-Host "Please install ngrok:" -ForegroundColor Yellow
            Write-Host "1. Go to: https://ngrok.com/download" -ForegroundColor White
            Write-Host "2. Download and extract ngrok.exe" -ForegroundColor White
            Write-Host "3. Add to PATH or place in this directory" -ForegroundColor White
            Write-Host ""
            Write-Host "Or sign up and install via:" -ForegroundColor White
            Write-Host "   choco install ngrok" -ForegroundColor Gray
            Write-Host ""
            exit
        }
        
        Write-Host "✅ ngrok found!" -ForegroundColor Green
        Write-Host ""
        Write-Host "Starting ngrok tunnel..." -ForegroundColor Yellow
        Write-Host "This will create a public URL for your local backend." -ForegroundColor Gray
        Write-Host ""
        
        # Start ngrok in background
        Start-Process ngrok -ArgumentList "http", "8000" -WindowStyle Minimized
        
        Write-Host "⏳ Waiting for ngrok to start..." -ForegroundColor Yellow
        Start-Sleep -Seconds 3
        
        # Get ngrok URL from API
        try {
            $ngrokInfo = Invoke-RestMethod -Uri "http://localhost:4040/api/tunnels" -ErrorAction Stop
            $publicUrl = $ngrokInfo.tunnels[0].public_url
            
            Write-Host ""
            Write-Host "✅ ngrok tunnel created!" -ForegroundColor Green
            Write-Host ""
            Write-Host "Your URLs:" -ForegroundColor Cyan
            Write-Host "  API Base:  $publicUrl" -ForegroundColor White
            Write-Host "  WebSocket: $($publicUrl -replace 'https://', 'wss://' -replace 'http://', 'ws://')" -ForegroundColor White
            Write-Host ""
            Write-Host "📋 Copy these to Vercel:" -ForegroundColor Yellow
            Write-Host "  NEXT_PUBLIC_API_BASE = $publicUrl" -ForegroundColor Gray
            Write-Host "  NEXT_PUBLIC_WS_URL = $($publicUrl -replace 'https://', 'wss://' -replace 'http://', 'ws://')" -ForegroundColor Gray
            Write-Host ""
            Write-Host "⚠️  Note: This URL will change when you restart ngrok." -ForegroundColor Yellow
            Write-Host "   For production, deploy your backend to a cloud platform." -ForegroundColor Yellow
            Write-Host ""
        } catch {
            Write-Host "❌ Could not get ngrok URL. Make sure ngrok is running." -ForegroundColor Red
            Write-Host "   Check: http://localhost:4040" -ForegroundColor Gray
        }
    }
    
    "2" {
        Write-Host ""
        $backendUrl = Read-Host "Enter your backend API URL (e.g., https://api.yourdomain.com or https://your-app.railway.app)"
        
        if ([string]::IsNullOrWhiteSpace($backendUrl)) {
            Write-Host "❌ URL cannot be empty!" -ForegroundColor Red
            exit
        }
        
        # Determine WebSocket URL
        if ($backendUrl -like "https://*") {
            $wsUrl = $backendUrl -replace "https://", "wss://"
        } elseif ($backendUrl -like "http://*") {
            $wsUrl = $backendUrl -replace "http://", "ws://"
        } else {
            $wsUrl = "wss://$backendUrl"
        }
        
        Write-Host ""
        Write-Host "✅ URLs configured!" -ForegroundColor Green
        Write-Host ""
        Write-Host "📋 Set these in Vercel:" -ForegroundColor Cyan
        Write-Host "  NEXT_PUBLIC_API_BASE = $backendUrl" -ForegroundColor White
        Write-Host "  NEXT_PUBLIC_WS_URL = $wsUrl" -ForegroundColor White
        Write-Host ""
        Write-Host "Test your backend:" -ForegroundColor Yellow
        Write-Host "  $backendUrl/api/v1/system/health" -ForegroundColor Gray
        Write-Host ""
    }
    
    "3" {
        Write-Host ""
        Write-Host "📚 Deployment Options:" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "1. Railway (Easiest):" -ForegroundColor White
        Write-Host "   - Go to: https://railway.app" -ForegroundColor Gray
        Write-Host "   - Deploy from GitHub" -ForegroundColor Gray
        Write-Host "   - Root directory: backend" -ForegroundColor Gray
        Write-Host ""
        Write-Host "2. Render:" -ForegroundColor White
        Write-Host "   - Go to: https://render.com" -ForegroundColor Gray
        Write-Host "   - New Web Service" -ForegroundColor Gray
        Write-Host "   - Connect GitHub repo" -ForegroundColor Gray
        Write-Host ""
        Write-Host "3. Fly.io:" -ForegroundColor White
        Write-Host "   - Install: https://fly.io/docs/getting-started/" -ForegroundColor Gray
        Write-Host "   - Run: fly launch (in backend directory)" -ForegroundColor Gray
        Write-Host ""
        Write-Host "See HOW_TO_GET_BACKEND_URLS.md for detailed instructions." -ForegroundColor Yellow
        Write-Host ""
    }
    
    default {
        Write-Host "❌ Invalid choice!" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Set environment variables in Vercel dashboard" -ForegroundColor White
Write-Host "2. Redeploy your Vercel project" -ForegroundColor White
Write-Host "3. Test your app!" -ForegroundColor White
Write-Host ""
