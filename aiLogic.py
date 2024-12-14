from treys import Card
from treys import Evaluator
from treys import Deck
import random
import printingDefs as printer

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

    '''
    Takes the amount of money that the player had at the start of this round, and  multiplies that by the 
    probability of the current hand winning. The AI will then bet a random number between the minimum amount to play 
    the round, and that previously calculated value. This will result in the AI betting less if it has a bad hand, 
    and betting more if it has a good hand.
    '''

    def bet_up_to_probability(self, probability=None):
        if probability is None:
            probability = self.probablility_of_winning(self.hand, self.board)
        max_willing = int(self.startingMoney * probability) - self.currentBet
        if max_willing <= self.min_to_play:
            return -1
        else:
            return random.randrange(self.min_to_play, max_willing) - self.min_to_play

    def evaluate_GTO_bet(self):
        probability = self.probablility_of_winning(self.hand, self.board)

        bet = 0

        if probability >= .55:  # Strong hand
            # Always bet
            bet = self.bet_up_to_probability()
        else:
            potential_probability = self.expected_final_hand(None)
            percent_increase = (potential_probability - probability) / probability

            if probability <= .45:  # Weak hand
                # If it has good potential, bet anyway
                if percent_increase >= .2:
                    bet = self.bet_up_to_probability(potential_probability)
                # Fold
                else:
                    bet = -1
            else:  # Medium hand
                # If it has good potential, bet anyway
                if percent_increase >= .05:
                    bet = self.bet_up_to_probability(potential_probability)
                # Fold
                else:
                    bet = -1

        # Temper the bet if it's determined that the chances of winning are based on just the table cards
        if self.best_on_table() and bet > 0:
            bet = bet - (bet - self.min_to_play)/2

        return bet

    '''
    Uses an expectimax tree to determine what the probability of winning is going to be once all cards are put on 
    the board. Takes the hand and the current state of the board, then goes through every permutation of cards that 
    could be drawn. It takes the probability of those cards being drawn multiplied by the probability of winning with 
    that drawing, using total probability to calculate the overall chances of winning with the current hand. This 
    will help determine how much potential a hand has, because if a given board state has nothing good, but it's only 
    one card away from a really good hand, then this will reflect that and produce a higher score than for a bad hand 
    with no potential to get better.
    '''

    def expected_final_hand(self, potentialBoard):
        printer.debug("Current Hand: " + str(self.hand))
        printer.debug("Potential Board: " + str(potentialBoard))
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
            total += 1 / len(futureCards) * self.expected_final_hand(tempBoard)

        return total

    '''
    Determines whether the majority of the probability of having a winning hand is solely based on the cards on 
    the table. If this is the case, then the opposing player also has at least those odds of winning, making our hand 
    not nearly as strong as it first appears. When running test runs before this project, when the best hand for all 
    players was the one on the table, then all of their percentages of how good their hands were were within 1 
    percent of each other. This threshold is used to compare the current probability with the expected probability 
    with a random hand to determine whether the best cards are all coming from the communal cards on the table. 
    '''
    def best_on_table(self):
        # Gets the probability of winning with the current hand
        current_prob = self.probablility_of_winning(self.hand, self.board)

        avg_prob = 0

        # Gets the probability of winning with essentially a random hand
        for idx in range(2):
            for card in Deck().cards:
                tempHand = self.hand.copy()
                tempHand[idx] = card
                avg_prob += self.probablility_of_winning(tempHand, self.board) * (1/2*52)

        # If the two probabilities are similar, return true
        return abs(avg_prob - current_prob) < .01




# Function being called within the actual game
# Only handles the valid value checking
# Actual logic to decide what should be done is implemented in another function
def aiBetting(player, highestBet: int, preFlop: bool, board) -> int:
    printer.debug(f"Highest: {highestBet}")
    printer.debug(f"Bet: {player.bet}")
    printer.debug(f"Money: {player.money}")
    max_to_play = player.money
    min_to_play = highestBet - player.bet

    # Calls the blinds, don't need logic for this
    if len(board) == 0:
        return min_to_play

    initial_state = State(player, highestBet, preFlop, board, min_to_play)
    amount = GTO(initial_state)  # THIS IS THE ONLY PART OF THE FUNCTION THAT SHOULD BE ALTERED

    if amount > max_to_play:  # bound to upper limit
        bet = max_to_play
    elif amount < min_to_play:  # fold if below lower limit
        bet = -1
    else:  # return calculated value if valid
        bet = amount

    # If the AI was going to fold, but they don't need to add any money to the pot to play, then it's more
    # advantageous to check and see what happens. Can always fold again later, so there's only the possibility to win
    # more money without any additional risk
    if bet == -1 and highestBet == 0:
        bet = 0

    return bet


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
