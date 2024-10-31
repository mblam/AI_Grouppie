from treys import Card
from treys import Evaluator
from treys import Deck

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
def aiBetting(player, highestBet: int, preFlop: bool) -> int:
    debug(f"Highest: {highestBet}")
    debug(f"Bet: {player.bet}")
    debug(f"Money: {player.money}")
    max_to_play = player.money
    min_to_play = highestBet - player.bet

    amount = alwaysFold(player, highestBet, preFlop) # THIS IS THE ONLY PART OF THE FUNCTION THAT SHOULD BE ALTERED

    if amount > max_to_play:    # bound to upper limit
        return max_to_play
    elif amount < min_to_play:  # fold if below lower limit
        return -1
    else:                       # return calculated value if valid
        return amount


# Option 1: always give up
def alwaysFold(player, highestBet: int, preFlop: bool) -> int:
    return -1


# Option 2: always match the other player's bet
def alwaysCall(player, highestBet, preFlop: bool) -> int:
    return highestBet - player.bet

