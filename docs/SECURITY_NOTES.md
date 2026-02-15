# Security Notes

## Authentication

### Magic Link Auth

- Tokens are hashed before storage (SHA-256)
- Tokens expire after 24 hours
- Tokens are single-use (cleared after verification)
- Session cookies are HttpOnly and Secure in production

### Session Management

- Sessions stored in HttpOnly cookies
- 7-day expiration
- SameSite=Lax to prevent CSRF

## Access Control

### Project Ownership

- All project operations require authentication
- Users can only access their own projects
- Image uploads are tied to projects
- Ownership is verified on every request

### Demo Mode

- Only enabled in development
- Bypasses authentication
- Should never be enabled in production

## File Upload Security

### Image Uploads

- **Max file size**: 10MB (configurable)
- **Allowed types**: JPEG, PNG, WebP
- **Dimension limits**: 4096x4096 pixels
- **MIME type validation**: Enforced server-side

### Audio Uploads

- **Max file size**: 5MB
- **Max duration**: 60 seconds
- **Allowed types**: WebM, WAV, MP3
- **MIME type validation**: Enforced server-side

## API Security

### Rate Limiting

- Per-IP rate limits (to be implemented)
- Per-user usage limits (enforced)
- GPU queue limits (enforced)

### Input Validation

- All inputs validated with Pydantic
- SQL injection prevented via SQLAlchemy ORM
- XSS prevented via proper escaping

## Storage Security

### Cloudflare R2

- Access keys stored in environment variables
- Bucket policies restrict access
- Public URLs use presigned tokens (optional)

## Data Privacy

### User Data

- Email addresses stored securely
- No passwords stored (magic link only)
- Usage statistics anonymized in analytics

### Generated Content

- Images stored in user-specific paths
- Automatic cleanup of orphaned files
- Version history retained per project

## Recommendations

1. **Enable HTTPS** in production
2. **Set secure cookies** (`secure=True`)
3. **Implement rate limiting** per IP
4. **Monitor for abuse** (excessive API calls)
5. **Regular security audits** of dependencies
6. **Keep dependencies updated**

## Known Limitations

- No 2FA (magic link only)
- No password reset (new magic link)
- No account deletion API (manual DB operation)
- No audit logging (to be implemented)
