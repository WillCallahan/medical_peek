import logging
from typing import List

from django.core.files import File
from pdf2image import convert_from_bytes
from core.utility.file_utility import get_extension
from core.aws.textract import extract_tables_from_byte_array

logger = logging.getLogger(__name__)


EXTENSION_PDF = {
    '.pdf'
}

EXTENSION_JPEG = {
    '.jpg',
    '.jpeg'
}

EXTENSION_PNG = {
    '.png'
}

ALLOWED_EXTENSIONS = EXTENSION_JPEG | EXTENSION_PDF | EXTENSION_PNG


def extract_tables_from_file(file_field: File) -> List[List]:
    file_extension = get_extension(file_field.name)
    if file_extension not in ALLOWED_EXTENSIONS:
        raise ValueError(f'File extension not supported  file_extension={file_extension}')
    if file_extension in EXTENSION_JPEG or file_extension in EXTENSION_PNG:
        contents = file_field.read()
        return extract_tables_from_byte_array(contents)
    elif file_extension in EXTENSION_PDF:
        contents = file_field.read()
        images = convert_from_bytes(contents)
        return extract_tables_from_byte_array(images)
    else:
        raise NotImplementedError(f'File extension extraction not implemented  file_extension={file_extension}')
