# 🚀 Complete Deployment Guide

## Step 1: Test Configuration ✅

Your configuration has been verified:
- ✅ Supabase password configured
- ✅ API keys added
- ✅ Environment variables set

---

## Step 2: Deploy to GitHub

### Option A: Using Script (Recommended)
```powershell
.\scripts\deploy-to-github.ps1
```

### Option B: Manual Steps

1. **Initialize Git** (if not done):
   ```bash
   git init
   ```

2. **Create .gitignore** (if not exists):
   - Already created with proper exclusions
   - Ensures `.env` is NOT committed

3. **Stage and Commit**:
   ```bash
   git add .
   git commit -m "Initial commit: AI Interior Designer MVP"
   ```

4. **Create GitHub Repository**:
   - Go to: https://github.com/new
   - Create a new repository
   - **Don't** initialize with README (you already have files)

5. **Add Remote and Push**:
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
   git branch -M main
   git push -u origin main
   ```

---

## Step 3: Deploy to Vercel

### Quick Steps

1. **Go to Vercel**: https://vercel.com/dashboard
2. **Import Repository**:
   - Click "Add New..." → "Project"
   - Select your GitHub repository
   - Or use existing project ID: `k6KjI0PFMQvhpMDtmzlZK9ca`

3. **Configure Project**:
   - **Root Directory**: `frontend` ⚠️ **IMPORTANT**
   - **Framework**: Next.js (auto-detected)
   - **Build Command**: `npm run build`
   - **Output Directory**: `.next`

4. **Set Environment Variables**:
   ```
   NEXT_PUBLIC_API_BASE=https://api.yourdomain.com
   NEXT_PUBLIC_WS_URL=wss://api.yourdomain.com
   NEXT_PUBLIC_DEMO_MODE=false
   ```

5. **Deploy**:
   - Click "Deploy"
   - Wait 2-5 minutes
   - Get your URL: `https://your-project.vercel.app`

6. **Update Backend**:
   - Add to backend `.env`: `FRONTEND_PUBLIC_URL=https://your-project.vercel.app`
   - Restart backend services

---

## Step 4: Test Supabase Connection

Before deploying backend, test the connection:

```bash
bash scripts/supabase-init.sh
```

This will:
- Test database connection
- Run migrations
- Create all tables

---

## Complete Checklist

### GitHub ✅
- [ ] Git repository initialized
- [ ] Files committed
- [ ] GitHub repository created
- [ ] Code pushed to GitHub

### Vercel ✅
- [ ] Repository connected to Vercel
- [ ] Root directory set to `frontend`
- [ ] Environment variables configured
- [ ] Deployment successful
- [ ] Vercel URL obtained

### Backend ✅
- [ ] Supabase connection tested
- [ ] Database initialized
- [ ] `.env` updated with Vercel URL
- [ ] Backend services running

### Testing ✅
- [ ] Frontend loads correctly
- [ ] API connection works
- [ ] Image upload works
- [ ] Complete flow tested

---

## Quick Commands

### GitHub
```bash
# Check status
git status

# Stage all
git add .

# Commit
git commit -m "Your message"

# Push
git push origin main
```

### Vercel
- Dashboard: https://vercel.com/dashboard
- Deploy: Automatic on push (if configured)
- Manual: Vercel dashboard → Deploy

### Testing
```bash
# Test Supabase
bash scripts/supabase-init.sh

# Test backend
cd backend && python -m uvicorn app.main:app --reload

# Test frontend
cd frontend && npm run dev
```

---

## Troubleshooting

### Git Issues
- **"Not a git repository"**: Run `git init`
- **"Remote already exists"**: Use `git remote set-url origin <new-url>`
- **Push rejected**: Pull first: `git pull origin main --rebase`

### Vercel Issues
- **Build fails**: Check logs, verify `frontend/package.json`
- **404 errors**: Check root directory is `frontend`
- **API errors**: Verify environment variables

### Connection Issues
- **Supabase fails**: Check password, host, firewall
- **Backend unreachable**: Check CORS, public URL
- **WebSocket fails**: Verify `NEXT_PUBLIC_WS_URL`

---

## Next Steps After Deployment

1. ✅ Get Vercel URL
2. ✅ Update backend `.env`
3. ✅ Setup domain (optional)
4. ✅ Configure HTTPS
5. ✅ Test complete flow
6. ✅ Launch! 🎉

---

## Helpful Links

- **GitHub**: https://github.com
- **Vercel Dashboard**: https://vercel.com/dashboard
- **Supabase Dashboard**: https://supabase.com/dashboard/project/pzsdvpemnroxylbhjirr
- **Your Vercel Project**: Search for `k6KjI0PFMQvhpMDtmzlZK9ca`
