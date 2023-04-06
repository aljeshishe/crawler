import re
import email
from datetime import datetime
from loguru import logger
import dotenv
import pandas as pd
import requests

from src import utils
from src.utils import S3Bucket

dotenv.load_dotenv()
FILE_NAME = "bazaraki.csv"


@utils.exception_safe
def process(name, url):
    logger.info(f"Processing {name} {url}")
    result = get_data(url)
    logger.info(f"{name}: properties found: {result}")
    store(name, result)


def store(name, result):
    s3 = S3Bucket()
    if s3.file_exists(FILE_NAME):
        in_file_path = s3.download_file(FILE_NAME)
        df = pd.read_csv(in_file_path)
    else:
        df = pd.DataFrame()
    data = dict(dt=datetime.utcnow(), name=name, value=result)
    df = df.append(data, ignore_index=True)
    out_file_path = s3.tmp_file_path()
    df.to_csv(out_file_path, index=False)
    s3.upload_file(src_path=out_file_path, dst_file=FILE_NAME)


def get_data(url):
    resp = requests.get(url=url)
    resp.raise_for_status()
    result = int(re.search(r"(\d+) ads near", resp.text).group(1))
    return result


@utils.exception_safe
def handler():
    url = "https://www.bazaraki.com/real-estate-to-rent/apartments-flats/lemesos-district-limassol/"
    process(name="bazaraki_apartments_all", url=url)
    
    url = "https://www.bazaraki.com/real-estate-to-rent/houses/lemesos-district-limassol/"
    process(name="bazaraki_houses_all", url=url)

    url = "https://www.bazaraki.com/real-estate-to-rent/apartments-flats/number-of-bedrooms---0/number-of-bedrooms---1/number-of-bedrooms---2/lemesos-district-limassol/?price_max=1500"
    process(name="bazaraki_apartments_0_1_2_rooms_1500_max", url=url)


if __name__ == "__main__":
    handler()
