# 🚀 START HERE - Quick Setup Guide

## Prerequisites

- Python 3.10+
- Node.js 18+
- Docker and Docker Compose
- NVIDIA GPU with CUDA (for inference)
- API keys: Mino AI, Perplexity AI, Cloudflare R2

## Quick Start (5 Steps)

### 1. Configure Environment

```bash
cp .env.example .env
# Edit .env with your API keys
```

Required variables:
- `MINO_AI_API_KEY`
- `PERPLEXITY_API_KEY`
- `R2_ACCOUNT_ID`, `R2_ACCESS_KEY_ID`, `R2_SECRET_ACCESS_KEY`, `R2_ENDPOINT`

### 2. Start Infrastructure

```bash
docker-compose up -d postgres qdrant
```

### 3. Setup Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
alembic upgrade head
```

### 4. Setup Inference Service

```bash
cd inference_service
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
# Models will download automatically on first run
```

### 5. Setup Frontend

```bash
cd frontend
npm install
cp .env.local.example .env.local
# Edit .env.local: NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Running the Services

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate
python run.py
```

**Terminal 2 - Inference Service:**
```bash
cd inference_service
source venv/bin/activate
python run.py
```

**Terminal 3 - Frontend:**
```bash
cd frontend
npm run dev
```

## Verify Setup

1. Check environment: `./scripts/check_environment.sh` (or `.ps1` on Windows)
2. Check GPU: `./scripts/check_gpu.sh` (or `.ps1` on Windows)
3. Backend health: http://localhost:8000/health
4. Inference health: http://localhost:8001/health
5. Frontend: http://localhost:3000

## Test the Flow

1. Open http://localhost:3000
2. Upload a room image
3. Type: "Make the wall warm beige"
4. Click "Apply Changes"
5. Wait for result!

## Troubleshooting

- **Models not downloading?** Check internet, ensure ~10GB free space
- **GPU not detected?** Run `nvidia-smi`, check CUDA installation
- **Database errors?** Ensure PostgreSQL container is running
- **Port conflicts?** Change ports in `.env` or docker-compose.yml

## Next Steps

- Read `docs/DEVELOPMENT.md` for detailed setup
- Check `docs/API.md` for API usage
- See `docs/EXAMPLES.md` for code examples

## Architecture

```
Frontend (Next.js :3000)
    ↓
Backend API (FastAPI :8000)
    ↓
Inference Service (GPU :8001)
    ↓
PostgreSQL + Qdrant + R2 Storage
```

## Support

- Check `IMPLEMENTATION_STATUS.md` for implementation details
- Review `docs/` for comprehensive documentation
- Check logs in each service for errors
