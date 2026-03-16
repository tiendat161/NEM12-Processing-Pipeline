import logging

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s]: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S' # Optional: make the time look cleaner)
)
logger = logging.getLogger(__name__)
