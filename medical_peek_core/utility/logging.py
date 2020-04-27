import logging

from datetime import datetime

logger = logging.getLogger(__name__)


def duration_logger(func, message = '', level = logging.DEBUG):
    """
    Logs a starting point, ending point, and duration of the execution of a function
    :param func: Function to execute
    :type func: *
    :param level: Log level
    :type level: int
    :param message: Optional message
    :type message: str
    :return: Function decorator
    :rtype: *
    """

    def function_wrapper(*args, **kwargs):
        formatted_message = ''
        if message:
            formatted_message = ' {0}'.format(message)
        start = datetime.now()
        logger.log(level, 'Executing {0} - (START) {1}'.format(
            func.__name__,
            formatted_message
        ))
        ret = func(*args, **kwargs)
        end = datetime.now()
        duration = end - start
        logger.log(level, 'Executing {0} - (END Duration={1}) {2}'.format(
            func.__name__,
            duration,
            formatted_message
        ))
        return ret

    return function_wrapper
