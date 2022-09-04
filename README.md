# A BlackJack Telegram Bot
A bot to play BlackJack (which is named "Huszonegy" in hungarian) against a Telegram bot.

Currently it's a work in progress. My goal with this project (beside doing something fun) is to learn making larger programns, learn better practices, or in this case, how to make a Telegram bot and how to use SQLite with Python.

As of currently, one can play against the bot, but there are space for a *lot* of improvements that I'm planning to do.

# Planned features:
:heavy_check_mark: The Black Jack game itself

:x: Multiple language support

:x: Saving player stats in a database (their money, number of wins/loses etc)

:x: Display player stats

:x: Leaderboard

:x: Achievements

# Installation:
Clone the repo, and then install dependencies:

```bash
pip install -r requirements.txt
```
Acquire a Telegram Bot Token from the BotFather (https://core.telegram.org/bots#6-botfather).

Create a file named ".env" with the following content:
```
TOKEN="here-comes-your-bots-token"
```
After that, run the program:
```bash
python3 main.py
```
