import uuid
import aioboto3
from .config import settings

session = aioboto3.Session(aws_access_key_id=settings.s3.s3_access_key,
                           aws_secret_access_key=settings.s3.s3_secret_key)

def _client():
    return session.client("s3", endpoint_url=settings.s3.s3_endpoint)

async def generate_presigned_upload_url(filename: str,
                                        content_type: str) -> tuple[str, str]:
    s3_key = f"{uuid.uuid4()}/{filename}"
    async with _client() as client:
        url = await client.generate_presigned_url("put_object",
                                                  Params={"Bucket": settings.s3.s3_bucket,
                                                          "Key": s3_key,
                                                          "ContentType": content_type},
                                                  ExpiresIn=300)
        return url, s3_key

async def generate_presigned_download_url(s3_key: str) -> str:
    async with _client() as client:
        url = await client.generate_presigned_url("get_object",
                                                  Params={"Bucket": settings.s3.s3_bucket,
                                                          "Key": s3_key},
                                                  ExpiresIn=3600)
        return url

async def delete_object(s3_key: str) -> None:
    async with _client() as client:
        await client.delete_object(Bucket=settings.s3.s3_bucket, Key=s3_key)