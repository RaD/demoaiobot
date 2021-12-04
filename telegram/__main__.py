import asyncio
from argparse import ArgumentParser

import aiogram
import required as required
from loguru import logger

from . import settings
from .handlers import dispatcher

params = None
logger.info(settings.TITLE)
logger.info(f'SOURCE_VERSION is "{settings.VERSION}".')
logger.info(f'SOURCE_COMMIT is "{settings.COMMIT}".')
logger.debug(f'TOKEN is "{settings.TOKEN}".')


def read_args():
    parser = ArgumentParser(description=settings.TITLE)
    parser.add_argument(
        '--admin', required=False, type=int, help='Telegram ID of admin')
    return parser.parse_args()


def main():
    try:
        aiogram.executor.start_polling(dispatcher, skip_updates=True)
    except asyncio.TimeoutError:
        logger.warning('Telegram service timeout detected')


if __name__ == '__main__':
    params = read_args()
    settings.PARAMS = params
    if params.admin:
        logger.debug(f'Admin ID is {params.admin}')
    main()
