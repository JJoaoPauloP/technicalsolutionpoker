import random
import time

from app.player_class import Player
from app.poker_score import players_score

#test: how many rounds should be played to see which probability given hand is to win pre-flop
deck = ['2C', '3C', '4C', '5C', '6C', '7C', '8C', '9C', 'TC', 'JC', 'QC', 'KC', 'AC', '2S', '3S', '4S',
        '5S',
        '6S', '7S', '8S', '9S', 'TS', 'JS', 'QS', 'KS', 'AS', '2H', '3H', '4H', '5H', '6H', '7H', '8H',
        '9H',
        'TH', 'JH', 'QH', 'KH', 'AH', '2D', '3D', '4D', '5D', '6D', '7D', '8D', '9D', 'TD', 'JD', 'QD',
        'KD', 'AD']

#complex user defined algorithm (probability simulation for poker hands)
start = time.time()
start_stack = 100
PlayerOne = Player('PlayerOne', start_stack)
PlayerTwo = Player('PlayerTwo', start_stack)
players_list = [PlayerOne, PlayerTwo ]

PlayerTwo.cards = ['AC', 'AD']

number_round = 5000
n_win = 0
n_tie = 0

for i in range(number_round): #list operations (deck manipulation)
    deck = ['2C', '3C', '4C', '5C', '6C', '7C', '8C', '9C', 'TC', 'JC', 'QC', 'KC', '2S', '3S', '4S', '5S', '6S',
            '7S', '8S', '9S', 'TS', 'JS', 'QS', 'KS', 'AS', '2H', '3H', '4H', '5H', '6H', '7H', '8H', '9H', 'TH', 'JH',
            'QH', 'KH', 'AH', '2D', '3D', '4D', '5D', '6D', '7D', '8D', '9D', 'TD', 'JD', 'QD', 'KD']

    PlayerTwo.cards = random.sample(deck, 2)
    [deck.remove(PlayerTwo.cards[i]) for i in range(2)] #list operations
    table = random.sample(deck, 5)
    [deck.remove(table[i]) for i in range(5)] #list operations
    players_score(players_list, table) #complex user defined algorithm (poker hand evaluation)
    if PlayerOne.score > PlayerTwo.score: 
        n_win += 1
    elif PlayerOne.score == PlayerTwo.score:
        n_tie += 1
stop = time.time()

print(n_win / number_round)

print('Time: ', stop - start)

