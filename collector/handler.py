import sys

from loguru import logger

from src import crawl_hh
from src import crawl_linkedin
from src import utils

utils.init_sentry()
logger.remove()
logger.add(sys.stdout, format="{time} - {level} - {message}", level="INFO", diagnose=False)


@utils.exception_safe
def run(event, context):
    crawl_hh.handler()
    crawl_linkedin.handler()


if __name__ == "__main__":
    run(None, None)
