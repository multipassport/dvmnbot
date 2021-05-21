import logging
import os
import requests
import telegram

from dotenv import load_dotenv
from requests.exceptions import ReadTimeout, ConnectionError
from urllib.parse import urljoin

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
    chat_id = os.getenv('CHAT_ID')
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO, filename='bot.log')

    while True:
        try:
            response = get_dvmn_response(dvmn_token, timestamp=None)
            if response['status'] == 'found':
                timestamp = response.get('last_attempt_timestamp')
                for attempt in response['new_attempts']:
                    message = define_answer(attempt)
                    send_notification(tg_token, chat_id, message)
            else:
                timestamp = response.get('timestamp_to_request')
        except ConnectionError:
            logging.error('ConnectionError')
            continue
        except ReadTimeout:
            logging.error('ReadTimeout')
            continue
