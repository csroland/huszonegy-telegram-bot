from cards import *

class Player:
    def __init__(self, name: str, money: int):
        self.name = name
        self.money = money
        self.cards = []
        self.finished = False

class BlackJackGame:
    def __init__(self, deck: CardDeck, player: Player, bot):
        self.deck = deck
        self.player = player
        self.dealer = Player("Dealer", 0)
        self.bot = bot


    def black_jack_round(self) -> None:
        bet_success = False
        while not bet_success:
            bet = int(input("Place your bet: "))
            if bet <= self.player.money and bet > 0:
                self.player.money -= bet
                bet_success = True
            else:
                print("can't do")
        self.player.cards.extend(self.deck.draw(1))
        self.dealer.cards.extend(self.deck.draw(1))
        self.player.cards.extend(self.deck.draw(1))
        self.dealer.cards.extend(self.deck.draw(1))

        while True:
            hand_value = self.bj_hand_value(self.player.cards)
            dealer_value = self.bj_hand_value(self.dealer.cards)
            print(self.player.name, "cards: \t\t", self.player.cards, "\t\t\t value:", hand_value)
            print(self.dealer.name, "cards: \t\t", [self.dealer.cards[0], "?"])
            if not self.player.finished:
                if dealer_value == 21:
                    if hand_value == 21:
                        self.print_stats()
                        print("Stalemate")
                        self.player.money += bet
                        return
                    else:
                        self.print_stats()
                        print("You lose")
                        return
                elif hand_value == 21:
                    self.print_stats()
                    print("You Won!")
                    return
                elif hand_value < 21:
                    match input("[s]tand, or [h]it"):
                        case "h":
                            self.player.cards.extend(self.deck.draw(1))
                        case "s":
                            self.player.finished = True
                            break
                        case _:
                            print("unkown")
                elif hand_value > 21:
                    print("Bust!")
                    return
            else:
                break

        while self.bj_hand_value(self.dealer.cards) < 17:
            self.dealer.cards.extend(self.deck.draw(1))
            self.print_stats()
        dealer_value = self.bj_hand_value(self.dealer.cards)
        if dealer_value > 21:
            self.print_stats()
            print("Dealer bust!")
            self.player.money += 2*bet
            return
        if dealer_value > hand_value:
            self.print_stats()
            print("Dealer won!")
            return
        elif dealer_value == hand_value:
            self.print_stats()
            print("Stalemate!")
            return
        else:
            print("You won!")
            self.print_stats()
            self.player.money += 2*bet
            return


    def print_stats(self):
        print(self.player.name, "cards: \t\t", self.player.cards, "\t value:", self.bj_hand_value(self.player.cards))
        print(self.dealer.name, "cards: \t\t", self.dealer.cards, "\t value:", self.bj_hand_value(self.dealer.cards))


    def reset_table(self) -> None:
        self.deck.out.extend(self.player.cards)
        self.deck.out.extend(self.dealer.cards)
        self.player.cards, self.dealer.cards = [], []
        self.player.finished = False


    def shuffle_deck(self, thres: int) -> None:
        if len(self.deck.deck) < thres:
            self.deck.shuffle_deck()


    def bj_hand_value(self, cards: list[str]) -> int:
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
        self.black_jack_round()
        self.reset_table()
        self.shuffle_deck(65)
        return self.play_again()
