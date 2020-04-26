import logging
from medical_peek_scrapper import settings
from medical_peek_scrapper.etl.http_extractor import scrape_product
from medical_peek_scrapper.etl.http_transformer import transform_product


logger = logging.getLogger(__name__)


def main(*args):
    product_html = scrape_product(settings.SCRAPE_URL, 1028127)
    product = transform_product(product_html)
    return product


if __name__ == '__main__':
    main()
