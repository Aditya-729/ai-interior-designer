# PowerShell environment checker script

Write-Host "🔍 Checking environment setup..." -ForegroundColor Cyan

# Check Python
if (Get-Command python -ErrorAction SilentlyContinue) {
    $pythonVersion = python --version
    Write-Host "✅ Python: $pythonVersion" -ForegroundColor Green
} else {
    Write-Host "❌ Python not found" -ForegroundColor Red
    exit 1
}

# Check Node.js
if (Get-Command node -ErrorAction SilentlyContinue) {
    $nodeVersion = node --version
    Write-Host "✅ Node.js: $nodeVersion" -ForegroundColor Green
} else {
    Write-Host "❌ Node.js not found" -ForegroundColor Red
    exit 1
}

# Check Docker
if (Get-Command docker -ErrorAction SilentlyContinue) {
    $dockerVersion = docker --version
    Write-Host "✅ Docker: $dockerVersion" -ForegroundColor Green
} else {
    Write-Host "❌ Docker not found" -ForegroundColor Red
    exit 1
}

# Check .env file
if (Test-Path .env) {
    Write-Host "✅ .env file exists" -ForegroundColor Green
    
    # Load .env (simple check)
    Get-Content .env | ForEach-Object {
        if ($_ -match '^([^#][^=]*)=(.*)$') {
            $name = $matches[1].Trim()
            $value = $matches[2].Trim()
            Set-Variable -Name $name -Value $value -Scope Script
        }
    }
    
    $requiredVars = @(
        "MINO_AI_API_KEY",
        "PERPLEXITY_API_KEY",
        "R2_ACCOUNT_ID",
        "R2_ACCESS_KEY_ID",
        "R2_SECRET_ACCESS_KEY",
        "R2_ENDPOINT"
    )
    
    $missingVars = @()
    foreach ($var in $requiredVars) {
        if (-not (Get-Variable -Name $var -ErrorAction SilentlyContinue) -or -not (Get-Variable -Name $var -ValueOnly)) {
            $missingVars += $var
        }
    }
    
    if ($missingVars.Count -eq 0) {
        Write-Host "✅ All required environment variables set" -ForegroundColor Green
    } else {
        Write-Host "❌ Missing environment variables:" -ForegroundColor Red
        foreach ($var in $missingVars) {
            Write-Host "   - $var" -ForegroundColor Yellow
        }
    }
} else {
    Write-Host "❌ .env file not found" -ForegroundColor Red
    exit 1
}

# Check PostgreSQL
if (docker ps | Select-String -Pattern "postgres") {
    Write-Host "✅ PostgreSQL container running" -ForegroundColor Green
} else {
    Write-Host "⚠️  PostgreSQL container not running" -ForegroundColor Yellow
}

# Check Qdrant
if (docker ps | Select-String -Pattern "qdrant") {
    Write-Host "✅ Qdrant container running" -ForegroundColor Green
} else {
    Write-Host "⚠️  Qdrant container not running" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "✅ Environment check complete!" -ForegroundColor Green
