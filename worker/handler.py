import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
from src import crawl_hh


def run(event, context):
    print("hell1o")
    crawl_hh.handler()
