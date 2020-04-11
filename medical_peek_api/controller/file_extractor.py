import logging
import uuid
import re

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
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (SessionAuthentication, TokenAuthentication,)

    @classmethod
    def cleanup_file_name(cls, file_name: str) -> str:
        pattern = re.compile(r'[^\w\.]')
        new_file_name = re.sub(pattern, '', file_name)
        return new_file_name

    @classmethod
    def save_files(cls, request, title, description):
        file_uuid = uuid.uuid1()
        for i, file_name in enumerate(request.FILES):
            file_extractor = FileExtractor()
            file_extractor.title = title
            file_extractor.description = description
            file_extractor.group_uuid = file_uuid
            file_extractor.file = request.FILES[file_name]
            file_extractor.file_name = cls.cleanup_file_name(request.FILES[file_name].name)
            file_extractor.mime_type = request.FILES[file_name].content_type
            file_extractor.save()

    @response_body
    def post(self, request, format = None):
        logger.info('Uploading a new file...')
        title = request.data.get('title', None)
        description = request.data.get('description', None)
        logger.debug(f'Got file information  title={title} description={description}')
        self.save_files(request, title, description)
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
