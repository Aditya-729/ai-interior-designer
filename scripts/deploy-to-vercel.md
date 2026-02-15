# 🚀 Deploy to Vercel - Step by Step

## Prerequisites
- ✅ Code pushed to GitHub
- ✅ Vercel account created
- ✅ Project ID: `k6KjI0PFMQvhpMDtmzlZK9ca`

---

## Step 1: Connect Repository to Vercel

1. Go to: https://vercel.com/dashboard
2. Click **"Add New..."** → **"Project"**
3. If your repository isn't listed:
   - Click **"Import Git Repository"**
   - Authorize Vercel to access your GitHub
   - Select your repository: `AI Interior Designer`

---

## Step 2: Configure Project Settings

### Basic Settings
- **Framework Preset**: Next.js (auto-detected)
- **Root Directory**: `frontend` ⚠️ **IMPORTANT**
- **Build Command**: `npm run build` (default)
- **Output Directory**: `.next` (default)
- **Install Command**: `npm install` (default)

### Environment Variables
Click **"Environment Variables"** and add:

```
NEXT_PUBLIC_API_BASE=https://api.yourdomain.com
NEXT_PUBLIC_WS_URL=wss://api.yourdomain.com
NEXT_PUBLIC_DEMO_MODE=false
```

**For testing (if backend is localhost):**
```
NEXT_PUBLIC_API_BASE=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8000
NEXT_PUBLIC_DEMO_MODE=true
```

---

## Step 3: Deploy

1. Click **"Deploy"**
2. Wait for build to complete (2-5 minutes)
3. Your app will be live at: `https://your-project.vercel.app`

---

## Step 4: Update Backend .env

After Vercel deployment, update your backend `.env`:

```bash
FRONTEND_PUBLIC_URL=https://your-project.vercel.app
```

---

## Step 5: Verify Deployment

1. Open your Vercel URL
2. Check browser console for errors
3. Test API connection
4. Test image upload

---

## Troubleshooting

### Build Fails
- Check build logs in Vercel dashboard
- Verify `frontend/package.json` has all dependencies
- Ensure `npm run build` works locally

### API Connection Fails
- Verify `NEXT_PUBLIC_API_BASE` is correct
- Check CORS settings on backend
- Ensure backend is accessible

### Environment Variables Not Working
- Redeploy after adding variables
- Check variable names are correct
- Verify no typos

---

## Quick Links

- **Vercel Dashboard**: https://vercel.com/dashboard
- **Your Project**: https://vercel.com/dashboard (search for `k6KjI0PFMQvhpMDtmzlZK9ca`)
- **Deployments**: Check deployment status and logs

---

## After Deployment

1. ✅ Get Vercel URL
2. ✅ Update backend `.env` with `FRONTEND_PUBLIC_URL`
3. ✅ Restart backend services
4. ✅ Test complete flow
5. ✅ Share your app! 🎉
