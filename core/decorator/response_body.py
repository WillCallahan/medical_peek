import json
import logging

from django.core import serializers
from django.http import HttpResponse

from core.exceptions.types import UnexpectedTypeError
from core.service.response_entity import ResponseEntity

logger = logging.getLogger(__name__)


def response_body(func):
    """
    Decorator function used to serialize output from functions
    and place the serialized object into an HttpResponse Object
    :param func: function being decorated
    :return: HttpResponse containing deserialized object
    """

    def response_body_wrapper(response):
        logger.debug("Deserializing object...")
        output = func(response)
        if type(output) in (int, float, bool, str):
            return HttpResponse(output)
        elif isinstance(output, ResponseEntity):
            if output.obj is None:
                return HttpResponse(status = output.status_code, content_type = output.content_type)
            elif type(output.obj) in (int, float, bool, str):
                return HttpResponse(output.obj, status = output.status_code, content_type = output.content_type)
            raw_data = serializers.serialize('python', output.obj)
            actual_data = [dict(obj['fields'], **{'id': obj['pk']}) for obj in raw_data]
            return HttpResponse(json.dumps(actual_data), status = output.status_code,
                                content_type = output.content_type)
        else:
            raise UnexpectedTypeError((ResponseEntity, str, int, float, bool, str), output)

    return response_body_wrapper
