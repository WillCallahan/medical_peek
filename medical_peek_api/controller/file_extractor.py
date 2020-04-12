import logging
import re
import uuid

from django.conf.urls import url
from rest_framework import permissions
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.parsers import FileUploadParser, FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from core.model.j_send import JSend
from core.service.generic_extractor import extract_tables_from_file
from core.utility.functional import thread_first
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
    def _build_file_name(cls, file_name: str, file_uuid: uuid) -> str:
        pattern = re.compile(r'[^\w\.]')
        file_pass_1 = str(file_name).replace(' ', '_')
        file_pass_2 = re.sub(pattern, '', file_pass_1)
        new_file_name = f'{file_uuid}-{file_pass_2}'
        return new_file_name

    @classmethod
    def _save_files(cls, request, title, description):
        files = []
        file_uuid = uuid.uuid1()
        for i, form_field in enumerate(request.FILES):
            file = request.FILES[form_field]
            actual_file_name = file.name
            file.name = cls._build_file_name(actual_file_name, file_uuid)
            file_extractor = FileExtractor()
            file_extractor.title = title
            file_extractor.description = description
            file_extractor.group_uuid = file_uuid
            file_extractor.file = file
            file_extractor.file_name = actual_file_name
            file_extractor.mime_type = request.FILES[form_field].content_type
            file_extractor.save()
            files.append(file_extractor)
        return files

    def post(self, request, format = None):
        logger.info('Uploading a new file...')
        title = request.data.get('title', None)
        description = request.data.get('description', None)
        logger.debug(f'Got file information  title={title} description={description}')
        extraction_results = thread_first(
            self._save_files(request, title, description),
            (map, lambda f: f.file.file,),
            (map, extract_tables_from_file,),
            (list,),
        )
        return Response(
            JSend(
                message = 'Successfully uploaded file(s)!',
                data = extraction_results,
                status = status.HTTP_201_CREATED,
                links = []
            ),
            status = status.HTTP_201_CREATED
        )

    def __get_urls(self, prefix = r'file-upload/?'):
        url_patterns = [
            url(regex = rf'{prefix}', view = FileExtractorUploadController.as_view()),
        ]
        return url_patterns

    @property
    def urls(self):
        return self.__get_urls()


file_extractor_upload_controller = FileExtractorUploadController()
