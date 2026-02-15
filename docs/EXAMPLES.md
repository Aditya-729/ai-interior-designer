# Usage Examples

## Example API Calls

### Complete Edit Workflow

#### 1. Upload Image
```bash
curl -X POST http://localhost:8000/api/upload-image \
  -F "file=@living_room.jpg" \
  -F "project_id=project-123"
```

Response:
```json
{
  "image_id": "img-456",
  "url": "https://r2.../images/img-456.jpg",
  "width": 1920,
  "height": 1080
}
```

#### 2. Analyze Scene
```bash
curl -X POST http://localhost:8000/api/analyze-scene \
  -H "Content-Type: application/json" \
  -d '{
    "image_id": "img-456"
  }'
```

Response:
```json
{
  "room_type": "living_room",
  "objects": [
    {
      "label": "wall",
      "confidence": 0.95,
      "bbox": [0, 0, 1920, 800],
      "mask": "base64...",
      "category": "structural"
    },
    {
      "label": "sofa",
      "confidence": 0.92,
      "bbox": [400, 600, 1200, 1000],
      "mask": "base64...",
      "category": "furniture"
    }
  ]
}
```

#### 3. Plan Edits
```bash
curl -X POST http://localhost:8000/api/plan-edits \
  -H "Content-Type: application/json" \
  -d '{
    "user_prompt": "Make the wall warm beige and change the sofa to dark blue",
    "image_id": "img-456",
    "project_id": "project-123"
  }'
```

Response:
```json
{
  "edits": [
    {
      "target_object": "wall",
      "operation": "recolor",
      "parameters": {
        "color": "warm beige",
        "strength": 0.8
      },
      "mask_id": "wall_mask_123",
      "confidence": 0.95
    },
    {
      "target_object": "sofa",
      "operation": "recolor",
      "parameters": {
        "color": "dark blue",
        "strength": 0.8
      },
      "mask_id": "sofa_mask_456",
      "confidence": 0.92
    }
  ],
  "validation": {
    "valid": true,
    "warnings": []
  },
  "room_type": "living_room"
}
```

#### 4. Get Design Knowledge (Optional)
```bash
curl -X POST http://localhost:8000/api/fetch-design-knowledge \
  -H "Content-Type: application/json" \
  -d '{
    "user_request": "warm beige wall with dark blue sofa",
    "image_id": "img-456",
    "project_id": "project-123"
  }'
```

#### 5. Run Inference
```bash
curl -X POST http://localhost:8000/api/run-inpainting \
  -H "Content-Type: application/json" \
  -d '{
    "image_id": "img-456",
    "edit_plan": {
      "edits": [...],
      "room_type": "living_room"
    },
    "project_id": "project-123",
    "client_id": "client-789"
  }'
```

Response:
```json
{
  "version_id": "version-101",
  "image_url": "https://r2.../versions/version-101.jpg",
  "processing_time": 45.2
}
```

## Example User Prompts

### Simple Recolor
```
"Make the wall warm beige"
```

### Material Change
```
"Change the floor tiles to marble"
```

### Multiple Edits
```
"Make the wall warm beige, change the floor tiles to marble, and make the sofa dark blue"
```

### Lighting
```
"Add warm ceiling lights"
```

### Complex Request
```
"Transform the living room: warm beige walls, marble floor tiles, dark blue sofa, and add warm ambient lighting"
```

## Example Edit Plans

### Single Edit
```json
{
  "edits": [
    {
      "target_object": "wall",
      "operation": "recolor",
      "parameters": {
        "color": "warm beige",
        "strength": 0.8
      },
      "mask_id": "wall_mask_123",
      "confidence": 0.95
    }
  ],
  "validation": {
    "valid": true,
    "warnings": []
  },
  "room_type": "living_room",
  "original_prompt": "Make the wall warm beige"
}
```

### Multi-Edit
```json
{
  "edits": [
    {
      "target_object": "wall",
      "operation": "recolor",
      "parameters": {
        "color": "warm beige",
        "strength": 0.8
      },
      "mask_id": "wall_mask_123",
      "confidence": 0.95
    },
    {
      "target_object": "floor",
      "operation": "texture",
      "parameters": {
        "material": "marble",
        "strength": 0.9
      },
      "mask_id": "floor_mask_456",
      "confidence": 0.88
    },
    {
      "target_object": "sofa",
      "operation": "recolor",
      "parameters": {
        "color": "dark blue",
        "strength": 0.85
      },
      "mask_id": "sofa_mask_789",
      "confidence": 0.92
    }
  ],
  "validation": {
    "valid": true,
    "warnings": []
  },
  "room_type": "living_room",
  "original_prompt": "Make the wall warm beige, change the floor tiles to marble, and make the sofa dark blue"
}
```

## Frontend Integration Example

```typescript
// Upload image
const uploadImage = async (file: File) => {
  const formData = new FormData()
  formData.append('file', file)
  
  const response = await axios.post('/api/upload-image', formData)
  return response.data
}

// Process edit
const processEdit = async (imageId: string, prompt: string) => {
  // 1. Analyze scene
  const analysis = await axios.post('/api/analyze-scene', { image_id: imageId })
  
  // 2. Plan edits
  const plan = await axios.post('/api/plan-edits', {
    user_prompt: prompt,
    image_id: imageId
  })
  
  // 3. Run inference
  const result = await axios.post('/api/run-inpainting', {
    image_id: imageId,
    edit_plan: plan.data
  })
  
  return result.data
}

// WebSocket for progress
const ws = new WebSocket('ws://localhost:8000/ws/client-123')
ws.onmessage = (event) => {
  const data = JSON.parse(event.data)
  if (data.status === 'processing') {
    updateProgress(data.progress)
  } else if (data.status === 'completed') {
    showResult(data.version_id)
  }
}
```
