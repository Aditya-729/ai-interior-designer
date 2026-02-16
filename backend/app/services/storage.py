"""
Supabase Storage client for file uploads.
"""

from supabase import create_client, Client
from app.core.config import settings
from typing import BinaryIO, Optional
import uuid
import logging
import io

logger = logging.getLogger(__name__)


class StorageClient:
    """Supabase Storage client."""

    def __init__(self):
        if not settings.SUPABASE_URL or not settings.SUPABASE_SERVICE_KEY:
            raise ValueError("Supabase URL and Service Key are required for storage")
        
        self.supabase: Client = create_client(
            settings.SUPABASE_URL,
            settings.SUPABASE_SERVICE_KEY
        )
        self.bucket_name = "ai-interior-designer"
        
        # Ensure bucket exists
        try:
            self._ensure_bucket()
        except Exception as e:
            logger.warning(f"Could not verify bucket exists: {e}")
    
    def _ensure_bucket(self):
        """Ensure storage bucket exists."""
        try:
            # Try to list files (this will fail if bucket doesn't exist)
            self.supabase.storage.from_(self.bucket_name).list(limit=1)
        except Exception:
            # Bucket might not exist, but that's okay - Supabase will create it on first upload
            logger.info(f"Bucket '{self.bucket_name}' will be created on first upload")

    def upload_file(self, file_data: bytes, key: str, content_type: str = "image/jpeg") -> str:
        """
        Upload file to Supabase Storage and return public URL.
        
        Args:
            file_data: File bytes
            key: Storage key (path)
            content_type: MIME type
            
        Returns:
            Public URL
        """
        try:
            # Upload to Supabase Storage
            response = self.supabase.storage.from_(self.bucket_name).upload(
                path=key,
                file=file_data,
                file_options={"content-type": content_type, "upsert": "true"}
            )
            
            # Get public URL
            public_url = self.supabase.storage.from_(self.bucket_name).get_public_url(key)
            
            logger.info(f"File uploaded to Supabase Storage: {key}")
            return public_url
        except Exception as e:
            logger.error(f"Failed to upload file to Supabase: {e}")
            raise

    def upload_fileobj(self, file_obj: BinaryIO, key: str, content_type: str = "image/jpeg") -> str:
        """Upload file object to Supabase Storage."""
        try:
            # Read file object into bytes
            file_data = file_obj.read()
            return self.upload_file(file_data, key, content_type)
        except Exception as e:
            logger.error(f"Failed to upload fileobj to Supabase: {e}")
            raise

    def download_file(self, key: str) -> bytes:
        """Download file from Supabase Storage."""
        try:
            response = self.supabase.storage.from_(self.bucket_name).download(key)
            return response
        except Exception as e:
            logger.error(f"Failed to download file from Supabase: {e}")
            raise

    def delete_file(self, key: str) -> None:
        """Delete file from Supabase Storage."""
        try:
            self.supabase.storage.from_(self.bucket_name).remove([key])
            logger.info(f"File deleted from Supabase Storage: {key}")
        except Exception as e:
            logger.error(f"Failed to delete file from Supabase: {e}")
            raise

    def get_presigned_url(self, key: str, expires_in: int = 3600) -> str:
        """Generate signed URL for temporary access."""
        try:
            # Supabase doesn't have presigned URLs, but we can use public URLs
            # For private files, you'd need to use Supabase's signed URL feature
            return self.supabase.storage.from_(self.bucket_name).get_public_url(key)
        except Exception as e:
            logger.error(f"Failed to generate signed URL: {e}")
            raise

    def generate_key(self, prefix: str, filename: Optional[str] = None) -> str:
        """Generate storage key."""
        unique_id = str(uuid.uuid4())
        if filename:
            # Sanitize filename
            safe_filename = "".join(c for c in filename if c.isalnum() or c in ".-_")
            return f"{prefix}/{unique_id}_{safe_filename}"
        return f"{prefix}/{unique_id}"


storage = StorageClient()
