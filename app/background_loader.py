"""
app/background_loader.py

This module handles loading and preparing all image assets used in the poker game.
It supports loading images with optional scaling and transparency settings.

Group B Models/Algorithms:
- Simple file access and image processing
- Use of pygame for image loading and transformation
"""

import pygame
from os import path
from app.constants import WIDTH, HEIGHT, WHITE

def load_image(filename, scale_to=None, colorkey=None):
    """
    Loads an image from the images directory.

    Optionally scales the image to a specified size and sets a transparency color key.

    :param filename: Name of the image file to load.
    :param scale_to: Tuple (width, height) to scale the image to. If None, keeps original size.
    :param colorkey: RGB tuple to set as transparent, or None for no transparency change.
    :return: Loaded pygame Surface (image) 
    """
    # Load image with alpha channel support for transparency
    img = pygame.image.load(path.join(images_direction, filename)).convert_alpha()

    # Set transparency color key if provided
    if colorkey is not None:
        img.set_colorkey(colorkey)

    # Scale image if scaling dimensions are provided
    if scale_to is not None:
        img = pygame.transform.scale(img, scale_to)
    return img

# Set up directory path for where images are stored
images_direction = path.join(path.dirname(__file__), '../images')

# Load and prepare all necessary images for the game UI
BACKGROUND = load_image('background.png', scale_to=(WIDTH, HEIGHT))  # Background image for the main game
BACKGROUND_MENU = load_image('menu_background.png')  # Background image for menu screen
label_player_image = load_image('label_player.png', colorkey=WHITE)  # Label image for identifying players
button_image = load_image('button.png', colorkey=WHITE)  # General button for in-game UI
button_new_game_image = load_image('button_new_game.png')  # Button image for 'new game' in menu
button_exit_image = load_image('button_exit.png')  # Button image for 'exit' in menu
