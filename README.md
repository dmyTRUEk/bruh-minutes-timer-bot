# Best Auto Sticker Bot

## Setup:
1) find [@BotFather](https://t.me/BotFather) in telegram, create your bot
2) create file named `secret_key.py`, and write in it:
  ```
  KEY = "your bot's token goes here"
  ```
  WARNING: don't tell your bot's token to anyone, it's secret!

3) launch bot:
```
python3 main.py
```

## Deploy to Heroku:
1) create account at [heroku](https://heroku.com)
2) deploy it to heroku
3) set heroku workers amount to zero:
  ```
  heroku ps:scale worker=0
  ```
  and then to one:
  ```
  heroku ps:scale worker=1
  ```

Source: [Telegram Bot Heroku Deploy](https://github.com/AnshumanFauzdar/telegram-bot-heroku-deploy)

