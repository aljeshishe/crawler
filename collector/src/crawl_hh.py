import re
from datetime import datetime

import dotenv
import pandas as pd
import requests
from loguru import logger

from src import utils
from src.utils import S3Bucket

dotenv.load_dotenv()
FILE_NAME = "hh.csv"


@utils.exception_safe
def process(name, url):
    logger.info(f"Processing {name} {url}")
    result = get_data(url)
    logger.info(f"{name}: vacancies found: {result}")
    store(name, result)


def store(name, result):
    s3 = S3Bucket()
    in_file_path = s3.download_file(FILE_NAME)
    df = pd.read_csv(in_file_path)
    data = dict(dt=datetime.utcnow(), name=name, value=result)
    df = df.append(data, ignore_index=True)
    out_file_path = s3.tmp_file_path()
    df.to_csv(out_file_path, index=False)
    s3.upload_file(src_path=out_file_path, dst_file=FILE_NAME)


def get_data(url):
    headers = {"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                             "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"}
    resp = requests.get(url=url, headers=headers)
    resp.raise_for_status()
    result = int(re.search("'vacancies_found': '(\d+)'", resp.text).group(1))
    return result


@utils.exception_safe
def handler():
    process(name="python_petersburg_and_others",
            url="https://hh.ru/search/vacancy?text=python&salary=&clusters=true&area=1001&area=2&ored_clusters=true&enable_snippets=true")
    process(name="python_petersburg",
            url="https://hh.ru/search/vacancy?text=python&salary=&clusters=true&area=2&ored_clusters=true&enable_snippets=true")


if __name__ == "__main__":
    handler()
