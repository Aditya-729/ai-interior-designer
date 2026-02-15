# 🧙 Setup Wizard - Step by Step

Follow these steps in order to get everything set up.

## Phase 1: Supabase Setup (10 minutes)

### Step 1.1: Create Account
1. Open browser → https://supabase.com
2. Click **"Start your project"**
3. Sign up with GitHub (easiest)

### Step 1.2: Create Project
1. Click **"New Project"**
2. Name: `AI Interior Designer`
3. **IMPORTANT**: Generate and save database password
4. Region: Choose closest to your GPU VM
5. Click **"Create new project"**
6. Wait 2-3 minutes

### Step 1.3: Get Credentials
1. Go to **Settings** → **Database**
2. Scroll to **Connection string**
3. Select **URI** format
4. Copy the connection string

### Step 1.4: Extract Details
From connection string: `postgresql://postgres:[PASSWORD]@db.xxxxx.supabase.co:5432/postgres`

Extract:
- Host: `db.xxxxx.supabase.co`
- Port: `5432`
- Database: `postgres`
- User: `postgres`
- Password: `[PASSWORD]` (the one you saved)

### Step 1.5: Add to .env
```bash
# Run this to create template
./scripts/setup-env-template.sh

# Then edit .env and add:
SUPABASE_DB_HOST=db.xxxxx.supabase.co
SUPABASE_DB_PORT=5432
SUPABASE_DB_NAME=postgres
SUPABASE_DB_USER=postgres
SUPABASE_DB_PASSWORD=your-actual-password
```

### Step 1.6: Test Connection
```bash
./scripts/verify-setup.sh
```

---

## Phase 2: Vercel Setup (10 minutes)

### Step 2.1: Create Account
1. Open browser → https://vercel.com
2. Click **"Sign up"**
3. Sign up with GitHub (connects to your repo)

### Step 2.2: Import Repository
1. Click **"Add New..."** → **"Project"**
2. Authorize Vercel to access GitHub
3. Find your repository: `AI Interior Designer`
4. Click **"Import"**

### Step 2.3: Configure Project
1. **Framework**: Next.js (auto-detected)
2. **Root Directory**: `frontend`
3. **Build Command**: `npm run build` (default)
4. **Output Directory**: `.next` (default)

### Step 2.4: Set Environment Variables
Before deploying, click **"Environment Variables"** and add:

**For Production:**
```
NEXT_PUBLIC_API_BASE=https://api.yourdomain.com
NEXT_PUBLIC_WS_URL=wss://api.yourdomain.com
NEXT_PUBLIC_DEMO_MODE=false
```

**For Testing (use Vercel URL):**
```
NEXT_PUBLIC_API_BASE=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8000
NEXT_PUBLIC_DEMO_MODE=true
```

### Step 2.5: Deploy
1. Click **"Deploy"**
2. Wait for build (2-5 minutes)
3. Your app is live at: `https://your-project.vercel.app`

### Step 2.6: Update Backend .env
After Vercel deployment, update your backend `.env`:
```bash
FRONTEND_PUBLIC_URL=https://your-project.vercel.app
```

---

## Phase 3: Verify Everything

### Test Supabase
```bash
./scripts/supabase-init.sh
```

### Test Vercel
1. Open: `https://your-project.vercel.app`
2. Should load without errors

### Test Complete Flow
```bash
./scripts/public-smoke-test.sh
```

---

## Quick Reference

### Supabase Dashboard
- URL: https://supabase.com/dashboard
- Get credentials: Settings → Database → Connection string

### Vercel Dashboard
- URL: https://vercel.com/dashboard
- Set env vars: Project → Settings → Environment Variables
- View logs: Project → Deployments → [deployment] → Logs

### Your Backend
- Health check: `https://api.yourdomain.com/api/v1/system/health`
- Or locally: `http://localhost:8000/api/v1/system/health`

---

## Troubleshooting

### "Supabase connection failed"
- Check password is correct
- Verify host/port are correct
- Check firewall allows outbound connections
- Try: `psql -h db.xxxxx.supabase.co -U postgres -d postgres`

### "Vercel build failed"
- Check `frontend/package.json` exists
- Verify `npm run build` works locally
- Check build logs in Vercel dashboard
- Ensure all dependencies are in `package.json`

### "Frontend can't connect to backend"
- Verify `NEXT_PUBLIC_API_BASE` is set correctly
- Check backend CORS allows Vercel domain
- Test backend health endpoint directly
- Check browser console for errors

---

## ✅ Completion Checklist

- [ ] Supabase account created
- [ ] Supabase project created
- [ ] Database credentials saved
- [ ] Supabase credentials in `.env`
- [ ] Supabase connection tested
- [ ] Vercel account created
- [ ] Repository imported to Vercel
- [ ] Environment variables set in Vercel
- [ ] Vercel deployment successful
- [ ] Frontend URL added to backend `.env`
- [ ] Complete flow tested

---

## 🎉 You're Done!

Once all checkboxes are checked, your system is ready for production!

Next: Set up your domain (see `docs/DOMAIN_SETUP.md`)
