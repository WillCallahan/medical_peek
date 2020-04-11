from django.conf.urls import url
from rest_framework import permissions
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.generics import ListAPIView, RetrieveAPIView

from core.service.url import UrlProperty
from medical_peek.model.dmo.medical_item import MedicalItem, MedicalItemSerializer


class MedicalItemDetail(RetrieveAPIView, UrlProperty):
    """
    Detailed Medical Item Information
    """

    queryset = MedicalItem.objects.all()
    serializer_class = MedicalItemSerializer
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)
    authentication_classes = (SessionAuthentication, TokenAuthentication,)

    def __get_urls(self, prefix = r'medical-item/'):
        url_patterns = [
            url(regex = prefix + r'(?P<pk>[0-9]+)/?$', view = MedicalItemDetail.as_view()),
        ]
        return url_patterns

    @property
    def urls(self):
        return self.__get_urls()


class MedicalItemList(ListAPIView, UrlProperty):
    """
    All Detailed Medical Item Information
    """

    queryset = MedicalItem.objects.all()
    serializer_class = MedicalItemSerializer
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)
    authentication_classes = (SessionAuthentication, TokenAuthentication,)

    def __get_urls(self, prefix = r'medical-item/?'):
        url_patterns = [
            url(regex = rf'{prefix}$', view = MedicalItemList.as_view()),
        ]
        return url_patterns

    @property
    def urls(self):
        return self.__get_urls()


medical_item_detail = MedicalItemDetail()
medical_item_list = MedicalItemList()
