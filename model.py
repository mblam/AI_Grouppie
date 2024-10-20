import treys
from treys import Card
from treys import Evaluator
from treys import Deck
import Chip
import sys

STARTING_AMOUNT = 50


# TODO: Add error checking for betting values
    # Must be > 0
    # Needs to at least call
    # Cannot be more than the player has
# TODO: Include option to choose how many players are AI v. not
# TODO: Maybe include option for custom player names
# TODO: Figure out GUI stuff (pygame)
# TODO: Include logic for AI player


class Player():
    def __init__(self, name, ai=False):
        self.hand = []
        self.name = name
        self.money = STARTING_AMOUNT
        self.AIPlayer = ai

    def getCard(self, card):
        self.hand.append(card)

    def printHand(self):
        Card.print_pretty_cards(self.hand)

    def makePlay(self):
        print(self.name + ": ", end="")
        self.printHand()
        if self.AIPlayer:
            pass
            # TODO: Fill in with AI logic
        else:
            play = input("\tWhat would you like to do (play or fold): ")
            if play.lower() == "fold":
                return -1
            else:
                amount = int(input("\tHow much would you like to bet: "))
                self.money -= amount
                return amount


# Object that represents the overall state of the game
class Table():
    # Initializes the deck, list of cards on the board, and list of players
    def __init__(self):
        self.deck = Deck()
        self.board = []
        self.allPlayers = []
        self.activePlayers = []
        self.pot = 0
        self.gameOver = False
        self.evaluator = Evaluator()

    # Initializes player objects and deals cards to them
    def initializePlayers(self, numPlayers):
        if numPlayers <= 0:
            sys.tracebacklimit = 0
            raise Exception("Invalid number of players")

        for i in range(numPlayers):
            self.allPlayers.append(Player("Player " + str(i + 1)))
        self.dealCardsToPlayers()

    # Deal cards to all players one at a time
    def dealCardsToPlayers(self):
        for i in range(2):
            for player in self.allPlayers:
                player.getCard(self.deck.draw(1)[0])

    def dealFirstRound(self):
        burn = self.deck.draw(1)
        self.board = self.deck.draw(3)

    def dealSecondRound(self):
        burn = self.deck.draw(1)
        self.board.append(self.deck.draw(1)[0])

    def dealThirdRound(self):
        self.board.append(self.deck.draw(1)[0])

    # Prints out the different players and their hands
    def printPlayers(self):
        for player in self.allPlayers:
            print(player.name + ": ", end="")
            player.printHand()

    # Game end state
    def winner(self, player):
        self.gameOver = True
        player.money += self.pot
        print(player.name + " wins $" + str(self.pot))

    def startGame(self):
        # Set up initial values
        print("Starting the game")
        self.activePlayers = self.allPlayers.copy()
        self.pot = 0

        # Goes through three rounds of plays
        for i in range(3):
            # Deals to the table using the rules for the given round
            print()
            print("***********************")
            match i:
                case 0:
                    print("Dealing the first round")
                    self.dealFirstRound()
                case 1:
                    print("Dealing the second round")
                    self.dealSecondRound()
                case 2:
                    print("Dealing the third round")
                    self.dealThirdRound()
            print("***********************\n")

            print("Cards on the table: ", end="")
            Card.print_pretty_cards(self.board)

            # Set up tracking variables
            highestBet = 0
            lastBetter = None
            currentPlayer = 0

            # While the bets are still increasing / being called
            while self.activePlayers[currentPlayer] != lastBetter:
                player = self.activePlayers[currentPlayer]

                # If only one player is left, they automatically win
                if len(self.activePlayers) == 1:
                    self.winner(player)
                    return

                # Has the current player make a decision
                bet = player.makePlay()

                # Remove them from the list of active players if they folded
                if bet == -1:
                    self.activePlayers.pop(currentPlayer)
                # Update the highest bet and overall pot based on bet value
                else:
                    if bet > highestBet:
                        highestBet = bet
                        lastBetter = player

                    self.pot += bet

                    currentPlayer += 1

                currentPlayer = currentPlayer % len(self.activePlayers)

        hands = {}
        for player in self.activePlayers:
            handValue = self.evaluator.evaluate(player.hand, self.board)
            hands[handValue] = player

        bestHand = min(hands.keys())
        self.winner(hands[bestHand])


# -------------------------Initialization-------------------------------
t = Table()
t.initializePlayers(2)
t.startGame()
