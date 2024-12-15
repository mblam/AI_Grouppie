import treys
from treys import Card
from treys import Evaluator
from treys import Deck
import Chip
import sys
from aiLogic import aiBetting
import printingDefs as printer
import pygame
import pygame
import gameTest as gameTest
import display.cardDisplay as cd
import time

STARTING_AMOUNT = 50
BIG_BLIND_AMOUNT = 2
SMALL_BLIND_AMOUNT = 1

black = (0, 0, 0)
brown = (111, 78, 55)
green = (53, 101, 73)
white = (255, 255, 255)

gameState = gameTest.gameTest()

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
        self.font = pygame.font.SysFont(None, 24)
        self.display = []

    def getCard(self, card):
        self.hand.append(card)

    def printHand(self):
        Card.print_pretty_cards(self.hand)
        
    def getCurrCards(self):
        for singleCard in self.hand:
            self.display.append(Card.int_to_str(singleCard))

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
                #error occurs around here
                return self.bet

        print("Hand" + ": ", end="")
        self.printHand()
        self.getCurrCards()
        cd.printPlayerHand(self.name, self.display, self.money)
        print(f"\tYou have {self.money} chips.")
        print(f"\tThe highest bet is {highestBet} chips.")
        # Display current bet made by the player
        print(f"\tYou have bet {self.bet} chips this round.")
        
        #pygame display
        pygame.draw.rect(pygame.display.get_surface(), green, (1200, 50, 250, 15))
        text = self.font.render(f"You have {self.money} chips.", True, white)
        pygame.display.get_surface().blit(text, (1200, 50))
        pygame.draw.rect(pygame.display.get_surface(), green, (1200, 70, 250, 15))
        text = self.font.render(f"The highest bet is {highestBet} chips.", True, white)
        pygame.display.get_surface().blit(text, (1200, 70))
        pygame.draw.rect(pygame.display.get_surface(), green, (1200, 90, 250, 15))
        text = self.font.render(f"You have bet {self.bet} chips this round.", True, white)
        pygame.display.get_surface().blit(text, (1200, 90))
        pygame.display.update()

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
                action = ""
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if gameState.Check.rect.collidepoint(event.pos):
                            action = "check"
                        elif gameState.Call.rect.collidepoint(event.pos):
                            action = "call"
                        elif gameState.Raise.rect.collidepoint(event.pos):
                            action = "raise"
                        elif gameState.Fold.rect.collidepoint(event.pos):
                            action = "fold"
                if action == "check":
                    if highestBet > 0 and highestBet != self.bet:
                        text = self.font.render("You cannot check, there is already a bet.", True, black)
                        pygame.display.get_surface().blit(text, (680, 30))
                        pygame.display.update()
                    else:
                        text = self.font.render(f"{self.name} checks.", True, black)
                        pygame.display.get_surface().blit(text, (680, 30))
                        pygame.display.update()
                        return 0 # Player checks, returns how much the player increased the bet
                elif action == "call":
                    amount_to_call = highestBet - self.bet
                    self.money -= amount_to_call
                    self.bet = highestBet  # Update current bet to match the highest
                    chip_text = self.font.render(f"{self.name} calls {amount_to_call} chips.", True, black)
                    if self.name == "Player 1":
                        pygame.draw.rect(pygame.display.get_surface(), brown, (25, 720, 200, 15))
                        text = self.font.render("Player 1\'s Earnings: " + f"{self.money}", True, black)
                        pygame.display.get_surface().blit(text, (25, 720))
                        pygame.display.update()
                    else:
                        pygame.draw.rect(pygame.display.get_surface(), brown, (25, 20, 200, 15))
                        text = self.font.render("Player 2\'s Earnings: " + f"{self.money}", True, black)
                        pygame.display.get_surface().blit(text, (25, 20))
                    pygame.display.get_surface().blit(chip_text, (680, 30))
                    pygame.display.update()
                    return highestBet  # Player calls
                #if they raise (raise the bet higher)
                elif action == "raise":
                    while True:
                        amount = int(input("\tHow much would you like to raise: "))
                        pygame.draw.rect(pygame.display.get_surface(), brown, (680, 30, 550, 15))
                        text = self.font.render("How much would you like to raise?", True, black)
                        pygame.display.get_surface().blit(text, (680, 30))
                        if amount <= highestBet or amount > self.money:
                            print("\tYou must raise more than the current highest bet and not exceed your total chips.")
                            pygame.draw.rect(pygame.display.get_surface(), brown, (680, 30, 550, 15))
                            text = self.font.render("You must raise more than the current highest bet and not exceed your total chips.", True, black)
                            pygame.display.get_surface().blit(text, (680, 30))
                        else:
                            self.money -= amount
                            self.bet += amount  # Update the current bet with the raise amount
                            highestBet = self.bet  # Update highestBet
                            pygame.draw.rect(pygame.display.get_surface(), brown, (680, 30, 550, 15))
                            text = self.font.render(f"{self.name} raises to {self.bet} chips.", True, black)
                            pygame.display.get_surface().blit(text, (680, 30))
                            if preFlop:    # handles the money they already put up on the preflop
                                return self.bet
                            if self.name == "Player 1":
                                pygame.draw.rect(pygame.display.get_surface(), brown, (25, 720, 200, 15))
                                text = self.font.render("Player 1\'s Earnings: " + f"{self.money}", True, black)
                                pygame.display.get_surface().blit(text, (25, 720))
                                pygame.display.update()
                            else:
                                pygame.draw.rect(pygame.display.get_surface(), brown, (25, 20, 200, 15))
                                text = self.font.render("Player 2\'s Earnings: " + f"{self.money}", True, black)
                                pygame.display.get_surface().blit(text, (25, 20))
                                pygame.display.update()
                            return amount  # Player raises
                # if they fold (they stop playing for the hand)
                elif action == "fold":
                    text = self.font.render(f"{self.name} folds.", True, black)
                    pygame.display.get_surface().blit(text, (680, 30))
                    pygame.display.update()
                    return -1  # Player folds
                elif action == "":
                    pass
                else:
                    text = self.font.render("Invalid action, please try again", True, black)
                    pygame.display.get_surface().blit(text, (1150, 50))
                    pygame.display.update()

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
        self.font = pygame.font.SysFont(None, 24)
        self.running = True

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
        cards = self.printCurrCards()
        cd.firstRoundBoard(cards)
            
    def dealSecondRound(self):
        burn = self.deck.draw(1)
        self.board.append(self.deck.draw(1)[0])
        cards = self.printCurrCards()
        cd.firstRoundBoard(cards)

    def dealThirdRound(self):
        self.board.append(self.deck.draw(1)[0])
        cards = self.printCurrCards()
        cd.firstRoundBoard(cards)
        
    def printCurrCards(self):
        cards = []
        for singleCard in self.board:
            cards.append(Card.int_to_str(singleCard))
        return cards
    
    def updatePot(self, newPot):
        pygame.draw.rect(pygame.display.get_surface(), green, (1245, 363, 200, 30))
        pot_font = pygame.font.SysFont(None, 36)
        main_pot = pot_font.render("The Pot: $" + str(newPot), True, white)
        pygame.display.get_surface().blit(main_pot, (1245, 363))
        pygame.display.update()
    
    def updateTextBelowPot(self, text):
        pygame.draw.rect(pygame.display.get_surface(), green, (1200, 400, 250, 100))
        pygame.display.get_surface().blit(text, (1200, 400))
        pygame.display.update()
    
    # Prints out the different players and their hands
    def printPlayers(self):
        for player in self.allPlayers:
            print(player.name + ": ", end="")
            player.printHand()

    # Game end state
    def winner(self, player):
        player.money += self.pot
        print(player.name + " wins $" + str(self.pot))
        text = self.font.render(player.name + " wins $" + str(self.pot), True, white)
        pygame.display.get_surface().blit(text, (500, 200))
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
            #reset all of the displays
            self.updateTextBelowPot(self.font.render("", True, white))
            pygame.draw.rect(pygame.display.get_surface(), brown, (680, 30, 550, 15))
            pygame.draw.rect(pygame.display.get_surface(), green, (1200, 50, 250, 15))
            pygame.draw.rect(pygame.display.get_surface(), green, (1200, 70, 250, 15))
            pygame.draw.rect(pygame.display.get_surface(), green, (1200, 90, 250, 15))
            
            print("Pot:",self.pot)
            self.updatePot(self.pot)
            current_player = players_in_round[current_player_index]

            # Skip player if they folded
            if current_player in folded_players:
                current_player_index = (current_player_index + 1) % 2  # Only two players
                continue

            print()
            time.sleep(1)
            print(printer.colored(f"{current_player.name}'s turn:", current_player.color))
            pygame.draw.rect(pygame.display.get_surface(), brown, (1300, 30, 200, 15))
            text = self.font.render(f"{current_player.name}'s turn", True, black)
            pygame.display.get_surface().blit(text, (1300, 30))
            # Simply skips the current player if they don't have any money to bet
            if current_player.money == 0:
                print(f"You have 0 chips and cannot make a play.")
                text = self.font.render("You have 0 chips and cannot make a play.", True, black)
                pygame.display.get_surface().blit(text, (680, 30))
                pygame.display.update()
            # Otherwise, bet as normal
            else:
                if not preFlop:  # Print board if cards are on board
                    print("Cards on the table: ", end="")
                    Card.print_pretty_cards(self.board)

                bet = current_player.betting(highestBet, self.board, preFlop) # If increasing the bet, this represents the difference to the pot
                
                if bet == -1:  # Player folds
                    folded_players.add(current_player)
                    print(f"{current_player.name} folds.")
                    text = self.font.render(f"{current_player.name} folds.", True, white)
                    self.updateTextBelowPot(text)
                    # The other player wins
                    remaining_player = players_in_round[1 - current_player_index]
                    print(f"{remaining_player.name} wins, {current_player.name} folded.")
                    text = self.font.render(f"{remaining_player.name} wins, {current_player.name} folded.", True, white)
                    self.updateTextBelowPot(text)
                    self.winner(remaining_player)
                    return -1
                elif bet + current_player.prev_bet > highestBet:  # Player raises
                    # Update the pot with the amount of the raise
                    self.pot += bet  # Add the difference between new bet and previous bet
                    self.updatePot(self.pot)
                    highestBet = bet + current_player.prev_bet  # Update the highest bet to the new raise
                    print(f"{current_player.name} raises to {highestBet} chips.")
                    text = self.font.render(f"{current_player.name} raises to {highestBet} chips.", True, white)
                    self.updateTextBelowPot(text)
                else:  # Player calls or checks
                    if bet != 0:  # They are calling the difference
                        call_amount = bet
                        self.pot += call_amount  # Accumulate the pot with the call amount
                        print(f"{current_player.name} calls {call_amount} chips.")
                        text = self.font.render(f"{current_player.name} calls {call_amount} chips.", True, white)
                        self.updateTextBelowPot(text)
                    else:
                        print(f"{current_player.name} checks.")
                        text = self.font.render(f"{current_player.name} checks.", True, white)
                        self.updateTextBelowPot(text)

                # Ensure the player's bet is updated correctly, already updated by calling betting
                # current_player.bet = highestBet  # Match the highest bet

            # Move to the next player
            current_player_index = (current_player_index + 1) % 2  # Toggle between 0 and 1

            # Check for end of betting round
            if current_player_index == 0:  # If it returns to the first player
                # Both players must have matched the highest bet
                if players_in_round[0].bet == players_in_round[1].bet:
                    time.sleep(1)
                    print("Both players have matched the highest bet, betting round complete.")
                    pygame.draw.rect(pygame.display.get_surface(), green, (1200, 400, 250, 100))
                    pygame.draw.rect(pygame.display.get_surface(), brown, (680, 30, 550, 15))
                    text = self.font.render("Both players have matched the highest bet, betting round complete.", True, black)
                    pygame.display.get_surface().blit(text, (680, 30))
                    time.sleep(2)
                    pygame.draw.rect(pygame.display.get_surface(), brown, (680, 30, 550, 15))
                    return highestBet
                # Prevents an infinite loop where both players are out of money
                elif players_in_round[0].money == 0 and players_in_round[1].money == 0:
                    time.sleep(1)
                    print("Both players are out of money, betting round complete.")
                    pygame.draw.rect(pygame.display.get_surface(), green, (1200, 400, 250, 100))
                    pygame.draw.rect(pygame.display.get_surface(), brown, (680, 30, 550, 15))
                    text = self.font.render("Both players have matched the highest bet, betting round complete.", True, black)
                    pygame.display.get_surface().blit(text, (680, 30))
                    time.sleep(2)
                    pygame.draw.rect(pygame.display.get_surface(), brown, (680, 30, 550, 15))
                    return highestBet
            time.sleep(2)



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
                text = self.font.render("Pre-Flop Betting", True, black)
                pygame.display.get_surface().blit(text, (680, 10))
                pygame.display.update()
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
                    pygame.draw.rect(pygame.display.get_surface(), brown, (680, 10, 130, 20))
                    text = self.font.render("Dealing the flop", True, black)
                    pygame.display.get_surface().blit(text, (680, 10))
                    cards = self.printCurrCards()
                    cd.firstRoundBoard(cards)
                    pygame.display.update()
                case 2:
                    print("Dealing the turn")
                    self.dealSecondRound()
                    pygame.draw.rect(pygame.display.get_surface(), brown, (680, 10, 130, 20))
                    text = self.font.render("Dealing the turn", True, black)
                    pygame.display.get_surface().blit(text, (680, 10))
                    cards = self.printCurrCards()
                    cd.secondRoundBoard(cards)
                    pygame.display.update()
                case 3:
                    print("Dealing the river")
                    self.dealThirdRound()
                    pygame.draw.rect(pygame.display.get_surface(), brown, (680, 10, 130, 20))
                    text = self.font.render("Dealing the river", True, black)
                    pygame.display.get_surface().blit(text, (680, 10))
                    cards = self.printCurrCards()
                    cd.thirdRoundBoard(cards)
                    pygame.display.update()

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
            
            gameState.startDisplay(self.pot)
            
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
    pygame.init()
    pygame.display.set_mode((1500, 750))
    t = Table()
    t.initializePlayers(2, 1)
    t.startGame()
