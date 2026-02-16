# 🚂 Automated Railway Deployment

I've prepared everything for Railway deployment. Here's what's ready:

## ✅ What's Prepared

1. **Railway CLI** - Installed ✅
2. **Procfile** - Start command configured ✅
3. **runtime.txt** - Python version specified ✅
4. **railway.json** - Railway configuration ✅
5. **Deployment Script** - Ready to run ✅

## 🚀 Quick Deploy Steps

### Step 1: Authenticate with Railway

Run this command (it will open your browser):

```powershell
railway login
```

This will:
- Open your browser
- Ask you to authorize Railway CLI
- Complete authentication automatically

### Step 2: Run Deployment Script

After authentication, run:

```powershell
.\scripts\deploy-to-railway.ps1
```

The script will:
- ✅ Check Railway authentication
- ✅ Link to your GitHub repo (or create new project)
- ✅ Configure the service
- ✅ Deploy your backend
- ✅ Get your backend URL

### Step 3: Set Environment Variables

The script will prompt you to set environment variables in Railway dashboard.

**Required variables:**
- `MINO_AI_API_KEY`
- `PERPLEXITY_API_KEY`
- `R2_ACCOUNT_ID`
- `R2_ACCESS_KEY_ID`
- `R2_SECRET_ACCESS_KEY`
- `R2_BUCKET_NAME=ai-interior-designer`
- `R2_ENDPOINT`
- `SUPABASE_DB_HOST`
- `SUPABASE_DB_PORT=5432`
- `SUPABASE_DB_NAME=postgres`
- `SUPABASE_DB_USER=postgres`
- `SUPABASE_DB_PASSWORD`
- `JWT_SECRET` (any random string)
- `ENVIRONMENT=production`
- `PRODUCTION=true`
- `INFERENCE_DEVICE=cpu`

### Step 4: Get Your Backend URL

After deployment, Railway will give you a URL like:
```
https://your-app.railway.app
```

### Step 5: Update Vercel

Set these in Vercel:
- `NEXT_PUBLIC_API_BASE` = `https://your-app.railway.app`
- `NEXT_PUBLIC_WS_URL` = `wss://your-app.railway.app`

---

## 🎯 Ready to Deploy?

1. **Authenticate**: `railway login`
2. **Run script**: `.\scripts\deploy-to-railway.ps1`
3. **Set variables** in Railway dashboard
4. **Get URL** and update Vercel

Let me know when you're ready and I can help with any step!
