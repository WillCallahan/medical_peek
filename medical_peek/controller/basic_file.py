import logging

from django.conf.urls import url
from rest_framework import permissions
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.parsers import FileUploadParser, FormParser, MultiPartParser
from rest_framework.views import APIView

from core.service.response_entity import ResponseEntity
from core.decorator.response_body import response_body
from medical_peek.model.dmo.basic_file import BasicFile, BasicFileSerializer

log = logging.getLogger(__name__)


class BasicFileUploadController(APIView):
    """
    Controller for uploading files
    """
    queryset = BasicFile.objects.all()
    serializer_class = BasicFileSerializer
    parser_classes = (MultiPartParser, FormParser, FileUploadParser)

    @staticmethod
    @response_body
    def post(request):
        log.info("Uploading a new file...")
        log.debug("File Category: " + request.META.get('HTTP_CATEGORY'))
        basic_file = BasicFile()
        basic_file.file = request.FILES['file']
        basic_file.file_name = request.FILES['file'].name.replace(" ", "_")
        basic_file.mime_type = request.FILES['file'].content_type
        basic_file.category = request.META.get('HTTP_CATEGORY')
        basic_file.save()
        return ResponseEntity("Successfully uploaded file!", status_code = status.HTTP_200_OK)

    def __get_urls(self, prefix = r'file-upload/?'):
        url_patterns = [
            url(regex = prefix + r'', view = BasicFileUploadController.as_view()),
        ]
        return url_patterns

    @property
    def urls(self):
        return self.__get_urls()


basic_file_upload_controller = BasicFileUploadController()
