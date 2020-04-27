import logging


logger = logging.getLogger(__name__)


def ignore_errors(func):
    """
    Ignores errors which occur and logs the error
    :param func: Function to execute
    :return: Function wrapper
    """
    def _ignore_errors(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f'Failed to execute function  func={func.__name__}')
            logger.error(e)
    return _ignore_errors
