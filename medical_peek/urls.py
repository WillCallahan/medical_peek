"""medical_peek URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from rest_framework import routers
from medical_peek.model.dmo.user import UserViewSet
# from medical_peek.controller.basic_file import basic_file_upload_controller
from medical_peek.controller.medical_item import medical_item_detail, medical_item_list

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    # url(r'^', include(basic_file_upload_controller.urls)),
    url(r'^', include(medical_item_detail.urls)),
    url(r'^', include(medical_item_list.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace = 'rest_framework'))
]
