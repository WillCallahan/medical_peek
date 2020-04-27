import logging
from typing import Callable, List

import requests


logger = logging.getLogger(__name__)


def _build_product_url(base_url: str, product_id: int):
    return f'{base_url.rstrip("/")}/{product_id:07}'


def scrape_product(base_url, product_id):
    product_url = _build_product_url(base_url, product_id)
    logger.debug(f'Extracting product information for "{product_url}"')
    response = requests.get(product_url)  # type: requests.Response
    response_text = response.text
    return product_url, response_text


def scrape_all_products_lazy(base_url, min_product_id, max_product_id) -> List[Callable]:
    for product_id in range(min_product_id, max_product_id):
        yield scrape_product(base_url, product_id)
