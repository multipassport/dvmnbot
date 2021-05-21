# TelegramNotificationBot для сайта dvmn.org

Данный проект отправляет в Telegram уведомления о проверках на основе информации, полученной с API [Девман](https://dvmn.org/api/docs/).

### Как установить

Должен быть установлен Python3. Для установки зависимостей запустите команду:
```bash
pip install -r requirements.txt
```

Создайте файл `.env` рядом с `run.py`. В нем укажите следующие переменные:
`DVMN_TOKEN` - API-токен [Девман](https://dvmn.org/api/docs/)
`TG_TOKEN` - токен Telegram-бота. Получается у [@BotFather](https://telegram.me/BotFather)
`CHAT_ID` - ваш chat_id. Получается у [@userinfobot](https://telegram.me/userinfobot)

### Запуск

Теперь вы можете запустить бота командой:

```bash
python run.py
```

### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).