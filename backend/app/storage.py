"""
Cloudflare R2 storage integration.
"""

import boto3
from botocore.config import Config
from app.config import settings
from typing import BinaryIO
import uuid


class R2Storage:
    """Cloudflare R2 storage client."""

    def __init__(self):
        self.s3_client = boto3.client(
            "s3",
            endpoint_url=settings.r2_endpoint,
            aws_access_key_id=settings.r2_access_key_id,
            aws_secret_access_key=settings.r2_secret_access_key,
            config=Config(signature_version="s3v4"),
        )
        self.bucket_name = settings.r2_bucket_name

    def upload_file(self, file_data: bytes, key: str, content_type: str = "image/jpeg") -> str:
        """Upload file to R2 and return public URL."""
        self.s3_client.put_object(
            Bucket=self.bucket_name,
            Key=key,
            Body=file_data,
            ContentType=content_type,
        )
        # Construct public URL (adjust based on your R2 setup)
        return f"{settings.r2_endpoint}/{self.bucket_name}/{key}"

    def upload_fileobj(self, file_obj: BinaryIO, key: str, content_type: str = "image/jpeg") -> str:
        """Upload file object to R2."""
        self.s3_client.upload_fileobj(
            file_obj,
            self.bucket_name,
            key,
            ExtraArgs={"ContentType": content_type},
        )
        return f"{settings.r2_endpoint}/{self.bucket_name}/{key}"

    def delete_file(self, key: str) -> None:
        """Delete file from R2."""
        self.s3_client.delete_object(Bucket=self.bucket_name, Key=key)

    def get_presigned_url(self, key: str, expires_in: int = 3600) -> str:
        """Generate presigned URL for temporary access."""
        return self.s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": self.bucket_name, "Key": key},
            ExpiresIn=expires_in,
        )

    def generate_key(self, prefix: str, filename: str = None) -> str:
        """Generate storage key."""
        if filename:
            return f"{prefix}/{uuid.uuid4()}_{filename}"
        return f"{prefix}/{uuid.uuid4()}"


storage = R2Storage()
