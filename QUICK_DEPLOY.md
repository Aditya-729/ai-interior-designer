# 🚀 Quick Deploy Guide

## Prerequisites
- Supabase account (free tier)
- Vercel account (free tier)
- GPU VM with public IP
- Domain name (optional but recommended)

## Step 1: Supabase (5 min)

1. Go to [supabase.com](https://supabase.com) → New Project
2. Save database password
3. Get connection details from Settings → Database
4. Add to `.env`:
```bash
SUPABASE_DB_HOST=db.xxxxx.supabase.co
SUPABASE_DB_PORT=5432
SUPABASE_DB_NAME=postgres
SUPABASE_DB_USER=postgres
SUPABASE_DB_PASSWORD=your-password
```
5. Run: `./scripts/supabase-init.sh`

## Step 2: GPU VM (10 min)

```bash
# On your GPU VM
git clone <your-repo>
cd ai-interior-designer

# Install Docker + NVIDIA runtime (if not already)
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Configure .env with all variables
nano .env

# Initialize database
./scripts/supabase-init.sh

# Start services
docker-compose -f docker-compose.gpu.yml up -d
```

## Step 3: Domain (15 min)

```bash
# Point DNS: api.yourdomain.com → VM IP

# Install Caddy (easiest)
sudo apt install -y debian-keyring debian-archive-keyring apt-transport-https
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' | sudo gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' | sudo tee /etc/apt/sources.list.d/caddy-stable.list
sudo apt update
sudo apt install caddy

# Create Caddyfile
sudo nano /etc/caddy/Caddyfile
```

Caddyfile:
```
api.yourdomain.com {
    reverse_proxy localhost:8000
}
```

```bash
sudo systemctl enable caddy
sudo systemctl start caddy
```

## Step 4: Vercel (5 min)

1. Go to [vercel.com](https://vercel.com)
2. Import repository
3. Root Directory: `frontend`
4. Environment Variables:
   - `NEXT_PUBLIC_API_BASE=https://api.yourdomain.com`
   - `NEXT_PUBLIC_WS_URL=wss://api.yourdomain.com`
   - `NEXT_PUBLIC_DEMO_MODE=false`
5. Deploy

## Step 5: Update Backend

```bash
# On GPU VM, update .env
FRONTEND_PUBLIC_URL=https://your-app.vercel.app
PUBLIC_BACKEND_URL=https://api.yourdomain.com

# Restart
docker-compose -f docker-compose.gpu.yml restart backend
```

## Step 6: Verify

```bash
# Test health
curl https://api.yourdomain.com/api/v1/system/health

# Test frontend
open https://your-app.vercel.app
```

## ✅ Done!

Your app is now live! 🎉
