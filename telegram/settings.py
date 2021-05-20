from datetime import datetime, timedelta
from typing import List, Tuple, Union

from environs import Env

env: Env = Env()
env.read_env()  # read .env file, if it exists


TITLE = """Demo Telegram Bot"""

DEBUG = env.bool('DEBUG', False)
PRODUCTION = env.bool('PRODUCTION', False)
TOKEN = env.str('TELEGRAM_TOKEN', '')
TIMEZONE = env.str('TZ', 'Europe/Moscow')
DATETIME_FORMAT = env.str('DATETIME_FORMAT', '%Y-%m-%dT%H:%M:%S.%f%z')
COMMIT = env.str('SOURCE_COMMIT', 'Unknown')
VERSION = env.str('SOURCE_VERSION', 'Unknown')
STARTED_IN = datetime.utcnow()

MANAGERS = ()
SUPPORTS = ()
