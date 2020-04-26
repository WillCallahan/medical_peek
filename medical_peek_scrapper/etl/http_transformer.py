import logging
from html.parser import HTMLParser
from typing import List

from core.utility.functional import thread_first, single, first, second

logger = logging.getLogger(__name__)


class MckessonProductHtmlParser(HTMLParser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title = []
        self.invoice_title = []
        self.description = []
        self.product_id = []
        self.features = []
        self.specifications = []
        self.more_information = []
        self._record_fields = []
        self._record_attrs = []
        self._record_tags = []

    @classmethod
    def _attr_equals(cls, attrs, key, value):
        return single(lambda o: first(o) == key and second(o) == value, attrs)

    @classmethod
    def _attr_contains(cls, attrs, key, value):
        if not attrs or len(attrs) < 1:
            return False
        return single(lambda o: first(o) == key and value in second(o), attrs)

    def _attr_stack_contains(self, attrs_stack, key, value):
        return thread_first(
            attrs_stack,
            (map, (lambda a: self._attr_contains(a, key, value)),),
            (single, (lambda t: t),)
        )

    def _has_product_id(self, tag, attrs):
        has_tag = tag == 'li'
        has_attr = self._attr_equals(attrs, 'class', 'product-header-id')
        stack_does_not_have_pop_attr = not self._attr_stack_contains(self._record_attrs, 'id', 'popularSuggest')
        stack_does_not_have_rec_attr = not self._attr_stack_contains(self._record_attrs, 'class', 'recommended')
        return has_tag and has_attr and stack_does_not_have_pop_attr and stack_does_not_have_rec_attr

    def _has_invoice_title(self, tag, attrs):
        has_tag = tag == 'li'
        inside_ul = first(self._record_tags) == 'ul'
        has_no_attr = len(self._record_attrs) > 1
        parent_has_class = not self._attr_contains(first(self._record_attrs), 'class', 'product-header')
        stack_does_not_have_pop_attr = not self._attr_stack_contains(self._record_attrs, 'id', 'popularSuggest')
        stack_does_not_have_rec_attr = not self._attr_stack_contains(self._record_attrs, 'class', 'recommended')
        return has_tag \
            and inside_ul \
            and has_no_attr \
            and parent_has_class \
            and stack_does_not_have_pop_attr \
            and stack_does_not_have_rec_attr

    def handle_starttag(self, tag, attrs):
        if self._has_product_id(tag, attrs):
            self._record_fields.insert(0, 'product_id')
            self._record_tags.insert(0, tag)
            self._record_attrs.insert(0, attrs)
        elif self._has_invoice_title(tag, attrs):
            self._record_fields.insert(0, 'invoice_title')
            self._record_tags.insert(0, tag)
            self._record_attrs.insert(0, attrs)
        else:
            self._record_fields.insert(0, None)
            self._record_tags.insert(0, tag)
            self._record_attrs.insert(0, attrs)

    def handle_endtag(self, tag):
        self._record_fields.pop(0)
        self._record_tags.pop(0)
        self._record_attrs.pop(0)

    def handle_data(self, data):
        if self._record_fields and first(self._record_fields):
            field_data = getattr(self, first(self._record_fields))  # type: List
            field_data.append(data)
            setattr(self, first(self._record_fields), field_data)

    def error(self, message):
        logger.error('Failed to parse HTML', message)


def is_valid_product(response_text: str):
    return 'product is no longer available' not in str(response_text)


def transform_product(response_text: str):
    parser = MckessonProductHtmlParser()
    parser.feed(response_text)
    return parser


def filter_products(product_texts: List[str]):
    return thread_first(
        product_texts,
        (filter, is_valid_product,),
        (transform_product,)
    )
