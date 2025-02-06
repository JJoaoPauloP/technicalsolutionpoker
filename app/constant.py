import pygame
from os import path
from app.card_class import Card

pygame.init()

#colour RGB
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BEIGE = (225, 198, 153)
RED = (255, 0, 0)

#screen settings
FPS = 1
HEIGHT = 720
WIDTH = 1280
#WIN = pygame.display.set_mode((WIDTH, HEIGHT))
WIN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN, pygame.RESIZABLE)

#blinds
SB, BB = 25, 50

#load images
images_direction = path.join(path.dirname(__file__), '../images')

#background game
BACKGROUND = pygame.image.load(path.join(images_direction, 'background.png')).convert()
BACKGROUND = pygame.transform.scale(BACKGROUND, (WIDTH, HEIGHT))

#background menu
BACKGROUND_MENU = pygame.image.load(path.join(images_direction, 'menu_background.png')).convert()

#button menu
button_new_game_image = pygame.image.load(path.join(images_direction, 'button_new_game.png')).convert_alpha()
button_exit_image = pygame.image.load(path.join(images_direction, 'button_exit.png')).convert_alpha()

#game button
button_image = pygame.image.load(path.join(images_direction, 'button.png')).convert_alpha()
button_image.set_colorkey(WHITE)

#label player
label_player_image = pygame.image.load(path.join(images_direction, 'label_player.png')).convert_alpha()
label_player_image.set_colorkey(WHITE)

# < cards

deck = ['2C', '3C', '4C', '5C', '6C', '7C', '8C', '9C', 'TC', 'JC', 'QC', 'KC', 'AC', '2S', '3S', '4S', '5S', '6S',
        '7S', '8S', '9S', 'TS', 'JS', 'QS', 'KS', 'AS', '2H', '3H', '4H', '5H', '6H', '7H', '8H', '9H', 'TH', 'JH',
        'QH', 'KH', 'AH', '2D', '3D', '4D', '5D', '6D', '7D', '8D', '9D', 'TD', 'JD', 'QD', 'KD', 'AD']

cards_list_images = ['2C.jpg', '3C.jpg', '4C.jpg', '5C.jpg', '6C.jpg', '7C.jpg', '8C.jpg', '9C.jpg', 'TC.jpg', 'JC.jpg',
                     'QC.jpg', 'KC.jpg', 'AC.jpg', '2S.jpg', '3S.jpg', '4S.jpg', '5S.jpg', '6S.jpg',
                     '7S.jpg', '8S.jpg', '9S.jpg', 'TS.jpg', 'JS.jpg', 'QS.jpg', 'KS.jpg', 'AS.jpg', '2H.jpg', '3H.jpg',
                     '4H.jpg', '5H.jpg', '6H.jpg', '7H.jpg', '8H.jpg', '9H.jpg', 'TH.jpg', 'JH.jpg',
                     'QH.jpg', 'KH.jpg', 'AH.jpg', '2D.jpg', '3D.jpg', '4D.jpg', '5D.jpg', '6D.jpg', '7D.jpg', '8D.jpg',
                     '9D.jpg', 'TD.jpg', 'JD.jpg', 'QD.jpg', 'KD.jpg', 'AD.jpg']

cards_images = [] #list operations (building a list of images)
for img in cards_list_images:
    card_img = pygame.image.load(path.join(images_direction, img)).convert_alpha() #loading card images
    cards_images.append(card_img) #list operations (appending images to the list)

#dictionary with cards object
cards_object = {} #hastag (cards_object acts as a hash table to store cards by their names)
for i in range(len(cards_images)):
    name = deck[i] #using deck to create keys for the dictionary
    cards_object[name] = Card(cards_images[i]) #hastag (storing card object in dictionary by name)

#opponent cards
card_reverse_image = pygame.image.load(path.join(images_direction, 'red_back.png')).convert_alpha() #loading reverse card image
cards_object['reverse_1'] = Card(card_reverse_image) #hashtag (reverse cards to the dictionary)
cards_object['reverse_2'] = Card(card_reverse_image)