import logging
from typing import Callable, List

import requests
from urllib3 import PoolManager

from medical_peek_core.decorator.exceptions import ignore_errors

logger = logging.getLogger(__name__)


def _build_product_url(base_url: str, product_id: int):
    return f'{base_url.rstrip("/")}/{product_id:07}'


def scrape_product(base_url, product_id):
    product_url = _build_product_url(base_url, product_id)
    logger.debug(f'Extracting product information for "{product_url}"')
    response = requests.get(product_url)  # type: requests.Response
    response_text = response.text
    return product_url, response_text


def scrape_product_lazy(base_url, product_id):
    def _scrape_product_lazy():
        return scrape_product(base_url, product_id)

    return _scrape_product_lazy


def scrape_all_products_lazy(base_url: str, min_product_id: int, max_product_id: int) -> List[Callable]:
    logger.info(f'Getting products  min_product_id={min_product_id} max_product_id={max_product_id}')
    for product_id in range(min_product_id, max_product_id):
        yield scrape_product_lazy(base_url, product_id)


def scrape_product_thread_safe(base_url, product_id):
    product_url = _build_product_url(base_url, product_id)
    logger.debug(f'Extracting product information for "{product_url}"')
    pool = PoolManager()
    response = pool.request('GET', product_url)
    response_text = response.data
    return product_url, response_text


@ignore_errors
def scrape_product_thread_safe_single_arg(args):
    base_url, product_id = args
    return scrape_product_thread_safe(base_url, product_id)
