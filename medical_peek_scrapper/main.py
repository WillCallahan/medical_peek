import logging
import os

from multiprocessing import Pool
from medical_peek_core.utility.functional import thread_first, first, second, log
from medical_peek_scrapper import settings
from medical_peek_scrapper.etl.es_loader import load_to_elastic_search, load_to_django_store
from medical_peek_scrapper.etl.http_extractor import scrape_product, scrape_all_products_lazy
from medical_peek_scrapper.etl.html_transformer import transform_product, is_valid_product

logger = logging.getLogger(__name__)


def main(*args):
    logger.info('Creating thread pool')
    pool = Pool(settings.PARALLEL_MAX_THREADS)
    thread_first(
        scrape_all_products_lazy(settings.SCRAPE_URL, 1002982, 2000000),
        (log, logging.INFO, 'Persisting scrapper results',),
        (filter, lambda v: is_valid_product(second(v)),),
        (map, lambda v: load_to_django_store(first(v), second(v)),),
        (list,),
    )
    logger.info('Scrape complete')
    # product_url, product_html = scrape_product(settings.SCRAPE_URL, 1028127)
    # product = transform_product(product_html)
    # load_to_elastic_search(settings.ES_HOSTS, product)
    # load_to_django_store(product_url, product_html)
    # return product


if __name__ == '__main__':
    main()
