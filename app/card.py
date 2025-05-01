"""
app/card.py

This module defines the Card class representing playing cards in the poker game.
It manages visual representation and positioning of cards on the game screen.
The class inherits from pygame.sprite.Sprite to leverage sprite rendering and collision detection.

Group B Models/Algorithms:
- Simple OOP model (Card class encapsulation)
- UI rendering and positioning based on screen resolution
"""

import pygame
from typing import List

from app.constants import (
    WIDTH, HEIGHT, CARD_WIDTH, CARD_HEIGHT,
    CARD_VERTICAL_OFFSET, CARD_HORIZONTAL_SPACING,
    PLAYER_CARDS_BOTTOM, OPPONENT_CARDS_BOTTOM,
    CARD_SIDE_OFFSET
)

class Card(pygame.sprite.Sprite):
    """
    A class representing a playing card in the poker game.
    
    This class handles the visual representation and positioning of cards on the game screen.
    It inherits from pygame.sprite.Sprite to utilize Pygame's sprite functionality for rendering
    and collision detection.
    """

    def __init__(self, image: pygame.Surface, type_card: str = '') -> None:
        """
        Initialize a new Card instance.

        Arguments:
            image (pygame.Surface): The image surface representing the card
            type_card (str, optional): The type/position of the card in the game. Defaults to ''
        """
        super().__init__()
        # Scale the card image to standard card dimensions
        self.image = pygame.transform.scale(image, (CARD_WIDTH, CARD_HEIGHT))
        self.type_card = type_card
        self.rect = self.image.get_rect()

    def _x_cor(self, width_space: int) -> List[int]:
        """
        Calculate x-coordinates for card placement in the center of the screen.

        Arguments:
            width_space (int): The horizontal spacing between cards

        Returns:
            List[int]: List of x-coordinates for card placement
        """
        # Calculate positions relative to center, from -2 to +2
        positions = range(-2, 3)
        return [
            WIDTH // 2 + pos * (CARD_WIDTH + width_space)
            for pos in positions
        ]

    def put_in_place(self) -> None:
        """
        Position the card on the screen based on its type.
        
        This method handles the placement of cards for:
        - Player's cards (bottom of screen)
        - Opponent's cards (top of screen)
        - Community cards (center of screen): flop, turn, and river
        """
        # Calculate base positions for community cards
        x_coordinates = self._x_cor(CARD_HORIZONTAL_SPACING)
        center_y = HEIGHT // 2 + self.image.get_height() // 2 + CARD_VERTICAL_OFFSET

        # Positioning player cards (at bottom of screen)
        if self.type_card in ['first_card_player', 'second_card_player']:
            self.rect.bottom = PLAYER_CARDS_BOTTOM
            offset = -CARD_SIDE_OFFSET if 'first' in self.type_card else CARD_SIDE_OFFSET
            self.rect.centerx = (WIDTH + offset + 
                               (CARD_WIDTH if 'second' in self.type_card else -CARD_WIDTH)) // 2

        # Positioning opponent cards (at top of screen)
        elif self.type_card in ['first_card_opponent', 'second_card_opponent']:
            self.rect.bottom = OPPONENT_CARDS_BOTTOM
            offset = -CARD_SIDE_OFFSET if 'first' in self.type_card else CARD_SIDE_OFFSET
            self.rect.centerx = (WIDTH + offset + 
                               (CARD_WIDTH if 'second' in self.type_card else -CARD_WIDTH)) // 2

        # Positioning community cards (center of screen)
        elif self.type_card == 'first_card_flop':
            self.rect.centerx = x_coordinates[0]
            self.rect.bottom = center_y
        elif self.type_card == 'second_card_flop':
            self.rect.centerx = x_coordinates[1]
            self.rect.bottom = center_y
        elif self.type_card == 'third_card_flop':
            self.rect.centerx = x_coordinates[2]
            self.rect.bottom = center_y
        elif self.type_card == 'turn_card':
            self.rect.centerx = x_coordinates[3]
            self.rect.bottom = center_y
        elif self.type_card == 'river_card':
            self.rect.centerx = x_coordinates[4]
            self.rect.bottom = center_y
