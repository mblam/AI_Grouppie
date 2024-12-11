import treys
from treys import Card
from treys import Evaluator
from treys import Deck
import Chip
import sys
from aiLogic import aiBetting
import printingDefs as printer

STARTING_AMOUNT = 50
BIG_BLIND_AMOUNT = 2
SMALL_BLIND_AMOUNT = 1

class Player:
    def __init__(self, name, ai=False, color=None):
        self.hand = []
        self.name = name
        self.money = STARTING_AMOUNT
        self.money_at_round_start = self.money
        self.AIPlayer = ai
        self.bet = 0
        self.color = color
        self.prev_bet = self.bet
        if ai: self.name += " (AI)"

    def getCard(self, card):
        self.hand.append(card)

    def printHand(self):
        Card.print_pretty_cards(self.hand)

    def betting(self, highestBet, board, preFlop=False):
        self.prev_bet = self.bet
        # Handle the logic if the player is being controlled by the AI
        if self.AIPlayer:
            # AI logic
            amount = aiBetting(self, highestBet, preFlop, board)

            if amount == -1:  # Short circuit if folding
                return amount
            else:  # Modify class members appropriately
                self.bet += amount
                self.money -= amount
                return self.bet

        print("Hand" + ": ", end="")
        self.printHand()
        print(f"\tYou have {self.money} chips.")
        print(f"\tThe highest bet is {highestBet} chips.")
        
        # Display current bet made by the player
        print(f"\tYou have bet {self.bet} chips this round.")

        while True:
            if self.money <= highestBet - self.bet:
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
                        return 0  # Player checks, returns how much the player increased the bet
                elif action.lower() in ["ca", "call"]:
                    amount_to_call = highestBet - self.bet
                    self.money -= amount_to_call
                    printer.debug(self.money)
                    self.bet = highestBet  # Update current bet to match the highest
                    print(f"\t{self.name} calls {amount_to_call} chips.")
                    return amount_to_call  # Player calls, returns the difference the player added
                elif action.lower() in ["r", "raise"]:
                    while True:
                        amount = int(input("\tHow much would you like to raise: "))
                        if amount + self.bet <= highestBet or amount > self.money:
                            print("\tYou must raise up to more than the current highest bet and not exceed your total chips.")
                        else:
                            self.money -= amount
                            self.bet += amount  # Update the current bet with the raise amount
                            print(f"\t{self.name} raises to {self.bet} chips.")
                            if preFlop:    # handles the money they already put up on the preflop
                                return amount
                            return amount  # Player raises, returns the difference the player added
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
    def initializePlayers(self, numPlayers, numAI):
        if numPlayers <= 0:
            sys.tracebacklimit = 0
            raise Exception("Invalid number of players")

        for i in range(numPlayers):
            if i < numAI:
                self.allPlayers.append(Player("Player "+str(i + 1), True, color="blue"))
            else:
                self.allPlayers.append(Player("Player " + str(i + 1), False, color="red"))
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
        printer.debug(player.money)

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
        players_in_round = [player for player in self.activePlayers]
        folded_players = set()
        current_player_index = self.rotator

        while True:
            print("Pot:",self.pot)
            current_player = players_in_round[current_player_index]

            # Skip player if they folded
            if current_player in folded_players:
                current_player_index = (current_player_index + 1) % 2  # Only two players
                continue

            print()
            print(printer.colored(f"{current_player.name}'s turn:", current_player.color))
            # Simply skips the current player if they don't have any money to bet
            if current_player.money == 0:
                print(f"You have 0 chips and cannot make a play.")
            # Otherwise, bet as normal
            else:
                if not preFlop:  # Print board if cards are on board
                    print("Cards on the table: ", end="")
                    Card.print_pretty_cards(self.board)

                bet = current_player.betting(highestBet, self.board, preFlop) # If increasing the bet, this represents the difference to the pot

                if bet == -1:  # Player folds
                    folded_players.add(current_player)
                    print(f"{current_player.name} folds.")
                    # The other player wins
                    remaining_player = players_in_round[1 - current_player_index]
                    print(f"{remaining_player.name} wins, {current_player.name} folded.")
                    self.winner(remaining_player)
                    return -1
                elif bet + current_player.prev_bet > highestBet:  # Player raises
                    # Update the pot with the amount of the raise
                    self.pot += bet  # Add the difference between new bet and previous bet
                    highestBet = bet + current_player.prev_bet  # Update the highest bet to the new raise
                    print(f"{current_player.name} raises to {highestBet} chips.")
                else:  # Player calls or checks
                    if bet != 0:  # They are calling the difference
                        call_amount = bet
                        self.pot += call_amount  # Accumulate the pot with the call amount
                        print(f"{current_player.name} calls {call_amount} chips.")
                    else:
                        print(f"{current_player.name} checks.")

                # Ensure the player's bet is updated correctly, already updated by calling betting
                # current_player.bet = highestBet  # Match the highest bet

            # Move to the next player
            current_player_index = (current_player_index + 1) % 2  # Toggle between 0 and 1

            # Check for end of betting round
            if current_player_index == 0:  # If it returns to the first player
                # Both players must have matched the highest bet
                if players_in_round[0].bet == players_in_round[1].bet:
                    print("Both players have matched the highest bet, betting round complete.")
                    return highestBet
                # Prevents an infinite loop where both players are out of money
                elif players_in_round[0].money == 0 and players_in_round[1].money == 0:
                    print("Both players are out of money, betting round complete.")
                    return highestBet



    def startRound(self):
        # Set up initial values
        print("Starting the game")
        self.activePlayers = self.allPlayers.copy()
        self.pot = 0

        # Error catching
        for player in self.activePlayers:
            player.bet = 0
            player.money_at_round_start = player.money

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

                printer.debug(str(self.pot)+"!")
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
                highestBet = 0  # Reset the highest bet for each new round
                highestBet = self.rotate_betting(highestBet)
                for player in self.activePlayers:
                    player.bet = 0 # Reset the current bet for each player
                if highestBet == -1:
                    self.rotator = (self.rotator + 1) % 2
                    return
                printer.debug(self.pot)


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

            # Break out of the game loop if either of the players runs out of money
            for player in self.allPlayers:
                if player.money == 0:
                    print(f"{player.name} is out of chips. Game over!")
                    done = True
            if 'done' in locals() and done:
                break

            again = input("Would you like to play again (y/n): ").lower()

            if again == "n" or again == "no":
                break
            elif again == "y" or again == "yes":
                continue
            else:
                print("Invalid response. Exiting.")
                break

        print("\n\nHere are the overall results: ")
        for player in self.allPlayers:
            print("\t",end="")
            # TODO make this print something useful


# -------------------------Initialization-------------------------------
if __name__ == "__main__":
    t = Table()
    t.initializePlayers(2, 0)
    t.startGame()
