from black_jack import *
import telebot
from dotenv import load_dotenv
import os


load_dotenv(".env")
bot = telebot.TeleBot(os.environ.get("TOKEN"), parse_mode="HTML")

@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    bot.reply_to(message, "Welcome to BlackJack Bot! Type /play to start playing!")

@bot.message_handler(commands=["play"])
def start_black_jack(message):
    deck = CardDeck(FRENCH, 6)
    deck.shuffle_deck()
    player = Player(str(message.from_user.id), 1000)
    game = BlackJackGame(deck, player, bot)
    cont = True
    while cont == True:
        cont = game.game_loop()

def main():
    bot.infinity_polling()
    # deck.shuffle_deck()
    # player = Player("Roland", 1000)
    # game = BlackJackGame(deck, player)
    # cont = True
    # while cont == True:
    #     cont = game.game_loop()

if __name__ == "__main__":
    main()
