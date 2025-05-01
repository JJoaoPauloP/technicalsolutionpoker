"""
app/utilities/display_utils.py

This module contains utility functions for displaying and setting up the GUI,
with functions handling specific events like showdown and recapping round or 
drawing players and giving cards.

Group A Models/Algorithms:
- Complex user-defined algorithms (pot splitting logic)
- List operations and sorting
- Simple GUI event handling with pygame
"""


import pygame
import sys
from app.player import Player
from app.constants import WIN, WIDTH, HEIGHT, BEIGE
from app.background_loader import BACKGROUND
from app.card_images_setup import cards_object

def show_down(common_cards):
    """
    Displays all cards on the table during the showdown phase:
    - Player and opponent hole cards
    - Flop, turn, and river cards

    :param common_cards: List of 5 community cards (flop, turn, river)
    :return: None
    """
    player_list = Player.player_list_chair
    cards = pygame.sprite.Group()

    def add_cards(group, location, card_data):
        """Adding rendered card sprites to the group based on location."""
        for card in give_card(location, card_data):
            group.add(card)

    add_cards(cards, 'player', player_list[0].cards)
    add_cards(cards, 'opponent', player_list[1].cards)
    add_cards(cards, 'flop', common_cards[:3])
    add_cards(cards, 'turn', [common_cards[3]])
    add_cards(cards, 'river', [common_cards[4]])

    cards.draw(WIN)

def recap_round(list_winner, common_cards=None):
    """
    Displays a summary of the round:
    - If one winner: show their name and winnings.
    - If multiple winners: show all names, winnings, and hands after revealing all cards.

    :param list_winner: List of tuples [(player, winnings), ...]
    :param common_cards: List of 5 community cards (optional)
    :return: None
    """
    font = pygame.font.SysFont('Inked Skin Personal Use', 35)
    WIN.blit(BACKGROUND, BACKGROUND.get_rect())
    draw_player()

    def calculate_y_positions(text_height, spacing, bottom_margin, count):
        """
        Calculates vertical Y positions for multiple lines of text.
        Returns a list of Y coordinates from bottom to top.
        """
        base_y = HEIGHT - text_height - bottom_margin
        return [
            base_y - i * (text_height + spacing)
            for i in reversed(range(count))
        ]

    if len(list_winner) == 1:
        player, winnings = list_winner[0]
        message = f"{player.name} won £{winnings}"
        rendered_text = font.render(message, True, BEIGE)
        y_pos = calculate_y_positions(rendered_text.get_height(), rendered_text.get_height() // 2, HEIGHT * 0.1, 1)[0]
        WIN.blit(rendered_text, (WIDTH * 0.05, y_pos))
        pygame.display.flip()
        pygame.time.delay(1000)
    else:
        show_down(common_cards)
        dummy_text = font.render("placeholder", True, BEIGE)
        y_positions = calculate_y_positions(dummy_text.get_height(), dummy_text.get_height() // 2, HEIGHT * 0.1, len(list_winner))
        for i, (player, winnings) in enumerate(list_winner):
            message = f"{player.name} won £{winnings} with {player.hand}"
            rendered_text = font.render(message, True, BEIGE)
            WIN.blit(rendered_text, (WIDTH * 0.05, y_positions[i]))
        pygame.display.flip()
        pygame.time.delay(3000)

def draw_player(active_player_index=0):
    """
    Displays player labels and bet information.

    :param active_player_index: Index of the active player
    :return: None
    """
    player_list_chair = Player.player_list_chair
    for index, player in enumerate(player_list_chair):
        is_turn = index == active_player_index
        player.player_label(WIN, is_turn)
        player.draw_bet(WIN)
    pygame.display.flip()

def give_card(type_card, cards):
    """
    Places the cards in the correct positions and returns a group of card sprites.

    :param type_card: Type of card location, one of 'player', 'opponent', 'flop', 'turn', 'river'
    :param cards: List of card identifiers, e.g. ['2S', '3C']
    :return: pygame.sprite.Group of card sprites
    """
    dict_cards = {
        'player': ['first_card_player', 'second_card_player'],
        'opponent': ['first_card_opponent', 'second_card_opponent'],
        'flop': ['first_card_flop', 'second_card_flop', 'third_card_flop'],
        'turn': ['turn_card'],
        'river': ['river_card']
    }

    sub_cards = pygame.sprite.Group()
    list_cards = dict_cards[type_card]

    for i in range(len(list_cards)):
        card_object = cards_object[cards[i]]
        card_object.type_card = list_cards[i]
        card_object.put_in_place()
        sub_cards.add(card_object)
    return sub_cards

def cover_up_cards():
    """
    Returns a group of card sprites representing the back side of opponent's cards.

    :return: pygame.sprite.Group of back side card sprites
    """
    back_side_cards = pygame.sprite.Group()
    back_side_card_1 = cards_object['back_side_1']
    back_side_card_2 = cards_object['back_side_2']
    back_side_card_1.type_card = 'first_card_opponent'
    back_side_card_2.type_card = 'second_card_opponent'
    back_side_card_1.put_in_place()
    back_side_card_2.put_in_place()
    back_side_cards.add(back_side_card_1)
    back_side_cards.add(back_side_card_2)
    return back_side_cards

def draw_buttons(buttons):
    """
    Draws active buttons on the screen.

    :param buttons: List of button objects
    :return: None
    """
    for button in buttons:
        if button.active:
            button.draw_if_active(WIN)

def arrange_room(common_cards=None, active_player_index=0):
    """
    Draws the background, player cards, opponent cards, and community cards.

    :param common_cards: List of community cards (optional)
    :param active_player_index: Index of the active player
    :return: None
    """
    player_list_chair = Player.player_list_chair
    WIN.blit(BACKGROUND, BACKGROUND.get_rect())

    cards = pygame.sprite.Group()

    #drawing the player cards
    sub_card = give_card('player', player_list_chair[0].cards)
    for card in sub_card:
        cards.add(card)

    #drawing the opponent cards
    if active_player_index == 1:
        sub_card = give_card('opponent', player_list_chair[1].cards)
    else:
        sub_card = cover_up_cards()
    for card in sub_card:
        cards.add(card)

    cards.draw(WIN)

    #drawing the community cards
    if common_cards is not None:
        Player.draw_pot(WIN)

        #drawing the flop cards
        sub_card = give_card('flop', common_cards[0:3])
        for card in sub_card:
            cards.add(card)

        #drawing the turn card
        if len(common_cards) >= 4:
            sub_card = give_card('turn', [common_cards[3]])
            for card in sub_card:
                cards.add(card)

        #drawing the river card
        if len(common_cards) == 5:
            sub_card = give_card('river', [common_cards[4]])
            for card in sub_card:
                cards.add(card)

    cards.draw(WIN)

def handle_esc_press(get_pressed):
    """
    Checks if the ESC key is pressed and gracefully exits the program.

    :param get_pressed: pygame key.get_pressed() list of key states
    :return: None
    """
    if get_pressed[pygame.K_ESCAPE]:
        pygame.quit()
        sys.exit()
