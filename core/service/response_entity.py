from django.core import serializers
from rest_framework import status


class ResponseEntity:
    __format = "json"

    def __init__(self, obj, headers = None, status_code = status.HTTP_200_OK, content_type = "application/json"):
        self.__obj = obj
        self.headers = headers
        self.status_code = status_code
        self.content_type = content_type

    def __str__(self):
        return serializers.serialize(self.__format, self.obj)

    @property
    def obj(self):
        if isinstance(self.__obj, (int, str, bool, float)):
            return '{"response":"' + self.__obj + '"}'
        return self.__obj
