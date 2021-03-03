import logging
import config

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

if not config.RUN_DEBUG:
    logging.disable(logging.DEBUG)
