import io
import logging
import multiprocessing

from typing import List
from PIL import Image

from django.core.files import File
from pdf2image import convert_from_bytes
from medical_peek_core.utility.file_utility import get_extension
from medical_peek_core.aws.textract import extract_tables_from_byte_array
from medical_peek_core.utility.functional import thread_first, flatten, log_message

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


def __convert_pil_to_format(pil, fmt = 'jpeg'):
    image = Image.open(pil.fp, mode = 'r')
    image_byte_array = io.BytesIO()
    image.save(image_byte_array, format = fmt)
    image_byte_array = image_byte_array.getvalue()
    return image_byte_array


def extract_tables_from_file(file_field: File) -> List[List]:
    file_extension = get_extension(file_field.name)
    if file_extension not in ALLOWED_EXTENSIONS:
        raise ValueError(f'File extension not supported  file_extension={file_extension}')
    if file_extension in EXTENSION_JPEG or file_extension in EXTENSION_PNG:
        contents = file_field.read()
        return extract_tables_from_byte_array(contents)
    elif file_extension in EXTENSION_PDF:
        contents = file_field.read()
        thread_pool = multiprocessing.Pool(maxtasksperchild = 4)
        tables = thread_first(
            convert_from_bytes(contents, fmt = 'jpeg'),
            (log_message, logging.INFO, 'Converted PDFs into images',),
            (map, lambda f: f.fp.getvalue(),),
            (lambda i: thread_pool.map(extract_tables_from_byte_array, i),),
            # (map, extract_tables_from_byte_array,),
            (flatten,),
            (list,),
        )
        return tables
    else:
        raise NotImplementedError(f'File extension extraction not implemented  file_extension={file_extension}')
