import asyncio
import json
from datetime import datetime
from functools import wraps
from typing import Union, Optional, Dict

import aiogram
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from loguru import logger

from . import commands, states
from . import keyboards
from . import messages
from . import settings

bot = aiogram.Bot(token=settings.TOKEN)
dispatcher = aiogram.Dispatcher(bot, storage=MemoryStorage())


def prefix_uri(msg: aiogram.types.Message) -> str:
    return f'{msg.from_user.id}@{msg.chat.id}'


def restart_on_exception(func):
    allowed_types = (aiogram.types.Message, aiogram.types.CallbackQuery)
    message = ('Хм, со времени нашей последней беседы меня обновили, '
               'появились новые возможности, давай начнём заново...')

    @wraps(func)
    async def wrapper(*args, **kwargs):
        # собираем все данные об источнике проблемы
        state = None
        for o in list(args) + list(kwargs.values()):
            if isinstance(o, FSMContext):
                state = await o.get_state()
        try:
            source = args[0]  # здесь message или query
            if isinstance(source, aiogram.types.CallbackQuery):
                source = source.message
        except (IndexError, AttributeError):
            prefix = f'[{func.__name__} {state}]'
        else:
            prefix = f'[{prefix_uri(source)} {state}] [{func.__name__}]'

        try:
            logger.debug(f'{prefix} Enter event')
            result = await func(*args, prefix=prefix, **kwargs)
            logger.debug(f'{prefix} Leave event')
            return result
        except Exception as e:
            msg = f'Exception: {e}'
            logger.exception(msg)
            await send_to_support(msg)

            try:
                obj = args[0]
                assert isinstance(obj, allowed_types)
                sender_id = obj.from_user.id
            except IndexError:
                logger.warning(f'{prefix}: No first argument!')
            except AssertionError:
                logger.warning(f'{prefix}: Unsupported type!')
            else:
                await bot.send_message(sender_id, message)

                if isinstance(obj, aiogram.types.CallbackQuery):
                    await callback_reset_bot(*args, **kwargs)
                if isinstance(obj, aiogram.types.Message):
                    await reset_bot(*args, **kwargs)

                logger.warning(f'{prefix}: Chat is restarted!')

    return wrapper


async def send_to(recipient: str, chat_id: Union[str, int], msg: str):
    """ Базовая функция отправки сообщения в чат"""
    if settings.DEBUG and not recipient.startswith('Ruslan'):
        return
    try:
        await bot.send_message(chat_id=chat_id, text=msg)
    except Exception as e:
        msg = f'[send_to] Chat [{chat_id}] Unable to send message: {e}'
        logger.exception(msg)


async def send_to_managers(msg: str):
    """ Отправляет сообщение менеджерам системы. """
    for name, chat_id in settings.MANAGERS:
        await send_to(name, chat_id, msg)


async def send_to_support(msg: str):
    """ Отправляет сообщение поддержке системы. """
    for name, chat_id in settings.SUPPORTS:
        await send_to(name, chat_id, msg)


async def send_reply(message, text, markup=None, state=None):
    """ Отправляет сообщение в чат.

    Следует переписать в виде отдельной задачи, которая берёт чат и сообщение
    из очереди и пытается их отправить, учитывая паузу между попытками.
    """
    prefix = f'[send_reply] [{prefix_uri(message)}]'
    try:
        await message.reply(text, reply_markup=markup)
    except Exception as e:
        logger.error(f'{prefix} Unable to reply to {message.chat.id}. '
                     f'Reason: {e}')
    else:
        logger.info(f'{prefix} Message sent')

    if state:
        status = await state.get_state()
        logger.debug(f'{prefix} State is <{status}>.')


@dispatcher.message_handler(commands=[commands.CMD_VERSION], state='*')
async def send_version(message: aiogram.types.Message):
    """ Выводит информацию о версии бота и его аптайме """
    diff = datetime.utcnow() - settings.STARTED_IN
    days = diff.days
    if days == 0:
        uptime = diff.seconds / 3600.0
        suffix = 's' if uptime >= 2.0 else ''
        uptime_str = f'{uptime:.02f} hour{suffix}'
    else:
        suffix = 's' if days >= 2.0 else ''
        uptime_str = f'{days:.02f} day{suffix}'
    await send_reply(message, messages.MSG_VERSION.format(
        version=settings.VERSION, commit=settings.COMMIT,
        uptime=uptime_str,
        started_in=settings.STARTED_IN.strftime('%y/%m/%d %H:%M:%S UTC'),
        user_id=message.from_user.id))


@restart_on_exception
async def show_start_page(message: aiogram.types.Message, state: FSMContext,
                          prefix: Optional[str] = None):
    logger.debug(f'{prefix} Show start page')
    await bot.send_message(
        message.from_user.id, messages.MSG_GREETING,
        reply_markup=keyboards.keyboard_greeting())
    await bot.send_message(
        message.from_user.id, 'Действия',
        reply_markup=keyboards.keyboard_actions(message))


@dispatcher.message_handler(commands=[commands.CMD_START], state='*')
async def reset_bot(message: aiogram.types.Message, state: FSMContext):
    prefix = f'[{prefix_uri(message)}] [reset_bot]'
    await state.finish()
    logger.debug(f'{prefix} Reset state')
    await states.Mode.ready.set()
    await show_start_page(message, state)



@dispatcher.callback_query_handler(
    keyboards.callbacks.filter(action=commands.CMD_START), state='*')
async def callback_reset_bot(query: aiogram.types.CallbackQuery,
                             callback_data: dict, state: FSMContext,
                             prefix: Optional[str] = None):
    await reset_bot(query.message, state)


@dispatcher.message_handler(commands=[commands.CMD_SETUP], state=states.Mode.ready)
async def process_setup(message: aiogram.types.Message, state: FSMContext):
    """ Обрабатывает запрос настройки """
    is_admin = settings.admin_required(message)
    if not is_admin:
        return
    cutlen = len(commands.CMD_SETUP) + 1  # 'count / prefix
    payload = message.text[cutlen:].strip()
    logger.debug(f'Payload: {payload}')
    payload = payload.replace('\'', '"')
    logger.debug(f'Payload: {payload}')

    try:
        data = json.loads(payload)
        settings.mapping_add(data)
    except settings.MappingException as e:
        await send_reply(message, e)
    except Exception as e:
        logger.exception(e)
    await show_start_page(message, state)


@dispatcher.callback_query_handler(
    keyboards.callbacks.filter(action=commands.CMD_PASSWORD),
    state=states.Mode.ready)
@restart_on_exception
async def callback_password_chosen(
        query: aiogram.types.CallbackQuery,
        callback_data: dict, state: FSMContext, prefix: str=None):
    """ Обрабатывает выбранный тип генерации пароля """
    value = callback_data['value']
    await bot.answer_callback_query(
        query.id, text=f'Выбрано действие: {value}')

    func = settings.HANDLER_MAPPING[value]
    result = func()
    await bot.send_message(query.from_user.id, result)


@dispatcher.callback_query_handler(
    keyboards.callbacks.filter(),
    state=states.Mode.ready)
@restart_on_exception
async def callback_admin_chosen(
        query: aiogram.types.CallbackQuery,
        callback_data: dict, state: FSMContext, prefix: str=None):
    """ Обрабатывает выбранный тип генерации пароля """
    action = callback_data['action']
    value = callback_data['value']
    cmd = f'{action} {value}'
    await bot.answer_callback_query(
        query.id, text=f'Выбрано действие: {cmd}')

    p = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)
    stdout, stderr = await p.communicate()
    logger.info(f'Result: {p.returncode}')
    if stdout:
        logger.debug(f'[stdout] {stdout.decode()}')
    if stderr:
        logger.debug(f'[stderr] {stderr.decode()}')
