import logging

from pyquery import PyQuery
from lxml import etree
from typing import List

from core.utility.functional import thread_first, join, partition, second, first
from medical_peek_scrapper.services.serializers import JObjectSerializer

logger = logging.getLogger(__name__)


class MckessonProduct(JObjectSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title = ''
        self.invoice_title = ''
        self.manufacturer_id = ''
        self.description = ''
        self.product_id = ''
        self.features = []
        self.specifications = []
        self.more_information = []


def get_product_id(py_query: PyQuery):
    matches = thread_first(
        py_query('div.page-content ul.product-header > li.product-header-id'),
        (lambda i: i.items(),),
        (filter, lambda t: not t.parents('.recommended')),
        (map, lambda t: t.text()),
        (list,),
        (join, ','),
    )
    return matches


def get_manufacturer_id(py_query: PyQuery):
    matches = thread_first(
        py_query('div.page-content ul.product-header > li:last-child'),
        (lambda i: i.items(),),
        (filter, lambda t: not t.parents('.recommended')),
        (map, lambda t: t.text()),
        (list,),
        (join, ','),
    )
    return matches


def get_product_features(py_query: PyQuery):
    matches = thread_first(
        py_query('#specifications ul.product-features > li'),
        (lambda i: i.items(),),
        (filter, lambda t: not t.parents('.recommended')),
        (map, lambda t: t.text()),
        (list,),
    )
    return matches


def get_product_title(py_query: PyQuery):
    matches = thread_first(
        py_query('h1.prod-title'),
        (lambda i: i.items(),),
        (filter, lambda t: not t.parents('.recommended')),
        (map, lambda t: t.text()),
        (list,),
    )
    return matches


def get_product_invoice_title(py_query: PyQuery):
    matches = thread_first(
        py_query('h1.prod-invoice-title'),
        (lambda i: i.items(),),
        (filter, lambda t: not t.parents('.recommended')),
        (map, lambda t: t.text()),
        (list,),
    )
    return matches


def get_specifications(py_query: PyQuery):
    matches = thread_first(
        py_query('#specifications table tr td'),
        (map, lambda t: t.text,),
        (list,),
        (partition, 2,),
        (map, lambda o: {'key': first(o), 'value': second(o)},),
        (list,),
    )
    return matches


def is_valid_product(response_text: str):
    return 'product is no longer available' not in str(response_text)


def transform_product(response_text: str):
    parser = etree.HTMLParser(recover = True, remove_blank_text = True)
    tree = etree.fromstring(response_text, parser = parser)
    py_query = PyQuery(tree)
    product = MckessonProduct()
    product.product_id = get_product_id(py_query)
    product.manufacturer_id = get_manufacturer_id(py_query)
    product.features = get_product_features(py_query)
    product.specifications = get_specifications(py_query)
    product.title = get_product_title(py_query)
    product.invoice_title = get_product_invoice_title(py_query)
    return product


def filter_products(product_texts: List[str]):
    return thread_first(
        product_texts,
        (filter, is_valid_product,),
        (transform_product,)
    )
