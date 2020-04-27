import logging
import json

from medical_peek_core.aws.es import store_doc
from medical_peek_core.model.dmo.medical_resource import MedicalResource


logger = logging.getLogger(__name__)


def load_to_elastic_search(hosts, product):
    store_doc(hosts, 'mckesson-product', json.dumps(vars(product)))


def load_to_django_store(product_url, product_html):
    logger.info(f'Persisting product  product_url={product_url}')
    medical_resource = MedicalResource(
        description = product_url,
        content = product_html,
        link = product_url
    )
    medical_resource.save()
    return medical_resource
