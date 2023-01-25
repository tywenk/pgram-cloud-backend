from fastapi import APIRouter
from dataclasses import dataclass
import logging
from typing import Union, Literal
from botocore.exceptions import ClientError
from app import DefaultConfig
from app import AWSClient
from urllib.parse import unquote


router = APIRouter(
    prefix="/user",
    tags=["user"],
    responses={404: {"description": "Not found"}},
)

config = DefaultConfig()
aws_client = AWSClient()
s3 = aws_client.s3
logger = logging.getLogger(__name__)


@router.get("/")
async def get_user():
    return "healthy"


@router.get("/buckets")
async def buckets():
    return s3.list_buckets()


@router.get("/upload")
async def upload(filename: str = ""):
    bucket = aws_client.S3_BUCKET_NAME
    key = "images/" + unquote(filename)
    url = generate_presigned_url(s3, "put_object", bucket, key)
    return url


@router.get("/view")
async def get_object(key: str):
    """gets a sample object from s3"""
    bucket = aws_client.S3_BUCKET_NAME
    url = generate_presigned_url(s3, "get_object", bucket, key)
    return url


def generate_presigned_url(
    s3_client,
    client_method: Union[Literal["get_object"], Literal["put_object"]],
    bucket_name: str,
    object_name: str,
    expiration: int = 100,
):
    """
    Generate a presigned Amazon S3 URL that can be used to perform an action.

    :param s3_client: A Boto3 Amazon S3 client.
    :param client_method: The name of the client method that the URL performs. put_object, get_object, etc.
    :param method_parameters: The parameters of the specified client method.
    :param expires_in: The number of seconds the presigned URL is valid for.
    :return: The presigned URL.
    """
    try:
        url = s3_client.generate_presigned_url(
            ClientMethod=client_method,
            Params={"Bucket": bucket_name, "Key": object_name},
            ExpiresIn=expiration,
        )
        logger.info("Got presigned URL: %s", url)
    except ClientError:
        logger.exception(
            "Couldn't get a presigned URL for client method '%s'.", client_method
        )
        raise
    return url
