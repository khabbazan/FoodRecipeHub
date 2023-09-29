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
        async with aiohttp.ClientSession() as session:
            async with session.get(self.s3.generate_presigned_url("get_object", Params={"Bucket": self.bucket, "Key": key})) as response:
                if response.status == 200:
                    file_byte_string = await response.read()
                    return Image.open(BytesIO(file_byte_string))
                else:
                    raise S3ImagesUploadFailed(_("Failed to fetch image {} from bucket {}").format(key, self.bucket))  # noqa P103

    async def delete_s3(self, key):
        status = await asyncio.to_thread(self.s3.delete_object, Bucket=self.bucket, Key=key)
        return status

    async def to_s3(self, img, key):
        buffer = BytesIO()
        img.save(buffer, self.__get_safe_ext(key))
        buffer.seek(0)
        sent_data = await asyncio.to_thread(self.s3.put_object, Bucket=self.bucket, ACL=self.acl, Key=key, Body=buffer, CacheControl=self.cache_control)
        if sent_data["ResponseMetadata"]["HTTPStatusCode"] != 200:
            raise S3ImagesUploadFailed(_("Failed to upload image {} to bucket {}").format(key, self.bucket))  # noqa P103

    def __get_safe_ext(self, key):
        ext = os.path.splitext(key)[-1].strip(".").upper()
        if ext in ["JPG", "JPEG"]:
            return "JPEG"
        elif ext in ["PNG"]:
            return "PNG"
        else:
            raise S3ImagesInvalidExtension(_("Extension is invalid"))
