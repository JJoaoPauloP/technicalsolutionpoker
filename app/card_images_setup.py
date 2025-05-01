"""
app/card_images_setup.py

This module loads and prepares all card images for the poker game.
It maps card names to Card objects with their corresponding images,
including special back side cards for hidden opponent cards.

Group B Models/Algorithms:
- Simple file access and image processing
- Dictionary mapping for efficient card lookup
- Use of pygame for image loading and transformation
"""

import pygame
from os import path
from app.card import Card
pygame.init()

# Setting the path to the images directory
images_directory = path.join(path.dirname(__file__), '../images')

# Defining the deck in text form (card names) e.g. 2C = 2 of Clubs
deck = [
    '2C', '3C', '4C', '5C', '6C', '7C', '8C', '9C', 'TC', 'JC', 'QC', 'KC', 'AC',
    '2S', '3S', '4S', '5S', '6S', '7S', '8S', '9S', 'TS', 'JS', 'QS', 'KS', 'AS',
    '2H', '3H', '4H', '5H', '6H', '7H', '8H', '9H', 'TH', 'JH', 'QH', 'KH', 'AH',
    '2D', '3D', '4D', '5D', '6D', '7D', '8D', '9D', 'TD', 'JD', 'QD', 'KD', 'AD'
]

# Defining the list of corresponding card image filenames
deck_image_filenames = [f"{card}.png" for card in deck]

# Loading all card images into a list
card_images = [] 
for filename in deck_image_filenames:
    image_path = path.join(images_directory, filename)
    card_image = pygame.image.load(image_path).convert_alpha()
    card_images.append(card_image)

# Creating a dictionary mapping card names to Card objects
cards_object = {}
for card_name, card_image in zip(deck, card_images):
    cards_object[card_name] = Card(card_image)

# Loading the card back image (for opponents hidden cards)
card_back_image = pygame.image.load(path.join(images_directory, 'black_back.png')).convert_alpha()

# Adding special "back side" cards to the dictionary
cards_object['back_side_1'] = Card(card_back_image)
cards_object['back_side_2'] = Card(card_back_image)
