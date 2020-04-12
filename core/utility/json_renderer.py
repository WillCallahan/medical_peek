from djangorestframework_camel_case.render import CamelCaseJSONRenderer
from djangorestframework_camel_case.util import camelize
from rest_framework import status
from rest_framework.renderers import JSONRenderer

from core.model.j_send import JSend, JSendSerializer
from core.utility.j_send_utility import JSendUtility


class JSendJsonRenderer(JSONRenderer):
    def render(self, data, *args, **kwargs):
        status_code = status.HTTP_200_OK
        if args[1] is not None \
                and args[1].get("response", None) is not None \
                and (args[1].get("response", None).get('status_code', None) is not None
                     or hasattr(args[1].get("response", None), 'status_code')):
            status_code = args[1]["response"].status_code
        if not isinstance(data, JSend):
            j_send = JSend()
            j_send.status = JSendUtility.get_status_by_status_code(status_code)
            j_send.code = status_code
            j_send.data = data
            j_send_serializer = JSendSerializer(data = j_send.__dict__)
        else:
            if data.code is None:
                data.code = status_code
            if data.status is None:
                data.status = JSendUtility.get_status_by_status_code(status_code)
            j_send_serializer = JSendSerializer(data = data.__dict__)
        j_send_serializer.is_valid(True)
        return super(JSendJsonRenderer, self).render(j_send_serializer.data, *args, **kwargs)


class JSendCamelCaseJsonRenderer(CamelCaseJSONRenderer):
    def render(self, data, *args, **kwargs):
        status_code = status.HTTP_200_OK
        if args[1] is not None \
                and args[1].get("response", None) is not None \
                and (args[1].get("response", None).get('status_code', None) is not None
                     or hasattr(args[1].get("response", None), 'status_code')):
            status_code = args[1]["response"].status_code
        if not isinstance(data, JSend):
            j_send = JSend()
            j_send.status = JSendUtility.get_status_by_status_code(status_code)
            j_send.code = status_code
            j_send.data = data
            j_send_serializer = JSendSerializer(data = j_send.__dict__)
        else:
            if data.code is None:
                data.code = status_code
            if data.status is None:
                data.status = JSendUtility.get_status_by_status_code(status_code)
            j_send_serializer = JSendSerializer(data = data.__dict__)
        j_send_serializer.is_valid(True)
        return super(CamelCaseJSONRenderer, self).render(camelize(j_send_serializer.data), *args, **kwargs)
