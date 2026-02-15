# Public Deployment Guide

Complete step-by-step guide to deploy AI Interior Designer publicly.

## Prerequisites

- Domain name
- GPU VM with public IP
- Supabase account (free tier)
- Vercel account (free tier)
- Docker installed on VM
- NVIDIA GPU with CUDA

## Step 1: Create Supabase Project

1. Go to [supabase.com](https://supabase.com)
2. Create new project
3. Save database password
4. Get connection details (see `scripts/create-supabase-env.md`)

## Step 2: Setup GPU VM

### 2.1 Install Docker & NVIDIA Runtime

```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install NVIDIA Container Toolkit
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list
sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit
sudo systemctl restart docker
```

### 2.2 Clone Repository

```bash
git clone <your-repo-url>
cd ai-interior-designer
```

### 2.3 Configure Environment

```bash
cp .env.example .env
nano .env
```

Required variables:
```bash
# Supabase
SUPABASE_DB_HOST=db.xxxxx.supabase.co
SUPABASE_DB_PORT=5432
SUPABASE_DB_NAME=postgres
SUPABASE_DB_USER=postgres
SUPABASE_DB_PASSWORD=your-password

# API Keys
MINO_AI_API_KEY=your-key
PERPLEXITY_API_KEY=your-key

# R2 Storage
R2_ACCOUNT_ID=your-id
R2_ACCESS_KEY_ID=your-key
R2_SECRET_ACCESS_KEY=your-secret
R2_ENDPOINT=https://xxxxx.r2.cloudflarestorage.com

# Public URLs (update after domain setup)
PUBLIC_BACKEND_URL=https://api.yourdomain.com
FRONTEND_PUBLIC_URL=https://your-app.vercel.app

# Production
PRODUCTION=true
DEMO_MODE=false
ENVIRONMENT=production
```

### 2.4 Initialize Database

```bash
./scripts/supabase-init.sh
```

### 2.5 Start Services

```bash
docker-compose -f docker-compose.gpu.yml up -d
```

## Step 3: Setup Domain & HTTPS

See `docs/DOMAIN_SETUP.md` for detailed instructions.

Quick summary:
1. Point DNS: `api.yourdomain.com` → VM IP
2. Install Caddy or Nginx
3. Configure reverse proxy
4. SSL certificate (automatic with Caddy)

## Step 4: Deploy Frontend to Vercel

### 4.1 Prepare Frontend

```bash
cd frontend
npm install
npm run build  # Verify build works
```

### 4.2 Deploy to Vercel

1. Go to [vercel.com](https://vercel.com)
2. Import your repository
3. Configure:
   - **Framework Preset**: Next.js
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `.next`

### 4.3 Set Environment Variables

In Vercel project settings → Environment Variables:

```
NEXT_PUBLIC_API_BASE=https://api.yourdomain.com
NEXT_PUBLIC_WS_URL=wss://api.yourdomain.com
NEXT_PUBLIC_DEMO_MODE=false
NEXT_PUBLIC_FRONTEND_URL=https://your-app.vercel.app
```

### 4.4 Deploy

Click "Deploy" and wait for build to complete.

## Step 5: Verify Deployment

### 5.1 Test Health Endpoint

```bash
curl https://api.yourdomain.com/api/v1/system/health
```

Should return:
```json
{
  "status": "healthy",
  "database": "connected",
  "qdrant": "connected",
  "inference_service": "connected",
  "gpu_queue": {...}
}
```

### 5.2 Test Frontend

1. Open `https://your-app.vercel.app`
2. Should load without errors
3. Check browser console for API calls

### 5.3 Test Share Page

1. Create a test project
2. Generate a version
3. Create share link
4. Open share link in incognito
5. Verify before/after slider works

## Step 6: Final Configuration

### 6.1 Update Backend URLs

After Vercel deployment, update backend `.env`:

```bash
FRONTEND_PUBLIC_URL=https://your-app.vercel.app
```

Restart backend:
```bash
docker-compose -f docker-compose.gpu.yml restart backend
```

### 6.2 Test Complete Flow

1. **Sign up**: Request magic link
2. **Upload image**: Should work
3. **Voice/text input**: Should transcribe/process
4. **Edit generation**: Should queue and process
5. **Share link**: Should be accessible publicly
6. **Export**: Should download with watermark

## Step 7: Monitoring

### 7.1 Check Logs

```bash
# Backend logs
docker logs -f interior_designer_backend

# Inference logs
docker logs -f interior_designer_inference

# All services
docker-compose -f docker-compose.gpu.yml logs -f
```

### 7.2 Monitor GPU

```bash
watch -n 1 nvidia-smi
```

### 7.3 Check Database

In Supabase dashboard:
- Monitor connection pool
- Check table sizes
- Review query performance

## Troubleshooting

### Frontend Can't Connect to Backend

- Check CORS settings in backend
- Verify `NEXT_PUBLIC_API_BASE` is correct
- Check browser console for errors
- Verify backend is accessible: `curl https://api.yourdomain.com/health`

### WebSocket Not Working

- Verify `NEXT_PUBLIC_WS_URL` uses `wss://`
- Check reverse proxy WebSocket configuration
- Test WebSocket: `wscat -c wss://api.yourdomain.com/ws/test`

### Database Connection Issues

- Verify Supabase credentials
- Check firewall allows outbound connections
- Test connection: `./scripts/supabase-init.sh`

### SSL Certificate Issues

- Ensure DNS is propagated
- Check port 80 is open for Let's Encrypt
- Review Caddy/Nginx logs

## Production Checklist

- [ ] Supabase database configured
- [ ] Domain DNS configured
- [ ] HTTPS working (SSL certificate)
- [ ] Backend accessible at public URL
- [ ] Frontend deployed to Vercel
- [ ] Environment variables set
- [ ] Health endpoint returns "healthy"
- [ ] Share links work publicly
- [ ] Export functionality works
- [ ] WebSocket connections work
- [ ] GPU queue functioning
- [ ] Usage limits enforced
- [ ] Authentication working
- [ ] CORS configured correctly

## Security Checklist

- [ ] `PRODUCTION=true` set
- [ ] `DEMO_MODE=false` set
- [ ] Strong database password
- [ ] API keys secured
- [ ] HTTPS enforced
- [ ] HttpOnly cookies enabled
- [ ] CORS restricted to frontend domain
- [ ] Rate limiting enabled (optional)

## Next Steps

After deployment:

1. Monitor usage and performance
2. Collect user feedback
3. Iterate on features
4. Scale as needed (more GPUs, load balancing)

## Support

For issues:
- Check logs: `docker logs <service>`
- Test endpoints: `curl https://api.yourdomain.com/health`
- Review documentation in `docs/`
