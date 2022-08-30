import random

#Standard 52-card french-suited playing cards without jokers
FRENCH = ["♣A", "♣2", "♣3", "♣4", "♣5", "♣6", "♣7", "♣8", "♣9", "♣10", "♣J", "♣Q", "♣K",
        "♦A", "♦2", "♦3", "♦4", "♦5", "♦6", "♦7", "♦8", "♦9", "♦10", "♦J", "♦Q", "♦K",
        "♥A", "♥2", "♥3", "♥4", "♥5", "♥6", "♥7", "♥8", "♥9", "♥10", "♥J", "♥Q", "♥K",
        "♠A", "♠2", "♠3", "♠4", "♠5", "♠6", "♠7", "♠8", "♠9", "♠10", "♠J", "♠Q", "♠K"]


class CardDeck:
    def __init__(self, cards: list[str], number_of_decks: int) -> None:
        """
        Initialize the deck of cards with custom cards
        """
        self.deck = cards*number_of_decks
        self.in_players_hands = []
        self.out = []

    def shuffle_deck(self) -> None:
        """
        Shuffle the cards that are in deck or out (not in player hands)
        """
        for i in range(len(self.out)):
            self.deck.append(self.out.pop(0))
        random.shuffle(self.deck)
    
    def draw(self, num: int) -> list[str]:
        """
        Draw a given number of cards
        """
        if num > len(self.deck):
            num = len(self.deck)
        cards = [self.deck.pop(0) for _ in range(num) if len(self.deck) > 0]
        self.in_players_hands.extend(cards)
        return cards