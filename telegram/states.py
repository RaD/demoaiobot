from aiogram.dispatcher.filters.state import State, StatesGroup


class UserStates(StatesGroup):
    """ Набор состояний """

    reset = State()
    initial = State()
