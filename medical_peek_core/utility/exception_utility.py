import logging

from django.core.exceptions import PermissionDenied as DjangoPermissionDenied
from rest_framework import status
from rest_framework.exceptions import PermissionDenied as RestPermissionDenied

from medical_peek_core.model.j_send import JSend

logger = logging.getLogger(__name__)


class ExceptionUtility(object):
    """
    Utility class for handling exceptions
    """

    @classmethod
    def is_error(cls, status_code):
        """
        Checks whether or not a HTTP Request has an error based on the Status Code of the response
        :param status_code: Status Code of the response
        :type status_code: int
        :return: Whether or not the response has an error
        :rtype: bool
        """
        return status_code >= 300

    @classmethod
    def get_jsend_from_exception(cls, exception):
        """
        Gets a JSend object representation of an exception that occurred within an HTTP Request
        :param exception: Exception that occurred
        :type exception: object
        :return: JSend representation of the exception
        :rtype:
        """
        logger.debug("Generating a JSend object for an exception...")
        j_send = JSend()
        # Determine the status code
        if isinstance(exception, DjangoPermissionDenied) or isinstance(exception, RestPermissionDenied):
            j_send.code = status.HTTP_401_UNAUTHORIZED
        elif hasattr(exception, 'status_code'):
            j_send.code = int(exception.status_code)
        else:
            j_send.code = status.HTTP_500_INTERNAL_SERVER_ERROR
        # Set the message based on the status code
        if j_send.code == status.HTTP_401_UNAUTHORIZED:
            j_send.message = 'Not authorized'
        elif hasattr(exception, 'detail'):
            j_send.message = str(exception.detail)
        elif j_send.code == status.HTTP_500_INTERNAL_SERVER_ERROR:
            j_send.message = str(exception)
        else:
            j_send.message = str(exception) or repr(exception)  # This may be unreachable
        # set the type and status to "error"
        j_send.status = JSend.Status.error
        logger.debug("Generated a JSend object for an exception!")
        return j_send
