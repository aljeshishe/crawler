import sys

from loguru import logger
# config = {
#     "handlers": [
#         {"sink": sys.stdout, "format": "{time} - {message} {extra}"},
#         # {"sink": "file.log", "serialize": True},
#     ],
#     "extra": {"user": "someone"}
# }
# logger.configure(**config)

logger.info("hi")

context_logger = logger.bind(ip="192.168.0.1", user="someone")
context_logger.info("Contextualize your logger easily")
context_logger.bind(user="someone_else").info("Inline binding of extra attribute")
context_logger.info("Use kwargs to add context during formatting: {user}", user="anybody")

new_level = logger.level("SNAKY", no=38, color="<yellow>", icon="🐍")

logger.log("SNAKY", "Here we go!")
with logger.catch():
    raise Exception()

# with logger.contextualize(task=1):
#     logger.info("End of task")
#
# @utils.exception_safe
# def my_function(x, y, z):
#     # An error? It's caught anyway!
#     return 1 / (x + y + z)
# my_function(0,0,0)
