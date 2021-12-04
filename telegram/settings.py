import random
import string
from collections import namedtuple
from datetime import datetime
from typing import Dict, List, Optional

import password as password
from environs import Env
from loguru import logger

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
PARAMS = None


def password(symbols, length):
    return ''.join(random.sample(symbols, length))


def password_easy():
    return password(string.digits, 4)


def password_middle():
    return password(string.ascii_letters + string.digits, 16)


def password_hard():
    return password(string.ascii_letters + string.digits, 32)


ROW = namedtuple('ROW', 'buttons')
BUTTON = namedtuple('BUTTON', 'title target command value')

ACTION_MAPPING = [
    ROW([
        BUTTON('Лёгкий', 'user', 'password', 'easy'),
        BUTTON('Средний', 'user', 'password', 'middle'),
        BUTTON('Сложный', 'user', 'password', 'hard'),
        ]),
    ]

HANDLER_MAPPING = {
    'easy': password_easy,
    'middle': password_middle,
    'hard': password_hard,
    }


def admin_required(message) -> bool:
    admin_id = PARAMS.admin
    user_id = message.from_user.id
    logger.debug(f'User ID: {user_id}')
    return admin_id is not None and user_id == admin_id


class MappingException(Exception):
    pass


def mapping_add(rows: List[List[Dict]]):
    if not isinstance(rows, list):
        raise MappingException(f'Mapping: Rows are not found')

    for row in rows:
        if not isinstance(row, list):
            raise MappingException(f'Mapping: Buttons are not found')

        try:
            buttons = [BUTTON(*(o['title'], 'admin', o['command'], o['value']))
                       for o in row]
        except Exception:
            raise MappingException(f'Mapping: Wrong button format')

        ACTION_MAPPING.append(ROW(buttons))
