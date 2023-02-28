from src import crawl_hh
from src import crawl_linkedin
from src import utils

utils.init_sentry()


@utils.exception_safe
def run(event, context):
    crawl_hh.handler()
    crawl_linkedin.handler()


if __name__ == "__main__":
    run(None, None)
