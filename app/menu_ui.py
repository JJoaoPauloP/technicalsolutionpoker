"""
app/menu_ui.py

This module manages the main menu and end-game menu UI for the poker game.
It provides interactive buttons for starting a new game or exiting, and displays the winner.

Group B Models/Algorithms:
- Simple OOP model (Button class encapsulation)
- UI event handling and rendering
"""

import pygame.transform
from app.constants import RATIO, BUTTON_WIDTH, BUTTON_HEIGHT
from app.background_loader import BACKGROUND_MENU, button_new_game_image, button_exit_image

# Scaling factors for button sizes

class Button:
    def __init__(self, x, y, image, width, height):
        """
        Initialize a button with given position, image, and size.

        Args:
            x (int): The x-coordinate of the button.
            y (int): The y-coordinate of the button.
            image (Surface): The image for the button.
            width (int): Width to scale the image to.
            height (int): Height to scale the image to.
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = pygame.transform.scale(image, (self.width, self.height))  
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def draw(self, surface):
        """Draws the button onto the given surface."""
        surface.blit(self.image, (self.x, self.y)) 
        
    def is_hovered(self, mouse_pos):
        """
        Checks if the mouse is over the button.

        Args:
            mouse_pos (tuple): Current position of the mouse.

        Returns:
            bool: True if mouse is over button, else False.
        """
        return self.rect.collidepoint(mouse_pos)

def menu_open():
    """
    Displays the main menu with 'New Game' and 'Exit' options.
    """
    from app.constants import WIN, WIDTH

    # Draw background
    WIN.blit(BACKGROUND_MENU, (0, 0))  
    
    # Create menu buttons centered horizontally
    button_new_game = Button((WIDTH - BUTTON_WIDTH) // 2, 200, button_new_game_image, BUTTON_WIDTH, BUTTON_HEIGHT)
    button_exit = Button((WIDTH - BUTTON_WIDTH) // 2, 400, button_exit_image, BUTTON_WIDTH, BUTTON_HEIGHT)

    # Main menu loop
    menu_active = True
    while menu_active:
        mouse_pos = pygame.mouse.get_pos()

        # Draw buttons
        button_new_game.draw(WIN)
        button_exit.draw(WIN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_new_game.is_hovered(mouse_pos):
                    menu_active = False  # Start the game
                elif button_exit.is_hovered(mouse_pos):
                    pygame.quit()
                    quit()

        pygame.display.flip()

def menu_close():
    """
    Displays the end-game menu showing the winner and options to start a new game or exit.

    Returns:
        bool: True if players choose to rebuy/start a new game, else exits the program.
    """
    from app.player import Player
    from app.constants import WIN, WIDTH, BEIGE

    # Determine the winner
    player_list = Player.player_list_chair  
    winner = next((player.name for player in player_list if player.stack != 0), None)
    if winner is None:
        winner = "Both players went all in. No one"

    # Draw background and winner text
    WIN.blit(BACKGROUND_MENU, (0, 0))
    font = pygame.font.SysFont('Inked Skin Personal Use', 60)
    winner_text = font.render(f"{winner} won the game.", True, BEIGE)
    WIN.blit(winner_text, ((WIDTH - winner_text.get_width()) // 2, 100))

    # Create buttons
    button_new_game = Button((WIDTH - BUTTON_WIDTH) // 2, 300, button_new_game_image, BUTTON_WIDTH, BUTTON_HEIGHT)
    button_exit = Button((WIDTH - BUTTON_WIDTH) // 2, 500, button_exit_image, BUTTON_WIDTH, BUTTON_HEIGHT)

    # End menu loop
    rebuy = False
    menu_active = True
    while menu_active:
        mouse_pos = pygame.mouse.get_pos()

        # Draw buttons
        button_new_game.draw(WIN)
        button_exit.draw(WIN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_new_game.is_hovered(mouse_pos):
                    rebuy = True
                    menu_active = False  # Restart the game
                elif button_exit.is_hovered(mouse_pos):
                    pygame.quit()
                    quit()

        pygame.display.flip()

    return rebuy
