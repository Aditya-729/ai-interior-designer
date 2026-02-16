# 🚂 Deploy Backend to Railway - Step by Step

This guide will help you deploy your backend to Railway and get the API URLs you need for Vercel.

## Prerequisites

- ✅ GitHub repository: `https://github.com/Aditya-729/ai-interior-designer`
- ✅ Railway account (sign up at https://railway.app if needed)
- ✅ Backend code is in the `backend` folder

---

## Step 1: Create New Project on Railway

1. **Go to Railway**: https://railway.app/new
2. **Click "GitHub Repository"** (first option)
3. **Authorize Railway** to access your GitHub (if first time)
4. **Select your repository**: `Aditya-729/ai-interior-designer`
5. **Click "Deploy Now"**

---

## Step 2: Configure the Service

After Railway imports your repo, you need to configure it:

### 2.1 Set Root Directory

1. Click on the service that was created
2. Go to **Settings** tab
3. Find **Root Directory**
4. Set it to: `backend`
5. Click **Save**

### 2.2 Configure Build Settings

1. Still in **Settings**
2. Find **Build Command** (or leave empty - Railway auto-detects Python)
3. Find **Start Command**
4. Set it to:
   ```
   uvicorn main:app --host 0.0.0.0 --port $PORT
   ```
5. Click **Save**

---

## Step 3: Add Environment Variables

1. Go to **Variables** tab in your Railway service
2. Click **+ New Variable**
3. Add all your environment variables from your `.env` file:

### Required Variables:

```bash
# API Keys
MINO_AI_API_KEY=your-mino-key
PERPLEXITY_API_KEY=your-perplexity-key

# Cloudflare R2 (Storage)
R2_ACCOUNT_ID=your-r2-account-id
R2_ACCESS_KEY_ID=your-r2-access-key
R2_SECRET_ACCESS_KEY=your-r2-secret-key
R2_BUCKET_NAME=ai-interior-designer
R2_ENDPOINT=https://your-account-id.r2.cloudflarestorage.com

# Database (Supabase)
SUPABASE_DB_HOST=db.xxxxx.supabase.co
SUPABASE_DB_PORT=5432
SUPABASE_DB_NAME=postgres
SUPABASE_DB_USER=postgres
SUPABASE_DB_PASSWORD=your-password

# Application
BACKEND_URL=https://your-app.railway.app
FRONTEND_PUBLIC_URL=https://frontend-jgsrttgb7-adityas-projects-e275b3df.vercel.app
JWT_SECRET=your-secret-key-here
ENVIRONMENT=production
PRODUCTION=true

# Inference Service (if separate)
INFERENCE_SERVICE_URL=http://localhost:8001
INFERENCE_DEVICE=cpu  # Railway doesn't have GPU, use CPU or external service
```

**Note:** 
- Railway will give you a URL like `https://your-app.railway.app` after deployment
- You can update `BACKEND_URL` after you get the actual URL
- For GPU inference, you'll need a separate service (like RunPod, Vast.ai, or your own GPU server)

---

## Step 4: Deploy

1. Railway will automatically start deploying
2. Watch the **Deployments** tab for progress
3. Wait for build to complete (2-5 minutes)

---

## Step 5: Get Your Backend URL

1. Once deployed, go to **Settings** tab
2. Scroll to **Domains** section
3. You'll see your Railway URL: `https://your-app.railway.app`
4. **Copy this URL** - this is your backend API URL!

---

## Step 6: Test Your Backend

Test that your backend is working:

```powershell
# Test health endpoint
curl https://your-app.railway.app/api/v1/system/health
```

Or open in browser:
```
https://your-app.railway.app/api/v1/system/health
```

Should return: `{"status": "healthy", ...}`

---

## Step 7: Update Vercel Environment Variables

Now that you have your backend URL:

1. **Go to Vercel**: https://vercel.com/dashboard
2. **Select your project**: `adityas-projects-e275b3df/frontend`
3. **Settings** → **Environment Variables**
4. **Add these variables:**

   **Variable 1:**
   - Name: `NEXT_PUBLIC_API_BASE`
   - Value: `https://your-app.railway.app` (your Railway URL)
   - Environment: Production (and Preview if you want)

   **Variable 2:**
   - Name: `NEXT_PUBLIC_WS_URL`
   - Value: `wss://your-app.railway.app` (same URL, but with `wss://`)
   - Environment: Production (and Preview if you want)

5. **Click Save**

---

## Step 8: Redeploy Vercel

1. Go to **Deployments** tab in Vercel
2. Click **⋯** (three dots) on the latest deployment
3. Click **Redeploy**
4. Wait for deployment to complete

---

## Step 9: Test Everything

1. **Open your Vercel app**: https://frontend-jgsrttgb7-adityas-projects-e275b3df.vercel.app
2. **Try uploading an image**
3. **Check browser console** (F12) for any errors
4. **Test the complete flow**

---

## Troubleshooting

### Build Fails

- Check **Deployments** → **View Logs** in Railway
- Make sure **Root Directory** is set to `backend`
- Verify all environment variables are set

### Backend Not Responding

- Check Railway **Deployments** tab for errors
- Verify `PORT` environment variable (Railway sets this automatically)
- Check that start command is correct

### CORS Errors

- Make sure `FRONTEND_PUBLIC_URL` in Railway matches your Vercel URL
- Check backend CORS configuration allows your Vercel domain

### Database Connection Issues

- Verify Supabase credentials are correct
- Check that Supabase allows connections from Railway's IPs
- Test connection: `psql -h db.xxxxx.supabase.co -U postgres -d postgres`

---

## Important Notes

### GPU Inference

Railway **does not support GPU**. For AI inference, you have options:

1. **Use CPU** (slower, but works):
   - Set `INFERENCE_DEVICE=cpu` in Railway
   - Inference will be slower but functional

2. **External GPU Service**:
   - Deploy inference service separately on:
     - RunPod (https://runpod.io)
     - Vast.ai (https://vast.ai)
     - Your own GPU server
   - Update `INFERENCE_SERVICE_URL` to point to that service

3. **Hybrid Setup**:
   - Backend on Railway (API, database)
   - Inference service on GPU server
   - Connect them via `INFERENCE_SERVICE_URL`

### Free Tier Limits

- Railway free tier has usage limits
- Consider upgrading for production use
- Monitor usage in Railway dashboard

---

## Quick Reference

**Your URLs:**
- **Backend API**: `https://your-app.railway.app`
- **Frontend**: `https://frontend-jgsrttgb7-adityas-projects-e275b3df.vercel.app`

**Vercel Environment Variables:**
```
NEXT_PUBLIC_API_BASE=https://your-app.railway.app
NEXT_PUBLIC_WS_URL=wss://your-app.railway.app
```

**Railway Environment Variables:**
- All your `.env` variables
- `FRONTEND_PUBLIC_URL=https://frontend-jgsrttgb7-adityas-projects-e275b3df.vercel.app`

---

## Next Steps

1. ✅ Deploy backend to Railway
2. ✅ Get Railway URL
3. ✅ Set Vercel environment variables
4. ✅ Redeploy Vercel
5. ✅ Test your app!

Your app should now work end-to-end! 🎉
