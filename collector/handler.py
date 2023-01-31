import logging

from src import crawl_hh
from src import crawl_linkedin

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def run(event, context):
    crawl_hh.handler()
    crawl_linkedin.handler()
