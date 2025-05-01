"""
app/button_ui.py

This module defines the Button class representing interactive buttons with dynamic text color changes on hover.
It also sets up button instances with calculated positions and sizes for the poker game UI.

Group B Models/Algorithms:
- Simple OOP model (Button class encapsulation)
- UI element positioning and scaling based on screen resolution
"""

import pygame
from app.background_loader import button_image
from app.constants import WIDTH, HEIGHT, BEIGE, BLUE

class Button:
    """
    Represents an interactive button with text that can change based on hover state.
    """

    def __init__(self, x, y, width, height, text=''):
        """
        Initialize a Button object.

        :param x: X-coordinate of the button.
        :param y: Y-coordinate of the button.
        :param width: Width of the button.
        :param height: Height of the button.
        :param text: Text label of the button.
        """
        self.name = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.active = False

        # Scale font size relative to screen height for consistent UI appearance
        font = pygame.font.SysFont('TimesNewRoman', int(HEIGHT / 30.85))
        self.text_surface = font.render(text, True, BEIGE)

        # Scale button image to specified dimensions
        self.image = pygame.transform.scale(button_image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.draft = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw_if_active(self, window):
        """
        Draw the button onto the given window if it is active.

        :param window: Pygame window surface where the button should be drawn.
        """
        if self.active:
            window.blit(self.image, (self.x, self.y))
            window.blit(self.text_surface, (
                self.x + (self.width // 2 - self.text_surface.get_width() // 2),
                self.y + (self.height // 2 - self.text_surface.get_height() // 2)
            ))

    def is_mouse_over(self, mouse_position):
        """
        Check if the mouse is currently hovering over the active button.

        :param mouse_position: Tuple (x, y) of mouse coordinates.
        :return: True if the mouse is over the active button, False otherwise.
        """
        return self.active and self.draft.collidepoint(mouse_position)

    def update_text_colour_on_hover(self, mouse_position):
        """
        Update the button's text colour dynamically based on whether the mouse is hovering over it.

        :param mouse_position: Tuple (x, y) of mouse coordinates.
        """
        font = pygame.font.SysFont('TimesNewRoman', int(HEIGHT / 30.85))  # scaling font size relative to screen height
        if self.draft.collidepoint(mouse_position):
            self.text_surface = font.render(self.name, True, BLUE)  # make the text blue when hovered
        else:
            self.text_surface = font.render(self.name, True, BEIGE)  # make the text beige if not hovered

# --- Button Setup ---

# Generate button spacing for vertical layout
n_spaces = list(range(1, 6))
n_buttons = list(range(5))

# Calculate button dimensions - adjusted for 1080p resolution
width_button = int(WIDTH / 8.2)  # Maintains relative width
height_button = int(HEIGHT / 10.8)  # Scales height relative to screen height
height_space = int(height_button * 0.2)  # Maintains proportional spacing
x_buttons = int(WIDTH / 38.4)  # Scales x position relative to screen width

# Calculate y-positions for each button - adjusted for 1080p resolution
y_button_positions = [
    HEIGHT - (5 * (height_button + height_space)) + (n_spaces[i] * height_space + n_buttons[i] * height_button)
    for i in range(5)
]

# Instantiate button objects with calculated positions and sizes
button_fold = Button(x_buttons, y_button_positions[0], width_button, height_button, 'fold')
button_allin = Button(x_buttons, y_button_positions[1], width_button, height_button, 'all-in')
button_call = Button(x_buttons, y_button_positions[2], width_button, height_button, 'call')
button_check = Button(x_buttons, y_button_positions[2], width_button, height_button, 'check')
button_raise = Button(x_buttons, y_button_positions[3], width_button, height_button, 'raise')

# Store all buttons in a list for easier handling in UI
buttons = [button_fold, button_allin, button_call, button_check, button_raise]
