import os
import uuid
from pathlib import Path

import boto3
import sentry_sdk
from botocore.exceptions import ClientError
from loguru import logger


class S3Bucket:
    def __init__(self):
        bucket = os.getenv("AWS_S3_BUCKET")
        self.bucket = boto3.resource("s3").Bucket(bucket)

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


def init_sentry():
    sentry_sdk.init(
        dsn="https://427075d336a042fdbc83c6f7499de777@o4504660828225536.ingest.sentry.io/4504660833009664",

        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        # We recommend adjusting this value in production.
        traces_sample_rate=1.0
    )


def exception_safe(func):
    return logger.catch(onerror=lambda ex: sentry_sdk.capture_exception(ex))(func)
