"""
simulations/flop_simulation.py

This module simulates poker rounds to estimate the probability of a given poker hand winning on the flop.
It runs multiple rounds where PlayerOne has a fixed hand, and PlayerTwo and table cards are randomly sampled.
The win ratio of PlayerOne is calculated over the specified number of rounds.

Group A Models/Algorithms:
- Complex user-defined algorithms (Monte Carlo simulation)
- Random sampling and probability estimation
"""

import random
from app.player import Player
from app.hand_ranker import assign_best_hand

def simulate_flop_win_probability(num_rounds=5000):
    """
    Simulates poker rounds to estimate the probability of PlayerOne winning on the flop.

    :param num_rounds: Number of simulation rounds to run
    :return: List of win probabilities after each round
    """
    # Define the full deck of cards
    full_deck = [
        '2C', '3C', '4C', '5C', '6C', '7C', '8C', '9C', 'TC', 'JC', 'QC', 'KC', 'AC',
        '2S', '3S', '4S', '5S', '6S', '7S', '8S', '9S', 'TS', 'JS', 'QS', 'KS', 'AS',
        '2H', '3H', '4H', '5H', '6H', '7H', '8H', '9H', 'TH', 'JH', 'QH', 'KH', 'AH',
        '2D', '3D', '4D', '5D', '6D', '7D', '8D', '9D', 'TD', 'JD', 'QD', 'KD', 'AD'
    ]

    # Initialize players with starting stacks
    start_stack = 100
    player_one = Player('PlayerOne', start_stack, 0)
    player_two = Player('PlayerTwo', start_stack, 1)
    players_list = [player_one, player_two]

    # Fixed hand for PlayerOne to test
    player_one.cards = ['JC', '5C']

    # Predefined flop cards
    flop = ['2D', '9D', 'AD']

    n_win = 0
    n_tie = 0
    win_history = []

    for round_index in range(num_rounds):
        # Create a fresh deck for each round excluding PlayerOne's cards and flop
        deck = [card for card in full_deck if card not in player_one.cards + flop]

        # Sample PlayerTwo's hand randomly from remaining deck
        player_two.cards = random.sample(deck, 2)
        for card in player_two.cards:
            deck.remove(card)

        # Sample two additional table cards (turn and river)
        table_cards = random.sample(deck, 2)
        for card in table_cards:
            deck.remove(card)

        # Combine table cards with the flop for evaluation
        table_cards += flop

        # Evaluate players' best hands
        assign_best_hand(players_list, table_cards)

        # Update win/tie counts based on scores
        if player_one.score > player_two.score:
            n_win += 1
        elif player_one.score == player_two.score:
            n_tie += 1

        # Record current win ratio after each round
        win_history.append(n_win / (round_index + 1))

    # Print final win probability after all rounds
    print(f"Win probability after {num_rounds} rounds: {win_history[-1]:.4f}")

    return win_history

if __name__ == "__main__":
    simulate_flop_win_probability()
