# TelegramNotificationBot для сайта dvmn.org

Данный проект отправляет в Telegram уведомления о проверках на основе информации, полученной с API [Девман](https://dvmn.org/api/docs/).

### Как установить

Должен быть установлен Python3. Для установки зависимостей запустите команду:
```bash
pip install -r requirements.txt
```

Создайте файл `.env` рядом с `run.py`. В нем укажите следующие переменные:
* `DVMN_TOKEN` - API-токен [Девман](https://dvmn.org/api/docs/)
* `TG_TOKEN` - токен Telegram-бота. Получается у [@BotFather](https://telegram.me/BotFather)
* `TG_CHAT_ID` - ваш chat_id. Получается у [@userinfobot](https://telegram.me/userinfobot)
* `LOGGER_TG_TOKEN` - токен запасного Telegram-бота для логгирования ошибок

### Запуск

Теперь вы можете запустить бота командой:

```bash
python run.py
```

### Запуск на Heroku

[Установите Docker](https://docs.docker.com/engine/install/)

Скачайте код из репозитория
```
git clone git@github.com:multipassport/dvmnbot.git
```

Войдите на Heroku
```
heroku login
```

Аутентифицируйтесь в Container Registry
```
heroku container:login
```

Зайдите в папку с приложением и создайте приложение на Heroky
```
cd dvmnbot
heroku create
```

Отправьте образ, созданный докером, в свежесозданное приложение на Heroku и запустите его
```
heroku container:push bot
heroku container:release web
```

### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).