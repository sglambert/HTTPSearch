import logging
from logging.handlers import RotatingFileHandler
import sys

log = logging
log.basicConfig(
        handlers=[RotatingFileHandler('HTTPSearch.log', maxBytes=2000000, backupCount=7),
                  log.StreamHandler(sys.stdout)],
        format="%(asctime)s | %(levelname)s | %(message)s")
log.root.setLevel(logging.NOTSET)
