"""
app/hand_ranker.py

This module contains functions to evaluate poker hands and assign the best hand to players.
It implements poker hand ranking logic using combinatorial algorithms.

Group A Models/Algorithms:
- Complex user-defined algorithms (poker hand evaluation)
- Combinatorial generation of 5-card hands from 7 cards (itertools.combinations)
"""

import itertools

def evaluate_hand(cards):
    """
    Evaluates the strength of a 5-card poker hand and returns its score and name.

    :param cards: A list of five cards as strings, e.g. ['2D', '3C', 'AH', 'AC', '7D']
    :return: A tuple (score, hand_name), e.g. (180, 'Royal flush')
    """
    # Mapping for face cards to numeric values for comparison
    face_card_values = {'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}

    # Extract values and suits from cards
    values = [face_card_values[card[0]] if card[0] in face_card_values else int(card[0]) for card in cards]
    suits = [card[1] for card in cards]

    # Sort values to facilitate hand pattern detection
    values.sort()

    # Detect if hand is a straight (including wheel: A-2-3-4-5)
    is_straight = values == list(range(values[0], values[0] + 5)) or values == [2, 3, 4, 5, 14]

    # Detect if hand is a flush (all suits the same)
    is_flush = len(set(suits)) == 1

    # Royal Flush: highest straight flush
    if values == [10, 11, 12, 13, 14] and is_flush:
        return 180, "Royal flush"

    # Straight Flush: straight and flush
    if is_straight and is_flush:
        return 160 + values[-1], "Straight flush"

    # Four of a Kind: four cards of the same value
    if values.count(values[2]) == 4:
        kicker = values[0] if values.count(values[0]) == 1 else values[-1]
        return 140 + values[2] + kicker / 100, "Four of a kind"

    # Full House: three of a kind plus a pair
    if len(set(values)) == 2:
        triple = values[2]
        pair = values[0] if values.count(values[0]) == 2 else values[-1]
        return 120 + triple + pair / 100, "Full house"

    # Flush: all cards same suit
    if is_flush:
        score = 100
        for i, v in enumerate(reversed(values)):
            score += v / (10 ** (i + 1))
        return score, "Flush"

    # Straight: consecutive values
    if is_straight:
        return 80 if values == [2, 3, 4, 5, 14] else 80 + values[-1], "Straight"

    # Three of a Kind: three cards of the same value
    if values.count(values[2]) == 3 and len(set(values)) == 3:
        kickers = sorted(set(values) - {values[2]}, reverse=True)
        return 60 + values[2] + kickers[0] / 100 + kickers[1] / 1000, "Three of a kind"

    # Two Pair: two different pairs
    if values.count(values[1]) == 2 and values.count(values[3]) == 2:
        pair_high = max(values[1], values[3])
        pair_low = min(values[1], values[3])
        kicker = list(set(values) - {pair_high, pair_low})[0]
        return 40 + pair_high + pair_low / 10 + kicker / 100, "Two pair"

    # One Pair: one pair
    if len(set(values)) == 4:
        pair_value = [v for v in values if values.count(v) == 2][0]
        kickers = sorted([v for v in values if v != pair_value], reverse=True)
        return 20 + pair_value + kickers[0] / 100 + kickers[1] / 10000 + kickers[2] / 100000, "Pair"

    # High Card: no other hand, score based on highest cards
    score = values[4] + values[3] / 10 + values[2] / 100 + values[1] / 1000 + values[0] / 10000
    return score, "High card"

def assign_best_hand(player_list, common_cards):
    """
    Determines the best possible 5-card poker hand for each player using their two hole cards
    and the shared community cards.

    Modifies each player object by setting `player.score` and `player.hand`.

    :param player_list: List of player objects, each with a `cards` attribute (2 cards).
    :param common_cards: List of 5 community cards (flop + turn + river).
    :return: None (player objects are modified in-place).
    """
    for player in player_list:
        best_score = 0
        best_hand_name = ""

        # Combine player and community cards, generate all 5-card combinations
        all_cards = common_cards + player.cards
        for combo in itertools.combinations(all_cards, 5):
            score, name = evaluate_hand(combo)
            if score > best_score:
                best_score = score
                best_hand_name = name

        player.score = best_score
        player.hand = best_hand_name
