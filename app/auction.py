from app.player_class import Player
from app.button_class import buttons
from app.utils import player_decision, arrange_room, draw_player
from app.constant import BB


def auction(common_cards=None):
    """
    The function displays each player's available options during an auction.
    Ends when all players have made a decision or all but one fold.
    :param common_cards: list of community cards, if the stage is preflop then common cards is None
    """
    player_list = Player.player_list

    #list operations (filtering players still in the round)
    player_list = [player for player in player_list if player.live]

    number_decisions = sum([player.decision for player in player_list])
    number_player = len(player_list)

    #auction ends when all players have made a decision or all but one fold
    every_fold = False
    while number_decisions != number_player and not every_fold:
        for active_player_index, player in enumerate(player_list):
            if not player.decision and player.live: #list operations (extracting player stacks and bets)
                input_stack_list = [p.input_stack for p in player_list]
                bet_list = [p.bet_auction for p in player_list]

                #ensure bet_list has at least two elements
                bet_list = sorted(bet_list, reverse=True)
                if len(bet_list) < 2:
                    bet_list.append(0)

                #create a set of options for the player
                dict_options = {'fold': True, 'all-in': True, 'call': False, 'check': False, 'raise': False}

                #calculate call, min raise, and max raise values
                call_value = max(input_stack_list) - player.input_stack
                min_raise = max(call_value + bet_list[0] - bet_list[1], BB)
                max_raise = player.stack

                #activate options for the player
                if player.input_stack == max(input_stack_list):
                    dict_options['check'] = True
                elif player.stack > call_value:
                    dict_options['call'] = True
                if player.stack > min_raise:
                    dict_options['raise'] = True

                pot = sum(input_stack_list)
                pot_table = sum(input_stack_list) - sum(bet_list)

                # complex user defined algorithm (ask player for decision)
                if player.kind == 'human':
                    decision = player_decision(buttons, dict_options, min_raise, max_raise, common_cards, active_player_index)
             
                # Process player's decision
                if decision[0] == 'raise':
                    chips = int(decision[1])
                decision = decision[0]

                #linked list maintenance (updating player state dynamically)
                if decision == 'call':
                    chips = call_value
                    if player.stack > chips:
                        player.drop(chips)
                    else:
                        player.drop(player.stack)
                        player.allin()
                elif decision == 'fold':
                    player.fold()
                elif decision == 'check':
                    player.decision = True
                elif decision == 'all-in':
                    player.drop(player.stack)
                    for p in player_list:
                        if p.live and p.decision and p.input_stack < player.input_stack:
                            p.decision = False
                    player.allin()
                elif decision == 'raise':
                    for p in player_list:
                        if p.live and p.decision:
                            p.decision = False
                    if player.stack > chips:
                        player.drop(chips)
                    else:
                        player.drop(player.stack)
                        player.allin()

                #server side scripting (updating UI elements dynamically)
                arrange_room(common_cards, active_player_index)
                draw_player()

            #check if only one player is still live
            sum_live = sum(p.live for p in player_list)
            sum_alin = sum(p.alin for p in player_list)
            if sum_live == 1 and sum_alin == 0:
                every_fold = True
                break

        number_decisions = sum(p.decision for p in player_list)

    #reset decisions for the next round
    for player in player_list:
        player.next_auction()
        if player.live:
            player.decision = False