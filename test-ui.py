import treys
from treys import Card
from treys import Evaluator
from treys import Deck
import Chip
import sys
import gameTest as gameTest
import pygame
import display.cardDisplay as cd
import asyncio

STARTING_AMOUNT = 50
BIG_BLIND_AMOUNT = 2
SMALL_BLIND_AMOUNT = 1

black = (0, 0, 0)
brown = (111, 78, 55)
green = (53, 101, 73)
white = (255, 255, 255)

gameState = gameTest.gameTest()

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
        self.display = []
        self.font = pygame.font.SysFont(None, 24)

    def getCard(self, card):
        self.hand.append(card)

    def printHand(self):
        Card.print_pretty_cards(self.hand)
    
    def getCurrCards(self):
        for singleCard in self.hand:
            self.display.append(Card.int_to_str(singleCard))

    #this is called in rotate betting
    #returns the amount of money that's being bet
    def betting(self, highestBet, preFlop=False):
        print("Hand" + ": ", end="")
        self.printHand()
        if len(self.display) == 0:
            self.getCurrCards()
            cd.printPlayerHand(self.name, self.display, self.money)
        print(f"\tYou have {self.money} chips.")
        print(f"\tThe highest bet is {highestBet} chips.")
        
        # Display current bet made by the player
        print(f"\tYou have bet {self.bet} chips this round.")

        while True:
            
            #This is for if they can't afford to bet any more
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
            #general betting
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
                #if they check (means they want to pass the action to the next player)
                if action == "check":
                    pygame.draw.rect(pygame.display.get_surface(), brown, (680, 30, 200, 15))
                    if highestBet > 0 and highestBet != self.bet:
                        pygame.draw.rect(pygame.display.get_surface(), brown, (680, 30, 200, 15))
                        text = self.font.render("\tYou cannot check, there is already a bet.", True, black)
                        pygame.display.get_surface().blit(text, (680, 30))
                    else:
                        text = self.font.render(f"{self.name} checks.", True, black)
                        pygame.display.get_surface().blit(text, (680, 30))
                        return 0  # Player checks
                #if they call (want to match a highest bet made by another player)
                elif action == "call":
                    amount_to_call = highestBet - self.bet
                    self.money -= amount_to_call
                    self.bet = highestBet  # Update current bet to match the highest
                    chip_text = self.font.render(f"{self.name} calls {amount_to_call} chips.", True, black)
                    if self.name == "Player 1":
                        pygame.draw.rect(pygame.display.get_surface(), brown, (25, 720, 200, 15))
                        text = self.font.render("Player 1\'s Earnings: " + f"{self.money}", True, black)
                        pygame.display.get_surface().blit(text, (25, 720))
                    else:
                        pygame.draw.rect(pygame.display.get_surface(), brown, (25, 20, 200, 15))
                        text = self.font.render("Player 2\'s Earnings: " + f"{self.money}", True, black)
                        pygame.display.get_surface().blit(text, (25, 20))
                    pygame.draw.rect(pygame.display.get_surface(), brown, (680, 30, 200, 15))
                    pygame.display.get_surface().blit(chip_text, (680, 30))
                    pygame.display.update()
                    return highestBet  # Player calls
                #if they raise (raise the bet higher)
                elif action == "raise":
                    pygame.draw.rect(pygame.display.get_surface(), brown, (680, 30, 200, 15))
                    while True:
                        amount = int(input("\tHow much would you like to raise: "))
                        if amount <= highestBet or amount > self.money:
                            print("\tYou must raise more than the current highest bet and not exceed your total chips.")
                        else:
                            self.money -= amount
                            self.bet += amount  # Update the current bet with the raise amount
                            highestBet = self.bet  # Update highestBet
                            text = self.font.render(f"{self.name} raises to {self.bet} chips.", True, black)
                            pygame.display.get_surface().blit(text, (680, 30))
                            if preFlop:    # handles the money they already put up on the preflop
                                return self.bet
                            if self.name == "Player 1":
                                pygame.draw.rect(pygame.display.get_surface(), brown, (25, 720, 200, 15))
                                text = self.font.render("Player 1\'s Earnings: " + f"{self.money}", True, black)
                                pygame.display.get_surface().blit(text, (25, 720))
                            else:
                                pygame.draw.rect(pygame.display.get_surface(), brown, (25, 20, 200, 15))
                                text = self.font.render("Player 2\'s Earnings: " + f"{self.money}", True, black)
                                pygame.display.get_surface().blit(text, (25, 20))
                            return amount  # Player raises
                # if they fold (they stop playing for the hand)
                elif action == "fold":
                    pygame.draw.rect(pygame.display.get_surface(), brown, (680, 30, 200, 15))
                    text = self.font.render(f"{self.name} folds.", True, black)
                    pygame.display.get_surface().update(text, (680, 30))
                    return -1  # Player folds
                else:
                    text = self.font.render("Invalid action, please try again", True, black)
                    pygame.display.get_surface().blit(text, (1150, 50))

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

    #how the betting starts 
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

            
            pygame.draw.rect(pygame.display.get_surface(), brown, (1200, 30, 200, 15))
            text = self.font.render(f"{current_player.name}'s turn", True, black)
            pygame.display.get_surface().blit(text, (1200, 30))
            

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


    #this is where the game starts 
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

            #This is for Pre-Flop
            if i == 0:
                self.smallBlind = self.activePlayers[self.rotator]
                self.bigBlind = self.activePlayers[(self.rotator + 1) % len(self.activePlayers)]
                highestBet = self.blindBetting(self.smallBlind, self.bigBlind)

                if highestBet == -1:
                    self.rotator = (self.rotator + 1) % 2
                    return  # Game ends

                print(str(self.pot)+"!")
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
                    pygame.draw.rect(pygame.display.get_surface(), brown, (680, 10, 130, 20))
                    text = self.font.render("Dealing the flop", True, black)
                    pygame.display.get_surface().blit(text, (680, 10))
                    self.dealFirstRound()
                case 2:
                    pygame.draw.rect(pygame.display.get_surface(), brown, (680, 10, 130, 20))
                    text = self.font.render("Dealing the turn", True, black)
                    pygame.display.get_surface().blit(text, (680, 10))
                    pygame.display.update()
                    self.dealSecondRound()
                case 3:
                    pygame.draw.rect(pygame.display.get_surface(), brown, (680, 10, 130, 20))
                    text = self.font.render("Dealing the river", True, black)
                    pygame.display.get_surface().blit(text, (680, 10))
                    pygame.display.update()
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
        
        while self.running:
            
            gameState.startDisplay(self.pot)
            
            self.startRound()
            
            again = input("Would you like to play again (y/n): ").lower()
            
            # Did the user click the window close button?
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            if again == "y" or again == "yes":
                continue
            else:
                print("\n\nHere are the overall results: ")
                for player in self.allPlayers:
                    print("\t",end="")
                    # TODO make this print something useful
                    self.running = False
                
    # Done! Time to quit.
    gameTest.pygame.quit()

# -------------------------Initialization-------------------------------
pygame.init()
pygame.display.set_mode((1500, 750))
t = Table()
t.initializePlayers(2)
t.startGame()
