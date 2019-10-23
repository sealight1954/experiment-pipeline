import logging
from logging import getLogger, StreamHandler, FileHandler

#See: https://stackoverflow.com/questions/25187083/python-logging-to-multiple-handlers-at-different-log-levels
logger = getLogger("pipeline")
handler = StreamHandler()
handler.setLevel(logging.DEBUG)
fhandler = FileHandler("results/log.txt")
fhandler.setLevel(logging.DEBUG)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(asctime)s %(funcName)s() at %(filename)s L%(lineno)d](%(levelname)s) %(message)s')
handler.setFormatter(formatter)
fhandler.setFormatter(formatter)

logger.addHandler(handler)
logger.addHandler(fhandler)