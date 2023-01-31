import os
import uuid
from pathlib import Path

import boto3
from botocore.exceptions import ClientError


class S3Bucket:
    def __init__(self):
        bucket = os.getenv("AWS_S3_BUCKET")
        aws_region = os.getenv("AWS_REGION")
        os.environ["AWS_CONFIG_FILE"] = str(Path(__file__).parent / "aws_config")
        self.bucket = boto3.resource("s3", region_name=aws_region).Bucket(bucket)

    def tmp_file_path(self) -> Path:
        file_path = Path(f"/tmp/dashboards/{uuid.uuid4()}")
        file_path.parent.mkdir(parents=True, exist_ok=True)
        return file_path

    def file_exists(self, file_name: str) -> bool:
        try:
            self.bucket.Object(file_name).load()
            return True
        except ClientError as e:
            if e.response["Error"]["Code"] == "404":
                return False
            raise

    def download_file(self, file_name: str) -> Path:
        dst_path = self.tmp_file_path()
        self.bucket.download_file(file_name, dst_path.as_posix())
        return dst_path

    def upload_file(self, src_path: Path, dst_file: str) -> None:
        self.bucket.upload_file(src_path.as_posix(), dst_file)
