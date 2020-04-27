import logging
from multiprocessing import Pool

from medical_peek_core.utility.functional import thread_first, first, second, log, partition
from medical_peek_scrapper import settings
from medical_peek_scrapper.etl.es_loader import load_to_django_store
from medical_peek_scrapper.etl.html_transformer import is_valid_product
from medical_peek_scrapper.etl.http_extractor import scrape_product_thread_safe_single_arg

logger = logging.getLogger(__name__)


def persist_products(product_partition):
    return thread_first(
        product_partition,
        (map, scrape_product_thread_safe_single_arg,),
        (filter, lambda v: is_valid_product(second(v)),),
        (map, lambda v: load_to_django_store(first(v), second(v)),),
        (list,),
    )


def main(*args):
    logger.info('Creating thread pool')
    min_product_id = settings.MIN_PRODUCT_ID
    max_product_id = settings.MAX_PRODUCT_ID
    partition_size = int((max_product_id - min_product_id) / settings.PARALLEL_MAX_THREADS)
    pool = Pool(settings.PARALLEL_MAX_THREADS)
    thread_first(
        range(min_product_id, max_product_id),
        (map, lambda i: (settings.SCRAPE_URL, i,),),
        (list,),
        (partition, partition_size,),
        (log, logging.INFO, 'Persisting scrapper results',),
        (pool.map, persist_products,),
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
