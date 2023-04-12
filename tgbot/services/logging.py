import logging


logging.basicConfig(
    level=logging.INFO,
    format=u'%(filename)s:%(lineno)d #%(levelname)-8s '
           u'[%(asctime)s] - %(name)s - %(message)s',
)
logger = logging.getLogger(__name__)
