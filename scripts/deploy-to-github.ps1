# Deploy to GitHub script

Write-Host "🚀 Deploying to GitHub..." -ForegroundColor Cyan
Write-Host ""

# Check if git is initialized
if (-not (Test-Path .git)) {
    Write-Host "Initializing git repository..." -ForegroundColor Yellow
    git init
}

# Check if .gitignore exists
if (-not (Test-Path .gitignore)) {
    Write-Host "⚠️  .gitignore not found - creating one..." -ForegroundColor Yellow
    @"
# Environment
.env
.env.local
.env*.local

# Python
__pycache__/
*.py[cod]
*.so
venv/
env/

# Node
node_modules/
.next/
out/
dist/

# Models
models/
*.ckpt
*.safetensors

# Database
*.db
*.sqlite

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db

# Uploads
uploads/
generated/
temp/
"@ | Out-File -FilePath ".gitignore" -Encoding UTF8
    Write-Host "✅ Created .gitignore" -ForegroundColor Green
}

# Check git status
Write-Host "Checking git status..." -ForegroundColor Yellow
$status = git status --porcelain

if ($status) {
    Write-Host "Files to commit:" -ForegroundColor Cyan
    git status --short
    
    Write-Host ""
    Write-Host "Staging all files..." -ForegroundColor Yellow
    git add .
    
    Write-Host "Creating commit..." -ForegroundColor Yellow
    git commit -m "Initial commit: AI Interior Designer MVP" 2>&1
    
    Write-Host ""
    Write-Host "✅ Files committed locally" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Cyan
    Write-Host "1. Create a repository on GitHub:" -ForegroundColor White
    Write-Host "   https://github.com/new" -ForegroundColor Blue
    Write-Host "2. Add remote and push:" -ForegroundColor White
    Write-Host "   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git" -ForegroundColor Gray
    Write-Host "   git branch -M main" -ForegroundColor Gray
    Write-Host "   git push -u origin main" -ForegroundColor Gray
} else {
    Write-Host "✅ No changes to commit" -ForegroundColor Green
    Write-Host ""
    Write-Host "To push to GitHub:" -ForegroundColor Cyan
    Write-Host "1. Create repository on GitHub" -ForegroundColor White
    Write-Host "2. Add remote: git remote add origin <your-repo-url>" -ForegroundColor White
    Write-Host "3. Push: git push -u origin main" -ForegroundColor White
}

# Check if remote exists
$remote = git remote -v 2>&1
if ($remote -and $remote -notlike "*fatal*") {
    Write-Host ""
    Write-Host "Current remotes:" -ForegroundColor Cyan
    Write-Host $remote
    Write-Host ""
    Write-Host "To push:" -ForegroundColor Yellow
    Write-Host "  git push origin main" -ForegroundColor Gray
} else {
    Write-Host ""
    Write-Host "No remote configured yet" -ForegroundColor Yellow
}
