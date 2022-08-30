from black_jack import *
import os


def main():
    deck = CardDeck(FRENCH, 6)
    deck.shuffle_deck()
    player = Player("Roland", 100)
    game = BlackJackGame(deck, player)
    while True:
        game.game_loop()

if __name__ == "__main__":
    main()
