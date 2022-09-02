from black_jack import *
import telebot
from dotenv import load_dotenv
import os

current_games = {}

load_dotenv(".env")
bot = telebot.TeleBot(os.environ.get("TOKEN"), parse_mode="HTML")

@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.reply_to(message, "Welcome to BlackJack Bot! Type /play to start playing!")

@bot.message_handler(commands=["play"])
def start_game(message):
    player_id = str(message.from_user.id)
    if player_id not in current_games:
        current_games[player_id] = BlackJackGame(player_id, bot)
        bot.reply_to(message, "Let's get started!")
        bot.send_message(player_id, "Please place your bet!")
    else:
        bot.reply_to(message, "You already have a game going on!")

@bot.message_handler(func=lambda msg: msg.text.isnumeric())
def handle_bet(message):
    player_id = str(message.from_user.id)
    amount = int(message.text)
    if player_id in current_games:
        game = current_games[player_id]
        if game.game_state == "BET":
            if amount > 0 and amount < game.player.money:
                game.player.money -= amount
                game.player.bet = amount
                bot.reply_to(message, "You've bet: " + message.text + " coins")
                game.game_state = "FIRST_ROUND"
                game.start_black_jack_round()
            else:
                bot.reply_to(message, "Invalid amount")
        else:
            bot.reply_to(message, "You can't bet currently")

@bot.callback_query_handler(func = lambda call: True)
def handle_query(call):
    print(call)
    bot.answer_callback_query(call.id)
    player_id = str(call.from_user.id)
    action = call.data
    if player_id in current_games:
        if call.data in ["hit", "stand", "double"]:
            current_games[player_id].update_black_jack_round(action)
        elif call.data == "new_game_yes":
            bot.edit_message_text("Place your bet!", player_id, call.message.id)
            current_games[player_id].reset_table()
            current_games[player_id].shuffle_deck(65)
            current_games[player_id].start_black_jack_round()
        elif call.data == "new_game_no":
            bot.edit_message_text("See you soon!",  player_id, call.message.id)
            del current_games[player_id]

def main():
    bot.infinity_polling()

if __name__ == "__main__":
    main()
