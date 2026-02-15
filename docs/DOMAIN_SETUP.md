# Domain & HTTPS Setup for GPU VM

## Overview

Your backend and inference service run on your GPU VM. To make them publicly accessible with HTTPS, you need:

1. A domain name
2. DNS configuration
3. Reverse proxy (Nginx or Caddy)
4. SSL certificate (Let's Encrypt)

## Step 1: Get a Domain

- Purchase from: Namecheap, Google Domains, Cloudflare, etc.
- Example: `yourdomain.com`

## Step 2: Point DNS to Your VM

### Option A: A Record (Direct IP)

1. Get your VM's public IP address
2. In your DNS provider:
   - Type: `A`
   - Name: `api` (or `@` for root)
   - Value: `your-vm-ip`
   - TTL: `3600`

This creates: `api.yourdomain.com` → your VM IP

### Option B: CNAME (If Using Load Balancer)

If using a cloud provider's load balancer:
- Type: `CNAME`
- Name: `api`
- Value: `your-load-balancer-url`

## Step 3: Install Reverse Proxy

### Option A: Caddy (Easiest - Auto HTTPS)

```bash
# Install Caddy
sudo apt install -y debian-keyring debian-archive-keyring apt-transport-https
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' | sudo gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' | sudo tee /etc/apt/sources.list.d/caddy-stable.list
sudo apt update
sudo apt install caddy

# Create Caddyfile
sudo nano /etc/caddy/Caddyfile
```

Caddyfile content:
```
api.yourdomain.com {
    reverse_proxy localhost:8000 {
        # WebSocket support
        header_up Connection {>Connection}
        header_up Upgrade {>Upgrade}
    }
}

inference.yourdomain.com {
    reverse_proxy localhost:8001
}
```

Start Caddy:
```bash
sudo systemctl enable caddy
sudo systemctl start caddy
```

Caddy automatically:
- Gets SSL certificate from Let's Encrypt
- Renews certificates automatically
- Handles HTTPS redirect

### Option B: Nginx + Certbot

```bash
# Install Nginx
sudo apt update
sudo apt install nginx

# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Create Nginx config
sudo nano /etc/nginx/sites-available/api
```

Nginx config:
```nginx
server {
    listen 80;
    server_name api.yourdomain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable and get SSL:
```bash
sudo ln -s /etc/nginx/sites-available/api /etc/nginx/sites-enabled/
sudo nginx -t
sudo certbot --nginx -d api.yourdomain.com
```

## Step 4: Configure Backend

Update `.env` on your GPU VM:

```bash
PUBLIC_BACKEND_URL=https://api.yourdomain.com
FRONTEND_PUBLIC_URL=https://your-app.vercel.app
PRODUCTION=true
DEMO_MODE=false
```

## Step 5: Configure Firewall

```bash
# Allow HTTP/HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Allow backend ports (internal only)
sudo ufw allow from 127.0.0.1 to any port 8000
sudo ufw allow from 127.0.0.1 to any port 8001
```

## Step 6: WebSocket Configuration

### Caddy (Automatic)

Caddy handles WebSocket upgrades automatically with the config above.

### Nginx

Ensure your Nginx config includes:
```nginx
proxy_set_header Upgrade $http_upgrade;
proxy_set_header Connection "upgrade";
```

## Step 7: Test

1. **Test HTTPS:**
   ```bash
   curl https://api.yourdomain.com/health
   ```

2. **Test WebSocket:**
   - Open browser console
   - Connect to `wss://api.yourdomain.com/ws/test`

3. **Test API:**
   ```bash
   curl https://api.yourdomain.com/api/v1/system/health
   ```

## Port Configuration

### Required Ports

- **80 (HTTP)**: For Let's Encrypt verification
- **443 (HTTPS)**: For API access
- **8000 (Backend)**: Internal only (behind proxy)
- **8001 (Inference)**: Internal only (behind proxy)

### Optional: Expose Inference Directly

If you want separate domain for inference:
- Create `inference.yourdomain.com`
- Point to same VM
- Proxy to `localhost:8001`

## Troubleshooting

### SSL Certificate Issues

- Ensure DNS is propagated (check with `dig api.yourdomain.com`)
- Ensure port 80 is open for Let's Encrypt verification
- Check Caddy/Nginx logs: `sudo journalctl -u caddy` or `sudo tail -f /var/log/nginx/error.log`

### WebSocket Not Working

- Verify proxy headers are set correctly
- Check browser console for connection errors
- Test with `wscat`: `wscat -c wss://api.yourdomain.com/ws/test`

### Connection Refused

- Check firewall: `sudo ufw status`
- Verify services are running: `docker ps`
- Check service logs: `docker logs interior_designer_backend`

## Security Recommendations

1. **Rate Limiting**: Add rate limiting in Nginx/Caddy
2. **DDoS Protection**: Use Cloudflare in front of your domain
3. **IP Whitelisting**: Optional - restrict inference endpoint to known IPs
4. **Regular Updates**: Keep Caddy/Nginx updated

## Example Complete Setup

```bash
# 1. Domain: api.yourdomain.com → VM IP
# 2. Caddyfile:
api.yourdomain.com {
    reverse_proxy localhost:8000
}

# 3. Backend .env:
PUBLIC_BACKEND_URL=https://api.yourdomain.com
PRODUCTION=true

# 4. Frontend .env (Vercel):
NEXT_PUBLIC_API_BASE=https://api.yourdomain.com
NEXT_PUBLIC_WS_URL=wss://api.yourdomain.com
```

## Next Steps

After domain is configured:

1. Update Vercel environment variables
2. Update backend `.env` with public URLs
3. Test health endpoint
4. Test share links
5. Deploy!
