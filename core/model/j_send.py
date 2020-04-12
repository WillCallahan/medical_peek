from rest_framework import serializers

from core.service.generic_serializers import ListOrDictField


class Link:
    def __init__(self, reference = None, resource_url = None,):
        """
        Creates a link to a resource

        :param reference: Reference to the primary key of the related object
        :type reference: str|int
        :param resource_url: URL of the resource
        :type resource_url: str
        """
        self.reference = reference
        self.resource_url = resource_url


class LinkSerializer(serializers.Serializer):
    reference = serializers.CharField(max_length = 2083, required = False, allow_null = True, allow_blank = True)
    resource_url = serializers.CharField(max_length = 2083, required = False, allow_null = True, allow_blank = True)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class JSend:
    """
    Represents a response object from a server implementing a flavor of the JSend standard
    See: https://labs.omniti.com/labs/jsend
    """

    class Status(object):
        error = "error"
        success = "success"

    def __init__(self, status = None, message = None, data = None, code = None, links = None):
        """

        :param status:
        :type status: str
        :param message:
        :type message: str
        :param data:
        :type data: object
        :param code:
        :type code: int
        :param links: Collection of Links
        :type links: list[Link]
        """
        self.status = status
        self.message = message
        if data is None:
            self.data = dict()
        else:
            self.data = data
        self.code = code
        if links is None:
            self.links = list()
        else:
            self.links = links


class JSendSerializer(serializers.Serializer):
    status = serializers.CharField(max_length = 255, required = False, allow_null = True)
    message = serializers.CharField(max_length = 50000, required = False, allow_null = True, allow_blank = True)
    data = ListOrDictField(required = False, allow_null = True)
    code = serializers.IntegerField(required = False, allow_null = True)
    links = LinkSerializer(required = False, allow_null = True, many = True)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass
