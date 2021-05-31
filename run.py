import logging
import os
import requests
import telegram
import time

from dotenv import load_dotenv
from requests.exceptions import ReadTimeout, ConnectionError
from urllib.parse import urljoin


class BotHandler(logging.Handler):
    def __init__(self, token, chat_id):
        super().__init__()
        self.token = token
        self.chat_id = chat_id

    def emit(self, record):
        bot = telegram.Bot(self.token)
        bot.send_message(chat_id=self.chat_id, text=str(record))


logger = logging.getLogger('BotHandler')


def send_notification(token, chat_id, message):
    bot = telegram.Bot(token)
    bot.send_message(chat_id=chat_id, text=message)


def get_dvmn_response(token, timestamp):
    dvmn_url = 'https://dvmn.org/api/long_polling'
    headers = {'Authorization': token}
    payload = {'timestamp': timestamp}
    response = requests.get(dvmn_url, headers=headers, params=payload)
    response.raise_for_status()
    return response.json()


def define_answer(response):
    lesson_title = response.get('lesson_title')
    dvmn_url = 'https://dvmn.org'
    lesson_url = urljoin(dvmn_url, response.get('lesson_url'))
    if response['is_negative']:
        message = f'Эх, урок {lesson_title} не приняли:( Ссылка:\n{lesson_url}'
    else:
        message = f'Грац, урок {lesson_title} приняли! Ссылка:\n{lesson_url}'
    return message


if __name__ == '__main__':
    load_dotenv()
    dvmn_token = os.getenv('DVMN_TOKEN')
    tg_token = os.getenv('TG_TOKEN')
    log_bot_token = os.getenv('LOGGER_TG_TOKEN')
    chat_id = os.getenv('TG_CHAT_ID')

    logger.setLevel(logging.INFO)
    logger.addHandler(BotHandler(log_bot_token, chat_id))

    logger.info('Bot is running')

    sleep_timer = 10 * 60
    timestamp = None
    connections_count = 0

    while True:
        try:
            response = get_dvmn_response(dvmn_token, timestamp)
            if response['status'] == 'found':
                timestamp = response.get('last_attempt_timestamp')
                for attempt in response['new_attempts']:
                    message = define_answer(attempt)
                    send_notification(tg_token, chat_id, message)
            else:
                timestamp = response.get('timestamp_to_request')
        except ConnectionError:
            logger.exception()
            while connections_count < 5:
                connections_count += 1
            else:
                connections_count = 0
                time.sleep(sleep_timer)
                logger.exception('Bot is disconnected for next 10 minutes')
            continue
        except ReadTimeout:
            logger.exception()
            continue
