# Devman_api

Telegram bot for Devman API.
The bot sends a message in a telegram with the details of the verified work by the teacher.


## Enviroments

- create new bot in Telegram and get the token   
  (you can obtain bot from @BotFather in Telegram, [See example](https://telegra.ph/Awesome-Telegram-Bot-11-11))
- create the file .env and fill in this data:
  - DEVMAN_API_TOKEN
  - TELEGRAM_API_TOKEN
  - TELEGRAM_CHAT_ID


## Installing

To get started go to terminal(mac os) or CMD (Windows)
- create virtualenv, [See example](https://python-scripts.com/virtualenv)

- clone github repository or download the code

```bash
$ git clone https://github.com/Rostwik/devman_api.git
```

- install packages

```bash
$ pip install -r requirements.txt
```
- run the program
```bash
$ python main.py
```

## Dockerization

- Clone repository:
```bash
$ git clone https://github.com/Rostwik/devman_api.git
```
- [Download and install Docker](https://docs.docker.com/get-docker/)
- Build the container image:
```bash
$ docker build -t devman_api .
```
- Start a container specifying the necessary environment variables from the [Environment](#enviroments) section with the '-e' flag:
```bash
$ docker run -e DEVMAN_API_TOKEN='' -e TELEGRAM_API_TOKEN='' -e TELEGRAM_CHAT_ID='' devman_api
```

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details


