"""medical_peek_api URL Configuration

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
from medical_peek_core.model.dmo.user import UserViewSet
from medical_peek_core.model.dmo.medical_item import MedicalItem
from medical_peek_core.model.dmo.medical_resource import MedicalResource
from medical_peek_api.controller.file_extractor import file_extractor_upload_controller
from medical_peek_api.controller.medical_item import medical_item_detail, medical_item_list
from medical_peek_api.controller.medical_resource import medical_resource_detail, medical_resource_list
from django.contrib import admin
from rest_framework_swagger.views import get_swagger_view

# Admin models
admin.site.site_header = 'Medical Peek Admin'
admin.site.site_title = 'Medical Peek Portal'
admin.site.index_title = 'Medical Peek'

admin.site.register(MedicalItem)
admin.site.register(MedicalResource)

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

# Swagger
schema_view = get_swagger_view(title = 'Medical Peek API')

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^$', schema_view),
    url(r'^', include(router.urls)),
    url(r'^', include(file_extractor_upload_controller.urls)),
    url(r'^', include(medical_item_detail.urls)),
    url(r'^', include(medical_item_list.urls)),
    url(r'^', include(medical_resource_detail.urls)),
    url(r'^', include(medical_resource_list.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace = 'rest_framework')),
    url('admin/', admin.site.urls),
]
