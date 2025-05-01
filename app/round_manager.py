"""
app/poker_round.py

This module manages the execution of a single round of Texas Hold'em poker.
It handles blinds collection, card dealing, betting phases, pot distribution,
and player position reordering for the next round.

Group A Models/Algorithms:
- Complex user-defined use of OOP model (Player class interactions)
- Complex game logic involving betting phases and pot distribution
"""

import random

from app.player import Player
from app.bet_manager import handle_betting_phase
from app.hand_ranker import assign_best_hand
from app.utilities import recap_round, split_pot, one_player_win, change_players_positions
from app.constants import small_blind, big_blind


def poker_round():
    """
    Executes a single round of Texas Hold'em poker, handling:
    - Blinds collection
    - Dealing hole and community cards
    - Betting phases
    - Determining and distributing the pot to the winner(s)
    - Reordering player positions for the next round
    """
    player_list = Player.player_list
    player_list_chair = Player.player_list_chair

    # Helper function to post blinds and handle all-in cases
    def post_blind(player, amount):
        # If player has enough chips, post the blind normally
        if player.stack > amount:
            player.blind(amount)
        else:
            # If player has fewer chips than blind, go all-in with remaining stack
            player.blind(player.stack)
            player.go_allin()

    # Post blinds: big blind (last player), small blind (second to last)
    post_blind(player_list[-1], big_blind)
    post_blind(player_list[-2], small_blind)

    # Initialize and shuffle the deck of cards
    deck = [rank + suit for rank in "23456789TJQKA" for suit in "CDHS"]
    random.shuffle(deck)

    # Deal two hole cards to each player in seating order
    for player in player_list_chair:
        player.cards = [deck.pop(), deck.pop()]

    # Initial betting phase (pre-flop)
    handle_betting_phase()

    # Function to count active and all-in players
    def active_player_count():
        # Count players still active (live) and those who are all-in
        live = sum(player.live for player in player_list)
        allin = sum(player.is_allin for player in player_list)
        return live, allin

    live, allin = active_player_count()
    # Determine shift decision for player position rotation based on number of players
    shift_decision = -1 if len(player_list_chair) == 2 else -2

    # If only one player remains active or all-in, they win immediately
    if live + allin == 1:
        recap_round(one_player_win())
        return

    # Flop: deal 3 community cards
    flop = [deck.pop() for _ in range(3)]
    change_players_positions(shift_decision)

    if live > 1:
        handle_betting_phase(flop)

    live, allin = active_player_count()
    # Check again if only one player remains after flop betting
    if live + allin == 1:
        recap_round(one_player_win())
        change_players_positions(shift_decision)
        return

    # Turn: deal 1 community card
    turn = deck.pop()
    common_cards = flop + [turn]

    if live > 1:
        handle_betting_phase(common_cards)

    live, allin = active_player_count()
    # Check again if only one player remains after turn betting
    if live + allin == 1:
        recap_round(one_player_win())
        change_players_positions(shift_decision)
        return

    # River: deal final community card
    river = deck.pop()
    common_cards.append(river)

    if live > 1:
        handle_betting_phase(common_cards)

    live, allin = active_player_count()
    # Final check if only one player remains after river betting
    if live + allin == 1:
        recap_round(one_player_win())
    else:
        # Showdown: calculate scores and split the pot among winners
        assign_best_hand(player_list_chair, common_cards)
        recap_round(split_pot(), common_cards)

    # Reset player positions for the next round
    change_players_positions(shift_decision)
