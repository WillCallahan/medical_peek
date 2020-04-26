import logging
import requests


logger = logging.getLogger(__name__)


def _build_product_url(base_url: str, product_id: int):
    return f'{base_url.rstrip("/")}/{product_id:06}'


def scrape_product(base_url, product_id):
    response = requests.get(_build_product_url(base_url, product_id))  # type: requests.Response
    response_text = response.text
    return response_text


def scrape_all_products(base_url):
    product_ids = range(1, 200000)
    responses = [scrape_product(base_url, product_id) for product_id in product_ids]
    return responses
