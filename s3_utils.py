import os
import logging
from minio import Minio

logger = logging.getLogger(__name__)

def upload_to_minio(file_path, minio_endpoint, minio_access_key, minio_secret_key, minio_bucket_name, minio_object_name):
    try:
        # Initialize the MinIO client
        minio_client = Minio(
            minio_endpoint,
            access_key=minio_access_key,
            secret_key=minio_secret_key,
            secure=False  # Set it as True if HTTPS is used
        )

        # Check if the bucket exists, create it if necessary
        if not minio_client.bucket_exists(minio_bucket_name):
            minio_client.make_bucket(minio_bucket_name)

        # Upload the file
        minio_client.fput_object(
            minio_bucket_name,
            minio_object_name,
            file_path
        )

        os.remove(file_path)  # Clean up: Remove the local file after uploading

    except Exception as e:
        logger.exception("An exception occurred: %s", str(e))

