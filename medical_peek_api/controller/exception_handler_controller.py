import logging

from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse
from django.views.defaults import server_error, page_not_found
from rest_framework import status

from medical_peek_core.model.j_send import JSend, JSendSerializer
from medical_peek_core.utility.exception_utility import ExceptionUtility

logger = logging.getLogger(__name__)


def rest_exception_handler(exception, context):
    """
    Exception handler utilized by the Django Rest Framework

    The exception handler will override the default implementation of the Django Rest Framework Exception handler if
    the "Accept" header of the request in the current context has "application/json" in its value. If this is true,
    a JSonResponse View will be returned to the user containing a JSend object that represents the exception.
    :param exception: Exception that occurred
    :type exception: object
    :param context: Context of the exception (i.e. request)
    :type context: dict
    :return: JSonResponse View with JSend error if the Accept header of the request has a value of "application/json"
    :rtype: JsonResponse
    """
    if context.get('request', None) is not None \
            and 'application/json' in context.get('request').META.get('HTTP_ACCEPT', ''):
        logger.error("Unhandled exception!")
        logger.exception(exception)
        j_send = ExceptionUtility.get_jsend_from_exception(exception)
        j_send_serializer = JSendSerializer(data = j_send.__dict__)
        j_send_serializer.is_valid(True)
        return JsonResponse(j_send_serializer.data, status = j_send.code)


def handler500(request, template_name = '500.html'):
    """
    Overrides the default Django implementation of a 500 error so that a JSon response will be provided if the accept
    header of the request has a value of "application/json". Otherwise the default server error implementation is
    called.

    To enable this handler, the DEBUG setting in the Django settings must be set to False
    :param request: Current Request
    :type request: WSGIRequest
    :param template_name: Template of the error page
    :type template_name: str
    :return: Response
    :rtype: object
    """
    if request is not None and 'application/json' in request.META.get('HTTP_ACCEPT', ''):
        logger.error("Unhandled exception!")
        j_send = JSend()
        j_send.status = JSend.Status.error
        j_send.code = status.HTTP_500_INTERNAL_SERVER_ERROR
        j_send.message = 'Unexpected API Server Error'
        j_send_serializer = JSendSerializer(data = j_send.__dict__)
        j_send_serializer.is_valid(True)
        return JsonResponse(j_send_serializer.data, status = status.HTTP_500_INTERNAL_SERVER_ERROR)
    return server_error(request = request, template_name = template_name)


def handler404(request, template_name = '404.html'):
    """
    Overrides the default Django implementation of a 404 error so that a JSon response will be provided if the accept
    header of the request has a value of "application/json". Otherwise the default server error implementation is
    called.

    To enable this handler, the DEBUG setting in the Django settings must be set to False
    :param request: Current Request
    :type request: WSGIRequest
    :param template_name: Template of the error page
    :type template_name: str
    :return: Response
    :rtype: object
    """
    if 'application/json' in request.META.get('HTTP_ACCEPT', ''):
        j_send = JSend()
        j_send.status = JSend.Status.error
        j_send.code = status.HTTP_404_NOT_FOUND
        j_send.message = 'Not found'
        j_send_serializer = JSendSerializer(data = j_send.__dict__)
        j_send_serializer.is_valid(True)
        return JsonResponse(j_send_serializer.data, status = j_send.code)
    return page_not_found(request, template_name)
