import treys
from treys import Card
from treys import Evaluator
from treys import Deck
import Chip
import sys

STARTING_AMOUNT = 50
BIG_BLIND_AMOUNT = 2
SMALL_BLIND_AMOUNT = 1


# TODO: Add error checking for betting values
    # Needs to at least call
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
            while True: # Keeps looping until valid set of actions occur
                print("\tYou have " + str(self.money) + " chips")
                play = input("\tWhat would you like to do, play [p] or fold [f]: ")
                if play.lower() == "fold" or play.lower() == "f":
                    return -1
                elif play.lower() == "play" or play.lower() == "p":

                    while True: # Keeps looping until valid set of actions occur
                        checkRaise = input("\tWould you like to check [c] or raise [r]: ")
                        if checkRaise.lower() == "raise" or checkRaise.lower() == "r":

                            while True:     
                                amount = int(input("\tHow much would you like to bet: "))
                                if amount > self.money or amount < 1:   #check for negative bet amount or exceeding their chip total
                                    print("\tinvalid amount of money, you have " + str(self.money) + " chips try inputting again")
                                else: 
                                    self.money -= amount    #remove money from self and add it to pot
                                    return amount
                                
                        elif checkRaise.lower() == "check" or checkRaise.lower() == "c":
                            return  #TODO implement check logic
                        else:
                            print("\tError, please input a valid action")
                else:
                    print("\tError, please input a valid action")
                


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
            
            # Rotating assignment of Blinds
            if i % 2 == 1:
                big_blind = self.activePlayers[0]
                small_blind = self.activePlayers[1]
            else:
                big_blind = self.activePlayers[1]
                small_blind = self.activePlayers[0] 

            # Initalize tracking variable
            highestBet = 0

            # Handle Blind logic
            if small_blind.money < 1:
                self.winner(big_blind)
            else:
                small_blind.money -= 1
                self.pot += 1

            if big_blind.money < 2:
                if big_blind.money == 0:
                    self.winner(small_blind)
                else:
                    big_blind.money -= 1
                    self.pot += 1
                    highestBet = 1
            else:
                big_blind.money -= 2
                self.pot += 2  
                highestBet = 2 

            #Pre dealing logic
            print("Pre Flop Betting")
                #TODO implement
            print("***********************\n")


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
