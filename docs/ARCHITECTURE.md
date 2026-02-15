# System Architecture

## Overview

The AI Interior Designer system is a modular, production-ready platform for AI-powered room design modifications.

## Architecture Diagram

```
┌─────────────┐
│   Frontend  │ (Next.js)
│  (Port 3000)│
└──────┬──────┘
       │ HTTP/WebSocket
       │
┌──────▼──────┐
│   Backend   │ (FastAPI)
│  (Port 8000)│
└──────┬──────┘
       │
       ├─────────┬──────────┬──────────┐
       │         │          │          │
┌──────▼──┐ ┌───▼───┐ ┌────▼────┐ ┌───▼────┐
│Inference│ │Postgres│ │ Qdrant  │ │   R2   │
│Service  │ │        │ │(Vector) │ │Storage │
│(Port    │ │        │ │         │ │        │
│ 8001)   │ │        │ │         │ │        │
└─────────┘ └────────┘ └─────────┘ └────────┘
```

## Components

### 1. Frontend (Next.js)

**Purpose:** User interface for uploading images, providing voice/text input, and viewing results.

**Key Features:**
- Image upload with drag-and-drop
- Voice recording and transcription
- Text input for design requests
- Before/after preview slider
- Project management dashboard
- Version history timeline
- Design suggestions panel

**Technology:**
- Next.js 14 (App Router)
- React 18
- TypeScript
- Tailwind CSS
- Axios for API calls

### 2. Backend API (FastAPI)

**Purpose:** Main API server handling all business logic and orchestration.

**Key Responsibilities:**
- File uploads (images, audio)
- Audio transcription (Whisper)
- Scene analysis coordination (Mino AI)
- Edit planning
- Design knowledge retrieval (Perplexity)
- Inference coordination
- Project and version management
- User preferences
- WebSocket for real-time updates

**Technology:**
- FastAPI
- SQLAlchemy (ORM)
- Alembic (migrations)
- WebSocket support

### 3. Inference Service (GPU)

**Purpose:** GPU-based image editing using Stable Diffusion.

**Key Responsibilities:**
- Stable Diffusion Inpainting
- ControlNet for geometry preservation
- Multi-edit processing
- Mask-based editing

**Technology:**
- PyTorch
- Diffusers library
- ControlNet
- CUDA for GPU acceleration

### 4. Database (PostgreSQL)

**Purpose:** Structured data storage.

**Tables:**
- `users`: User accounts
- `projects`: Design projects
- `images`: Uploaded images
- `versions`: Edited image versions
- `edit_history`: Edit operation history
- `user_preferences`: User style preferences

### 5. Vector Database (Qdrant)

**Purpose:** Semantic search for design references and style memory.

**Use Cases:**
- Similar design search
- Style profile extraction
- Design recommendation based on history

**Technology:**
- Qdrant
- Sentence Transformers for embeddings

### 6. Object Storage (Cloudflare R2)

**Purpose:** File storage for images, audio, and generated outputs.

**Stored Files:**
- Original room images
- Audio recordings
- Generated edited images
- Segmentation masks

## Data Flow

### Edit Request Flow

1. **User Input:**
   - User uploads room image
   - User provides voice or text command

2. **Transcription (if voice):**
   - Audio → Whisper → Text

3. **Scene Analysis:**
   - Image → Mino AI → Object detection + masks

4. **Edit Planning:**
   - Text + Detected objects → Planner → Structured edit plan

5. **Design Knowledge (optional):**
   - Request → Perplexity AI → Design recommendations

6. **Inference:**
   - Image + Masks + Edit plan → Inference Service → Edited image

7. **Storage:**
   - Edited image → R2 → Database record

8. **Response:**
   - WebSocket updates → Frontend display

## Integration Points

### Mino AI API

**Purpose:** Visual understanding and object detection.

**Input:** Room image
**Output:** 
- Room type
- Detected objects with labels
- Bounding boxes
- Segmentation masks

**Usage:** Scene analysis endpoint

### Perplexity AI API

**Purpose:** Design knowledge and recommendations.

**Input:** User request + room context
**Output:**
- Color harmony suggestions
- Material compatibility
- Lighting recommendations
- Design trends
- Safety considerations

**Usage:** Design knowledge endpoint

## Scalability Considerations

### Horizontal Scaling

- **Backend:** Stateless, can scale horizontally
- **Inference:** One instance per GPU (or GPU sharing)
- **Database:** Read replicas for queries
- **Storage:** R2 handles scaling automatically

### Caching

- Cache Mino analysis results
- Cache Perplexity responses
- Cache frequently accessed images

### Queue System (Future)

For production at scale, consider:
- Redis for job queues
- Celery for async processing
- Background workers for inference

## Security

- JWT authentication (to be implemented)
- API rate limiting
- CORS configuration
- Input validation
- Secure file uploads
- Environment variable secrets

## Monitoring

- Health check endpoints
- Logging (structured logs)
- Error tracking
- Performance metrics
- GPU utilization monitoring

## Future Enhancements

- User authentication and authorization
- Team collaboration features
- Export functionality (PDF, 3D)
- Mobile app
- Real-time collaboration
- Advanced editing features
- Style transfer
- 3D room visualization
