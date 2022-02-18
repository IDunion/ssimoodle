import logging
from logging.handlers import TimedRotatingFileHandler

_handler = TimedRotatingFileHandler("app.log", when="midnight", interval=1)
_handler.suffix = "%Y%m%d"

# config logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        _handler,
        logging.StreamHandler()
    ]
)