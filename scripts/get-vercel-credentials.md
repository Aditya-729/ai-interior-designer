# 🚀 Getting Vercel Project Details

## Your Vercel Project ID
**Project ID**: `k6KjI0PFMQvhpMDtmzlZK9ca`

## Steps to Configure

### 1. Access Your Project
1. Go to: https://vercel.com/dashboard
2. Find your project (search for the ID: `k6KjI0PFMQvhpMDtmzlZK9ca`)
3. Click on the project

### 2. Get Project URL
1. In your project dashboard, you'll see the deployment URL
2. It will look like: `https://your-project-name.vercel.app`
3. Copy this URL - this is your `FRONTEND_PUBLIC_URL`

### 3. Set Environment Variables
1. In your Vercel project, go to **Settings** → **Environment Variables**
2. Add these variables:

**For Production:**
```
NEXT_PUBLIC_API_BASE=https://api.yourdomain.com
NEXT_PUBLIC_WS_URL=wss://api.yourdomain.com
NEXT_PUBLIC_DEMO_MODE=false
```

**For Testing (if backend is on localhost):**
```
NEXT_PUBLIC_API_BASE=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8000
NEXT_PUBLIC_DEMO_MODE=true
```

### 4. Update Backend .env
After getting your Vercel URL, update your backend `.env`:
```bash
FRONTEND_PUBLIC_URL=https://your-project-name.vercel.app
```

### 5. Redeploy (if needed)
1. Go to **Deployments** tab
2. Click **Redeploy** if you changed environment variables
3. Or push a new commit to trigger auto-deploy

---

## Quick Access

- **Vercel Dashboard**: https://vercel.com/dashboard
- **Project Settings**: https://vercel.com/dashboard/[your-project]/settings
- **Environment Variables**: https://vercel.com/dashboard/[your-project]/settings/environment-variables
- **Deployments**: https://vercel.com/dashboard/[your-project]/deployments

---

## Project Configuration

Your project should have:
- **Framework**: Next.js
- **Root Directory**: `frontend`
- **Build Command**: `npm run build`
- **Output Directory**: `.next`

---

## Next Steps

1. ✅ Get Vercel project URL
2. ✅ Set environment variables in Vercel
3. ✅ Update backend `.env` with `FRONTEND_PUBLIC_URL`
4. ✅ Test deployment
5. ✅ Verify frontend can connect to backend
