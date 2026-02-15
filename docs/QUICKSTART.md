# Quick Start Guide

Get up and running in 5 minutes!

## Prerequisites Check

- ✅ Python 3.10+
- ✅ Node.js 18+
- ✅ Docker installed
- ✅ NVIDIA GPU (for inference)
- ✅ API keys (Mino AI, Perplexity)

## Step 1: Clone and Configure

```bash
# Clone repository
git clone <your-repo-url>
cd ai-interior-designer

# Copy environment file
cp .env.example .env

# Edit .env with your API keys
# Required: MINO_AI_API_KEY, PERPLEXITY_API_KEY
# Optional: R2 credentials, Supabase
```

## Step 2: Start Infrastructure

```bash
# Start PostgreSQL and Qdrant
docker-compose up -d postgres qdrant

# Wait 10 seconds for services to start
sleep 10
```

## Step 3: Setup Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Run migrations
alembic upgrade head

# Start backend (in separate terminal)
uvicorn main:app --reload
```

## Step 4: Setup Inference Service

```bash
cd inference_service
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Download models (first time only, takes 10-20 minutes)
# This downloads ~5GB of models
python -c "from huggingface_hub import snapshot_download; snapshot_download('runwayml/stable-diffusion-inpainting', local_dir='./models/sd-inpainting')"

# Start inference service (in separate terminal)
python server.py
```

## Step 5: Setup Frontend

```bash
cd frontend
npm install

# Create .env.local
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local

# Start frontend (in separate terminal)
npm run dev
```

## Step 6: Test It!

1. Open http://localhost:3000
2. Upload a room image
3. Type: "Make the wall warm beige"
4. Click "Apply Changes"
5. Wait for result!

## Troubleshooting

### Models not downloading?
- Check internet connection
- Ensure you have ~10GB free space
- Try manual download from HuggingFace

### GPU not detected?
- Check: `nvidia-smi`
- Verify CUDA installation
- Inference will fall back to CPU (slow)

### Port already in use?
- Change ports in `.env` or docker-compose.yml
- Kill existing processes

### Database connection error?
- Ensure PostgreSQL is running: `docker ps`
- Check credentials in `.env`

## Next Steps

- Read `docs/DEVELOPMENT.md` for detailed setup
- Check `docs/API.md` for API usage
- See `docs/EXAMPLES.md` for code examples

## Need Help?

- Check existing issues
- Read documentation in `docs/`
- Open a new issue
