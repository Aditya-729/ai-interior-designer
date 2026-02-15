# Deploying on GPU VM

## Prerequisites

- Ubuntu 22.04 LTS VM
- NVIDIA GPU with CUDA 11.8+
- Docker and Docker Compose
- NVIDIA Container Toolkit

## Step 1: Install NVIDIA Container Toolkit

```bash
# Add NVIDIA package repositories
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list

# Install
sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit
sudo systemctl restart docker
```

## Step 2: Verify GPU Access

```bash
# Test GPU in Docker
docker run --rm --gpus all nvidia/cuda:11.8.0-base-ubuntu22.04 nvidia-smi
```

## Step 3: Configure Environment

```bash
# Copy environment file
cp .env.example .env

# Edit with your values
nano .env
```

Required variables:
- All API keys
- Database credentials
- R2 credentials
- `ENVIRONMENT=production`
- `DEMO_MODE=false`

## Step 4: Deploy with Docker Compose

```bash
# Use GPU-enabled compose file
docker-compose -f docker-compose.gpu.yml up -d
```

## Step 5: Run Migrations

```bash
# Enter backend container
docker exec -it interior_designer_backend bash

# Run migrations
alembic upgrade head
```

## Step 6: Verify Services

```bash
# Check all services
docker-compose -f docker-compose.gpu.yml ps

# Check GPU usage
docker exec -it interior_designer_inference nvidia-smi

# Check logs
docker-compose -f docker-compose.gpu.yml logs -f
```

## Network Configuration

### Frontend → Backend

Frontend should connect to:
```
http://your-vm-ip:8000
```

Or use a reverse proxy (Nginx) for HTTPS.

### Backend → Inference

Backend connects to inference service:
```
http://inference:8001
```

(Internal Docker network)

## Reverse Proxy (Nginx)

Example configuration:

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
    }

    location /api {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /ws {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

## Monitoring

### GPU Usage

```bash
# Watch GPU usage
watch -n 1 nvidia-smi
```

### Service Health

```bash
# Backend health
curl http://localhost:8000/health

# Inference health
curl http://localhost:8001/health
```

## Troubleshooting

### GPU Not Detected

1. Check NVIDIA drivers: `nvidia-smi`
2. Verify Container Toolkit: `docker run --rm --gpus all nvidia/cuda:11.8.0-base-ubuntu22.04 nvidia-smi`
3. Check compose file GPU configuration

### Out of Memory

- Reduce `GPU_MAX_CONCURRENT` in config
- Use smaller models
- Enable model CPU offload

### Port Conflicts

- Change ports in `.env` or `docker-compose.gpu.yml`
- Update firewall rules

## Scaling

### Multiple GPUs

To use multiple GPUs, modify `docker-compose.gpu.yml`:

```yaml
deploy:
  resources:
    reservations:
      devices:
        - driver: nvidia
          device_ids: ['0', '1']  # Use GPU 0 and 1
          capabilities: [gpu]
```

### Horizontal Scaling

- Backend: Scale horizontally (stateless)
- Inference: One instance per GPU
- Database: Use connection pooling

## Backup

### Database

```bash
# Backup
docker exec interior_designer_postgres pg_dump -U postgres interior_designer > backup.sql

# Restore
docker exec -i interior_designer_postgres psql -U postgres interior_designer < backup.sql
```

### Storage

R2 backups are handled by Cloudflare (versioning enabled).

## Updates

```bash
# Pull latest code
git pull

# Rebuild and restart
docker-compose -f docker-compose.gpu.yml up -d --build

# Run migrations
docker exec interior_designer_backend alembic upgrade head
```
