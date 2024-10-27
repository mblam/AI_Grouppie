import treys
from treys import Card
from treys import Evaluator
from treys import Deck


deck = Deck()
print(deck)
# Draw cards from the deck
board = deck.draw(5)
hand1 = deck.draw(2)
hand2 = deck.draw(2)
hand3 = deck.draw(2)
hand4 = deck.draw(2)
hand5 = deck.draw(2)
hand6 = deck.draw(2)
# Print cards to terminal
Card.print_pretty_cards(board)
Card.print_pretty_cards(hand1)
Card.print_pretty_cards(hand2)
# Initialize evaluator
evaluator = Evaluator()
val1 = evaluator.evaluate(board, hand1)
print(Card.int_to_str(hand1[0]))
print(Card.get_rank_int(hand1[0]))
print(Card.get_suit_int(hand1[1]))
print(Card.get_rank_int(hand1[1]))
val2 = evaluator.evaluate(board, hand2)
print(Card.get_suit_int(hand2[0]))
print(Card.get_rank_int(hand2[0]))
print(Card.get_suit_int(hand2[1]))
print(Card.get_rank_int(hand2[1]))
print("1: ",val1)
print("2: ",val2)
print(evaluator.class_to_string(evaluator.get_rank_class(val1)))
print(evaluator.class_to_string(evaluator.get_rank_class(val2)))

# Lower values represent better hands
if(val1 < val2):
    print("Hand 1 wins")
elif(val2 < val1):
    print("Hand 2 wins")
else:
    print("Tie")

evaluator.hand_summary(board, [hand1,hand2,hand3,hand4,hand5,hand6])
