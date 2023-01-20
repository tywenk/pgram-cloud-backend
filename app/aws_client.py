import os
from dataclasses import dataclass
from dotenv import load_dotenv
import boto3
from botocore.config import Config

@dataclass
class AWSClient():
    load_dotenv(".env.local")
    
    S3_BUCKET_NAME: str = "pgram-cloud-s3"
    AWS_ACCESS_KEY: str | None = os.getenv("AWS_ACCESS_KEY")
    AWS_SECRET_ACCESS_KEY: str | None = os.getenv("AWS_SECRET_ACCESS_KEY")
    
    aws_config = Config(
        region_name="us-east-1",
        signature_version="v4",
        retries={"max_attempts": 10, "mode": "standard"},
    )
    
    s3 = boto3.client(
        "s3",
        config=aws_config,
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    )
    

        

        