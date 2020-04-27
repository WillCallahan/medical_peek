import logging
import os
from medical_peek_core.aws.ssm import get_secret_kvp
from medical_peek_core.utility.functional import rename_keys

logger = logging.getLogger(__name__)


def get_database_connection_string(connection_file_path, ssm_parameter_name):
    """
    Gets Django Database connection parameters

    If the connection_file_name is found on the local path, then the file is used. If the file is not found, the
    credentials will be retrieved from AWS SSM.

    :param connection_file_path: Path to the Django connection definition
    :param ssm_parameter_name: AWS SSM Secret Name
    :return: Database connection information
    """
    logging.info(f'Attempting to get database connection from path  connection_file_path={connection_file_path}')
    path_exists = os.path.exists(connection_file_path)
    if path_exists:
        logging.info('Found database connection info in path')
        return {
            'OPTIONS': {
                'read_default_file': connection_file_path
            }
        }

    logger.info('Database connection info not found in path')
    logger.info(f'Searching AWS SSM for database connection  ssm_parameter_name={ssm_parameter_name}')
    raw_connection_params = get_secret_kvp(ssm_parameter_name)
    connection_params = rename_keys(raw_connection_params, lambda k: str(k).upper())
    logger.info('Found database connection info in AWS SSM')
    return connection_params
