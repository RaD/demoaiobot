from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from . import commands

callbacks = CallbackData('button', 'action', 'value')


def keyboard_greeting() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()
    keyboard.row(
        InlineKeyboardButton('Сайт', url='https://github.com/'),
        InlineKeyboardButton(
            'Обновить',
            callback_data=callbacks.new(
                action=commands.CMD_REFRESH, value='none')))
    return keyboard
