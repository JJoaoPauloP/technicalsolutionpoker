import pygame
from app.constant import BLACK, WIDTH, HEIGHT, label_player_image, BEIGE

class Player(object): #linked list maintenance (using class level lists to track players)
    player_list = [] #lis to track all player objects ( a type of dynamic collection of objects)
    player_list_chair = [] #list to track the seating arrangement of players
    _position = 0 #tracking position of players (index or seat number)

    def __init__(self, name, stack, kind='human'): #dynamic generation of objects based on complex user defined use of OOP model
        self.__class__.player_list.append(self) #adding the player object to the player list
        self.__class__.player_list_chair.append(self) #adding player object to seating arrangement
        self.name = name
        self.kind = kind  
        self.stack = stack
        self.position = Player._position
        self.live = True
        self.alin = False
        self.cards = []  #updated to store cards as a list
        self.score = 0
        self.hand = ''
        self.input_stack = 0  #how much $ player bet in round
        self.bet_auction = 0  #how much $ player bet in one auction, after each auction this attribute will be reset
        self.win_chips = 0 #chips the player wins
        self.decision = False #whether the player has made a decision
        self.action_history = [] #history of actions taken by the player
        self.probability = 0.0  #monte carlo probability (default: 0)
        Player._position += 1

    def allin(self):
        self.live = False
        self.alin = True
        self.decision = True #player makes a decision and goes all in

    def win(self, chips):
        self.stack += int(chips) #incrementing the player's stack when they win chips
        self.win_chips += chips #tracking the total chips the player wins in this round

    def drop(self, chips):
        self.stack -= int(chips) #decrementing the player's stack wfor dropped chips
        self.input_stack += chips #adding dropped chips to input stack for the round
        self.decision = True #player has made a decision
        self.bet_auction += chips #incrementing bet in this auction

    def blind(self, chips):
        self.stack -= chips #decrementing the player's stack for the blind bet
        self.input_stack += chips #adding blind bet to input stack for round
        self.bet_auction += chips #incrementing bet in auction

    def next_round(self): #resetting player data for the next round
        self.live = True
        self.alin = False
        self.cards = []
        self.score = 0
        self.hand = ''
        self.input_stack = 0
        self.win_chips = 0
        self.decision = False
        self.probability = 0.0  #reset probability for the new round

    def fold(self):
        self.live = False #player is no longer live in the round after folding
        self.score = 0 #resetting score for folded player
        self.decision = True #player has made a decision (folded)

    def next_auction(self): #resetting auction specific data for the next auction
        self.bet_auction = 0
        self.action_history = []

    def player_label(self, win, is_turn):
        """
        Draws player label and optionally displays cards if it's the player's turn.
        :param win: Pygame window object
        :param is_turn: Boolean indicating if it's the player's turn
        """
        font = pygame.font.SysFont('Arial', 15)
        text1 = font.render(self.name, True, BLACK) #rendering player name
        text2 = font.render(f'{self.stack}$', True, BLACK) #rendering player's stack
        text3 = font.render(f'M.C. Prob: {self.probability:.2%}', True, BLACK) #rendering monte carlo probability
        width = WIDTH * 0.1 #width for the player label
        height = HEIGHT * 0.1 #height for the player label
        image = pygame.transform.scale(label_player_image, (width, height)) #resizing player label

        if self == self.player_list_chair[0]:
            x, y = 750, 550 #position for the first player
        elif self == self.player_list_chair[1]:
            x, y = 400, 50 #positioion for the second player

        #draw player label
        win.blit(image, (x, y))
        win.blit(text1, (x + (width // 2 - text1.get_width() // 2),
                         y + (height // 4 - text1.get_height() // 3)))
        win.blit(text2, (x + (width // 2 - text2.get_width() // 2),
                         y + (2 * height // 4 - text2.get_height() // 3)))
        win.blit(text3, (x + (width // 2 - text3.get_width() // 2),
                         y + (3 * height // 4 - text3.get_height() // 3)))

        #show cards if it's the player's turn
        if is_turn:
            cards_text = font.render(f'Cards: {" ".join(self.cards)}', True, BLACK)
            win.blit(cards_text, (x + (width // 2 - cards_text.get_width() // 2),
                                  y + (4 * height // 4 - cards_text.get_height() // 3)))

    def draw_bet(self, win):
        if self.bet_auction > 0: #drawing bet amount if it's greater than zero
            font = pygame.font.SysFont('timesnewroman', 20)
            text = font.render(f'{self.bet_auction}$', True, BEIGE)

            if self == self.player_list_chair[0]:
                x, y = (WIDTH - text.get_width()) // 2, 470 #position for player one's bet
            elif self == self.player_list_chair[1]:
                x, y = (WIDTH - text.get_width()) // 2, 220 #position for player two's bet

            win.blit(text, (x, y))

    @staticmethod
    def draw_pot(win): #agregate SQL functions / List operations (calculating the total pot from all players' contributions)
        input_stack = sum(player.input_stack for player in Player.player_list) #summing all players' input stack
        bets = sum(player.bet_auction for player in Player.player_list) #summing all players' auction bets
        font = pygame.font.SysFont('timesnewroman', 20)
        text = font.render(f'Pot: {input_stack - bets}$', True, BEIGE) #displaying total pot amount
        x, y = (WIDTH - text.get_width()) // 2, 270
        win.blit(text, (x, y))