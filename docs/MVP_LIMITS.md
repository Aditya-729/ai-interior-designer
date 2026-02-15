# MVP Usage Limits

## Free Tier Limits

### Default Limits (per user)

- **Projects**: 10 maximum
- **Edits per day**: 50
- **Inference calls per day**: 20

### Configuration

Limits are stored in the `users` table and can be customized per user:

```sql
UPDATE users SET 
  max_projects = 20,
  max_edits_per_day = 100,
  max_inference_per_day = 50
WHERE id = 'user-id';
```

### Usage Tracking

Daily usage is tracked in the `usage_stats` table:
- Resets at midnight UTC
- Automatically creates new stats record if none exists
- Increments on each operation

### API Endpoint

```
GET /api/v1/usage
```

Returns:
```json
{
  "projects": {
    "current": 5,
    "limit": 10
  },
  "edits": {
    "today": 3,
    "limit": 50
  },
  "inference": {
    "today": 2,
    "limit": 20
  }
}
```

## GPU Queue Limits

### Configuration

- **Max concurrent jobs**: 2 (configurable via `GPU_MAX_CONCURRENT`)
- **Max queue size**: 10 (configurable via `GPU_QUEUE_MAX_SIZE`)

### Behavior

- Jobs are queued when GPU is at capacity
- Queue position is reported via WebSocket
- Jobs are rejected when queue is full (HTTP 503)
- Queue depth is exposed in API responses

### Monitoring

Queue status is available via:
- WebSocket progress updates
- API response includes `queue_status`
- Health check endpoint

## Rate Limiting

### Per-IP Limits (Future)

- Upload: 10 requests/minute
- Inference: 5 requests/minute
- API calls: 100 requests/minute

## Demo Mode

In development with `DEMO_MODE=true`:
- Auth is bypassed
- Limits are not enforced
- All users share "demo-user-id"

## Upgrading Limits

To increase limits for a user:

1. Update database:
```sql
UPDATE users SET max_projects = 50 WHERE email = 'user@example.com';
```

2. Or via admin API (to be implemented)
