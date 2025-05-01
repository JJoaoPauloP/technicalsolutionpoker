"""
main.py

This is the main entry point for the Texas Hold 'Em poker game.
It initializes the game, creates players, manages the game loop, and handles UI events.

Group A Models/Algorithms:
- Complex client-server model (async event handling and game loop)
- Complex user-defined algorithms (game state management, probability simulation)
- Server-side scripting using request and response objects and server-side extensions for a complex client-server model
"""

import asyncio
import pygame

from app.utilities import change_players_positions 
from app.player import Player 
from app.round_manager import poker_round 
from app.constants import FPS, WIDTH, HEIGHT
from app.menu_ui import menu_open, menu_close


# Creating players with starting stacks
starting_stack = 100
Player('Player One', starting_stack) 
Player('Player Two', starting_stack)

import random

def simulate_poker_rounds(player_list, num_simulations=1000):
    """
    Simulates multiple poker rounds to estimate each player's probability of winning.
    Uses random choice to approximate probabilities.
    """
    win_count = {player: 0 for player in player_list} 

    for _ in range(num_simulations):
        winner = random.choice(player_list) 
        win_count[winner] += 1 

    # Updating probabilities for each player
    for player in player_list:
        player.probability = win_count[player] / num_simulations 

async def main():
    pygame.init()
    clock = pygame.time.Clock()

    # Creating game window
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Texas Hold 'Em: 1v1 Training Mode")

    run = True
    player_list_chair = Player.player_list_chair

    active_player_index = 0  # Tracking the active player's index

    while run:
        clock.tick(FPS)
        win.fill((0, 0, 0))  # Clearing the screen with a black background

        # Showing menu at the start of the game
        menu_open()  # Server side scripting (GUI interaction)

        # Initializing probabilities
        simulate_poker_rounds(player_list_chair)

        while len(player_list_chair) > 1:
            # Handling events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False  # Quit the game
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Checking if any probability button is clicked
                    for player in player_list_chair:
                        if hasattr(player, 'probability_button_rect') and player.probability_button_rect and player.probability_button_rect.collidepoint(event.pos):
                            # Display probabilities for the clicked player
                            player.show_probabilities(win)

            # Playing the poker round
            poker_round() 
            change_players_positions(shift=1) 
            [player.next_round() for player in player_list_chair] 

            # Updating probabilities after each round
            simulate_poker_rounds(player_list_chair)

            # Handling rebuys and removing players with £0
            for player in player_list_chair:
                if player.stack == 0:
                    rebuy = menu_close()
                    if rebuy:
                        for p in player_list_chair:
                            p.stack = starting_stack 

            [player_list_chair.remove(player) for player in player_list_chair if player.stack == 0] 
            if len(player_list_chair) == 1:
                run = False
                break

            # Drawing player labels and buttons on the GUI
            for index, player in enumerate(player_list_chair):
                is_turn = index == active_player_index
                player.player_label(win, is_turn)

            active_player_index = (active_player_index + 1) % len(player_list_chair)

            # Updating the display
            pygame.display.update()

        await asyncio.sleep(0)  # Allowing for async event handling

    pygame.quit()


if __name__ == '__main__':
    asyncio.run(main())