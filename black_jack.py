from cards import *
from telebot import types

#Define the markups used for the custom keyboards for the game:
inline_btn_double = types.InlineKeyboardButton("Double", callback_data = "double")
inline_btn_hit = types.InlineKeyboardButton("Hit", callback_data = "hit")
inline_btn_pass = types.InlineKeyboardButton("Pass", callback_data = "pass")
first_round_markup = types.InlineKeyboardMarkup([[inline_btn_double, inline_btn_hit, inline_btn_pass]])
other_round_markup = types.InlineKeyboardMarkup([[inline_btn_hit, inline_btn_pass]])

class Player:
    def __init__(self, name: str, money: int):
        self.name = name
        self.money = money
        self.cards = []
        self.finished = False

class BlackJackGame:
    def __init__(self, player_id: str, bot):
        """
        Starts the game by initializing the deck, the player and the dealer, starting in 'BET' state
        """
        self.deck = CardDeck(FRENCH, 6)
        self.deck.shuffle_deck()
        self.player_id = player_id
        self.player = Player(self.player_id, 1000) #placeholder money
        self.dealer = Player("Dealer", 0)
        self.bot = bot
        self.game_message_id = None
        self.game_state = "BET"

    def start_black_jack_round(self) -> None:
        """
        Starts the game after the bet was succesful and saves the game_message_id so the message can be later edited after user action
        """
        for i in range(2):
            self.player.cards.extend(self.deck.draw(1))
            self.dealer.cards.extend(self.deck.draw(1))
        first_msg_string = "".join(["<b>Dealer:</b>\n", self.dealer.cards[0], " ??\n\n", "<b>Your cards:</b>\n", self.player.cards[0], " ", self.player.cards[1]])
        self.game_message_id = self.bot.send_message(self.player_id, first_msg_string, reply_markup = first_round_markup).message_id

    def update_black_jack_round(self, action: str) -> None:
        """
        The main logic of the game, it updates the state of the game after user actions
        """
        hand_value = self.bj_hand_value(self.player.cards)
        dealer_value = self.bj_hand_value(self.dealer.cards)
        print(self.player.name, "cards: \t\t", self.player.cards, "\t\t\t value:", hand_value)
        print(self.dealer.name, "cards: \t\t", [self.dealer.cards[0], "?"])
        if not self.player.finished:
            if dealer_value == 21:
                self.dealer.finished = True
                self.player.finished = True
                if hand_value == 21:
                    self.print_stats()
                    print("Stalemate")
                    self.bot.edit_message_text(self.gen_game_edit(), self.player_id, self.game_message_id)
                    self.player.money += bet
                    return
                else:
                    self.print_stats()
                    self.bot.edit_message_text(self.gen_game_edit(), self.player_id, self.game_message_id)
                    print("You lose")
                    return
            elif hand_value == 21:
                self.player.finished = True
                self.dealer.finished = True
                self.print_stats()
                self.bot.edit_message_text(self.gen_game_edit(), self.player_id, self.game_message_id)
                print("You Won!")
                return
            elif hand_value < 21:
                match action:
                    case "hit":
                        self.player.cards.extend(self.deck.draw(1))
                        self.bot.edit_message_text(self.gen_game_edit(), self.player_id, self.game_message_id, reply_markup = other_round_markup)
                        return
                    case "stand":
                        self.bot.edit_message_text(self.gen_game_edit(), self.player_id, self.game_message_id, reply_markup = other_round_markup)
                        self.player.finished = True
                        return
                    case _:
                        print("unkown")
                        return
            elif hand_value > 21:
                self.player.finished = True
                self.bot.edit_message_text(self.gen_game_edit(), self.player_id, self.game_message_id)
                print("Bust!")
                return
        self.dealer.finished = True
        while self.bj_hand_value(self.dealer.cards) < 17:
            self.dealer.cards.extend(self.deck.draw(1))
            self.bot.edit_message_text(self.gen_game_edit(), self.player_id, self.game_message_id)
            self.print_stats()
        dealer_value = self.bj_hand_value(self.dealer.cards)
        if dealer_value > 21:
            self.print_stats()
            print("Dealer bust!")
            self.player.money += 2*bet
            self.bot.edit_message_text(self.gen_game_edit(), self.player_id, self.game_message_id)
            self.bot.send_message(self.player_id, "You won!")
            return
        if dealer_value > hand_value:
            self.print_stats()
            print("Dealer won!")
            self.bot.edit_message_text(self.gen_game_edit(), self.player_id, self.game_message_id)
            self.bot.send_message(self.player_id, "You lost!")
            return
        elif dealer_value == hand_value:
            self.print_stats()
            print("Stalemate!")
            self.bot.edit_message_text(self.gen_game_edit(), self.player_id, self.game_message_id)
            self.bot.send_message(self.player_id, "Stalemate")
            return
        else:
            print("You won!")
            self.print_stats()
            self.player.money += 2*bet
            self.bot.edit_message_text(self.gen_game_edit(), self.player_id, self.game_message_id)
            self.bot.send_message(self.player_id, "You won!")
            return


    def print_stats(self):
        """
        Prints both player's and dealer's stats, used for debugging
        """
        print(self.player.name, "cards: \t\t", self.player.cards, "\t value:", self.bj_hand_value(self.player.cards))
        print(self.dealer.name, "cards: \t\t", self.dealer.cards, "\t value:", self.bj_hand_value(self.dealer.cards))

    def gen_game_edit(self) -> str:
        """
        Generates the string of the edited message sent after each update
        """
        if self.dealer.finished:
            line_1 = "<b>Dealer: </b>\n" + str(self.bj_hand_value(self.dealer.cards))
            line_2 = " ".join(self.dealer.cards) + "\n\n"
            line_3 = "<b>Your cards: </b>" + str(self.bj_hand_value(self.player.cards)) + "\n"
            line_4 = " ".join(self.player.cards)
        else:
            line_1 = "<b>Dealer:</b>\n"
            line_2 = self.dealer.cards[0] + " ??" + "\n\n"
            line_3 = "<b>Your cards: </b>" + str(self.bj_hand_value(self.player.cards)) + "\n"
            line_4 = " ".join(self.player.cards)
        return "".join([line_1, line_2, line_3, line_4])

    def reset_table(self) -> None:
        """
        Resets the table after the round is over
        """
        self.deck.out.extend(self.player.cards)
        self.deck.out.extend(self.dealer.cards)
        self.player.cards, self.dealer.cards = [], []
        self.player.finished = False


    def shuffle_deck(self, thres: int) -> None:
        """
        Shuffles the whole deck after only a certain amount of cards remained
        """
        if len(self.deck.deck) < thres:
            self.deck.shuffle_deck()


    def bj_hand_value(self, cards: list[str]) -> int:
        """
        Calculates the value of a given list of cards
        """
        value = 0
        cards = [x[1:] for x in cards]
        for card in cards:
            if card.isnumeric():
                value += int(card)
            elif card in ["J", "Q", "K"]:
                value += 10
        if "A" in cards:
            for i in range(cards.count("A")):
                if value + 11 <= 21:
                    value += 11
                else:
                    value += 1
        return value


    def play_again(self) -> bool:
        print("Your balance: ", self.player.money)
        if input("want to play another round?: [y]es") == "y":
            return True
        else:
            return False


    def game_loop(self) -> bool:
        self.update_black_jack_round()
        self.reset_table()
        self.shuffle_deck(65)
        return self.play_again()
