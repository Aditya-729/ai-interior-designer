"""
S3-compatible storage client (Cloudflare R2).
"""

import boto3
from botocore.config import Config
from botocore.exceptions import ClientError
from app.core.config import settings
from typing import BinaryIO, Optional
import uuid
import logging

logger = logging.getLogger(__name__)


class StorageClient:
    """S3-compatible storage client."""

    def __init__(self):
        self.s3_client = boto3.client(
            "s3",
            endpoint_url=settings.R2_ENDPOINT,
            aws_access_key_id=settings.R2_ACCESS_KEY_ID,
            aws_secret_access_key=settings.R2_SECRET_ACCESS_KEY,
            config=Config(signature_version="s3v4"),
        )
        self.bucket_name = settings.R2_BUCKET_NAME

    def upload_file(self, file_data: bytes, key: str, content_type: str = "image/jpeg") -> str:
        """
        Upload file to R2 and return public URL.
        
        Args:
            file_data: File bytes
            key: Storage key
            content_type: MIME type
            
        Returns:
            Public URL
        """
        try:
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=key,
                Body=file_data,
                ContentType=content_type,
            )
            
            # Return public URL
            if settings.R2_PUBLIC_URL:
                return f"{settings.R2_PUBLIC_URL}/{key}"
            else:
                return f"{settings.R2_ENDPOINT}/{self.bucket_name}/{key}"
        except ClientError as e:
            logger.error(f"Failed to upload file: {e}")
            raise

    def upload_fileobj(self, file_obj: BinaryIO, key: str, content_type: str = "image/jpeg") -> str:
        """Upload file object to R2."""
        try:
            self.s3_client.upload_fileobj(
                file_obj,
                self.bucket_name,
                key,
                ExtraArgs={"ContentType": content_type},
            )
            
            if settings.R2_PUBLIC_URL:
                return f"{settings.R2_PUBLIC_URL}/{key}"
            else:
                return f"{settings.R2_ENDPOINT}/{self.bucket_name}/{key}"
        except ClientError as e:
            logger.error(f"Failed to upload fileobj: {e}")
            raise

    def download_file(self, key: str) -> bytes:
        """Download file from R2."""
        try:
            response = self.s3_client.get_object(Bucket=self.bucket_name, Key=key)
            return response["Body"].read()
        except ClientError as e:
            logger.error(f"Failed to download file: {e}")
            raise

    def delete_file(self, key: str) -> None:
        """Delete file from R2."""
        try:
            self.s3_client.delete_object(Bucket=self.bucket_name, Key=key)
        except ClientError as e:
            logger.error(f"Failed to delete file: {e}")
            raise

    def get_presigned_url(self, key: str, expires_in: int = 3600) -> str:
        """Generate presigned URL for temporary access."""
        try:
            return self.s3_client.generate_presigned_url(
                "get_object",
                Params={"Bucket": self.bucket_name, "Key": key},
                ExpiresIn=expires_in,
            )
        except ClientError as e:
            logger.error(f"Failed to generate presigned URL: {e}")
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
