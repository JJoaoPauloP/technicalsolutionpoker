import random

from app.player_class import Player
from app.auction import auction
from app.poker_score import players_score
from app.utils import recap_round, split_pot, one_player_win, change_players_positions
from app.constant import SB, BB


def poker_round():
    """
    Function play one round of dealing cards.
    """

    #in player_list players order will change after each round
    player_list_chair = Player.player_list_chair  #accessing a class variable
    player_list = Player.player_list  #accessing a class variable

    #take blinds from players
    if player_list[-1].stack > BB:
        player_list[-1].blind(BB)  #blinds mechanism for the big blind (BB)
    else:
        player_list[-1].blind(player_list[-1].stack)  #all-in if not enough stack
        player_list[-1].allin()

    if player_list[-2].stack > SB:
        player_list[-2].blind(SB)  #blinds mechanism for the small blind (SB)
    else:
        player_list[-2].blind(player_list[-2].stack)  #all-in if not enough stack
        player_list[-2].allin()

    #create a deck of cards
    deck = ['2C', '3C', '4C', '5C', '6C', '7C', '8C', '9C', 'TC', 'JC', 'QC', 'KC', 'AC', '2S', '3S', '4S', '5S', '6S',
            '7S', '8S', '9S', 'TS', 'JS', 'QS', 'KS', 'AS', '2H', '3H', '4H', '5H', '6H', '7H', '8H', '9H', 'TH', 'JH',
            'QH', 'KH', 'AH', '2D', '3D', '4D', '5D', '6D', '7D', '8D', '9D', 'TD', 'JD', 'QD', 'KD', 'AD']  #a deck of cards, hardcoded

    #deal the cards to the player
    for player in player_list_chair:
        player.cards = random.sample(deck, 2)  #deal two cards to each player
        [deck.remove(player.cards[i]) for i in range(2)]  #remove the dealt cards from the deck

    #first auction
    auction()  #first auction phase (bidding)

    #check how many players are in the game and all-in
    number_live_players = sum([player.live for player in player_list])  #count live players
    number_allin_players = sum([player.alin for player in player_list])  #count all-in players

    #change order decision player
    if len(player_list_chair) == 2:
        shift_decision = -1  #shift for only 2 players in the game
    else:
        shift_decision = -2  #shift for more than 2 players in the game

    #if there is only one player left in the game, he wins
    if number_live_players + number_allin_players == 1:
        list_winner = one_player_win()  #one player wins if only one remains
        recap_round(list_winner)  #recap the round
    else:
        #flop
        flop = random.sample(deck, 3)  #deal 3 cards for the flop
        [deck.remove(flop[i]) for i in range(3)]  #remove the flop cards from the deck

        #change order decision players
        change_players_positions(shift_decision)  #change the decision order of players

        if number_live_players > 1:
            #second auction
            auction(flop)  #auction phase with the flop cards

        #check how many players are in the game and all-in
        number_live_players = sum([player.live for player in player_list])  #update number of live players
        number_allin_players = sum([player.alin for player in player_list])  #update number of all-in players

        #if there is only one player left in the game, he wins
        if number_live_players + number_allin_players == 1:
            list_winner = one_player_win()  #one player wins if only one remains
            recap_round(list_winner)  #recap the round
            #return to the original position
            change_players_positions(shift_decision)
        else:
            #deal the cards to the turn
            turn = random.sample(deck, 1)  #deal 1 card for the turn
            deck.remove(turn[0])  #remove the turn card from the deck
            common_cards = flop + turn  #combine flop and turn cards

            if number_live_players > 1:
                #third auction
                auction(common_cards)  #auction phase with the flop + turn cards

            #check how many players are in the game and all-in
            number_live_players = sum([player.live for player in player_list])  #update live players
            number_allin_players = sum([player.alin for player in player_list])  #update all-in players

            #if there is only one player left in the game, he wins
            if number_live_players + number_allin_players == 1:
                list_winner = one_player_win()  #one player wins if only one remains
                recap_round(list_winner)  #recap the round
                #return to the original position
                change_players_positions(shift_decision)
            else:

                #deal the cards to the river
                river = random.sample(deck, 1)  #deal 1
