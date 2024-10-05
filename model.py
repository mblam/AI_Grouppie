import treys
from treys import Card
from treys import Evaluator
from treys import Deck
import Chip

class Player():
    def __init__(self, name):
        self.hand = []
        self.name = name

    def getCard(self, card):
        self.hand.append(card)

    def printHand(self):
        Card.print_pretty_cards(self.hand)

# Object that represents the overall state of the game
class Table():
    # Initializes the deck, list of cards on the board, and list of players
    def __init__(self):
        self.deck = Deck()
        self.board = []
        self.players = []

    # Initializes player objects and deals cards to them
    def initializePlayers(self, numPlayers):
        for i in range(numPlayers):
            self.players.append(Player("Player "+str(i+1)))
        self.dealCards()

    # Deal cards to all players one at a time
    def dealCards(self):
        for i in range(2):
            for player in self.players:
                player.getCard(self.deck.draw(1)[0])

    # Prints out the different players and their hands
    def printPlayers(self):
        for player in self.players:
            print(player.name+": ",end="")
            player.printHand()


# TODO: have an option for the number of AI players vs real players
# TODO: create an actual play loop that goes around all of the players and gets their bets
# TODO: Create functionality that deals the initial three cards to the table (burn, place 3), then the next (burn, place 1), the the last


t = Table()
t.initializePlayers(3)
t.printPlayers()