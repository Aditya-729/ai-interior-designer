# ⚡ Quick Start - Your Project

## Your Project IDs

✅ **Supabase Org**: `vqdppqslarmzzgmyixsw`  
✅ **Vercel Project ID**: `k6KjI0PFMQvhpMDtmzlZK9ca`

---

## Step 1: Get Supabase Database Credentials (5 min)

### 1.1 Open Supabase Dashboard
👉 **Go to**: https://supabase.com/dashboard/org/vqdppqslarmzzgmyixsw

### 1.2 Access Your Project
- Click on your project (or create one if you haven't)

### 1.3 Get Connection String
1. Click **Settings** (gear icon) → **Database**
2. Scroll to **Connection string** section
3. Select **URI** tab
4. **Copy the connection string**

It looks like:
```
postgresql://postgres:[PASSWORD]@db.xxxxx.supabase.co:5432/postgres
```

### 1.4 Extract Values
From the connection string, extract:

| Variable | Value | Example |
|----------|-------|---------|
| `SUPABASE_DB_HOST` | Part after `@` | `db.abcdefghijklmnop.supabase.co` |
| `SUPABASE_DB_PORT` | Usually `5432` | `5432` |
| `SUPABASE_DB_NAME` | Usually `postgres` | `postgres` |
| `SUPABASE_DB_USER` | Usually `postgres` | `postgres` |
| `SUPABASE_DB_PASSWORD` | Your password | `MyPassword123` |

### 1.5 Add to .env
Create or edit `.env` file in project root:

```bash
SUPABASE_DB_HOST=db.xxxxx.supabase.co
SUPABASE_DB_PORT=5432
SUPABASE_DB_NAME=postgres
SUPABASE_DB_USER=postgres
SUPABASE_DB_PASSWORD=your-actual-password
```

---

## Step 2: Get Vercel Project URL (2 min)

### 2.1 Open Vercel Dashboard
👉 **Go to**: https://vercel.com/dashboard

### 2.2 Find Your Project
- Search for project ID: `k6KjI0PFMQvhpMDtmzlZK9ca`
- Or browse your projects

### 2.3 Get Deployment URL
- Your project will show a URL like: `https://your-project-name.vercel.app`
- **Copy this URL**

### 2.4 Add to Backend .env
```bash
FRONTEND_PUBLIC_URL=https://your-project-name.vercel.app
```

### 2.5 Add to Vercel Environment Variables
In Vercel project → **Settings** → **Environment Variables**, add:

```
NEXT_PUBLIC_API_BASE=https://api.yourdomain.com
NEXT_PUBLIC_WS_URL=wss://api.yourdomain.com
NEXT_PUBLIC_DEMO_MODE=false
```

*(Replace `yourdomain.com` with your actual domain, or use `http://localhost:8000` for testing)*

---

## Step 3: Initialize Database (2 min)

On your GPU VM or local machine:

```bash
# If on Linux/Mac
./scripts/supabase-init.sh

# If on Windows (use Git Bash or WSL)
bash scripts/supabase-init.sh
```

This will:
- Test the connection
- Run database migrations
- Create all required tables

---

## Step 4: Verify Setup (1 min)

```bash
# If on Linux/Mac
./scripts/verify-setup.sh

# If on Windows
bash scripts/verify-setup.sh
```

---

## Step 5: Deploy & Test

### 5.1 Deploy to Vercel
1. Push your code to GitHub (if not already)
2. Vercel will auto-deploy
3. Or manually trigger: Vercel Dashboard → Deployments → Redeploy

### 5.2 Test Frontend
1. Open your Vercel URL
2. Check browser console for errors
3. Try uploading an image

### 5.3 Test Backend
```bash
curl https://api.yourdomain.com/api/v1/system/health
# Or locally:
curl http://localhost:8000/api/v1/system/health
```

---

## Direct Links

### Supabase
- **Dashboard**: https://supabase.com/dashboard/org/vqdppqslarmzzgmyixsw
- **Projects**: https://supabase.com/dashboard/org/vqdppqslarmzzgmyixsw/projects
- **Settings**: https://supabase.com/dashboard/org/vqdppqslarmzzgmyixsw/settings

### Vercel
- **Dashboard**: https://vercel.com/dashboard
- **Project**: https://vercel.com/dashboard (search for `k6KjI0PFMQvhpMDtmzlZK9ca`)

---

## Complete .env Template

```bash
# Supabase Database
SUPABASE_DB_HOST=db.xxxxx.supabase.co
SUPABASE_DB_PORT=5432
SUPABASE_DB_NAME=postgres
SUPABASE_DB_USER=postgres
SUPABASE_DB_PASSWORD=your-password

# Vercel Frontend
FRONTEND_PUBLIC_URL=https://your-project.vercel.app

# Backend Public URL (your domain or localhost)
PUBLIC_BACKEND_URL=https://api.yourdomain.com

# API Keys
MINO_AI_API_KEY=your-key
PERPLEXITY_API_KEY=your-key

# R2 Storage
R2_ACCOUNT_ID=your-id
R2_ACCESS_KEY_ID=your-key
R2_SECRET_ACCESS_KEY=your-secret
R2_ENDPOINT=https://xxxxx.r2.cloudflarestorage.com

# Production
PRODUCTION=false
DEMO_MODE=false
```

---

## Troubleshooting

### Can't find Supabase project?
- Make sure you're logged in
- Check: https://supabase.com/dashboard/org/vqdppqslarmzzgmyixsw/projects
- Create a new project if needed

### Can't find Vercel project?
- Search for: `k6KjI0PFMQvhpMDtmzlZK9ca`
- Or check: https://vercel.com/dashboard

### Connection failed?
- Verify password is correct
- Check host/port are correct
- Test with: `psql -h db.xxxxx.supabase.co -U postgres -d postgres`

---

## Next Steps

1. ✅ Get Supabase credentials → Add to `.env`
2. ✅ Get Vercel URL → Add to `.env` and Vercel
3. ✅ Initialize database → `./scripts/supabase-init.sh`
4. ✅ Verify setup → `./scripts/verify-setup.sh`
5. ✅ Test deployment
6. → Setup domain (optional) → See `docs/DOMAIN_SETUP.md`

---

## Help

- **Detailed Supabase Guide**: `scripts/get-supabase-credentials.md`
- **Detailed Vercel Guide**: `scripts/get-vercel-credentials.md`
- **Complete Setup**: `YOUR_SETUP.md`
- **Deployment Guide**: `docs/PUBLIC_DEPLOY.md`
