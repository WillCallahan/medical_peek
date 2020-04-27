import json
import logging
import boto3
from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth


logger = logging.getLogger(__name__)


def get_client(hosts, region = 'us-east-1'):
    credentials = boto3.Session().get_credentials()
    auth = AWS4Auth(credentials.access_key, credentials.secret_key, region, 'es', session_token = credentials.token)
    client = Elasticsearch(
        hosts = hosts,
        http_auth = auth,
        use_ssl = True,
        verify_certs = True,
        connection_class = RequestsHttpConnection
    )
    return client


def store_doc(hosts, index, body, identity = None, region = 'us-east-1'):
    client = get_client(hosts, region)
    return client.index(index = index, id = identity, body = body)


def delete_doc(hosts, index, identifier, region = 'us-east-1'):
    client = get_client(hosts, region)
    return client.delete(index = index, id = identifier)


def create_index(hosts, index, region = 'us-east-1'):
    client = get_client(hosts, region)
    client.indices.create(index = index, ignore = 400)
