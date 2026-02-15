# PowerShell GPU availability checker script

Write-Host "🔍 Checking GPU availability..." -ForegroundColor Cyan

# Check NVIDIA GPU
if (Get-Command nvidia-smi -ErrorAction SilentlyContinue) {
    Write-Host "✅ NVIDIA drivers installed" -ForegroundColor Green
    nvidia-smi --query-gpu=name,memory.total --format=csv,noheader
    Write-Host ""
    
    # Check CUDA with Python
    try {
        $result = python -c "import torch; print('CUDA available:', torch.cuda.is_available())" 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ PyTorch CUDA check:" -ForegroundColor Green
            python -c "import torch; print('   CUDA available:', torch.cuda.is_available())"
            python -c "import torch; print('   Device count:', torch.cuda.device_count())"
            python -c "import torch; print('   Device name:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'N/A')"
        } else {
            Write-Host "⚠️  PyTorch not installed or CUDA not available" -ForegroundColor Yellow
        }
    } catch {
        Write-Host "⚠️  Could not check PyTorch CUDA" -ForegroundColor Yellow
    }
} else {
    Write-Host "❌ nvidia-smi not found - GPU may not be available" -ForegroundColor Red
    Write-Host "   Inference will run on CPU (much slower)" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "✅ GPU check complete!" -ForegroundColor Green
