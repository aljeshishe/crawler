import logging
from pathlib import Path

from pydantic import BaseSettings

log = logging.getLogger(__name__)

ROOT_PATH = Path(__file__).parent
class Settings(BaseSettings):
    AWS_S3_BUCKET: str

    class Config:
        env_file = ROOT_PATH / '.env'

settings = Settings()
