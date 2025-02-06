import pygame
from app.constant import BLACK, label_player_image, WIDTH, HEIGHT


class PlayerLabel:
    def __init__(self, x, y, player):
        self.x = x
        self.y = y
        font = pygame.font.SysFont('timesnewroman', 20)
        self.text1 = font.render(str(player.name), True, BLACK)  #rendering player name text
        self.text2 = font.render(str(player.stack), True, BLACK)  #rendering player stack text
        #self.text2 = font.render("DUMMMM", True, BLACK)
        #self.image = label_player_image
        self.width = WIDTH * 0.1  #width of the label, scaled to the window's width
        self.height = HEIGHT * 0.1  #height of the label, scaled to the window's height
        self.image = pygame.transform.scale(label_player_image, (self.width, self.height))  #resizing label image
        #self.rect = self.image.get_rect()

    def draw(self, win):
        #displays player label on the window
        win.blit(self.image, (self.x, self.y))  #drawing the label image at the specified position
        win.blit(self.text1,
                 (self.x + (self.width // 2 - self.text1.get_width() // 2),
                  self.y + (self.height // 4 - self.text1.get_height() // 3)))  #drawing player name

        win.blit(self.text2,
                 (self.x + (self.width // 2 - self.text1.get_width() // 3),
                  self.y + (3 * self.height // 4 - self.text1.get_height() // 1.5)))  #drawing player stack
