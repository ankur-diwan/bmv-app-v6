"""
IBM Cloud Object Storage Client
Handles file uploads to COS bucket
"""
import ibm_boto3
from ibm_botocore.client import Config
import os
from typing import BinaryIO, Optional
import logging

logger = logging.getLogger(__name__)


class COSClient:
    """IBM Cloud Object Storage client for file operations"""

    def __init__(
        self,
        api_key: str,
        service_instance_id: str,
        endpoint_url: str = "https://s3.us-south.cloud-object-storage.appdomain.cloud",
        bucket_name: str = "bankvalidationapp"
    ):
        """
        Initialize COS client

        Args:
            api_key: IBM Cloud API key
            service_instance_id: COS service instance ID (resource_instance_id)
            endpoint_url: COS endpoint URL
            bucket_name: Name of the bucket to use
        """
        self.bucket_name = bucket_name

        # Initialize COS client
        self.cos_client = ibm_boto3.client(
            "s3",
            ibm_api_key_id=api_key,
            ibm_service_instance_id=service_instance_id,
            config=Config(signature_version="oauth"),
            endpoint_url=endpoint_url
        )

        # Create a separate client for presigned URLs (uses different signature)
        self.cos_client_presigned = ibm_boto3.client(
            "s3",
            aws_access_key_id=os.getenv("COS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("COS_SECRET_ACCESS_KEY"),
            endpoint_url=endpoint_url
        )

        logger.info(f"COS client initialized for bucket: {bucket_name}")

    def upload_file(
        self,
        file_obj: BinaryIO,
        object_name: str,
        content_type: Optional[str] = None
    ) -> bool:
        """
        Upload a file to COS bucket

        Args:
            file_obj: File object to upload
            object_name: Name for the object in COS
            content_type: MIME type of the file

        Returns:
            bool: True if upload successful, False otherwise
        """
        try:
            extra_args = {}
            if content_type:
                extra_args['ContentType'] = content_type

            self.cos_client.upload_fileobj(
                file_obj,
                self.bucket_name,
                object_name,
                ExtraArgs=extra_args
            )

            logger.info(f"Successfully uploaded {object_name} to {self.bucket_name}")
            return True

        except Exception as e:
            logger.error(f"Failed to upload {object_name}: {str(e)}")
            return False

    def upload_file_from_path(
        self,
        file_path: str,
        object_name: Optional[str] = None,
        content_type: Optional[str] = None
    ) -> bool:
        """
        Upload a file from local path to COS bucket

        Args:
            file_path: Local path to the file
            object_name: Name for the object in COS (defaults to filename)
            content_type: MIME type of the file

        Returns:
            bool: True if upload successful, False otherwise
        """
        if object_name is None:
            object_name = os.path.basename(file_path)

        try:
            with open(file_path, 'rb') as file_obj:
                return self.upload_file(file_obj, object_name, content_type)
        except Exception as e:
            logger.error(f"Failed to read file {file_path}: {str(e)}")
            return False

    def download_file(self, object_name: str, file_path: str) -> bool:
        """
        Download a file from COS bucket

        Args:
            object_name: Name of the object in COS
            file_path: Local path to save the file

        Returns:
            bool: True if download successful, False otherwise
        """
        try:
            self.cos_client.download_file(
                self.bucket_name,
                object_name,
                file_path
            )
            logger.info(f"Successfully downloaded {object_name} to {file_path}")
            return True

        except Exception as e:
            logger.error(f"Failed to download {object_name}: {str(e)}")
            return False

    def list_objects(self, prefix: str = "") -> list:
        """
        List objects in the bucket with metadata

        Args:
            prefix: Filter objects by prefix

        Returns:
            list: List of dictionaries with object details
        """
        try:
            response = self.cos_client.list_objects_v2(
                Bucket=self.bucket_name,
                Prefix=prefix
            )

            if 'Contents' in response:
                return [{
                    'key': obj['Key'],
                    'size': obj['Size'],
                    'last_modified': obj['LastModified'],
                    'etag': obj['ETag']
                } for obj in response['Contents']]
            return []

        except Exception as e:
            logger.error(f"Failed to list objects: {str(e)}")
            return []

    def get_latest_files_by_type(self, prefix: str = "uploads/") -> dict:
        """
        Get the latest uploaded files by type (train, test, oot, documents)

        Args:
            prefix: Folder prefix to search in

        Returns:
            dict: Dictionary with latest files by type
        """
        try:
            objects = self.list_objects(prefix)

            if not objects:
                return {}

            # Sort by last modified (newest first)
            objects.sort(key=lambda x: x['last_modified'], reverse=True)

            latest_files = {
                'train': None,
                'test': None,
                'oot': None,
                'documents': []
            }

            for obj in objects:
                filename = obj['key'].split('/')[-1].lower()

                # Identify CSV datasets
                if filename.endswith('.csv'):
                    if 'train' in filename and not latest_files['train']:
                        latest_files['train'] = obj
                    elif 'test' in filename and not latest_files['test']:
                        latest_files['test'] = obj
                    elif ('oot' in filename or 'out_of_time' in filename) and not latest_files['oot']:
                        latest_files['oot'] = obj

                # Identify documents
                elif filename.endswith(('.pdf', '.docx', '.txt')):
                    latest_files['documents'].append(obj)

            # Keep only the latest document
            if latest_files['documents']:
                latest_files['documents'] = [latest_files['documents'][0]]

            logger.info(f"Found latest files: train={latest_files['train'] is not None}, "
                       f"test={latest_files['test'] is not None}, "
                       f"oot={latest_files['oot'] is not None}, "
                       f"documents={len(latest_files['documents'])}")

            return latest_files

        except Exception as e:
            logger.error(f"Failed to get latest files: {str(e)}")
            return {}

    def delete_object(self, object_name: str) -> bool:
        """
        Delete an object from the bucket

        Args:
            object_name: Name of the object to delete

        Returns:
            bool: True if deletion successful, False otherwise
        """
        try:
            self.cos_client.delete_object(
                Bucket=self.bucket_name,
                Key=object_name
            )
            logger.info(f"Successfully deleted {object_name}")
            return True

        except Exception as e:
            logger.error(f"Failed to delete {object_name}: {str(e)}")
            return False

    def get_object_url(self, object_name: str, expiration: int = 3600) -> Optional[str]:
        """
        Generate a presigned URL for an object

        Args:
            object_name: Name of the object
            expiration: URL expiration time in seconds (default: 1 hour)

        Returns:
            str: Presigned URL or None if failed
        """
        try:
            # Use the presigned client with HMAC credentials
            url = self.cos_client_presigned.generate_presigned_url(
                'get_object',
                Params={
                    'Bucket': self.bucket_name,
                    'Key': object_name
                },
                ExpiresIn=expiration
            )
            return url

        except Exception as e:
            logger.error(f"Failed to generate URL for {object_name}: {str(e)}")
            return None


def get_cos_client() -> COSClient:
    """
    Factory function to create COS client from environment variables

    Returns:
        COSClient: Configured COS client instance
    """
    api_key = os.getenv("COS_API_KEY")
    service_instance_id = os.getenv("COS_RESOURCE_INSTANCE_ID")
    endpoint_url = os.getenv("COS_ENDPOINT_URL", "https://s3.us-south.cloud-object-storage.appdomain.cloud")
    bucket_name = os.getenv("COS_BUCKET_NAME", "bankvalidationapp")

    if not api_key or not service_instance_id:
        raise ValueError("COS_API_KEY and COS_RESOURCE_INSTANCE_ID must be set in environment variables")

    return COSClient(
        api_key=api_key,
        service_instance_id=service_instance_id,
        endpoint_url=endpoint_url,
        bucket_name=bucket_name
    )

# Made with Bob
