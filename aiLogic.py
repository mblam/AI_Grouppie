from treys import Card
from treys import Evaluator
from treys import Deck
import random
import pkgutil

DEBUG = False

# Adds debug statements that are toggleable through the DEBUG variable
# If termcolor is installed, these statements will be colored for easy visability
# If termcolor isn't installed, they will be printed normally, just with "Debug: " in front
if DEBUG:
    if pkgutil.find_loader('termcolor') is not None:
        from termcolor import colored
    else:
        def colored(string, color): return string
    def debug(text, color="magenta"): print(colored("Debug: "+str(text), color))
else:
    def debug(text, color=None): pass

"""
Player members for reference
    self.hand = []
    self.name = name
    self.money = STARTING_AMOUNT
    self.AIPlayer = ai
    self.bet = 0
    self.color = color
"""

from enum import Enum
class HandStrength(Enum):
    STRONG = 0
    MEDIUM = 1
    WEAK   = 2

class State:
    def __init__(self, player, highestBet, preFlop, board, min_to_play):
        self.currentBet = player.bet
        self.remainingMoney = player.money
        self.startingMoney = player.money_at_round_start
        self.hand = player.hand
        self.highestBet = highestBet
        self.preFlop = preFlop
        self.board = board
        self.min_to_play = min_to_play
    def new_action(self, amount_to_bet):
        raise Exception("Function not defined")

    def generate_successors(self):
        raise Exception("Function not defined")

    @staticmethod
    def probablility_of_winning(hand, board):
        hand_value = Evaluator().evaluate(hand, board)
        probability = 1 - Evaluator().get_five_card_rank_percentage(hand_value)

        return probability

    '''Takes the amount of money that the player had at the start of this round, and  multiplies that by the 
    probability of the current hand winning. The AI will then bet a random number between the minimum amount to play 
    the round, and that previously calculated value. This will result in the AI betting less if it has a bad hand, 
    and betting more if it has a good hand. '''
    def bet_up_to_probability(self, probability = None):
        if probability is None:
            probability = self.probablility_of_winning(self.hand, self.board)
        max_willing = int(self.startingMoney * probability) - self.currentBet
        if max_willing <= self.min_to_play:
            return -1
        else:
            return random.randrange(self.min_to_play, max_willing) - self.min_to_play

    def evaluate_GTO_bet(self):
        probability = self.probablility_of_winning(self.hand, self.board)

        if probability >= .67:      # Strong hand
            # Always bet
            return self.bet_up_to_probability()
        else:
            potential_probability = self.expected_final_hand(None)
            percent_increase = (potential_probability - probability) / probability
            if probability <= .33:    # Weak hand
                # If it has good potential, bet anyway
                if percent_increase >= .5: # TODO: Figure out a reasoning for this value
                    return self.bet_up_to_probability(potential_probability)
                # Fold
                else:
                    return -1
            else:                       # Medium hand
                # If it has good potential, bet anyway
                if percent_increase >= .33: # TODO: Figure out a reasoning for this value
                    return self.bet_up_to_probability(potential_probability)
                # Fold
                else:
                    return -1

    '''Uses an expectimax tree to determine what the probability of winning is going to be once all cards are put on 
    the board. Takes the hand and the current state of the board, then goes through every permutation of cards that 
    could be drawn. It takes the probability of those cards being drawn multiplied by the probability of winning with 
    that drawing, using total probability to calculate the overall chances of winning with the current hand. This 
    will help determine how much potential a hand has, because if a given board state has nothing good, but it's only 
    one card away from a really good hand, then this will reflect that and produce a higher score than for a bad hand 
    with no potential to get better. '''
    def expected_final_hand(self, potentialBoard):
        debug("Current Hand: "+str(self.hand))
        debug("Potential Board: "+str(potentialBoard))
        if potentialBoard is None:
            potentialBoard = self.board

        if len(potentialBoard) == 5:
            return self.probablility_of_winning(self.hand, potentialBoard)

        total = 0

        # Create a deck with only valid cards to pull from
        futureCards = Deck.GetFullDeck()
        for card in self.hand:
            futureCards.remove(card)
        for card in potentialBoard:
            futureCards.remove(card)

        # Go through every card and see what the probability is of winning with that board
        for card in futureCards:
            tempBoard = potentialBoard.copy()
            tempBoard.append(card)
            total += 1/len(futureCards) * self.expected_final_hand(tempBoard)

        return total




# NOTE: probably going to try and implement an expectimax tree to determine what action should be taken
# TODO: create a state object
# TODO: create evaluation function
    # TODO: cost should be (probability of winning * amount going to bet) - (probability of losing * amount already bet)
        # Probably going to update this formula as we go along
    # After this is implemented, maybe also account for the potential of that hand to get better
        # i.e. a hand that's one card away from a flush is better than completely random
# TODO: Actually traverse the tree and pick the best path


# Function being called within the actual game
# Only handles the valid value checking
# Actual logic to decide what should be done will be implemented in another function
def aiBetting(player, highestBet: int, preFlop: bool, board) -> int:
    debug(f"Highest: {highestBet}")
    debug(f"Bet: {player.bet}")
    debug(f"Money: {player.money}")
    max_to_play = player.money
    min_to_play = highestBet - player.bet

    # Calls the blinds, don't need logic for this
    if len(board) == 0:
        return min_to_play

    initial_state = State(player, highestBet, preFlop, board, min_to_play)
    amount = GTO(initial_state) # THIS IS THE ONLY PART OF THE FUNCTION THAT SHOULD BE ALTERED

    if amount > max_to_play:    # bound to upper limit
        return max_to_play
    elif amount < min_to_play:  # fold if below lower limit
        return -1
    else:                       # return calculated value if valid
        return amount


# Option 1: always give up
def alwaysFold(initial_state: State) -> int:
    return -1


# Option 2: always match the other player's bet
def alwaysCall(initial_state: State) -> int:
    return initial_state.highestBet - initial_state.currentBet


# Option 3: bet a random amount up to a ceiling based on the probability of the hand winning
def randomToLimit(initial_state: State) -> int:
    return initial_state.bet_up_to_probability()

# Option 4: Use Game Theory Optimal to determine the best move in the current situation
def GTO(initial_state: State) -> int:
    return initial_state.evaluate_GTO_bet()

