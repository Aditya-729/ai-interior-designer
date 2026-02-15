# AI Interior Designer - Production System

A complete end-to-end web platform for interior designers that allows users to upload room photos and modify materials, colours, tiles, walls, ceilings, lighting, and furniture using voice commands or typed prompts.

## Architecture Overview

```
Frontend (Next.js)
    ↓
Backend API (FastAPI)
    ↓
Inference Service (GPU - Stable Diffusion)
    ↓
Storage (Cloudflare R2) + Database (PostgreSQL) + Vector DB (Qdrant)
```

## Features

- **Dual Input Modes**: Voice (Whisper) and text commands
- **Visual Understanding**: Mino AI API for scene segmentation
- **Design Intelligence**: Perplexity AI API for design recommendations
- **Realistic Editing**: Stable Diffusion Inpainting with ControlNet
- **Project Management**: Full history, versions, and style memory
- **Vector Memory**: Semantic search across past projects

## Quick Start

### Prerequisites

- NVIDIA GPU with CUDA support
- Docker and Docker Compose
- Python 3.10+
- Node.js 18+

### Setup

1. **Clone and configure environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and configuration
   ```

2. **Start infrastructure services:**
   ```bash
   docker-compose up -d postgres qdrant
   ```

3. **Download models:**
   ```bash
   ./scripts/download_models.sh
   ```

4. **Start backend:**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   uvicorn main:app --reload
   ```

5. **Start inference service:**
   ```bash
   cd inference_service
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   python server.py
   ```

6. **Start frontend:**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

7. **Access the application:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

## Project Structure

```
.
├── backend/              # FastAPI backend
├── frontend/             # Next.js frontend
├── inference_service/    # GPU inference service
├── shared/               # Shared types and utilities
├── docker-compose.yml    # Infrastructure services
├── scripts/              # Setup and utility scripts
└── docs/                 # Documentation
```

## Environment Variables

See `.env.example` for all required configuration.

## API Endpoints

- `POST /api/upload-image` - Upload room image
- `POST /api/upload-audio` - Upload audio for transcription
- `POST /api/transcribe` - Transcribe audio to text
- `POST /api/analyze-scene` - Analyze scene with Mino AI
- `POST /api/plan-edits` - Generate edit plan from user request
- `POST /api/fetch-design-knowledge` - Get design recommendations
- `POST /api/run-inpainting` - Execute image editing
- `POST /api/save-version` - Save edited version
- `GET /api/projects` - List user projects
- `GET /api/projects/{id}` - Get project details
- `GET /api/history` - Get edit history

## Development

See `docs/DEVELOPMENT.md` for detailed development guidelines.

## Deployment

See `docs/DEPLOYMENT.md` for production deployment instructions.
