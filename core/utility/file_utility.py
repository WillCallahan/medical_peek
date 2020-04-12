import logging
import os

logger = logging.getLogger(__name__)


def get_extension(file_name) -> str:
    name, extension = os.path.splitext(file_name)
    return extension


def get_files_in_request(request):
    files = []
    for i, file_name in enumerate(request.FILES):
        files.append(request.FILES.get(file_name, None))
    return files
