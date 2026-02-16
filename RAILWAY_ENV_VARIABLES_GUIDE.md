# Railway Environment Variables Guide

## Where to Set Environment Variables in Railway

### Step-by-Step Instructions:

1. **Go to Railway Dashboard**
   - URL: https://railway.com/project/df46718f-fd2b-48e5-94b7-8e95758397d8

2. **Click on your service** (`ai-interior-designer-backend`)

3. **Click on the "Variables" tab** (in the service view)

4. **Add each variable** by clicking "New Variable"
   - Enter the variable name
   - Enter the variable value
   - Click "Add"

---

## Required Environment Variables

### 🔴 CRITICAL (Required for app to start)

These MUST be set or the backend will crash on startup:

```bash
# API Keys (REQUIRED)
MINO_AI_API_KEY=your-mino-api-key-here
PERPLEXITY_API_KEY=your-perplexity-api-key-here

# Cloudflare R2 Storage (REQUIRED)
R2_ACCOUNT_ID=your-r2-account-id
R2_ACCESS_KEY_ID=your-r2-access-key-id
R2_SECRET_ACCESS_KEY=your-r2-secret-access-key
R2_ENDPOINT=https://your-account-id.r2.cloudflarestorage.com
R2_BUCKET_NAME=ai-interior-designer

# Database (REQUIRED - Use Supabase)
SUPABASE_DB_HOST=db.pzsdvpemnroxylbhjirr.supabase.co
SUPABASE_DB_PORT=5432
SUPABASE_DB_NAME=postgres
SUPABASE_DB_USER=postgres
SUPABASE_DB_PASSWORD=cuetpassaiinterior

# Application URLs (REQUIRED)
FRONTEND_PUBLIC_URL=https://frontend-inky-eight-53.vercel.app
FRONTEND_URL=https://frontend-inky-eight-53.vercel.app
BACKEND_URL=https://ai-interior-designer-backend-production.up.railway.app
PUBLIC_BACKEND_URL=https://ai-interior-designer-backend-production.up.railway.app

# Environment (REQUIRED)
ENVIRONMENT=production
PRODUCTION=true
JWT_SECRET=your-secret-jwt-key-change-this-in-production
```

### 🟡 IMPORTANT (For full functionality)

```bash
# Inference Settings
INFERENCE_DEVICE=cpu
INFERENCE_SERVICE_URL=http://localhost:8001

# Whisper Settings (if using transcription)
WHISPER_MODEL=base
WHISPER_DEVICE=cpu

# GPU Queue Settings
GPU_MAX_CONCURRENT=2
GPU_QUEUE_MAX_SIZE=10

# Logging
LOG_LEVEL=INFO
```

### 🟢 OPTIONAL (Can be left as defaults)

```bash
# Supabase (if using Supabase features)
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_KEY=your-service-key

# Vector Database (if using Qdrant)
QDRANT_HOST=localhost
QDRANT_PORT=6333

# Demo Mode (should be false in production)
DEMO_MODE=false
```

---

## Quick Copy-Paste List for Railway

Copy these into Railway Variables tab:

### Minimum Required Set:

```
MINO_AI_API_KEY=your-mino-api-key
PERPLEXITY_API_KEY=your-perplexity-api-key
R2_ACCOUNT_ID=your-r2-account-id
R2_ACCESS_KEY_ID=your-r2-access-key
R2_SECRET_ACCESS_KEY=your-r2-secret-key
R2_ENDPOINT=your-r2-endpoint-url
R2_BUCKET_NAME=ai-interior-designer
SUPABASE_DB_HOST=db.pzsdvpemnroxylbhjirr.supabase.co
SUPABASE_DB_PORT=5432
SUPABASE_DB_NAME=postgres
SUPABASE_DB_USER=postgres
SUPABASE_DB_PASSWORD=cuetpassaiinterior
FRONTEND_PUBLIC_URL=https://frontend-inky-eight-53.vercel.app
FRONTEND_URL=https://frontend-inky-eight-53.vercel.app
BACKEND_URL=https://ai-interior-designer-backend-production.up.railway.app
PUBLIC_BACKEND_URL=https://ai-interior-designer-backend-production.up.railway.app
ENVIRONMENT=production
PRODUCTION=true
JWT_SECRET=prod-secret-change-this-to-random-string
INFERENCE_DEVICE=cpu
```

---

## How to Check Which Variables Are Missing

### Method 1: Check Railway Logs
1. Go to Railway dashboard
2. Click on your service
3. Go to "Deploy Logs" or "HTTP Logs"
4. Look for error messages mentioning missing variables

### Method 2: Check Backend Startup Errors
The backend will fail to start if required variables are missing. Check logs for:
- `ValidationError`
- `Field required`
- `Missing required environment variable`

### Method 3: Test Locally
Run the backend locally and check which variables it complains about.

---

## Common Issues

### Issue: Backend crashes on startup
**Solution:** Check if all REQUIRED variables are set (especially API keys and database credentials)

### Issue: Database connection fails
**Solution:** Verify `SUPABASE_DB_*` variables are correct

### Issue: CORS errors
**Solution:** Make sure `FRONTEND_PUBLIC_URL` and `FRONTEND_URL` are set correctly

### Issue: File upload fails
**Solution:** Verify all `R2_*` variables are set correctly

---

## Railway Dashboard Direct Link

**Variables Tab:**
https://railway.com/project/df46718f-fd2b-48e5-94b7-8e95758397d8/service/[SERVICE_ID]/variables

(Replace `[SERVICE_ID]` with your actual service ID)

---

## After Setting Variables

1. **Save all variables** in Railway
2. **Railway will automatically redeploy** when variables change
3. **Wait 2-3 minutes** for redeployment
4. **Check logs** to verify backend starts successfully
5. **Test the health endpoint:** https://ai-interior-designer-backend-production.up.railway.app/api/v1/system/health

---

## Notes

- Variables are case-sensitive in Railway
- No quotes needed around values
- Railway automatically redeploys when variables are added/changed
- Check Railway logs if backend still doesn't start after setting variables
