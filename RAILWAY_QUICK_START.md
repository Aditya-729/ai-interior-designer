# 🚂 Railway Quick Start Guide

## Current Step: You're on Railway's "New Project" Page

### What to Do Now:

1. **Click "GitHub Repository"** (first option with GitHub icon)
2. **Authorize Railway** (if prompted)
3. **Select**: `Aditya-729/ai-interior-designer`
4. **Click "Deploy Now"**

---

## After Railway Imports Your Repo:

### Step 1: Configure Service

1. Railway will create a service automatically
2. **Click on the service** to open it
3. Go to **Settings** tab
4. Set **Root Directory** to: `backend`
5. **Save**

### Step 2: Add Environment Variables

1. Go to **Variables** tab
2. Click **+ New Variable**
3. Add these **one by one**:

**Copy from your `.env` file:**

```bash
MINO_AI_API_KEY=...
PERPLEXITY_API_KEY=...
R2_ACCOUNT_ID=...
R2_ACCESS_KEY_ID=...
R2_SECRET_ACCESS_KEY=...
R2_BUCKET_NAME=ai-interior-designer
R2_ENDPOINT=...
SUPABASE_DB_HOST=...
SUPABASE_DB_PORT=5432
SUPABASE_DB_NAME=postgres
SUPABASE_DB_USER=postgres
SUPABASE_DB_PASSWORD=...
JWT_SECRET=your-secret-here
ENVIRONMENT=production
PRODUCTION=true
INFERENCE_DEVICE=cpu
```

**Important:** 
- Don't set `BACKEND_URL` yet - Railway will give you the URL after deployment
- Don't set `FRONTEND_PUBLIC_URL` yet - we'll add it after

### Step 3: Wait for Deployment

1. Railway will automatically start building
2. Watch the **Deployments** tab
3. Wait 2-5 minutes for build to complete

### Step 4: Get Your Backend URL

1. Once deployed, go to **Settings** tab
2. Scroll to **Domains** section
3. You'll see: `https://your-app.railway.app`
4. **Copy this URL!** ✅

---

## Next: Update Vercel

Once you have your Railway URL:

1. Go to: https://vercel.com/dashboard
2. Your project → **Settings** → **Environment Variables**
3. Add:
   - `NEXT_PUBLIC_API_BASE` = `https://your-app.railway.app`
   - `NEXT_PUBLIC_WS_URL` = `wss://your-app.railway.app`
4. **Redeploy** Vercel

---

## Test Your Backend

Open in browser:
```
https://your-app.railway.app/api/v1/system/health
```

Should show: `{"status": "healthy", ...}`

---

## Need Help?

- See full guide: `DEPLOY_TO_RAILWAY.md`
- Check Railway logs: **Deployments** → **View Logs**
- Railway docs: https://docs.railway.app
