"""
app/constants.py

This module defines constants used throughout the poker game,
including colors, screen settings, card dimensions, and positioning.

Group C Models/Algorithms:
- Appropriate choice of simple data types
- Simple mathematical calculations for scaling and positioning
"""

import pygame
pygame.init()

# Defining common colors in RGB format
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BEIGE = (245, 245, 220)
BLACK = (0, 0, 0)
BLUE = (80, 125, 250)

# Screen settings
FPS = 1  # Frames per second for game loop timing
WIDTH, HEIGHT = 1920, 1080  # Screen resolution
WIN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN, pygame.RESIZABLE)  # Game window
RATIO = 8  # General ratio used for scaling UI elements
BUTTON_WIDTH = int(576 / 2)  # Larger button width for menu
BUTTON_HEIGHT = int(220 / 2)  # Larger button height for menu

# Blinds values for betting rounds
small_blind, big_blind = 5, 10

# Positioning card and its dimensions
CARD_SCALE_RATIO = 6  # Reduced to make cards larger
CARD_WIDTH = int(691 / CARD_SCALE_RATIO)  # Original card width scaled down
CARD_HEIGHT = int(1056 / CARD_SCALE_RATIO)  # Original card height scaled down
CARD_VERTICAL_OFFSET = int(HEIGHT / 36)  # Scales with screen height
CARD_HORIZONTAL_SPACING = int(WIDTH / 192)  # Scales with screen width

# Card positioning constants
PLAYER_CARDS_BOTTOM = HEIGHT - int(HEIGHT / 13.5)  # Proportional bottom margin for player cards
OPPONENT_CARDS_BOTTOM = int(HEIGHT / 5.4)  # Moved down (changed from 7.2 to 5.4) for opponent cards
CARD_SIDE_OFFSET = int(WIDTH / 384)  # Scales with screen width for card side offset
