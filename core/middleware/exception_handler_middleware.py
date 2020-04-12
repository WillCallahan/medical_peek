import logging

from django.http import JsonResponse
from rest_framework import status

from core.middleware.core_middleware import HookMiddleware
from core.model.j_send import JSendSerializer
from core.utility.exception_utility import ExceptionUtility

logger = logging.getLogger(__name__)


class ExceptionMiddleware(HookMiddleware):
    # noinspection PyMethodMayBeStatic
    def process_exception(self, request, exception):
        """
        Handles all uncaught exceptions that occur within Django. This should appear as the very first middleware
        class that is defined in the Django MIDDLEWARE_CLASSES setting the the settings.py
        :param request: Current HttpRequest
        :type request: django.http.HttpRequest
        :param exception: Thrown Exception
        :type exception: Exception
        :return:
        :rtype:
        """
        logger.error("Unhandled exception!")
        logger.exception(exception)
        if "application/json" in request.META.get('HTTP_ACCEPT', ''):
            j_send = ExceptionUtility.get_jsend_from_exception(exception)
            j_send_serializer = JSendSerializer(data = j_send.__dict__)
            j_send_serializer.is_valid(True)
            return JsonResponse(j_send_serializer.data, status = status.HTTP_500_INTERNAL_SERVER_ERROR)
