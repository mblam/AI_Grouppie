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

    def evaluate(self):
        if len(self.board) == 0:
            return self.min_to_play
        hand_value = Evaluator().evaluate(self.hand, self.board)
        probability = 1 - Evaluator().get_five_card_rank_percentage(hand_value)
        max_willing = int(self.startingMoney * probability) - self.currentBet
        if max_willing <= self.min_to_play:
            return -1
        else:
            return random.randrange(self.min_to_play, max_willing) - self.min_to_play

    def new_action(self, amount_to_bet):
        raise Exception("Function not defined")

    def generate_successors(self):
        raise Exception("Function not defined")



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
    return initial_state.evaluate()

