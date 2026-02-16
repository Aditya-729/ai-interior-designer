# 🔗 How to Get Your Backend API URLs

You need two URLs for your Vercel frontend:
1. **NEXT_PUBLIC_API_BASE** - Your backend API URL
2. **NEXT_PUBLIC_WS_URL** - Your WebSocket URL

Here are **3 options** depending on your situation:

---

## Option 1: Quick Testing with ngrok (Easiest - 5 minutes)

If your backend is running **locally** on your computer, use ngrok to create a public tunnel.

### Step 1: Install ngrok
1. Go to: https://ngrok.com/download
2. Download and install ngrok
3. Sign up for a free account (required for custom domains)

### Step 2: Start Your Backend
```powershell
# In your project directory
cd backend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
python main.py
# Backend should be running on http://localhost:8000
```

### Step 3: Create ngrok Tunnel
```powershell
# In a new terminal
ngrok http 8000
```

You'll see output like:
```
Forwarding  https://abc123.ngrok-free.app -> http://localhost:8000
```

### Step 4: Use These URLs in Vercel
- **NEXT_PUBLIC_API_BASE**: `https://abc123.ngrok-free.app`
- **NEXT_PUBLIC_WS_URL**: `wss://abc123.ngrok-free.app`

**Note:** Free ngrok URLs change each time you restart. For production, use Option 2 or 3.

---

## Option 2: Deploy to Cloud Platform (Recommended for Production)

Deploy your backend to a cloud platform. Here are popular options:

### A. Railway (Easiest - Free tier available)

1. **Sign up**: https://railway.app
2. **Create new project** → "Deploy from GitHub repo"
3. **Select your repository**
4. **Configure**:
   - Root Directory: `backend`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. **Add environment variables** (from your `.env` file)
6. **Deploy** - Railway gives you a URL like: `https://your-app.railway.app`

**Use these URLs:**
- **NEXT_PUBLIC_API_BASE**: `https://your-app.railway.app`
- **NEXT_PUBLIC_WS_URL**: `wss://your-app.railway.app`

### B. Render (Free tier available)

1. **Sign up**: https://render.com
2. **New** → "Web Service"
3. **Connect GitHub** → Select your repo
4. **Configure**:
   - Name: `ai-interior-designer-backend`
   - Root Directory: `backend`
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. **Add environment variables**
6. **Deploy** - Render gives you: `https://your-app.onrender.com`

**Use these URLs:**
- **NEXT_PUBLIC_API_BASE**: `https://your-app.onrender.com`
- **NEXT_PUBLIC_WS_URL**: `wss://your-app.onrender.com`

### C. Fly.io (Good for WebSockets)

1. **Install Fly CLI**: https://fly.io/docs/getting-started/installing-flyctl/
2. **Sign up**: `fly auth signup`
3. **In your backend directory**:
   ```powershell
   cd backend
   fly launch
   ```
4. **Follow prompts** - Fly.io will create a `fly.toml` file
5. **Deploy**: `fly deploy`
6. **Get URL**: `fly info` - shows your app URL

**Use these URLs:**
- **NEXT_PUBLIC_API_BASE**: `https://your-app.fly.dev`
- **NEXT_PUBLIC_WS_URL**: `wss://your-app.fly.dev`

### D. DigitalOcean App Platform

1. **Sign up**: https://www.digitalocean.com
2. **Create App** → "GitHub" → Select repo
3. **Configure**:
   - Component Type: "Web Service"
   - Source Directory: `backend`
   - Build Command: `pip install -r requirements.txt`
   - Run Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. **Add environment variables**
5. **Deploy**

**Use these URLs:**
- **NEXT_PUBLIC_API_BASE**: `https://your-app.ondigitalocean.app`
- **NEXT_PUBLIC_WS_URL**: `wss://your-app.ondigitalocean.app`

---

## Option 3: Deploy to Your Own Server/VM (Most Control)

If you have a server or VM (like AWS EC2, Google Cloud, Azure, etc.):

### Step 1: Set Up Your Server
1. **SSH into your server**
2. **Install dependencies**:
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip docker docker-compose nginx
   ```

### Step 2: Deploy Backend
```bash
# Clone your repo
git clone https://github.com/Aditya-729/ai-interior-designer.git
cd ai-interior-designer

# Configure .env file
nano .env  # Add all your environment variables

# Start with Docker
docker-compose -f docker-compose.prod.yml up -d
```

### Step 3: Set Up Domain (Optional but Recommended)

1. **Point DNS** to your server IP:
   - Create A record: `api.yourdomain.com` → Your server IP

2. **Install Caddy** (auto HTTPS):
   ```bash
   sudo apt install -y debian-keyring debian-archive-keyring apt-transport-https
   curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' | sudo gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg
   curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' | sudo tee /etc/apt/sources.list.d/caddy-stable.list
   sudo apt update
   sudo apt install caddy
   ```

3. **Create Caddyfile** (`/etc/caddy/Caddyfile`):
   ```
   api.yourdomain.com {
       reverse_proxy localhost:8000
   }
   ```

4. **Start Caddy**:
   ```bash
   sudo systemctl enable caddy
   sudo systemctl start caddy
   ```

**Use these URLs:**
- **NEXT_PUBLIC_API_BASE**: `https://api.yourdomain.com`
- **NEXT_PUBLIC_WS_URL**: `wss://api.yourdomain.com`

---

## Quick Reference: URL Patterns

| Platform | API URL Pattern | WebSocket URL Pattern |
|----------|----------------|----------------------|
| **ngrok** | `https://abc123.ngrok-free.app` | `wss://abc123.ngrok-free.app` |
| **Railway** | `https://your-app.railway.app` | `wss://your-app.railway.app` |
| **Render** | `https://your-app.onrender.com` | `wss://your-app.onrender.com` |
| **Fly.io** | `https://your-app.fly.dev` | `wss://your-app.fly.dev` |
| **Custom Domain** | `https://api.yourdomain.com` | `wss://api.yourdomain.com` |

**Rule:** 
- If API URL starts with `https://`, WebSocket URL is `wss://` (same domain)
- If API URL starts with `http://`, WebSocket URL is `ws://` (same domain)

---

## Testing Your Backend URL

Before setting it in Vercel, test that your backend is accessible:

```powershell
# Test health endpoint
curl https://your-backend-url.com/api/v1/system/health

# Should return: {"status": "healthy", ...}
```

Or open in browser:
```
https://your-backend-url.com/api/v1/system/health
```

---

## Setting in Vercel

Once you have your URLs:

1. Go to: https://vercel.com/dashboard
2. Click your project: `adityas-projects-e275b3df/frontend`
3. **Settings** → **Environment Variables**
4. Add:
   - **NEXT_PUBLIC_API_BASE** = `https://your-backend-url.com`
   - **NEXT_PUBLIC_WS_URL** = `wss://your-backend-url.com`
5. **Save**
6. **Deployments** → Click **⋯** on latest → **Redeploy**

---

## Recommendation

- **For Quick Testing**: Use **ngrok** (Option 1)
- **For Production**: Use **Railway** or **Render** (Option 2) - easiest setup
- **For Full Control**: Use your own server (Option 3)

---

## Need Help?

If you're stuck, check:
- Backend logs: `docker-compose logs backend` or check platform logs
- Health endpoint: `https://your-url/api/v1/system/health`
- Browser console (F12) for CORS errors
