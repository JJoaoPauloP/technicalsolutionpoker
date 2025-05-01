"""
app/player.py

This module defines the Player class, which represents a poker player and manages their game state.
It handles player attributes such as stack, cards, betting actions, and game status.
The class uses class-level lists to maintain player tracking and seating arrangements.

Group A Models/Algorithms:
- Complex user-defined use of OOP model (dynamic object generation, linked list maintenance)
"""

import pygame
from app.background_loader import label_player_image
from app.constants import WIDTH, HEIGHT, BEIGE, BLUE

# Block: Player class definition and class-level attributes
class Player(object):
    """
    A class to represent a poker player and manage their game state.
    
    This class handles all player-related functionality including managing their stack,
    cards, betting actions, and game status. It uses class-level lists to maintain
    player tracking and seating arrangements.
    
    Class Attributes:
        player_list (list): List tracking all player objects
        player_list_chair (list): List tracking seating arrangement of players
        _position (int): Tracks position/seat number of players
    
    Instance Attributes:
        name (str): Player's name
        stack (int): Current amount of chips/money the player has
        position (int): Player's position/seat number
        live (bool): Whether player is still active in current round
        is_allin (bool): Whether player has gone all-in
        cards (list): Player's hole cards
        score (int): Player's hand score
        hand (str): Description of player's hand
        input_stack (int): Amount player has bet in current round
        bet_betting_phase (int): Amount bet in current betting phase
        win_chips (int): Amount of chips won in current round
        decision (bool): Whether player has made a decision
        action_history (list): History of player's actions
        probability (float): Monte Carlo probability calculation
    
    Methods:
        go_allin(): Puts player all-in
        win(chips): Adds won chips to player's stack
        drop(chips): Removes bet amount from player's stack
        blind(chips): Handles blind bets
        next_round(): Resets player data for new round
        fold(): Handles player folding
        next_betting_phase(): Resets betting phase data
        player_label(): Displays player information on screen
        draw_bet(): Displays bet amount on screen
        draw_pot(): Displays total pot amount on screen
    """
        
    # Class-level lists to track all player objects and seating arrangement
    player_list = []  # List to track all player objects (dynamic collection)
    player_list_chair = []  # List to track the seating arrangement of players
    _position = 0  # Tracking position of players (index or seat number)

    def __init__(self, name, stack):
        """
        Initialize a new Player instance.

        Args:
            name (str): Player's name.
            stack (int): Initial chip count for the player.

        This method dynamically generates player objects and maintains linked lists
        of players and their seating arrangement (Group A model).
        """
        self.__class__.player_list.append(self)  # Add player to player list
        self.__class__.player_list_chair.append(self)  # Add player to seating arrangement
        self.name = name
        self.stack = stack
        self.position = Player._position
        self.live = True
        self.is_allin = False
        self.cards = []  # Store player's hole cards as a list
        self.score = 0
        self.hand = ''
        self.input_stack = 0  # Amount player bet in current round
        self.bet_betting_phase = 0  # Amount bet in current betting phase; resets after each phase
        self.win_chips = 0  # Chips won in current round
        self.decision = False  # Whether player has made a decision
        self.action_history = []  # History of player's actions
        self.probability = 0.0  # Monte Carlo probability (default 0)
        Player._position += 1

    def go_allin(self):
        """
        Put the player all-in, marking them as no longer live but all-in.

        This method updates player state to reflect an all-in decision.
        """
        self.live = False
        self.is_allin = True
        self.decision = True  # Player has made a decision and goes all-in

    def win(self, chips):
        """
        Add won chips to the player's stack and track total chips won this round.

        Args:
            chips (int): Number of chips won.
        """
        self.stack += int(chips)  # Increment player's stack
        self.win_chips += chips  # Track total chips won this round

    def drop(self, chips):
        """
        Deduct chips from player's stack as a bet and update betting phase totals.

        Args:
            chips (int): Number of chips to bet/drop.

        This method reflects the player's betting action and updates decision status.
        """
        self.stack -= int(chips)  # Decrement player's stack
        self.input_stack += chips  # Add to input stack for the round
        self.decision = True  # Player has made a decision
        self.bet_betting_phase += chips  # Increment bet in current betting phase

    def blind(self, chips):
        """
        Deduct blind bet chips from player's stack and update betting phase totals.

        Args:
            chips (int): Number of chips for blind bet.

        This method handles posting blinds during betting rounds.
        """
        self.stack -= chips  # Decrement player's stack for blind bet
        self.input_stack += chips  # Add blind bet to input stack
        self.bet_betting_phase += chips  # Increment bet in betting phase

    def next_round(self):
        """
        Reset player data for the next round.

        This method prepares the player state for a new round of poker.
        """
        self.live = True
        self.is_allin = False
        self.cards = []
        self.score = 0
        self.hand = ''
        self.input_stack = 0
        self.win_chips = 0
        self.decision = False
        self.probability = 0.0  # Reset probability for new round

    def fold(self):
        """
        Handle player folding by marking them as no longer live and resetting score.

        This method updates player state to reflect a fold decision.
        """
        self.live = False  # Player no longer active in round
        self.score = 0  # Reset score for folded player
        self.decision = True  # Player has made a decision (folded)

    def next_betting_phase(self):
        """
        Reset betting phase specific data for the next betting phase.

        This method clears bets and action history for the new betting phase.
        """
        self.bet_betting_phase = 0
        self.action_history = []

    def player_label(self, win, is_turn):
        """
        Draw the player label and display top cards if it's the player's turn.

        Args:
            win (pygame.Surface): Pygame window object to draw on.
            is_turn (bool): Indicates if it is the player's turn.

        This method visually represents player info on the game screen.
        """
        font = pygame.font.SysFont('TimesNewRoman', int(HEIGHT / 72))  # Scale font with resolution
        text1 = font.render(self.name, True, BEIGE)  # Render player name
        text2 = font.render(f'£{self.stack}', True, BEIGE)  # Render player's stack
        text3 = font.render(f'W Probability: {self.probability:.2%}', True, BLUE)  # Render Monte Carlo probability
        width = WIDTH * 0.12  # Width for player label
        height = HEIGHT * 0.12  # Height for player label
        image = pygame.transform.scale(label_player_image, (width, height))  # Resize player label image

        # Calculate positions relative to screen dimensions
        if self == self.player_list_chair[0]:
            x = int(WIDTH * 0.5675)  # Position for first player (bottom)
            y = int(HEIGHT * 0.75)
        elif self == self.player_list_chair[1]:
            x = int(WIDTH * 0.315)  # Position for second player (top)
            y = int(HEIGHT * 0.05)

        # Draw player label with improved text positioning
        win.blit(image, (x, y))
        win.blit(text1, (x + (width // 2 - text1.get_width() // 2),
                         y + (height * 0.25 - text1.get_height() // 2)))  # Name at 25%
        win.blit(text2, (x + (width // 2 - text2.get_width() // 2),
                         y + (height * 0.5 - text2.get_height() // 2)))  # Stack at 50%
        win.blit(text3, (x + (width // 2 - text3.get_width() // 2),
                         y + (height * 0.75 - text3.get_height() // 2)))  # Probability at 75%

    def draw_bet(self, win):
        """
        Draw the bet amount on the screen if greater than zero.

        Args:
            win (pygame.Surface): Pygame window object to draw on.

        This method visually represents the player's current bet.
        """
        if self.bet_betting_phase > 0:
            font = pygame.font.SysFont('timesnewroman', int(HEIGHT / 36))  # Scale font with resolution
            text = font.render(f'£{self.bet_betting_phase}', True, BEIGE)

            if self == self.player_list_chair[0]:
                x = (WIDTH - text.get_width()) // 2  # Center horizontally
                y = int(HEIGHT * 0.70)  # Position for player one's bet (bottom)
            elif self == self.player_list_chair[1]:
                x = (WIDTH - text.get_width()) // 2  # Center horizontally
                y = int(HEIGHT * 0.275)  # Position for player two's bet (top)

            win.blit(text, (x, y))

    @staticmethod
    def draw_pot(win):
        """
        Draw the total pot amount on the screen.

        Args:
            win (pygame.Surface): Pygame window object to draw on.

        This method sums all players' input stacks and bets to display the pot.
        """
        input_stack = sum(player.input_stack for player in Player.player_list)  # Sum all players' input stack
        bets = sum(player.bet_betting_phase for player in Player.player_list)  # Sum all players' bets
        font = pygame.font.SysFont('timesnewroman', int(HEIGHT / 36))  # Scale font with resolution
        text = font.render(f'Pot: £{input_stack - bets}', True, BEIGE)  # Display total pot amount
        x = (WIDTH - text.get_width()) // 2  # Center horizontally
        y = int(HEIGHT * 0.35)  # Position pot text at 35% of screen height
        win.blit(text, (x, y))
