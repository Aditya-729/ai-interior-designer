# Development Guide

## Local Development Setup

### Prerequisites

- Python 3.10+
- Node.js 18+
- Docker and Docker Compose
- NVIDIA GPU with CUDA (for inference service)
- CUDA 11.8+ and cuDNN

### Initial Setup

1. **Clone and configure:**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

2. **Start infrastructure:**
   ```bash
   docker-compose up -d postgres qdrant
   ```

3. **Download models:**
   ```bash
   ./scripts/download_models.sh
   ```

4. **Setup backend:**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   alembic upgrade head
   ```

5. **Setup inference service:**
   ```bash
   cd inference_service
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

6. **Setup frontend:**
   ```bash
   cd frontend
   npm install
   cp .env.local.example .env.local
   # Edit .env.local with API URL
   ```

### Running Services

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload
```

**Terminal 2 - Inference Service:**
```bash
cd inference_service
source venv/bin/activate
python server.py
```

**Terminal 3 - Frontend:**
```bash
cd frontend
npm run dev
```

### API Testing

- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Inference Service: http://localhost:8001
- Frontend: http://localhost:3000

## Architecture

### Backend (FastAPI)

- **Location:** `backend/`
- **Main entry:** `backend/main.py`
- **Routers:** `backend/app/routers/`
- **Services:** `backend/app/services/`
- **Models:** `backend/app/models.py`

### Inference Service

- **Location:** `inference_service/`
- **Main entry:** `inference_service/server.py`
- **Models:** Loaded on startup, stored in `models/` directory

### Frontend (Next.js)

- **Location:** `frontend/`
- **Pages:** `frontend/app/`
- **Components:** `frontend/components/`

## Database Migrations

```bash
cd backend
source venv/bin/activate

# Create migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

## Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

## Code Style

- **Python:** Follow PEP 8, use Black formatter
- **TypeScript:** Use ESLint, follow Next.js conventions
- **Commit messages:** Use conventional commits

## Debugging

### Backend
- Use FastAPI's automatic docs at `/docs`
- Enable debug logging in `.env`: `ENVIRONMENT=development`

### Inference Service
- Check GPU availability: `nvidia-smi`
- Monitor memory usage during inference
- Use smaller models for development

### Frontend
- Use React DevTools
- Check browser console for errors
- Use Next.js dev mode for hot reload
