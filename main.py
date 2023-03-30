import os
import time
import textwrap

import requests
import telegram
import logging
from dotenv import load_dotenv


class TelegramLogsHandler(logging.Handler):

    def __init__(self, tg_bot, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.tg_bot = tg_bot

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)


def send_telegram_msg(chat_id, results, telegram_bot):
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

    telegram_bot.send_message(chat_id=chat_id, text=textwrap.dedent(text))


def main():
    load_dotenv()
    devman_api_token = os.getenv('DEVMAN_API_TOKEN')
    telegram_api_token = os.getenv('TELEGRAM_API_TOKEN')
    telegram_chat_id = os.getenv('TELEGRAM_CHAT_ID')
    payload = {}

    bot = telegram.Bot(token=telegram_api_token)

    logging.basicConfig(format="%(process)d %(levelname)s %(message)s")
    logger = logging.getLogger('database')
    logger.setLevel(logging.WARNING)
    logger.addHandler(TelegramLogsHandler(bot, telegram_chat_id))
    logger.info('Бот запущен.')

    while True:
        try:
            headers = {
                'Authorization': f'Token {devman_api_token}'
            }

            url = 'https://dvmn.org/api/long_polling/'

            response = requests.get(url, headers=headers, params=payload, timeout=60)
            response.raise_for_status()
            results = response.json()

            if results:
                if results['status'] == 'found':
                    payload['timestamp'] = results['last_attempt_timestamp']
                    for result in results['new_attempts']:
                        send_telegram_msg(telegram_chat_id, result, bot)
                if results['status'] == 'timeout':
                    payload['timeout'] = results['timestamp_to_request']

        except requests.exceptions.ReadTimeout:
            pass
        except requests.exceptions.ConnectionError:
            print('Интернет исчез')
            time.sleep(5)
        except Exception as err:
            logger.error(f'Бот упал с ошибкой: {err}', exc_info=True)


if __name__ == '__main__':
    main()
