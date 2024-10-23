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
        self.bet = 0

    def getCard(self, card):
        self.hand.append(card)

    def printHand(self):
        Card.print_pretty_cards(self.hand)

    def betting(self, highestBet, preFlop=False):

        print("Hand" + ": ", end="")
        self.printHand()
        print(f"\tYou have {self.money} chips.")
        print(f"\tThe highest bet is {highestBet} chips.")
        
        # Display current bet made by the player
        print(f"\tYou have bet {self.bet} chips this round.")

        while True:
            if self.money <= highestBet:
                print("\tYou can either fold or go all-in.")
                choice = input("\tWould you like to go all-in [a] or fold [f]: ")
                if choice.lower() in ["a", "all-in"]:
                    amount = self.money
                    self.bet += amount  # Update bet with the amount going all-in
                    self.money = 0
                    print(f"\t{self.name} goes all-in for {amount} chips.")
                    return amount  # Player goes all-in
                elif choice.lower() in ["f", "fold"]:
                    return -1  # Player folds
                else:
                    print("\tInvalid choice, please try again.")
            else:
                action = input("\tWould you like to check [c], call [ca], raise [r], or fold [f]: ")
                if action.lower() in ["c", "check"]:
                    if highestBet > 0 and highestBet != self.bet:
                        print("\tYou cannot check, there is already a bet.")
                    else:
                        print(f"\t{self.name} checks.")
                        return 0  # Player checks
                elif action.lower() in ["ca", "call"]:
                    amount_to_call = highestBet - self.bet
                    self.money -= amount_to_call
                    print(self.money)
                    self.bet = highestBet  # Update current bet to match the highest
                    print(f"\t{self.name} calls {amount_to_call} chips.")
                    return highestBet  # Player calls
                elif action.lower() in ["r", "raise"]:
                    while True:
                        amount = int(input("\tHow much would you like to raise: "))
                        if amount <= highestBet or amount > self.money:
                            print("\tYou must raise more than the current highest bet and not exceed your total chips.")
                        else:
                            self.money -= amount
                            self.bet += amount  # Update the current bet with the raise amount
                            highestBet = self.bet  # Update highestBet
                            print(f"\t{self.name} raises to {self.bet} chips.")
                            if preFlop:    # handles the money they already put up on the preflop
                                return self.bet
                            return amount  # Player raises
                elif action.lower() in ["f", "fold"]:
                    print(f"\t{self.name} folds.")
                    return -1  # Player folds
                else:
                    print("\tInvalid action, please try again.")

# Object that represents the overall state of the game
class Table():
    # Initializes the deck, list of cards on the board, and list of players
    def __init__(self):
        self.deck = Deck()
        self.board = []
        self.allPlayers = []
        self.activePlayers = []
        self.pot = 0
        self.evaluator = Evaluator()
        self.bigBlind = None
        self.smallBlind = None
        self.rotator = 0

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
        player.money += self.pot
        print(player.name + " wins $" + str(self.pot))
        print(player.money)

    def blindBetting(self, smallBlind, bigBlind):
        highestBet = 0

        # Handle Small Blind
        if smallBlind.money < SMALL_BLIND_AMOUNT:
            print(f"{smallBlind.name} cannot post small blind, they are all-in.")
            highestBet = smallBlind.money
            smallBlind.bet = smallBlind.money
            self.pot += highestBet
            smallBlind.money = 0
        else:
            highestBet = SMALL_BLIND_AMOUNT
            smallBlind.bet = SMALL_BLIND_AMOUNT
            smallBlind.money -= SMALL_BLIND_AMOUNT
            self.pot += SMALL_BLIND_AMOUNT

        # Handle Big Blind
        if bigBlind.money < BIG_BLIND_AMOUNT:
            print(f"{bigBlind.name} cannot post big blind, they are all-in.")
            highestBet = max(highestBet, bigBlind.money)  # Ensure highestBet is updated correctly
            bigBlind.bet = bigBlind.money
            self.pot += bigBlind.money
            bigBlind.money = 0
        else:
            bigBlind.bet = BIG_BLIND_AMOUNT
            bigBlind.money -= BIG_BLIND_AMOUNT
            self.pot += BIG_BLIND_AMOUNT
            highestBet = BIG_BLIND_AMOUNT  # Set highestBet to the big blind amount

        return highestBet

    def rotate_betting(self, highestBet, preFlop=False):
        # Get the two active players
        players_in_round = [player for player in self.activePlayers if player.money > 0]
        folded_players = set()
        current_player_index = self.rotator

        while True:
            print(self.pot)
            current_player = players_in_round[current_player_index]

            # Skip player if they folded
            if current_player in folded_players:
                current_player_index = (current_player_index + 1) % 2  # Only two players
                continue

            print(f"{current_player.name}'s turn:")

            if not preFlop:  # Print board if cards are on board
                print("Cards on the table: ", end="")
                Card.print_pretty_cards(self.board)

            bet = current_player.betting(highestBet, preFlop)

            if bet == -1:  # Player folds
                folded_players.add(current_player)
                print(f"{current_player.name} folds.")
                # The other player wins
                remaining_player = players_in_round[1 - current_player_index]
                print(f"{remaining_player.name} wins, {current_player.name} folded.")
                if not preFlop and not highestBet == 2:
                    self.pot += highestBet
                self.winner(remaining_player)
                return -1
            elif bet > highestBet:  # Player raises
                # Update the pot with the amount of the raise
                self.pot += bet - current_player.bet  # Add the difference between new bet and previous bet
                highestBet = bet  # Update the highest bet to the new raise
                print(f"{current_player.name} raises to {bet} chips.")
            elif bet == 2 and preFlop and current_player == self.smallBlind:  # Edge case where pot doesnt increase when calling big blind
                self.pot += 1
            else:  # Player calls or checks
                if bet < highestBet:  # They are calling the difference
                    call_amount = highestBet - current_player.bet
                    self.pot += call_amount  # Accumulate the pot with the call amount
                    print(f"{current_player.name} calls {call_amount} chips.")
                else:
                    print(f"{current_player.name} checks.")

            # Ensure the player's bet is updated correctly
            current_player.bet = highestBet  # Match the highest bet

            # Move to the next player
            current_player_index = (current_player_index + 1) % 2  # Toggle between 0 and 1

            # Check for end of betting round
            if current_player_index == 0:  # If it returns to the first player
                # Both players must have matched the highest bet
                if players_in_round[0].bet == players_in_round[1].bet:
                    print("Both players have matched the highest bet, betting round complete.")
                    return highestBet



    def startRound(self):
        # Set up initial values
        print("Starting the game")
        self.activePlayers = self.allPlayers.copy()
        self.pot = 0

        # Error catching
        for player in self.activePlayers:
            player.bet = 0

        for i in range(4):
            print()
            print("***********************")

            if i == 0:
                self.smallBlind = self.activePlayers[self.rotator]
                self.bigBlind = self.activePlayers[(self.rotator + 1) % len(self.activePlayers)]
                highestBet = self.blindBetting(self.smallBlind, self.bigBlind)

                if highestBet == -1:
                    self.rotator = (self.rotator + 1) % 2
                    return  # Game ends

                print(str(self.pot)+"!")
                print("Pre-Flop Betting")
                highestBet = self.rotate_betting(highestBet, preFlop=True)
                if highestBet == -1:
                    self.rotator = (self.rotator + 1) % 2
                    return

                for player in self.activePlayers:
                    player.bet = 0

            # Dealing logic for flop, turn, and river
            match i:
                case 1:
                    print("Dealing the flop")
                    self.dealFirstRound()
                case 2:
                    print("Dealing the turn")
                    self.dealSecondRound()
                case 3:
                    print("Dealing the river")
                    self.dealThirdRound()

            print("***********************\n")

            # Normal post-flop betting (post-flop, turn, river)
            if i != 0:
                print(f"Post-flop betting round {i}")
                highestBet = 0  # Reset highest bet for each new round
                highestBet = self.rotate_betting(highestBet)
                if highestBet == -1:
                    self.rotator = (self.rotator + 1) % 2
                    return
                self.pot += highestBet* 2
                print(self.pot)


            # Evaluate hands and declare the winner after river round
            if i == 3:  # After the river, evaluate hands
                hands = {}
                for player in self.activePlayers:
                    handValue = self.evaluator.evaluate(player.hand, self.board)
                    hands[handValue] = player

                # The best hand wins (lower values mean better hands in poker evaluation)
                # TODO have this print who won with what hand
                bestHand = min(hands.keys())
                self.winner(hands[bestHand])
                self.rotator = (self.rotator + 1) % 2

            # End of the current betting round  

    def startGame(self):
        while True:
            self.startRound()

            again = input("Would you like to play again (y/n): ").lower()

            if again == "y" or again == "yes":
                continue
            else:
                print("\n\nHere are the overall results: ")
                for player in self.allPlayers:
                    print("\t",end="")
                    # TODO make this print something useful
                return

# -------------------------Initialization-------------------------------
t = Table()
t.initializePlayers(2)
t.startGame()
