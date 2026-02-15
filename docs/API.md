# API Documentation

## Base URL

- Development: `http://localhost:8000`
- Production: `https://api.yourdomain.com`

## Authentication

Currently, the API uses simple user IDs. In production, implement JWT authentication.

## Endpoints

### Upload

#### Upload Image
```
POST /api/upload-image
Content-Type: multipart/form-data

Body:
- file: Image file
- project_id: Optional project ID

Response:
{
  "image_id": "uuid",
  "url": "https://...",
  "width": 1920,
  "height": 1080
}
```

#### Upload Audio
```
POST /api/upload-audio
Content-Type: multipart/form-data

Body:
- file: Audio file

Response:
{
  "audio_id": "uuid",
  "url": "https://..."
}
```

### Transcription

#### Transcribe Audio
```
POST /api/transcribe
Content-Type: multipart/form-data

Body:
- file: Audio file
- language: Optional language code

Response:
{
  "text": "transcribed text",
  "language": "en"
}
```

### Scene Analysis

#### Analyze Scene
```
POST /api/analyze-scene

Body:
{
  "image_id": "uuid",
  "image_url": "https://..." // Optional
}

Response:
{
  "room_type": "living_room",
  "objects": [...],
  "layout": {...}
}
```

#### Get Segmentation Masks
```
POST /api/get-segmentation-masks

Body:
{
  "image_id": "uuid",
  "objects": ["wall", "floor"] // Optional
}

Response:
{
  "wall": {
    "mask": "base64...",
    "bbox": [x1, y1, x2, y2]
  },
  ...
}
```

### Planning

#### Plan Edits
```
POST /api/plan-edits

Body:
{
  "user_prompt": "Make the wall warm beige",
  "image_id": "uuid",
  "project_id": "uuid" // Optional
}

Response:
{
  "edits": [
    {
      "target_object": "wall",
      "operation": "recolor",
      "parameters": {
        "color": "warm beige",
        "strength": 0.8
      },
      "mask_id": "uuid"
    }
  ],
  "validation": {
    "valid": true,
    "warnings": []
  }
}
```

### Design Knowledge

#### Fetch Design Knowledge
```
POST /api/fetch-design-knowledge

Body:
{
  "user_request": "warm beige wall color",
  "image_id": "uuid",
  "project_id": "uuid" // Optional
}

Response:
{
  "recommendations": "...",
  "color_harmony": {...},
  "material_compatibility": {...}
}
```

### Inference

#### Run Inpainting
```
POST /api/run-inpainting

Body:
{
  "image_id": "uuid",
  "edit_plan": {...},
  "project_id": "uuid", // Optional
  "client_id": "uuid" // Optional, for WebSocket updates
}

Response:
{
  "version_id": "uuid",
  "image_url": "https://...",
  "processing_time": 45.2
}
```

### Projects

#### Create Project
```
POST /api/projects

Body:
{
  "name": "Living Room Design",
  "description": "...",
  "user_id": "uuid"
}

Response:
{
  "id": "uuid",
  "name": "...",
  ...
}
```

#### List Projects
```
GET /api/projects?user_id=uuid

Response:
[
  {
    "id": "uuid",
    "name": "...",
    ...
  }
]
```

#### Get Project
```
GET /api/projects/{project_id}

Response:
{
  "id": "uuid",
  "name": "...",
  "images": [...],
  "versions": [...]
}
```

### History

#### Get History
```
GET /api/history?project_id=uuid&limit=50&offset=0

Response:
[
  {
    "id": "uuid",
    "user_prompt": "...",
    "edit_plan": {...},
    ...
  }
]
```

### Preferences

#### Get Preferences
```
GET /api/preferences/{user_id}

Response:
{
  "preferred_colors": [...],
  "preferred_materials": [...],
  ...
}
```

#### Update Preferences
```
PUT /api/preferences/{user_id}

Body:
{
  "preferred_colors": ["warm beige", "navy blue"],
  "preferred_materials": ["marble", "wood"]
}

Response:
{
  "preferred_colors": [...],
  ...
}
```

## WebSocket

### Connection
```
WS /ws/{client_id}
```

### Messages

**From Server:**
```json
{
  "status": "processing",
  "progress": 50,
  "message": "Running AI model..."
}
```

**Status values:**
- `processing`: Edit in progress
- `completed`: Edit finished
- `error`: Error occurred

## Error Responses

```json
{
  "detail": "Error message"
}
```

**Status codes:**
- `400`: Bad Request
- `404`: Not Found
- `500`: Internal Server Error
- `503`: Service Unavailable
