import json

from medical_peek_core.aws.es import store_doc


def load_to_elastic_search(hosts, product):
    store_doc(hosts, 'mckesson-product', json.dumps(vars(product)))
