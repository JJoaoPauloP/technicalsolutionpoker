"""
app/pot_splitter.py

This module contains functions to split the pot among players based on their scores and bets.
It handles complex pot distribution logic including ties and all-in scenarios.

Group A Models/Algorithms:
- Complex user-defined algorithms (pot splitting and distribution)
- List operations and sorting for game state management
"""

def split_pot():
    """
    Splits the pot among players based on their scores and input stacks.
    Adjusts each player's stack accordingly and returns a list of winners with their winnings.

    Returns:
        list_winner (list of tuples): Each tuple contains a player object and the amount they have won (excluding returned input stack).
    """
    import operator
    from app.player import Player

    player_list = Player.player_list_chair.copy()  # Copy current players at the table
    number_of_players = len(player_list)

    # Sort players first by input_stack (ascending) then by score (descending)
    player_list.sort(key=operator.attrgetter('input_stack'))
    player_list.sort(key=operator.attrgetter('score'), reverse=True)

    player_scores = [player.score for player in player_list]
    input_stacks = [player.input_stack for player in player_list]

    win_list = [0] * number_of_players  # Initialize winnings and in-game contributions
    input_in_game = [0] * number_of_players

    # Calculate how much of their stack each player gets returned
    for player_index in range(number_of_players):
        if player_scores[player_index] == max(player_scores):
            input_in_game[player_index] = input_stacks[player_index]
        else:
            # Find the maximum input_stack among players with different (higher) scores
            aux_input = [
                input_stacks[other_index] if player_scores[other_index] != player_scores[player_index] else 0
                for other_index in range(number_of_players)
            ]
            max_aux_input = max(aux_input[:player_index]) if aux_input[:player_index] else 0

            if input_stacks[player_index] - max_aux_input < 0:
                input_in_game[player_index] = 0
            else:
                input_in_game[player_index] = input_stacks[player_index] - max_aux_input

    # Calculate actual winnings distributed among players
    for player_index in range(number_of_players):
        number_of_tied_players = player_scores[player_index:].count(player_scores[player_index])

        for opponent_index in range(player_index + 1, number_of_players):
            if player_scores[player_index] > player_scores[opponent_index]:
                if input_stacks[player_index] >= input_stacks[opponent_index]:
                    win_list[player_index] += input_stacks[opponent_index] / number_of_tied_players
                    input_stacks[opponent_index] = 0
                else:
                    win_list[player_index] += input_stacks[player_index] / number_of_tied_players
                    input_stacks[opponent_index] -= input_stacks[player_index]

        # Equalize winnings for tied players
        if number_of_tied_players > 1:
            for tied_player_index in range(player_index + 1, number_of_players):
                if player_scores[player_index] == player_scores[tied_player_index]:
                    win_list[tied_player_index] = win_list[player_index]
                    input_stacks[tied_player_index] -= input_stacks[player_index]

    # Combine winnings and returned stacks
    list_winner = []
    for player_index in range(number_of_players):
        total_win = input_in_game[player_index] + win_list[player_index]
        list_winner.append((player_list[player_index], int(win_list[player_index])))  # Only the "new" winnings are shown
        player_list[player_index].win(total_win)  # Update player's stack with total winnings

    return list_winner


def one_player_win():
    """
    Handles the case where only one player wins the entire pot.
    Updates the winning player's stack and returns a list containing 
    a tuple of the winning player and their profit (excluding their own input stack).
    
    Returns:
        list_winner (list of tuples): Each tuple is (Player, profit).
    """
    from app.player import Player

    player_list = Player.player_list_chair.copy()
    list_winner = []

    for player in player_list:
        if player.live or player.is_allin:
            # Winner collects the sum of all players' input stacks
            total_pot = sum(p.input_stack for p in player_list)
            player.win(total_pot)
            # Profit is total pot minus the winner's own contribution
            list_winner.append((player, total_pot - player.input_stack))

    return list_winner
