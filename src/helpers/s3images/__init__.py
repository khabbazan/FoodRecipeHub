import os
import aiohttp
import boto3
from PIL import Image
from io import BytesIO
import asyncio

from fastapi_babel import _


class S3ImagesInvalidExtension(Exception):
    pass


class S3ImagesUploadFailed(Exception):
    pass


class S3Images:
    """
    S3Images is a utility class for working with images stored in Amazon S3.

    This class provides methods for fetching images from S3, deleting images in S3, and uploading images to S3.

    Args:
        service_name (str): The name of the AWS service (e.g., 's3').
        aws_access_key_id (str): The AWS access key ID.
        aws_secret_access_key (str): The AWS secret access key.
        aws_s3_endpoint_url (str): The AWS S3 endpoint URL.
        aws_s3_region_name (str): The AWS S3 region name.
        aws_storage_bucket_name (str): The name of the S3 bucket for storing images.
        aws_default_acl (str): The default AWS S3 ACL (Access Control List) for uploaded images.
        **kwargs: Additional keyword arguments, including 'aws_s3_object_parameters' for object parameters like cache control.

    Methods:
        from_s3(key: str) -> Image:
            Fetch an image from S3 based on its key.

        delete_s3(key: str) -> dict:
            Delete an image in S3 based on its key.

        to_s3(img: Image, key: str):
            Upload an image to S3 with the specified key.

    Example usage:

    ```python
    s3_images = S3Images(
        service_name="s3",
        aws_access_key_id="your-access-key-id",
        aws_secret_access_key="your-secret-access-key",
        aws_s3_endpoint_url="https://s3.example.com",
        aws_s3_region_name="us-east-1",
        aws_storage_bucket_name="your-bucket-name",
        aws_default_acl="public-read",
        aws_s3_object_parameters={"cachecontrol": "max-age=3600"},
    )

    image = await s3_images.from_s3("image_key.jpg")
    await s3_images.to_s3(image, "new_image_key.jpg")
    await s3_images.delete_s3("image_key.jpg")
    ```

    In this example, the `S3Images` class is used to work with images stored in an Amazon S3 bucket. The class provides
    methods for fetching, deleting, and uploading images to and from S3.

    """

    def __init__(
        self, service_name, aws_access_key_id, aws_secret_access_key, aws_s3_endpoint_url, aws_s3_region_name, aws_storage_bucket_name, aws_default_acl, **kwargs
    ):
        self.acl = aws_default_acl
        self.bucket = aws_storage_bucket_name
        self.cache_control = kwargs["aws_s3_object_parameters"]["cachecontrol"]
        self.s3 = boto3.client(
            service_name=service_name,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            endpoint_url=aws_s3_endpoint_url,
            region_name=aws_s3_region_name,
        )

    async def from_s3(self, key):
        """
        Fetch an image from Amazon S3 based on its key.

        Args:
            key (str): The key of the image in the S3 bucket.

        Returns:
            Image: The fetched image as a PIL Image object.

        Raises:
            S3ImagesUploadFailed: If fetching the image from S3 fails.
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(self.s3.generate_presigned_url("get_object", Params={"Bucket": self.bucket, "Key": key})) as response:
                if response.status == 200:
                    file_byte_string = await response.read()
                    return Image.open(BytesIO(file_byte_string))
                else:
                    raise S3ImagesUploadFailed(_("Failed to fetch image {} from bucket {}").format(key, self.bucket))  # noqa P103

    async def delete_s3(self, key):
        """
        Delete an image in Amazon S3 based on its key.

        Args:
            key (str): The key of the image in the S3 bucket.

        Returns:
            dict: The response status of the delete operation.

        """
        status = await asyncio.to_thread(self.s3.delete_object, Bucket=self.bucket, Key=key)
        return status

    async def to_s3(self, img, key):
        """
        Upload an image to Amazon S3 with the specified key.

        Args:
            img (Image): The image to upload as a PIL Image object.
            key (str): The key to use when storing the image in the S3 bucket.

        Raises:
            S3ImagesUploadFailed: If uploading the image to S3 fails.
        """
        buffer = BytesIO()
        img.save(buffer, self.__get_safe_ext(key))
        buffer.seek(0)
        sent_data = await asyncio.to_thread(self.s3.put_object, Bucket=self.bucket, ACL=self.acl, Key=key, Body=buffer, CacheControl=self.cache_control)
        if sent_data["ResponseMetadata"]["HTTPStatusCode"] != 200:
            raise S3ImagesUploadFailed(_("Failed to upload image {} to bucket {}").format(key, self.bucket))  # noqa P103

    def __get_safe_ext(self, key):
        """
        Get the safe file extension for an S3 object based on its key.

        Args:
            key (str): The key of the S3 object.

        Returns:
            str: The safe file extension (e.g., 'JPEG', 'PNG').

        Raises:
            S3ImagesInvalidExtension: If the extension is invalid.
        """
        ext = os.path.splitext(key)[-1].strip(".").upper()
        if ext in ["JPG", "JPEG"]:
            return "JPEG"
        elif ext in ["PNG"]:
            return "PNG"
        else:
            raise S3ImagesInvalidExtension(_("Extension is invalid"))
