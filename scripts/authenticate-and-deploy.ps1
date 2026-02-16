# Authenticate and deploy to GitHub and Vercel

Write-Host "🔐 Authentication and Deployment Setup" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Git Configuration
Write-Host "Step 1: Git Configuration" -ForegroundColor Yellow
$gitName = git config --global user.name 2>&1
$gitEmail = git config --global user.email 2>&1

if ($gitName -and $gitName -notlike "*error*") {
    Write-Host "  ✅ Git user.name: $gitName" -ForegroundColor Green
} else {
    Write-Host "  ⚠️  Git user.name not set" -ForegroundColor Yellow
    $name = Read-Host "Enter your Git username"
    git config --global user.name $name
    Write-Host "  ✅ Git user.name set" -ForegroundColor Green
}

if ($gitEmail -and $gitEmail -notlike "*error*") {
    Write-Host "  ✅ Git user.email: $gitEmail" -ForegroundColor Green
} else {
    Write-Host "  ⚠️  Git user.email not set" -ForegroundColor Yellow
    $email = Read-Host "Enter your Git email"
    git config --global user.email $email
    Write-Host "  ✅ Git user.email set" -ForegroundColor Green
}

Write-Host ""

# Step 2: Check GitHub remote
Write-Host "Step 2: GitHub Remote" -ForegroundColor Yellow
$remote = git remote -v 2>&1
if ($remote -and $remote -notlike "*fatal*") {
    Write-Host "  ✅ Remote configured:" -ForegroundColor Green
    Write-Host "  $remote" -ForegroundColor Gray
} else {
    Write-Host "  ⚠️  No remote configured" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "To add GitHub remote:" -ForegroundColor Cyan
    Write-Host "  1. Create repository at: https://github.com/new" -ForegroundColor White
    Write-Host "  2. Run:" -ForegroundColor White
    Write-Host "     git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git" -ForegroundColor Gray
    Write-Host "  3. Push:" -ForegroundColor White
    Write-Host "     git push -u origin main" -ForegroundColor Gray
}

Write-Host ""

# Step 3: GitHub Authentication
Write-Host "Step 3: GitHub Authentication" -ForegroundColor Yellow
Write-Host "  GitHub uses HTTPS or SSH authentication" -ForegroundColor White
Write-Host "  For HTTPS, you'll be prompted for credentials when pushing" -ForegroundColor White
Write-Host "  For SSH, you need to set up SSH keys:" -ForegroundColor White
Write-Host "    https://docs.github.com/en/authentication/connecting-to-github-with-ssh" -ForegroundColor Blue
Write-Host ""
Write-Host "  Or use GitHub CLI (gh):" -ForegroundColor White
$ghInstalled = Get-Command gh -ErrorAction SilentlyContinue
if ($ghInstalled) {
    Write-Host "  ✅ GitHub CLI installed" -ForegroundColor Green
    Write-Host "  Run: gh auth login" -ForegroundColor Gray
} else {
    Write-Host "  ⚠️  GitHub CLI not installed" -ForegroundColor Yellow
    Write-Host "  Install: winget install GitHub.cli" -ForegroundColor Gray
}

Write-Host ""

# Step 4: Vercel CLI
Write-Host "Step 4: Vercel CLI" -ForegroundColor Yellow
$vercelInstalled = Get-Command vercel -ErrorAction SilentlyContinue
if ($vercelInstalled) {
    Write-Host "  ✅ Vercel CLI installed" -ForegroundColor Green
    $vercelVersion = vercel --version 2>&1
    Write-Host "  Version: $vercelVersion" -ForegroundColor Gray
    Write-Host ""
    Write-Host "  To login:" -ForegroundColor Cyan
    Write-Host "    vercel login" -ForegroundColor Gray
    Write-Host ""
    Write-Host "  To deploy:" -ForegroundColor Cyan
    Write-Host "    cd frontend" -ForegroundColor Gray
    Write-Host "    vercel" -ForegroundColor Gray
} else {
    Write-Host "  ⚠️  Vercel CLI not installed" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "  Install Vercel CLI:" -ForegroundColor Cyan
    Write-Host "    npm install -g vercel" -ForegroundColor Gray
    Write-Host "  Or use web interface:" -ForegroundColor White
    Write-Host "    https://vercel.com/dashboard" -ForegroundColor Blue
}

Write-Host ""
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host "1. Configure Git (if not done)" -ForegroundColor White
Write-Host "2. Create GitHub repo and add remote" -ForegroundColor White
Write-Host "3. Authenticate with GitHub (gh auth login or HTTPS)" -ForegroundColor White
Write-Host "4. Push to GitHub: git push -u origin main" -ForegroundColor White
Write-Host "5. Install Vercel CLI: npm install -g vercel" -ForegroundColor White
Write-Host "6. Login to Vercel: vercel login" -ForegroundColor White
Write-Host "7. Deploy: cd frontend && vercel" -ForegroundColor White
