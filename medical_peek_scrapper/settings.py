import os


SCRAPE_URL = 'https://mms.mckesson.com/product'

MIN_PRODUCT_ID = int(os.environ.get('MIN_PRODUCT_ID', 1024361))
MAX_PRODUCT_ID = int(os.environ.get('MAX_PRODUCT_ID', 1050000))

ES_HOSTS = [
    {
        'host': 'vpc-medical-peek-test-uh6v7oq4a4xh63gil64tr3vzkq.us-east-1.es.amazonaws.com',
        'port': 443
    }
]

PARALLEL_MAX_THREADS = 15
