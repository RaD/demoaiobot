# Развёртывание

Создаём каталог `/opt/telebot` и клонируем туда репозиторий.

В репозитории выполняем создание окружения:

    pyenv install -v 3.8.12
    pyenv exec python -m pipenv install

Для интеграции данного сервиса с Telegram следует создать новый бот 
с помощью команды @BotFather `/newbot`. Полученный токен сохранить
в файле `.env` в виде:

    TELEGRAM_TOKEN=xxxxxxxxx:YYYYYYYYYYYYYYYYYYYYYYY

Проверяем работоспособность:

    pipenv run service

В телеграм переходим в чат с созданным ботом и даём команду:

    /version

В нижней строке будет ваш идентификатор, запишите его.

## Автозапуск

Теперь пропишем запуск бота в systemd.

Создаём файл `/etc/systemd/system/telebot.service` следующего содержания:

    [Unit]
    Description=Docker compose executor for telebot service
    
    [Service]
    Restart=always
    
    WorkingDirectory=/opt/telebot
    EnvironmentFile=-/opt/telebot/.env
    
    User=root
    Group=docker
    
    ExecStart=pipenv run service --admin=ИДЕНТИФИКАТОР_АДМИНА
    
    [Install]
    WantedBy=multi-user.target
