# Бот Telegram

Бот для телеграм, который помогает создавать пароли различной сложности.

## Требования

Данный сервис использует ряд проектов с открытым исходым кодом:

- [Python 3.8];
- [AioGram].

## Конфигурация

Все настройки производятся через переменные окружения:

 * `DEBUG`, булево, признак работы в отладочном режиме;
 * `TOKEN`, строка, токен для бота;

## Разработка

Мы рекомендуем использовать виртуальное окружение для разработки данного сервиса. 

Например:

    pyenv local 3.8.0
    pyenv exec python -m pipenv install
    pipenv sync -d

Для интеграции данного сервиса с Telegram следует:
* Создать новый бот с помощью команды @BotFather `/newbot`;

# Лицензия
(c) 2020 HALFAKOP.

[aiogram]: <https://docs.aiogram.dev/>
[asyncio]: <https://docs.python.org/3/library/asyncio.html>
[make]: <https://www.gnu.org/software/make/>
[python 3.8]: <https://docs.python.org/3/whatsnew/3.8.html>
