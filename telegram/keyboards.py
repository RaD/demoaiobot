from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from . import commands, settings

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


def keyboard_actions(message) -> InlineKeyboardMarkup:
    is_admin = settings.admin_required(message)
    keyboard = InlineKeyboardMarkup()
    for row in settings.ACTION_MAPPING:
        keyboard.row()
        for button in row.buttons:
            if button.target == 'admin' and not is_admin:
                continue
            callback = callbacks.new(action=button.command, value=button.value)
            btn = InlineKeyboardButton(button.title, callback_data=callback)
            keyboard.insert(btn)
    return keyboard
