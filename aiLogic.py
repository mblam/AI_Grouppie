from treys import Card
from treys import Evaluator
from treys import Deck
import random

DEBUG = False

if DEBUG:
    from termcolor import colored
    def debug(text, color="magenta"): print(colored(text, color))
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

    def bet_up_to_probability(self):
        probability = self.probablility_of_winning(self.hand, self.board)
        max_willing = int(self.startingMoney * probability) - self.currentBet
        if max_willing <= self.min_to_play:
            return -1
        else:
            return random.randrange(self.min_to_play, max_willing) - self.min_to_play

    def evaluate_GTO_bet(self):
        probability = self.probablility_of_winning(self.hand, self.board)

        if probability >= .75:      # Strong hand
            pass
            # Always bet
        elif probability <= .25:    # Weak hand
            pass
            # Usually just check
                # Up until what point though???
            # Occassionally bet
                # this will be based on whether or not our cards block a good hand for the opponent
                # also based on the possibility for the hand to get better as more cards are flipped
                    # Create fresh deck, loop through all possible draws (recursive) and get expectimax from those values
        else:                       # Medium hand
            pass
            # Probably 50:50, same reasoning as for weak, just tweak the threshold for each of the decisions

    def expected_final_hand(self, potentialBoard):
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
    amount = randomToLimit(initial_state) # THIS IS THE ONLY PART OF THE FUNCTION THAT SHOULD BE ALTERED

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

def GTO(initial_state: State) -> int:
    pass

