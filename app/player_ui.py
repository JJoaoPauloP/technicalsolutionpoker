"""
app/player_ui.py

This module defines the PlayerLabel class responsible for displaying player information on the game screen.
It visually represents the player's name and current stack using a background label image.

Group B Models/Algorithms:
- Simple OOP model (PlayerLabel class encapsulation)
- UI rendering and positioning based on screen resolution
"""

import pygame
from app.background_loader import label_player_image
from app.constants import BEIGE, WIDTH, HEIGHT


class PlayerLabel:
    """
    Represents and displays the player information on the game screen.
    
    This class handles the visual representation of a player's information including their name and current stack (money amount)
    using a background label image.
    
    Attributes:
        x (int): X-coordinate position of the label on screen
        y (int): Y-coordinate position of the label on screen
        text1 (Surface): Rendered text surface for player's name
        text2 (Surface): Rendered text surface for player's stack amount
        width (float): Width of the label (10% of screen width)
        height (float): Height of the label (10% of screen height)
        image (Surface): Scaled background image for the label
    
    Methods:
        draw(win): Draws the player label on the specified window surface,
                  displaying the player's name and stack amount centered on the label.
    """
        
    def __init__(self, x, y, player):
        self.x = x
        self.y = y
        # Scale font size relative to screen height for consistent UI appearance
        font = pygame.font.SysFont('timesnewroman', int(HEIGHT / 54))
        self.text1 = font.render(str(player.name), True, BEIGE)  # Render player name text
        self.text2 = font.render(str(player.stack), True, BEIGE)  # Render player stack text
        self.width = WIDTH * 0.12  
        self.height = HEIGHT * 0.12  
        # Resize label background image to fit label dimensions
        self.image = pygame.transform.scale(label_player_image, (self.width, self.height))

    def draw(self, win):
        # Display player label on the window
        win.blit(self.image, (self.x, self.y))  # Draw the label image at the specified position
        # Center the name text horizontally and position it vertically at 1/3 height
        win.blit(self.text1,
                 (self.x + (self.width // 2 - self.text1.get_width() // 2),
                  self.y + (self.height // 3 - self.text1.get_height() // 2)))  # Draw player name

        # Center the stack text horizontally and position it vertically at 2/3 height
        win.blit(self.text2,
                 (self.x + (self.width // 2 - self.text2.get_width() // 2),
                  self.y + (2 * self.height // 3 - self.text2.get_height() // 2)))  # Draw player stack
