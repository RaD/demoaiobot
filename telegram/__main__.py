import asyncio

import aiogram

from . import settings
from .tools import logger as logging
from .handlers import dispatcher

params = None
logger = logging.get_logger(__name__)
logger.info(settings.TITLE)
logger.info(f'SOURCE_VERSION is "{settings.VERSION}".')
logger.info(f'SOURCE_COMMIT is "{settings.COMMIT}".')
logger.info(f'TOKEN is "{settings.TOKEN}".')

try:
    loop = asyncio.get_event_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)


def main():
    try:
        aiogram.executor.start_polling(dispatcher, skip_updates=True)
    except asyncio.TimeoutError:
        logger.warning('Telegram service timeout detected')


if __name__ == '__main__':
    main()
