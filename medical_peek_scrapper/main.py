import json
import logging

from medical_peek_core.aws.es import create_index, store_doc
from medical_peek_scrapper import settings
from medical_peek_scrapper.etl.http_extractor import scrape_product
from medical_peek_scrapper.etl.html_transformer import transform_product, MckessonProduct

logger = logging.getLogger(__name__)


def main(*args):
    product_html = scrape_product(settings.SCRAPE_URL, 1028127)
    product = transform_product(product_html)
    # create_index(settings.ES_HOSTS, 'mckesson-product')
    # store_doc(settings.ES_HOSTS, 'mckesson-product', json.dumps(vars(product)))
    return product


if __name__ == '__main__':
    main()
