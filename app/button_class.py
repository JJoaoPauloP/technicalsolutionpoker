import pygame
from app.constant import button_image, BLACK, WIDTH, HEIGHT


class Button: #complex user defined use of OOP model (class defining button objects)
    def __init__(self, x, y, width, height, text=''):
        self.name = text
        self.x = x
        self.y = y
        self.active = False
        font = pygame.font.SysFont('Arial', 30)
        self.text = font.render(text, True, BLACK)
        self.width = width
        self.height = height
        self.image = pygame.transform.scale(button_image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.draft = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, win): #server side scripting (rendering button dynamically based on state)
        if self.active:
            win.blit(self.image, (self.x, self.y))
            win.blit(self.text,
                     (self.x + (self.width // 2 - self.text.get_width() // 2),
                      self.y + (self.height // 2 - self.text.get_height() // 2)))

    def isOver(self, mouse_position): #list operations (checking if the button is hovered over)
        if self.draft.collidepoint(mouse_position) and self.active:
            return True
        return False

    def bigger(self, mouse_position): #complex user defined algorithm(changing button text colour dynamically based on hover state)
        font = pygame.font.SysFont('Arial', 30)
        if self.draft.collidepoint(mouse_position):
            self.text = font.render(self.name, True, (0, 0, 255))
        else:
            self.text = font.render(self.name, True, BLACK)

#list operations (creating lists using list comprehensions)
n_spaces = [i for i in range(1, 6)]
n_buttons = [i for i in range(5)]

#calculate button properties
width_button = int(WIDTH / 8.2)

height_button = 100
height_space = int(height_button * 0.2)
x_buttons = 50

#list operations (generating y positions for buttons)
y_button = [n_spaces[i] * height_space + n_buttons[i] * height_button for i in range(5)]
top_space = HEIGHT - 5 * (height_button + height_space)
y_button = [top_space + y_button[i] for i in range(5)]


#dynamic generation of objects based on complex user defined use of OOP model
#creting button objects dynamically
button_fold = Button(x_buttons, y_button[0], width_button, height_button, 'fold')
button_allin = Button(x_buttons, y_button[1], width_button, height_button, 'all-in')
button_call = Button(x_buttons, y_button[2], width_button, height_button, 'call')
button_check = Button(x_buttons, y_button[2], width_button, height_button, 'check')
button_raise = Button(x_buttons, y_button[3], width_button, height_button, 'raise')
#list operations (storing button objects in a list)
buttons = [button_fold, button_allin, button_call, button_check, button_raise]
