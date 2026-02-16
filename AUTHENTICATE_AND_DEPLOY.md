# 🔐 Authenticate and Deploy - Complete Guide

## Prerequisites Check ✅

- ✅ Git installed
- ✅ Node.js installed
- ✅ npm installed
- ✅ Code committed locally

---

## Part 1: GitHub Authentication & Push

### Option A: Using GitHub CLI (Easiest)

1. **Install GitHub CLI** (if not installed):
   ```powershell
   winget install GitHub.cli
   ```

2. **Authenticate**:
   ```powershell
   gh auth login
   ```
   - Follow prompts
   - Choose: GitHub.com
   - Choose: HTTPS
   - Authenticate: Login with a web browser

3. **Create Repository**:
   ```powershell
   gh repo create ai-interior-designer --public --source=. --remote=origin --push
   ```
   This will:
   - Create repo on GitHub
   - Add remote
   - Push your code

### Option B: Manual GitHub Setup

1. **Create Repository**:
   - Go to: https://github.com/new
   - Name: `ai-interior-designer`
   - Don't initialize with README
   - Click "Create repository"

2. **Add Remote and Push**:
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/ai-interior-designer.git
   git branch -M main
   git push -u origin main
   ```
   - You'll be prompted for GitHub username/password
   - Use Personal Access Token (not password)

---

## Part 2: Vercel Authentication & Deploy

### Step 1: Install Vercel CLI

```powershell
npm install -g vercel
```

### Step 2: Login to Vercel

```powershell
vercel login
```

This will:
- Open browser for authentication
- Link your Vercel account

### Step 3: Deploy Frontend

```powershell
cd frontend
vercel
```

Follow prompts:
- **Set up and deploy?** → Yes
- **Which scope?** → Your account
- **Link to existing project?** → No (or Yes if you have project ID `k6KjI0PFMQvhpMDtmzlZK9ca`)
- **Project name?** → `ai-interior-designer` (or your choice)
- **Directory?** → `./` (current directory)
- **Override settings?** → No

### Step 4: Set Environment Variables

After deployment, set environment variables:

```powershell
vercel env add NEXT_PUBLIC_API_BASE
# Enter value: https://api.yourdomain.com (or http://localhost:8000 for testing)

vercel env add NEXT_PUBLIC_WS_URL
# Enter value: wss://api.yourdomain.com (or ws://localhost:8000 for testing)

vercel env add NEXT_PUBLIC_DEMO_MODE
# Enter value: false (or true for testing)
```

Or use Vercel dashboard:
- Go to: https://vercel.com/dashboard
- Select your project
- Settings → Environment Variables
- Add variables

### Step 5: Redeploy

After adding environment variables:

```powershell
vercel --prod
```

---

## Quick Commands Summary

### GitHub
```bash
# Authenticate
gh auth login

# Create and push
gh repo create ai-interior-designer --public --source=. --remote=origin --push

# Or manual
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

### Vercel
```bash
# Install
npm install -g vercel

# Login
vercel login

# Deploy
cd frontend
vercel

# Add env vars
vercel env add NEXT_PUBLIC_API_BASE
vercel env add NEXT_PUBLIC_WS_URL
vercel env add NEXT_PUBLIC_DEMO_MODE

# Redeploy
vercel --prod
```

---

## Automated Script

Run the automated script:

```powershell
.\scripts\quick-deploy.ps1
```

This will:
- Check prerequisites
- Install Vercel CLI if needed
- Guide you through authentication
- Show deployment commands

---

## Troubleshooting

### GitHub Authentication Issues

**"Authentication failed"**
- Use Personal Access Token instead of password
- Create token: GitHub → Settings → Developer settings → Personal access tokens
- Use token as password when pushing

**"Repository not found"**
- Verify repository name is correct
- Check you have access to the repository
- Verify remote URL is correct

### Vercel Issues

**"Command not found: vercel"**
- Install: `npm install -g vercel`
- Verify: `vercel --version`

**"Login failed"**
- Try: `vercel login --debug`
- Check internet connection
- Try web login: https://vercel.com/login

**"Build failed"**
- Check `frontend/package.json` exists
- Verify `npm run build` works locally
- Check build logs in Vercel dashboard

---

## After Deployment

1. ✅ Get Vercel URL (e.g., `https://ai-interior-designer.vercel.app`)
2. ✅ Update backend `.env`:
   ```bash
   FRONTEND_PUBLIC_URL=https://ai-interior-designer.vercel.app
   ```
3. ✅ Test Supabase connection: `bash scripts/supabase-init.sh`
4. ✅ Initialize database: `cd backend && alembic upgrade head`
5. ✅ Test complete flow
6. ✅ Launch! 🚀

---

## Your Project IDs

- **GitHub**: Your repository URL
- **Vercel Project**: `k6KjI0PFMQvhpMDtmzlZK9ca`
- **Supabase Project**: `pzsdvpemnroxylbhjirr`

---

## Help

- **GitHub CLI Docs**: https://cli.github.com/manual/
- **Vercel CLI Docs**: https://vercel.com/docs/cli
- **Troubleshooting**: See `DEPLOYMENT_GUIDE.md`
