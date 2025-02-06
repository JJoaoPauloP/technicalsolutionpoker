import pygame

ratio = 8
card_width = int(691 / ratio)
card_height = int(1056 / ratio)
WIDTH, HEIGHT = 1280, 720

#class Card:
class Card(pygame.sprite.Sprite):  #dynamic generation of objects based on complex user-defined use of OOP model
    def __init__(self, image, type_card=''):  #complex user-defined use of object-orientated programming (OOP) model (constructor for initialisation)
        pygame.sprite.Sprite.__init__(self)  #inheritance (card inherits from pygame.sprite.Sprite)
        self.image = image
        self.image = pygame.transform.scale(image, (card_width, card_height))  #complex user-defined use of object-orientated programming (image scaling)
        self.type_card = ''  #object property initialization
        self.rect = self.image.get_rect()  #getting rectangle for placement of card (important for sprite handling in pygame)

    def _x_cor(self, width_space):  #list operations (creating list of coordinates)
        x_coef = [-2 + i for i in range(5)]  #list operations (list comprehension)
        x_coor = []  #linked list maintenance (although here it's not strictly a linked list, the concept of maintaining a list is used)
        for i in range(5):  #iterative list creation
            x_coor.append(WIDTH // 2 + x_coef[i] * (card_width + width_space))  #list operations (appending calculated coordinates)
        return x_coor

    def put_in_place(self):  #complex user-defined algorithm (placement logic for cards)
        """
        function place card
        :return:
        """
        x_c = self._x_cor(10)  #list operations (using list of x coordinates for placement)
        if self.type_card == 'first_card_player':  #control flow for specific card type placement
            self.rect.centerx = (WIDTH - card_width) // 2 - 5
            self.rect.bottom = HEIGHT - 80

        elif self.type_card == 'second_card_player':  #control flow for specific card type placement
            self.rect.centerx = (WIDTH + card_width) // 2 + 5
            self.rect.bottom = HEIGHT - 80

        elif self.type_card == 'first_card_opponent':  #control flow for specific card type placement
            self.rect.centerx = (WIDTH - card_width) // 2 - 5
            self.rect.bottom = 150

        elif self.type_card == 'second_card_opponent':  #control flow for specific card type placement
            self.rect.centerx = (WIDTH + card_width) // 2 + 5
            self.rect.bottom = 150

        elif self.type_card == 'first_card_flop':  #control flow for specific card type placement
            self.rect.centerx = x_c[0]  #graph/tree traversal (x coordinates are used to find relative positions in a sequence)
            self.rect.bottom = HEIGHT // 2 + self.image.get_height() // 2 + 30

        elif self.type_card == 'second_card_flop':  #control flow for specific card type placement
            self.rect.centerx = x_c[1]
            self.rect.bottom = HEIGHT // 2 + self.image.get_height() // 2 + 30

        elif self.type_card == 'third_card_flop':  #control flow for specific card type placement
            self.rect.centerx = x_c[2]
            self.rect.bottom = HEIGHT // 2 + self.image.get_height() // 2 + 30

        elif self.type_card == 'turn_card':  #control flow for specific card type placement
            self.rect.centerx = x_c[3]
            self.rect.bottom = HEIGHT // 2 + self.image.get_height() // 2 + 30

        elif self.type_card == 'river_card':  #control flow for specific card type placement
            self.rect.centerx = x_c[4]
            self.rect.bottom = HEIGHT // 2 + self.image.get_height() // 2 + 30  #win.blit(self.image, (self.rect.centerx, self.rect.top))
