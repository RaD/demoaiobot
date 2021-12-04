from aiogram.dispatcher.filters.state import State, StatesGroup

class Mode(StatesGroup):
    ready = State()
