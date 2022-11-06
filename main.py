import os

import requests
import telegram
from dotenv import load_dotenv


def get_homeworks_list(devman_token, check_result):
    headers = {
        'Authorization': f'Token {devman_token}'
    }
    payload = {}

    if check_result:
        payload['timestamp'] = check_result['timestamp']

    url = 'https://dvmn.org/api/long_polling/'

    response = requests.get(url, headers=headers, params=payload, timeout=60)
    response.raise_for_status()
    check_result = response.json()['new_attempts'][0]

    return check_result


def send_telegram_msg(chat_id, check_result, telegram_token):
    bot = telegram.Bot(token=telegram_token)

    if check_result['is_negative']:
        text = f'У Вас проверили работу "{check_result["lesson_title"]}".' \
               f' К сожалению, в работе нашли ошибки.' \
               f' Ссылка на урок: {check_result["lesson_url"]}'
    else:
        text = f'У Вас проверили работу "{check_result["lesson_title"]}".' \
               f' Преподавателю все понравилось, можно приступать к следующему уроку.'

    bot.send_message(chat_id=chat_id, text=text)


def main():
    load_dotenv()

    devman_api_token = os.getenv('DEVMAN_API_TOKEN')
    telegram_api_token = os.getenv('TELEGRAM_API_TOKEN')
    telegram_chat_id = os.getenv('TELEGRAM_CHAT_ID')
    check_result = {}

    while True:
        try:
            check_result = get_homeworks_list(devman_api_token, check_result)
            send_telegram_msg(telegram_chat_id, check_result, telegram_api_token)
        except requests.exceptions.ReadTimeout:
            print('Новых работ нет')
        except requests.exceptions.ConnectionError:
            print('Интернет исчез')


if __name__ == '__main__':
    main()
