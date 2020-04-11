import logging

from django.conf.urls import url
from rest_framework import permissions
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.parsers import FileUploadParser, FormParser, MultiPartParser
from rest_framework.views import APIView

from core.service.response_entity import ResponseEntity
from core.decorator.response_body import response_body
from medical_peek_api.model.dmo.file_extractor import FileExtractor, FileExtractorSerializer

logger = logging.getLogger(__name__)


class FileExtractorUploadController(APIView):
    """
    Controller for uploading files
    """
    queryset = FileExtractor.objects.all()
    serializer_class = FileExtractorSerializer
    parser_classes = (MultiPartParser, FormParser, FileUploadParser)
    permission_classes = (permissions.DjangoObjectPermissions,)
    authentication_classes = (SessionAuthentication, TokenAuthentication,)

    @response_body
    def post(self, request):
        logger.info('Uploading a new file...')
        logger.debug(f'File Category: {request.META.get("HTTP_CATEGORY")}')
        file_extractor = FileExtractor()
        file_extractor.file = request.FILES['file']
        file_extractor.file_name = request.FILES['file'].name.replace(' ', '_')
        file_extractor.mime_type = request.FILES['file'].content_type
        file_extractor.category = request.META.get('HTTP_CATEGORY')
        file_extractor.save()
        return ResponseEntity('Successfully uploaded file!', status_code = status.HTTP_200_OK)

    def __get_urls(self, prefix = r'file-upload/?'):
        url_patterns = [
            url(regex = rf'{prefix}', view = FileExtractorUploadController.as_view()),
        ]
        return url_patterns

    @property
    def urls(self):
        return self.__get_urls()


file_extractor_upload_controller = FileExtractorUploadController()
