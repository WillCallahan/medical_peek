import logging
import os

from urllib3 import PoolManager
from multiprocessing import Pool
from medical_peek_core.utility.functional import thread_first, first, second, log
from medical_peek_scrapper import settings
from medical_peek_scrapper.etl.es_loader import load_to_elastic_search, load_to_django_store
from medical_peek_scrapper.etl.http_extractor import scrape_product, scrape_all_products_lazy, \
    scrape_all_products_thread_safe_lazy, scrape_product_thread_safe
from medical_peek_scrapper.etl.html_transformer import transform_product, is_valid_product

logger = logging.getLogger(__name__)


def main(*args):
    logger.info('Creating thread pool')
    http_pool = PoolManager(1)
    request_pool = Pool(int(settings.PARALLEL_MAX_THREADS / 2))
    store_pool = Pool(int(settings.PARALLEL_MAX_THREADS / 2))
    thread_first(
        (i for i in range(1002998, 1003000)),
        (request_pool.map, lambda i: scrape_product_thread_safe(settings.SCRAPE_URL, i, http_pool),),
        (log, logging.INFO, 'Persisting scrapper results',),
        (filter, lambda v: is_valid_product(second(v)),),
        (store_pool.map, lambda v: load_to_django_store(first(v), second(v)),),
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
