from cards import *
from telebot import types

#Define the markups used for the custom keyboards for the game:
inline_btn_double = types.InlineKeyboardButton("Double", callback_data = "double")
inline_btn_hit = types.InlineKeyboardButton("Hit", callback_data = "hit")
inline_btn_pass = types.InlineKeyboardButton("Stand", callback_data = "stand")
inline_btn_new_game_yes = types.InlineKeyboardButton("Yes", callback_data = "new_game_yes")
inline_btn_new_game_no = types.InlineKeyboardButton("No", callback_data = "new_game_no")

first_round_markup = types.InlineKeyboardMarkup([[inline_btn_double, inline_btn_hit, inline_btn_pass]])
other_round_markup = types.InlineKeyboardMarkup([[inline_btn_hit, inline_btn_pass]])
new_game_markup = types.InlineKeyboardMarkup([[inline_btn_new_game_yes, inline_btn_new_game_no]])

class Player:
    def __init__(self, name: str, money: int):
        self.name = name
        self.money = money
        self.bet = 0
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
        self.game_message_text = ""
        self.game_state = "BET"

    def start_black_jack_round(self) -> None:
        """
        Starts the game after the bet was succesful and saves the game_message_id so the message can be later edited after user action
        """
        for i in range(2):
            self.player.cards.extend(self.deck.draw(1))
            self.dealer.cards.extend(self.deck.draw(1))
        self.game_message_id = self.bot.send_message(self.player_id, self.gen_game_edit(), reply_markup = first_round_markup).message_id
        hand_value = self.bj_hand_value(self.player.cards)
        dealer_value = self.bj_hand_value(self.dealer.cards)
        if dealer_value == 21:
            self.dealer.finished = True
            self.player.finished = True
            if hand_value == 21:
                self.print_stats()
                print("Stalemate")
                self.bot.edit_message_text(self.gen_game_edit(), self.player_id, self.game_message_id)
                self.player.money += self.bet
                self.reset_table()
                self.play_again()
                return
            else:
                self.print_stats()
                self.bot.edit_message_text(self.gen_game_edit(), self.player_id, self.game_message_id)
                print("You lose")
                self.reset_table()
                self.play_again()
                return
        elif hand_value == 21:
            self.player.finished = True
            self.dealer.finished = True
            self.player.money += 2*self.bet
            self.print_stats()
            self.bot.edit_message_text(self.gen_game_edit(), self.player_id, self.game_message_id)
            print("You Won!")
            self.reset_table()
            self.play_again()
            return

    def update_black_jack_round(self, action: str = "") -> bool:
        """
        The main logic of the game, it updates the state of the game after user actions.
        """
        hand_value = self.bj_hand_value(self.player.cards)
        dealer_value = self.bj_hand_value(self.dealer.cards)
        print(self.player.name, "cards: \t\t", self.player.cards, "\t\t\t value:", hand_value)
        print(self.dealer.name, "cards: \t\t", [self.dealer.cards[0], "?"])
        if not self.player.finished:
            if hand_value < 21:
                match action:
                    case "hit":
                        self.player.cards.extend(self.deck.draw(1))
                        self.update_game_text(other_round_markup)
                        self.update_black_jack_round()
                        return
                    case "stand":
                        self.player.finished = True
                        self.dealer.finished = True
                        self.update_game_text(other_round_markup)
                        self.update_black_jack_round()
                        return
                    case "double":
                        self.player.money -= self.player.bet
                        self.player.bet *= 2
                        self.update_game_text(other_round_markup)
                        self.update_black_jack_round()
                        return
                    case "":
                        return
                    case _:
                        print("unkown")
                        return
            elif hand_value > 21:
                self.player.finished = True
                self.bot.edit_message_text(self.gen_game_edit(), self.player_id, self.game_message_id)
                self.bot.send_message(self.player_id, "You lose!")
                print("Bust!")
                self.play_again()
                return
        self.dealer.finished = True
        self.bot.edit_message_text(self.gen_game_edit(), self.player_id, self.game_message_id)
        while self.bj_hand_value(self.dealer.cards) < 17:
            self.dealer.cards.extend(self.deck.draw(1))
            self.bot.edit_message_text(self.gen_game_edit(), self.player_id, self.game_message_id)
            self.print_stats()
        dealer_value = self.bj_hand_value(self.dealer.cards)
        if dealer_value > 21:
            self.print_stats()
            print("Dealer bust!")
            self.player.money += 2*self.player.bet
            self.bot.send_message(self.player_id, "You won!")
            self.play_again()
            return
        if dealer_value > hand_value:
            self.print_stats()
            print("Dealer won!")
            self.bot.send_message(self.player_id, "You lost!")
            self.play_again()
            return
        elif dealer_value == hand_value:
            self.print_stats()
            self.player.money += self.player.bet
            print("Stalemate!")
            self.bot.send_message(self.player_id, "Stalemate")
            self.play_again()
            return
        else:
            print("You won!")
            self.print_stats()
            self.player.money += 2*self.player.bet
            self.bot.send_message(self.player_id, "You won!")
            self.play_again()
            return

    def update_game_text(self, markup):
        """
        Check if the game text has changed, if yes, update it
        """
        new = self.gen_game_edit()
        if new == self.game_message_text:
            pass
        else:
            self.game_message_text = new
            self.bot.edit_message_text(self.game_message_text, self.player_id, self.game_message_id, reply_markup = markup)

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
            line_1 = "<b>Dealer: </b>" + str(self.bj_hand_value(self.dealer.cards)) + "\n"
            line_2 = " ".join(self.dealer.cards) + "\n\n"
            line_3 = "<b>Your cards: </b>" + str(self.bj_hand_value(self.player.cards)) + "\n"
            line_4 = " ".join(self.player.cards+ ["\n\n"])
            line_5 = "<b>Balance: </b>" + str(self.player.money) 
        else:
            line_1 = "<b>Dealer:</b>\n"
            line_2 = self.dealer.cards[0] + " ??" + "\n\n"
            line_3 = "<b>Your cards: </b>" + str(self.bj_hand_value(self.player.cards)) + "\n"
            line_4 = " ".join(self.player.cards + ["\n\n"])
            line_5 = "<b>Balance: </b>" + str(self.player.money) 
        return "".join([line_1, line_2, line_3, line_4, line_5])

    def reset_table(self) -> None:
        """
        Resets the table after the round is over
        """
        self.player.bet = 0
        self.game_state = "BET"
        self.deck.out.extend(self.player.cards)
        self.deck.out.extend(self.dealer.cards)
        self.player.cards, self.dealer.cards = [], []
        self.player.finished = False
        self.dealer.finished = False

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

    def play_again(self) -> None:
        """
        Ask the player if it wants to play again?
        """
        self.bot.send_message(self.player_id, "Another round?", reply_markup = new_game_markup)