# Quick deploy script - guides through authentication and deployment

Write-Host "🚀 Quick Deploy Script" -ForegroundColor Cyan
Write-Host "=====================" -ForegroundColor Cyan
Write-Host ""

# Check prerequisites
Write-Host "Checking prerequisites..." -ForegroundColor Yellow

# Check Git
$gitInstalled = Get-Command git -ErrorAction SilentlyContinue
if ($gitInstalled) {
    Write-Host "  ✅ Git installed" -ForegroundColor Green
} else {
    Write-Host "  ❌ Git not installed" -ForegroundColor Red
    Write-Host "  Install from: https://git-scm.com/download/win" -ForegroundColor Yellow
    exit 1
}

# Check Node.js
$nodeInstalled = Get-Command node -ErrorAction SilentlyContinue
if ($nodeInstalled) {
    $nodeVersion = node --version
    Write-Host "  ✅ Node.js installed: $nodeVersion" -ForegroundColor Green
} else {
    Write-Host "  ❌ Node.js not installed" -ForegroundColor Red
    Write-Host "  Install from: https://nodejs.org" -ForegroundColor Yellow
    exit 1
}

# Check npm
$npmInstalled = Get-Command npm -ErrorAction SilentlyContinue
if ($npmInstalled) {
    Write-Host "  ✅ npm installed" -ForegroundColor Green
} else {
    Write-Host "  ❌ npm not installed" -ForegroundColor Red
    exit 1
}

Write-Host ""

# GitHub Setup
Write-Host "📦 GitHub Setup" -ForegroundColor Cyan
Write-Host ""

# Check if remote exists
$remote = git remote -v 2>&1
if ($remote -and $remote -notlike "*fatal*") {
    Write-Host "  ✅ GitHub remote configured" -ForegroundColor Green
    Write-Host "  $remote" -ForegroundColor Gray
} else {
    Write-Host "  ⚠️  GitHub remote not configured" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "  To set up GitHub:" -ForegroundColor Cyan
    Write-Host "  1. Create repo: https://github.com/new" -ForegroundColor White
    Write-Host "  2. Add remote:" -ForegroundColor White
    Write-Host "     git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git" -ForegroundColor Gray
}

# Check GitHub CLI
$ghInstalled = Get-Command gh -ErrorAction SilentlyContinue
if ($ghInstalled) {
    Write-Host ""
    Write-Host "  ✅ GitHub CLI (gh) installed" -ForegroundColor Green
    Write-Host "  To authenticate: gh auth login" -ForegroundColor Gray
} else {
    Write-Host ""
    Write-Host "  💡 Install GitHub CLI for easier authentication:" -ForegroundColor Yellow
    Write-Host "     winget install GitHub.cli" -ForegroundColor Gray
    Write-Host "  Or authenticate via HTTPS when pushing" -ForegroundColor White
}

Write-Host ""

# Vercel Setup
Write-Host "🌐 Vercel Setup" -ForegroundColor Cyan
Write-Host ""

$vercelInstalled = Get-Command vercel -ErrorAction SilentlyContinue
if ($vercelInstalled) {
    Write-Host "  ✅ Vercel CLI installed" -ForegroundColor Green
    Write-Host ""
    Write-Host "  To login:" -ForegroundColor Yellow
    Write-Host "    vercel login" -ForegroundColor Gray
    Write-Host ""
    Write-Host "  To deploy:" -ForegroundColor Yellow
    Write-Host "    cd frontend" -ForegroundColor Gray
    Write-Host "    vercel" -ForegroundColor Gray
} else {
    Write-Host "  ⚠️  Vercel CLI not installed" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "  Installing Vercel CLI..." -ForegroundColor Cyan
    npm install -g vercel 2>&1 | Out-Null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✅ Vercel CLI installed" -ForegroundColor Green
        Write-Host ""
        Write-Host "  Now run: vercel login" -ForegroundColor Yellow
    } else {
        Write-Host "  ❌ Failed to install Vercel CLI" -ForegroundColor Red
        Write-Host "  Install manually: npm install -g vercel" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "Ready to Deploy!" -ForegroundColor Green
Write-Host ""
Write-Host "Commands to run:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. GitHub:" -ForegroundColor Cyan
Write-Host "   gh auth login  # (if using GitHub CLI)" -ForegroundColor Gray
Write-Host "   git push -u origin main" -ForegroundColor Gray
Write-Host ""
Write-Host "2. Vercel:" -ForegroundColor Cyan
Write-Host "   vercel login" -ForegroundColor Gray
Write-Host "   cd frontend" -ForegroundColor Gray
Write-Host "   vercel" -ForegroundColor Gray
