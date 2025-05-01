"""
app/utilities/game_logic_utils.py

This module contains utility functions for game logic and player interaction,
including player decision GUI, pot splitting, and player position management.

Group A Models/Algorithms:
- Complex user-defined algorithms (pot splitting logic)
- List operations and sorting
- Simple GUI event handling with pygame
"""

import pygame
import sys
from app.constants import WIN, BEIGE
from app.button_ui import x_buttons, y_button_positions, width_button
from app.player import Player
from app.utilities.display_utils import arrange_room, draw_player, draw_buttons, handle_esc_press

def player_decision(buttons, dict_options, min_raise, max_raise, common_cards=None, active_player_index=0):
    """
    Displays GUI for player decision and returns the action.

    Arguements:
        buttons (list): List of button objects.
        dict_options (dict): Dict indicating which buttons are active.
        min_raise (int): Minimum raise value.
        max_raise (int): Maximum raise value.
        common_cards (list, optional): List of common cards.
        active_player_index (int, optional): Index of the active player.

    Returns:
        list: List containing the action and raise amount if applicable.

    This function handles user input for betting decisions, including raise amounts,
    and updates the GUI accordingly.
    """
    font = pygame.font.SysFont('Timesnewroman', 40)
    input_box = pygame.Rect(x_buttons, y_button_positions[4] + 30, width_button * 2, 40)
    input_color_active = (94, 151, 82)
    input_color_inactive = BEIGE
    input_color = input_color_inactive
    input_text = ""

    for button in buttons:
        button.active = dict_options.get(button.name, False)

    cards = pygame.sprite.Group()
    arrange_room(common_cards, active_player_index=active_player_index)
    cards.update()
    draw_player()

    pause_action = True
    active_input = False
    decision = None

    while pause_action:
        draw_buttons(buttons)

        for event in pygame.event.get():
            mouse_position = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active_input = True
                    input_color = input_color_active
                else:
                    active_input = False
                    input_color = input_color_inactive

                for button in buttons:
                    if button.is_mouse_over(mouse_position) and button.active:
                        if button.name == 'raise':
                            if input_text.isdigit():
                                raise_amount = int(input_text)
                                if min_raise <= raise_amount <= max_raise:
                                    decision = [button.name, raise_amount]
                                    pause_action = False
                                else:
                                    print(f"Raise amount must be between {min_raise} and {max_raise}.")
                            else:
                                print("Please enter a valid number.")
                        else:
                            decision = [button.name]
                            pause_action = False

            if event.type == pygame.KEYDOWN and active_input:
                if event.key == pygame.K_RETURN:
                    if input_text.isdigit():
                        raise_amount = int(input_text)
                        if min_raise <= raise_amount <= max_raise:
                            decision = ['raise', raise_amount]
                            pause_action = False
                        else:
                            print(f"Raise amount must be between {min_raise} and {max_raise}.")
                    else:
                        print("Please enter a valid number.")
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                    WIN.fill((0, 0, 0))
                    arrange_room(common_cards, active_player_index=active_player_index)
                    draw_player()
                    draw_buttons(buttons)
                    pygame.draw.rect(WIN, input_color, input_box, 2)
                    text_surface = font.render(input_text, True, BEIGE)
                    WIN.blit(text_surface, (input_box.x + 10, input_box.y + 5))
                    pygame.display.update()
                else:
                    input_text += event.unicode

            if event.type == pygame.MOUSEMOTION:
                for button in buttons:
                    if button.active:
                        button.update_text_colour_on_hover(mouse_position)

        pygame.draw.rect(WIN, input_color, input_box, 2)
        text_surface = font.render(input_text, True, BEIGE)
        WIN.blit(text_surface, (input_box.x + 10, input_box.y + 5))
        pygame.display.update()

        get_pressed = pygame.key.get_pressed()
        handle_esc_press(get_pressed)

    return decision

def split_pot():
    """
    Adjusts players' stacks and returns how much they win in the round.

    Returns:
        list: List of tuples (player, winnings).

    This function implements complex pot splitting logic based on player scores and bets,
    using list operations and sorting (Group A algorithms).
    """
    import operator
    player_list = Player.player_list_chair.copy()

    #removing players who folded and are not all-in
    player_list = [p for p in player_list if p.live or p.is_allin]

    #sorting players by input_stack ascending, then by score descending
    player_list.sort(key=operator.attrgetter('input_stack'))
    player_list.sort(key=operator.attrgetter('score'), reverse=True)

    n = len(player_list)
    player_score = [p.score for p in player_list]
    input_stack = [p.input_stack for p in player_list]

    win_list = [0] * n
    input_in_game = [0] * n

    for i in range(n):
        if player_score[i] == max(player_score):
            input_in_game[i] = input_stack[i]
        else:
            aux = [1 if player_score[j] != player_score[i] else 0 for j in range(n)]
            new_input = [aux[j] * input_stack[j] for j in range(n)]
            if input_stack[i] - max(new_input[0:i]) < 0:
                input_in_game[i] = 0
            else:
                input_in_game[i] = input_stack[i] - max(new_input[0:i])

    for i in range(n):
        number_division = player_score[i:].count(player_score[i])
        for j in range(i + 1, n):
            if player_score[i] > player_score[j]:
                if input_stack[i] >= input_stack[j]:
                    win_list[i] += input_stack[j] / number_division
                    input_stack[j] = 0
                else:
                    win_list[i] += input_stack[i] / number_division
                    input_stack[j] -= input_stack[i]
        if number_division > 1:
            for k in range(i + 1, n):
                if player_score[i] == player_score[k]:
                    win_list[k] = win_list[i]
                    input_stack[k] -= input_stack[i]

    list_winner = []
    for i in range(n):
        win_value = input_in_game[i] + win_list[i]
        list_winner.append((player_list[i], int(win_list[i])))
        player_list[i].win(win_value)

    return list_winner

def one_player_win():
    """
    Adjusts the stack of the winning player and returns a list of tuples with the winner and amount won.

    Returns:
        list: List of tuples (player, winnings).

    This function handles the case where only one player remains active or all-in.
    """
    player_list = Player.player_list_chair.copy()
    list_winner = []
    for player in player_list:
        if player.live or player.is_allin:
            win_value = sum(p.input_stack for p in player_list)
            player.win(win_value)
            list_winner.append((player, win_value - player.input_stack))
    return list_winner

def change_players_positions(shift):
    """
    Changes each player's position by a given shift.

    Arguments:
        shift (int): Integer shift value.

    Returns:
        None.

    This function updates player positions cyclically and sorts the player list accordingly.
    """
    import operator
    player_list = Player.player_list
    number_players = len(player_list)
    for player in player_list:
        player.position = (player.position + shift) % number_players
    player_list.sort(key=operator.attrgetter('position'))
