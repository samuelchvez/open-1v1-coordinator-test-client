import os
import argparse
import json

from utils import logger
from utils.configurations_manager import ConfigurationsManager
from utils.configure_requests import configure_requests_logging
from home import menu as home_menu


parser = argparse.ArgumentParser(
    description='Tournament coordinator test client'
)

parser.add_argument(
    '--config',
    dest='config',
    metavar='C',
    type=str,
    nargs=1,
    help='Configuration file'
)

# Make requests verbose
if os.getenv('OPEN_1V1_STAGE') == 'DEBUG':
    configure_requests_logging()

args = parser.parse_args()
with open(args.config[0]) as f:
    data = json.load(f)
    configurations_manager = ConfigurationsManager(data)

    home_menu.start()

    print(logger.log_title("Bye!"))
