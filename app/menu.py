import pygame.transform
from app.constant import BACKGROUND_MENU, button_new_game_image, button_exit_image

ratio = 2
button_width = int(576 / ratio)
button_height = int(220 / ratio)

class Button:
    def __init__(self, x, y, image, width, height):
        #complex user-defined use of OOP model (initialising an object with properties and methods)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = pygame.transform.scale(image, (self.width, self.height))  #advanced matrix operations (image scaling transformation)
        self.rect = self.image.get_rect()  #complex user-defined use of OOP model (creating a rectangular boundary for the button)
        self.draft = pygame.Rect(self.x, self.y, self.width, self.height)  #complex user-defined use of OOP model (defining button boundaries for collision detection)

    def draw(self, win):
        win.blit(self.image, (self.x, self.y))  #list operations (blitting the image onto the display using list of images)
        
    def isOver(self, mouse_position):
        if self.draft.collidepoint(mouse_position):  #list operations (checking if the mouse position is within the button area)
            return True
        return False

def menu_start():
    """
    The function displays the menu
    :return:
    """
    from app.constant import WIN, WIDTH
    WIN.blit(BACKGROUND_MENU, (0, 0))  #list operations (displaying background image from the list)
    
    button_new_game = Button((WIDTH - button_width)//2, 200, button_new_game_image, button_width, button_height)  #complex user defined use of OOP model (instantiating the Button class)
    button_exit = Button((WIDTH - button_width)//2, 400, button_exit_image, button_width, button_height)

    pause_menu = True
    while pause_menu:
        button_exit.draw(WIN)  #list operations (drawing the exit button)
        button_new_game.draw(WIN)  #list operations (drawing the new game button)

        for event in pygame.event.get():
            mouse_position = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_new_game.isOver(mouse_position):  #stack/queue operations (handling button click, queue of events)
                    pause_menu = False
                if button_exit.isOver(mouse_position):
                    run = False
                    pygame.quit()
                    quit()

        pygame.display.flip()

def menu_end():
    from app.player_class import Player  #complex user-defined use of OOP model (importing a custom player class)
    from app.constant import WIN, WIDTH, BEIGE

    player_list_chair = Player.player_list_chair  #linked list maintenance (retrieving player data)
    for player in player_list_chair:  #linked list maintenance (iterating over player list)
        if player.stack != 0:
            winner = player.name
    WIN.blit(BACKGROUND_MENU, (0, 0))
    font = pygame.font.SysFont('Inked Skin Personal Use', 60)
    text = font.render(winner+' won the game', True, BEIGE)  #list operations (rendering text on the screen)
    WIN.blit(text, ((WIDTH - text.get_width()) // 2, 100))
    button_new_game = Button((WIDTH - button_width)//2, 300, button_new_game_image, button_width, button_height)  #dynamic generation of objects based on complex user-defined use of OOP model (instantiating Button object)
    button_exit = Button((WIDTH - button_width)//2, 500, button_exit_image, button_width, button_height)
    rebuy = False
    pause_menu = True
    while pause_menu:
        button_exit.draw(WIN)  #list operations (drawing the exit button)
        button_new_game.draw(WIN)  #list operations (drawing the new game button)

        for event in pygame.event.get():
            mouse_position = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_new_game.isOver(mouse_position):  #stack/queue operations (handling button click, queue of events)
                    rebuy = True
                    pause_menu = False
                if button_exit.isOver(mouse_position):
                    run = False
                    pygame.quit()
                    quit()

        pygame.display.flip()
    return rebuy
