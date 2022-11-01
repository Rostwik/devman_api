import os

import requests
from dotenv import load_dotenv


def get_homeworks_list(token):
    headers = {
        'Authorization': f'Token {token}'
    }
    url = 'https://dvmn.org/api/long_polling/'
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    print(response.json())


def main():
    load_dotenv()

    devman_api_token = os.getenv('DEVMAN_API_TOKEN')

    get_homeworks_list(devman_api_token)


if __name__ == '__main__':
    main()
