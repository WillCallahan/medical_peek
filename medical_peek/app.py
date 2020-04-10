import os
import sys
import logging

from django.core.management import execute_from_command_line


if __name__ == '__main__':
    # Set up structured logging
    logging.basicConfig(
        format = '%(message)s\n',
        stream = sys.stdout,
        level = logging.DEBUG,
    )

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
    execute_from_command_line(sys.argv)
