"""
app/bet_manager.py

This module handles the betting phases of the poker game, managing player actions such as fold, raise, call, check, and all-in.
It controls the flow of betting rounds until completion conditions are met.

Group A Models/Algorithms:
- Complex client-server model (managing player state and decisions in betting rounds)
- Complex user-defined algorithms (betting logic and decision handling)
"""

from app.player import Player
from app.button_ui import buttons
from app.utilities import player_decision, arrange_room, draw_player
from app.constants import big_blind

def handle_betting_phase(common_cards=None):
    """
    Handles the betting phase where players can fold, raise, call, check, or go all-in.

    The round ends when both players have made a decision, one player folds, or both go all-in.

    :param common_cards: The list of community cards. If preflop, this is None.
    """
    player_list = [player for player in Player.player_list if player.live]

    number_decisions = sum(player.decision for player in player_list)
    number_players = len(player_list)

    every_fold = False

    while number_decisions != number_players and not every_fold:
        for active_player_index, player in enumerate(player_list):
            if not player.decision and player.live:
                # Extract current bets and stacks for all players
                input_stack_list = [p.input_stack for p in player_list]
                bet_list = sorted([p.bet_betting_phase for p in player_list], reverse=True)
                if len(bet_list) < 2:
                    bet_list.append(0)

                # Calculate call and raise values based on current bets
                call_value = max(input_stack_list) - player.input_stack
                min_raise = max(call_value + bet_list[0] - bet_list[1], big_blind)
                max_raise = player.stack

                # Set available options for the player based on game state
                dict_options = {
                    'fold': True,
                    'all-in': True,
                    'call': False,
                    'check': False,
                    'raise': False
                }

                if player.input_stack == max(input_stack_list):
                    dict_options['check'] = True
                elif player.stack > call_value:
                    dict_options['call'] = True
                if player.stack > min_raise:
                    dict_options['raise'] = True

                # Get and process the player's decision
                decision_info = player_decision(
                    buttons, dict_options, min_raise, max_raise,
                    common_cards, active_player_index
                )
                
                decision, *decision_value = decision_info
                chips = int(decision_value[0]) if decision_value else 0

                if decision == 'call':
                    chips = call_value
                    if player.stack > chips:
                        player.drop(chips)
                    else:
                        player.drop(player.stack)
                        player.go_allin()

                elif decision == 'fold':
                    player.fold()

                elif decision == 'check':
                    player.decision = True

                elif decision == 'all-in':
                    player.drop(player.stack)
                    # Reset decisions for players who need to respond to the all-in raise
                    for p in player_list:
                        if p.live and p.decision and p.input_stack < player.input_stack:
                            p.decision = False
                    player.go_allin()

                elif decision == 'raise':
                    # Reset decisions for all players to respond to the raise
                    for p in player_list:
                        if p.live and p.decision:
                            p.decision = False
                    if player.stack > chips:
                        player.drop(chips)
                    else:
                        player.drop(player.stack)
                        player.go_allin()

                arrange_room(common_cards, active_player_index)  # Update UI after a player acts
                draw_player()

            # Check if only one player remains live (others folded)
            sum_live = sum(p.live for p in player_list)
            sum_allin = sum(p.is_allin for p in player_list)

            if sum_live == 1 and sum_allin == 0:
                every_fold = True
                break

        number_decisions = sum(p.decision for p in player_list)

    # Reset player decisions for the next betting phase
    for player in player_list:
        player.next_betting_phase()
        if player.live:
            player.decision = False
