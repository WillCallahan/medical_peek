import logging
import boto3
import base64
import json

logger = logging.getLogger(__name__)


def get_secret_kvp(secret_name: str) -> dict:
    session = boto3.session.Session()
    client = session.client(service_name = 'secretsmanager')

    logger.debug(f'Getting secret from SSM  secret_name={secret_name}')

    get_secret_value_response = client.get_secret_value(
        SecretId = secret_name
    )
    if 'SecretString' in get_secret_value_response:
        secret = get_secret_value_response['SecretString']
        logger.debug('Extracting secret string from SSM response')
    else:
        secret = base64.b64decode(get_secret_value_response['SecretBinary'])
        logger.debug('Extracting binary string from SSM response')

    logger.debug('Converting secret to a dict')
    kvp = json.loads(secret)
    return kvp
