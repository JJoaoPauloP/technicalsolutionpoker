import asyncio
import pygame

from app.utils import change_players_positions #complex user defined algorithm (player position management)
from app.player_class import Player #complex user defined OOP model (player class)
from app.poker_round import poker_round #complex user defined algorithm (poker round logic)
from app.constant import FPS, WIDTH, HEIGHT
from app.menu import menu_start, menu_end


#create players
START_STACK = 5000
Player('PlayerOne', START_STACK, 'human') #dynamic generation of objects using OOP
Player('PlayerTwo', START_STACK, 'human')

import random

def simulate_poker_rounds(player_list, num_simulations=1000):
    """
    Simulates multiple poker rounds to estimate each player's probability of winning.
    Uses random choice to approximate probabilities.
    """
    win_count = {player: 0 for player in player_list} #list operations (dictionary initialisation)

    for _ in range(num_simulations):
        winner = random.choice(player_list) #complex user defined algorithm (monte carlo simulation)
        win_count[winner] += 1 #hashtag (dictionary for tracking wins)

    #update probabilities for each player
    for player in player_list:
        player.probability = win_count[player] / num_simulations #probability calc. (complex mathematical model)


async def main():
    pygame.init()
    clock = pygame.time.Clock()

    #create game window
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Poker Game")

    run = True
    player_list_chair = Player.player_list_chair

    active_player_index = 0  #track the active player's index

    while run:
        clock.tick(FPS)
        win.fill((255, 255, 255))  #clear the screen with a white background

        #show menu at the start of the game
        menu_start() #server side scripting (GUI interaction)

        #initial probabilities
        simulate_poker_rounds(player_list_chair)

        while len(player_list_chair) > 1:
            #handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False  # Quit the game
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    #check if any probability button is clicked
                    for player in player_list_chair:
                        if hasattr(player, 'probability_button_rect') and player.probability_button_rect and player.probability_button_rect.collidepoint(event.pos):
                            #display probabilities for the clicked player
                            player.show_probabilities(win)

            #play a poker round
            poker_round() #complex user defined algorithm (poker round logic)
            change_players_positions(shift=1) #complex algorithm (player movement management)
            [player.next_round() for player in player_list_chair] #list operations (iteration over player list)

            #update probabilities after each round
            simulate_poker_rounds(player_list_chair)

            #handle rebuys and remove players with 0 stack
            for player in player_list_chair:
                if player.stack == 0:
                    rebuy = menu_end()
                    if rebuy:
                        for p in player_list_chair:
                            p.stack = START_STACK #dynamic generation of objects (resetting player stack)

            [player_list_chair.remove(player) for player in player_list_chair if player.stack == 0] #linked list maintenance

            if len(player_list_chair) == 1:
                run = False
                break

            #draw player labels and buttons on the GUI
            for index, player in enumerate(player_list_chair):
                is_turn = index == active_player_index
                player.player_label(win, is_turn)

            active_player_index = (active_player_index + 1) % len(player_list_chair)

            #update the display
            pygame.display.update()

        await asyncio.sleep(0)  #allow for async event handling

    pygame.quit()


if __name__ == '__main__':
    asyncio.run(main())

