from django.conf.urls import url
from rest_framework import permissions
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.generics import ListAPIView, RetrieveAPIView

from medical_peek_core.service.url import UrlProperty
from medical_peek_api.model.dmo.medical_resource import MedicalResource, MedicalResourceSerializer


class MedicalResourceDetail(RetrieveAPIView, UrlProperty):
    """
    Relationships to resources of medical information
    """

    queryset = MedicalResource.objects.all()
    serializer_class = MedicalResourceSerializer
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)
    authentication_classes = (SessionAuthentication, TokenAuthentication,)

    def __get_urls(self, prefix = r'medical-resource/'):
        url_patterns = [
            url(regex = prefix + r'(?P<pk>[0-9]+)/?$', view = MedicalResourceDetail.as_view()),
        ]
        return url_patterns

    @property
    def urls(self):
        return self.__get_urls()


class MedicalResourceList(ListAPIView, UrlProperty):
    """
    All relationships to resources of medical information
    """

    queryset = MedicalResource.objects.all()
    serializer_class = MedicalResourceSerializer
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)
    authentication_classes = (SessionAuthentication, TokenAuthentication,)

    def __get_urls(self, prefix = r'medical-resource/?'):
        url_patterns = [
            url(regex = rf'{prefix}$', view = MedicalResourceList.as_view()),
        ]
        return url_patterns

    @property
    def urls(self):
        return self.__get_urls()


medical_resource_detail = MedicalResourceDetail()
medical_resource_list = MedicalResourceList()
