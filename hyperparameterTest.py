from model import Player
from treys import Card
from aiLogic import aiBetting

'''
This file allows us to manually send in the current state of the user's hand, the board, and the highest bet state 
to force AI decisions on specific setups. This is intended to be used when playing test games online to get data on 
how well our AI is performing against an established AI. 

The user will manually input what they see on their end (the hand and current board state). The program will then 
print out how much the AI says the user should raise in their game. The user can then use this information to play 
against an online poker bot. By keeping track of how well our bot does on each game with the current hyperparameters 
set, we can start to get a feeling for whether out bot is good or bad. 
'''

def getInput(pf):
    while True:
        hb = int(input("current highest bet (-1 to exit): "))

        if hb == -1:
            break
        else:
            num = aiBetting(example, hb, pf, board)
            if num > 0:
                example.bet += num
                example.money -= num
            print(num)

example = Player("hi :)")
example.hand = []
example.bet = 0
example.money = int(input("How much money: "))
example.money_at_round_start = example.money
board = []

example.hand.append(Card.new(input("first hand card:  ")))
example.hand.append(Card.new(input("second hand card: ")))
Card.print_pretty_cards(example.hand)

getInput(True)

board.append(Card.new(input("first board card:  ")))
board.append(Card.new(input("second board card: ")))
board.append(Card.new(input("third board card:  ")))
Card.print_pretty_cards(board)

getInput(False)

board.append(Card.new(input("fourth board card: ")))
Card.print_pretty_cards(board)

getInput(False)

board.append(Card.new(input("fifth board card:  ")))
Card.print_pretty_cards(board)

getInput(False)



