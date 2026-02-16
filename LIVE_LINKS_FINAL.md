# 🚀 Live Application Links

## ✅ Deployment Status

### GitHub
- **Repository:** https://github.com/Aditya-729/ai-interior-designer
- **Status:** All changes pushed to `master` branch
- **Latest Commits:**
  - Fix missing import for init_gpu_queue
  - Make ML packages optional (whisper, sentence-transformers)
  - Fix Railway Dockerfile configuration

### Frontend (Vercel)
- **Status:** ✅ Deployed and Live
- **Auto-deploy:** Enabled (deploys automatically on git push)

### Backend (Railway)
- **Status:** ⚠️ Deploying (should complete in 2-5 minutes)
- **Auto-deploy:** Enabled (deploys automatically on git push)

---

## 🔗 Live Links

### Frontend (Vercel)
**Production URL:** https://frontend-inky-eight-53.vercel.app

**Status:** ✅ Live and Working

### Backend (Railway)
**Production URL:** https://ai-interior-designer-backend-production.up.railway.app

**Status:** ⚠️ Deploying (check Railway dashboard for status)

**Health Check:** https://ai-interior-designer-backend-production.up.railway.app/api/v1/system/health

---

## 📋 Quick Access

### Main Application
**https://frontend-inky-eight-53.vercel.app**

### Backend API
**https://ai-interior-designer-backend-production.up.railway.app**

### Backend Health Check
**https://ai-interior-designer-backend-production.up.railway.app/api/v1/system/health**

---

## 🎯 Dashboard Links

- **Railway Dashboard:** https://railway.com/project/df46718f-fd2b-48e5-94b7-8e95758397d8
- **Vercel Dashboard:** https://vercel.com/dashboard
- **GitHub Repository:** https://github.com/Aditya-729/ai-interior-designer

---

## ⚙️ Configuration Status

### Vercel Environment Variables
- ✅ `NEXT_PUBLIC_API_BASE` = https://ai-interior-designer-backend-production.up.railway.app
- ✅ `NEXT_PUBLIC_WS_URL` = wss://ai-interior-designer-backend-production.up.railway.app

### Railway Environment Variables
Set these in Railway dashboard:
- `FRONTEND_PUBLIC_URL` = https://frontend-inky-eight-53.vercel.app
- `FRONTEND_URL` = https://frontend-inky-eight-53.vercel.app
- `ENVIRONMENT` = production
- `PRODUCTION` = true
- `INFERENCE_DEVICE` = cpu
- Database credentials (Supabase)
- API keys (MINO_AI_API_KEY, PERPLEXITY_API_KEY, R2 credentials)

---

## 📝 Notes

1. **Backend Deployment:** Railway is currently deploying. Wait 2-5 minutes for it to complete.
2. **ML Packages:** Whisper and sentence-transformers are optional. App will work without them (with reduced functionality).
3. **Auto-Deploy:** Both Vercel and Railway are connected to GitHub and will auto-deploy on push.

---

## 🎉 Your Application is Live!

**Main URL:** https://frontend-inky-eight-53.vercel.app

Once Railway deployment completes, the full application will be functional!
