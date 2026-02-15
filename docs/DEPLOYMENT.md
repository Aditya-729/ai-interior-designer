# Deployment Guide

## Production Deployment

### Prerequisites

- Server with NVIDIA GPU (for inference)
- Docker and Docker Compose installed
- Domain name (optional)
- SSL certificate (for HTTPS)

### Environment Setup

1. **Create production `.env` file:**
   ```bash
   cp .env.example .env
   # Fill in all production values
   ```

2. **Required environment variables:**
   - All API keys (Mino, Perplexity)
   - Database credentials
   - R2 storage credentials
   - JWT secret
   - Production URLs

### Docker Deployment

1. **Build and start all services:**
   ```bash
   docker-compose -f docker-compose.prod.yml up -d --build
   ```

2. **Check service status:**
   ```bash
   docker-compose -f docker-compose.prod.yml ps
   ```

3. **View logs:**
   ```bash
   docker-compose -f docker-compose.prod.yml logs -f
   ```

### Manual Deployment

#### Backend

1. **Setup:**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   alembic upgrade head
   ```

2. **Run with Gunicorn:**
   ```bash
   gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
   ```

#### Inference Service

1. **Setup:**
   ```bash
   cd inference_service
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Run:**
   ```bash
   python server.py
   ```

#### Frontend

1. **Build:**
   ```bash
   cd frontend
   npm install
   npm run build
   ```

2. **Run:**
   ```bash
   npm start
   ```

### Reverse Proxy (Nginx)

Example Nginx configuration:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    location /api {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Monitoring

- **Health checks:** `/health` endpoints on all services
- **Logs:** Use Docker logs or centralized logging (e.g., ELK stack)
- **Metrics:** Consider Prometheus + Grafana
- **GPU monitoring:** `nvidia-smi` or nvidia-ml-py

### Scaling

- **Backend:** Scale horizontally with load balancer
- **Inference:** One instance per GPU (or use GPU sharing)
- **Database:** Use connection pooling, consider read replicas
- **Storage:** R2 handles scaling automatically

### Security

- Use HTTPS (Let's Encrypt)
- Set strong JWT secret
- Restrict API access with rate limiting
- Use environment variables for secrets
- Enable CORS only for your domain
- Regular security updates

### Backup

- **Database:** Regular PostgreSQL backups
- **Vector DB:** Qdrant snapshots
- **Storage:** R2 versioning enabled
- **Code:** Git repository

### Updates

1. Pull latest code
2. Update dependencies
3. Run migrations: `alembic upgrade head`
4. Rebuild Docker images
5. Restart services
