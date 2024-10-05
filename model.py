import treys
from treys import Card
from treys import Evaluator
from treys import Deck

class Player():
    def __init__(self):
        self.hand = []

    def getCard(self, card):
        self.hand.append(card)

    def printHand(self):
        Card.print_pretty_cards(self.hand)

deck = Deck()
board = deck.draw(3)
player1 = Player()
player2 = Player()
players = [player1, player2]
for i in range(2):
    for player in players:
        card = deck.draw(1)[0]
        player.getCard(card)

player1.printHand()
player2.printHand()