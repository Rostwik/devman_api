import os
import time
import textwrap

import requests
import telegram
from dotenv import load_dotenv


def send_telegram_msg(chat_id, results, telegram_token):
    bot = telegram.Bot(token=telegram_token)

    if results['is_negative']:
        text = f'''
                   У Вас проверили работу "{results['lesson_title']}".
                   К сожалению, в работе нашли ошибки.
                   Ссылка на урок: {results['lesson_url']}
                   '''

    else:
        text = f'''
                   У Вас проверили работу "{results['lesson_title']}".
                   Преподавателю все понравилось, можно приступать к следующему уроку.
                   '''

    bot.send_message(chat_id=chat_id, text=textwrap.dedent(text))


def main():
    load_dotenv()

    devman_api_token = os.getenv('DEVMAN_API_TOKEN')
    telegram_api_token = os.getenv('TELEGRAM_API_TOKEN')
    telegram_chat_id = os.getenv('TELEGRAM_CHAT_ID')
    results = {}

    while True:
        try:
            headers = {
                'Authorization': f'Token {devman_api_token}'
            }
            payload = {}

            if results:
                if results['status'] == 'found':
                    payload['timestamp'] = results['last_attempt_timestamp']
                if results['status'] == 'timeout':
                    payload['timeout'] = results['timestamp_to_request']

            url = 'https://dvmn.org/api/long_polling/'

            response = requests.get(url, headers=headers, params=payload, timeout=60)
            response.raise_for_status()
            results = response.json()

            for result in results['new_attempts']:
                send_telegram_msg(telegram_chat_id, result, telegram_api_token)

        except requests.exceptions.ReadTimeout:
            pass
        except requests.exceptions.ConnectionError:
            print('Интернет исчез')
            time.sleep(5)


if __name__ == '__main__':
    main()
