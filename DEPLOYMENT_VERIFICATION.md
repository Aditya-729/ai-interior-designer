# Deployment Verification Checklist

## ✅ Code Verification Complete

### Backend
- ✅ Configuration updated for Supabase
- ✅ Public URL support added
- ✅ CORS configured for production
- ✅ Cookies hardened for HTTPS
- ✅ System health endpoint created
- ✅ WebSocket URL endpoint added
- ✅ GPU queue status method added
- ✅ Production safety flags validated

### Frontend
- ✅ All API calls use environment variables
- ✅ WebSocket connection with auto-reconnect
- ✅ Share page with SEO metadata
- ✅ Export functionality with watermark
- ✅ Vercel configuration added
- ✅ Build hardening (framer-motion SSR)
- ✅ Next.js config optimized

### Scripts
- ✅ Supabase init script created
- ✅ Smoke test script created
- ✅ Backup script created
- ✅ All scripts are executable

### Documentation
- ✅ Complete deployment guide
- ✅ Domain setup guide
- ✅ Supabase setup instructions
- ✅ Environment variable examples

## 🚀 Next Steps (Manual - Require Your Accounts)

### 1. Create Supabase Project
```bash
# Go to supabase.com
# Create new project
# Get database credentials
# Add to .env file
```

### 2. Setup GPU VM
```bash
# SSH into your GPU VM
# Install Docker + NVIDIA runtime
# Clone repository
# Configure .env with Supabase credentials
# Run: ./scripts/supabase-init.sh
# Start: docker-compose -f docker-compose.gpu.yml up -d
```

### 3. Configure Domain
```bash
# Point DNS: api.yourdomain.com → VM IP
# Install Caddy or Nginx
# Configure reverse proxy
# SSL auto-configured
```

### 4. Deploy to Vercel
```bash
# Go to vercel.com
# Import repository
# Set environment variables:
#   NEXT_PUBLIC_API_BASE=https://api.yourdomain.com
#   NEXT_PUBLIC_WS_URL=wss://api.yourdomain.com
#   NEXT_PUBLIC_DEMO_MODE=false
# Deploy
```

### 5. Verify Deployment
```bash
# Run smoke test
./scripts/public-smoke-test.sh

# Test endpoints
curl https://api.yourdomain.com/api/v1/system/health
curl https://your-app.vercel.app
```

## 📋 Environment Variables Checklist

### Backend (.env on GPU VM)
- [ ] SUPABASE_DB_HOST
- [ ] SUPABASE_DB_PORT
- [ ] SUPABASE_DB_NAME
- [ ] SUPABASE_DB_USER
- [ ] SUPABASE_DB_PASSWORD
- [ ] PUBLIC_BACKEND_URL
- [ ] FRONTEND_PUBLIC_URL
- [ ] PRODUCTION=true
- [ ] DEMO_MODE=false
- [ ] All API keys (MINO_AI_API_KEY, PERPLEXITY_API_KEY, etc.)
- [ ] R2 storage credentials

### Frontend (Vercel Environment Variables)
- [ ] NEXT_PUBLIC_API_BASE
- [ ] NEXT_PUBLIC_WS_URL
- [ ] NEXT_PUBLIC_DEMO_MODE=false

## ✅ Code is Ready

All code changes are complete and verified. The system is ready for deployment once you:

1. Create Supabase account and project
2. Configure your GPU VM
3. Set up domain and DNS
4. Deploy to Vercel
5. Configure environment variables

**Everything else is automated!** 🎉
