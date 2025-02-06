import pygame
import pygame_widgets

def show_down(common_cards):
    """
    Function display showdown
    :param common_cards: list of common cards
    :return:
    """

    #draw opponent card
    from app.player_class import Player
    from app.constant import WIN
    player_list_chair = Player.player_list_chair
    cards = pygame.sprite.Group()

    #draw player cards
    sub_card = give_card('player', player_list_chair[0].cards)
    [cards.add(card) for card in sub_card]

    #draw opponent cards
    sub_card = give_card('opponent', player_list_chair[1].cards)
    [cards.add(card) for card in sub_card]

    #draw table cards
    sub_card = give_card('flop', common_cards[0:3])
    [cards.add(card) for card in sub_card]
    sub_card = give_card('turn', [common_cards[3]])
    [cards.add(card) for card in sub_card]
    sub_card = give_card('river', [common_cards[4]])
    [cards.add(card) for card in sub_card]

    cards.draw(WIN)


def recap_round(list_winner, common_cards=None):
    """
    Function displays the round summary
    :param list_winner: list_winner = [(player1, win_value1),(player2, win_value2)]
    :param common_cards:
    :return:
    """

    from app.constant import WIN, BACKGROUND, WIDTH, HEIGHT, BEIGE
    font = pygame.font.SysFont('Inked Skin Personal Use', 20)
    WIN.blit(BACKGROUND, BACKGROUND.get_rect())
    draw_player()

    def y_coordinate(HEIGHT, text_height, space_height, space_bottom, n_winner):
        #calculates the height position for the round summary subtitles
        w = [n_winner - 1 - i for i in range(n_winner)]
        x = HEIGHT - text_height - space_bottom
        y_co = []
        for i in range(len(w)):
            y_co.append(x - w[i] * (text_height + space_height))
        return y_co

    #display who, how much win
    if len(list_winner) == 1:
        text = '{} won {}$'.format(str(list_winner[0][0].name), str(list_winner[0][1]))
        text = font.render(text, True, BEIGE)
        y_c = y_coordinate(HEIGHT, text.get_height(), text.get_height() // 2, HEIGHT * 0.1, len(list_winner))
        x, y = WIDTH * 0.05, y_c[0]
        WIN.blit(text, (x, y))
        pygame.display.flip()
        pygame.time.delay(1000)
    else:
        show_down(common_cards)
        text = ''
        text = font.render(text, True, BEIGE)
        y_c = y_coordinate(HEIGHT, text.get_height(), text.get_height() // 2, HEIGHT * 0.1, len(list_winner))
        for i in range(len(list_winner)):
            text = '{} won {}$ with {}'.format(str(list_winner[i][0].name), str(list_winner[i][1]),
                                               str(list_winner[i][0].hand))
            text = font.render(text, True, BEIGE)
            x, y = WIDTH * 0.05, y_c[i]
            WIN.blit(text, (x, y))
        pygame.display.flip()
        #take a second pause
        pygame.time.delay(3000)


def draw_player(active_player_index=0):
    #function displays player labels and bet information
    from app.player_class import Player
    from app.constant import WIN
    player_list_chair = Player.player_list_chair
    for index, player in enumerate(player_list_chair):
        is_turn = index == active_player_index
        player.player_label(WIN, is_turn)
        player.draw_bet(WIN)
    pygame.display.flip()



def give_card(type_card, cards):
    """
    Function put the cards on the right place and return group of cards sprite.
    :param type_card: type of card, one of these player, opponent, flop, turn, river
    :param cards: list of cards ex. ['2S', '3C']
    :return:group of cards sprite
    """

    import pygame
    from app.constant import cards_object

    dict_cards = {'player': ['first_card_player', 'second_card_player'],
                  'opponent': ['first_card_opponent', 'second_card_opponent'],
                  'flop': ['first_card_flop', 'second_card_flop', 'third_card_flop'],
                  'turn': ['turn_card'],
                  'river': ['river_card']}

    sub_cards = pygame.sprite.Group()
    list_cards = dict_cards[type_card]  # 'first_card_player', 'second_card_player'

    for i in range(len(list_cards)):
        card_object = cards_object[cards[i]]
        card_object.type_card = list_cards[i]
        card_object.put_in_place()
        sub_cards.add(card_object)
    return sub_cards


def event_ESC_pressed(get_pressed):
    if get_pressed[pygame.K_ESCAPE]:
        exit()


def cover_up_cards():
    #function return cover up cards opponents
    from app.constant import cards_object
    reverse_cards = pygame.sprite.Group()
    reverse_card_1 = cards_object['reverse_1']
    reverse_card_2 = cards_object['reverse_2']
    reverse_card_1.type_card = 'first_card_opponent'
    reverse_card_2.type_card = 'second_card_opponent'
    reverse_card_1.put_in_place()
    reverse_card_2.put_in_place()
    reverse_cards.add(reverse_card_1)
    reverse_cards.add(reverse_card_2)
    return reverse_cards


def draw_buttons(buttons):
    #function displays buttons
    from app.constant import WIN
    [button.draw(WIN) for button in buttons if button.active]


def arrange_room(common_cards=None, active_player_index=0):
    """
    Function to draw the background, player cards, and opponent cards.
    :param common_cards: list of community cards
    :param active_player_index: index of the active player
    """
    from app.constant import WIN, BACKGROUND
    from app.player_class import Player

    player_list_chair = Player.player_list_chair
    WIN.blit(BACKGROUND, BACKGROUND.get_rect())

    cards = pygame.sprite.Group()

    #draw player cards
    sub_card = give_card('player', player_list_chair[0].cards)
    [cards.add(card) for card in sub_card]

    #draw opponent cards 
    if active_player_index == 1:
        sub_card = give_card('opponent', player_list_chair[1].cards)
    else:  
        sub_card = cover_up_cards()
    [cards.add(card) for card in sub_card]

    cards.draw(WIN)

    #draw community cards
    if common_cards is not None:
        #draw pot table
        Player.draw_pot(WIN)

        #draw flop cards
        sub_card = give_card('flop', common_cards[0:3])
        [cards.add(card) for card in sub_card]

        #draw turn card
        if len(common_cards) >= 4:
            sub_card = give_card('turn', [common_cards[3]])
            [cards.add(card) for card in sub_card]

        #draw river card
        if len(common_cards) == 5:
            sub_card = give_card('river', [common_cards[4]])
            [cards.add(card) for card in sub_card]

    cards.draw(WIN)


def player_decision(buttons, dict_options, min_raise, max_raise, common_cards=None, active_player_index=0):
    """
    Function display GUI for player and return action
    :param buttons: buttons object
    :param dict_options: dict options where is information about which buttons are active
    :param min_raise: minimum raise value
    :param max_raise: maximum raise value
    :param common_cards: list of common cards
    :param active_player_index: index of the active player
    :return: information about which button has been pressed,
    and if the button raise has been pressed, then information about how much is the raise
    """
    from app.constant import WIN, BEIGE
    from app.button_class import x_buttons, y_button, width_button
    import pygame
    import sys

    font = pygame.font.SysFont('Arial', 40)

    #input box settings
    input_box = pygame.Rect(x_buttons, y_button[4] + 30, width_button * 2, 40)
    input_color_active = (94, 151, 82)
    input_color_inactive = BEIGE
    input_color = input_color_inactive
    input_text = ""

    #activate proper buttons
    for button in buttons:
        if dict_options[button.name]:
            button.active = True
        else:
            button.active = False

    cards = pygame.sprite.Group()
    arrange_room(common_cards, active_player_index=active_player_index)

    cards.update()
    draw_player()

    pause_action = True
    active_input = False
    decision = None

    while pause_action:
        draw_buttons(buttons)

        for event in pygame.event.get():
            mouse_position = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                #check if input box is clicked
                if input_box.collidepoint(event.pos):
                    active_input = True
                    input_color = input_color_active
                else:
                    active_input = False
                    input_color = input_color_inactive

                #check if a button is clicked
                for button in buttons:
                    if button.isOver(mouse_position) and button.active:
                        if button.name == 'raise':
                            if input_text.isdigit():
                                raise_amount = int(input_text)
                                if min_raise <= raise_amount <= max_raise:
                                    decision = [button.name, raise_amount]
                                    pause_action = False
                                else:
                                    print(f"Raise amount must be between {min_raise} and {max_raise}.")
                            else:
                                print("Please enter a valid number.")
                        else:
                            decision = [button.name]
                            pause_action = False

            if event.type == pygame.KEYDOWN:
                if active_input:
                    if event.key == pygame.K_RETURN:
                        if input_text.isdigit():
                            raise_amount = int(input_text)
                            if min_raise <= raise_amount <= max_raise:
                                decision = ['raise', raise_amount]
                                pause_action = False
                            else:
                                print(f"Raise amount must be between {min_raise} and {max_raise}.")
                        else:
                            print("Please enter a valid number.")
                    elif event.key == pygame.K_BACKSPACE:
                        #handle backspace
                        if len(input_text) > 0:
                            input_text = input_text[:-1]
                        WIN.fill((0, 0, 0))  #clear screen
                        arrange_room(common_cards, active_player_index=active_player_index)
                        draw_player()
                        draw_buttons(buttons)
                        pygame.draw.rect(WIN, input_color, input_box, 2)
                        text_surface = font.render(input_text, True, BEIGE)
                        WIN.blit(text_surface, (input_box.x + 10, input_box.y + 5))
                        pygame.display.update()
                    else:
                        input_text += event.unicode

            if event.type == pygame.MOUSEMOTION:
                for button in buttons:
                    if button.active:
                        button.bigger(mouse_position)

        #draw the input box
        pygame.draw.rect(WIN, input_color, input_box, 2)
        text_surface = font.render(input_text, True, BEIGE)
        WIN.blit(text_surface, (input_box.x + 10, input_box.y + 5))
        pygame.display.update()

        get_pressed = pygame.key.get_pressed()
        event_ESC_pressed(get_pressed)

    return decision




def split_pot():
    #function changing players stack and returns how much they win in round.
    import operator
    from app.player_class import Player
    player_list = Player.player_list_chair.copy()

    #remove players which fold
    for player in player_list:
        if player.live is False and player.alin is False:
            player_list.remove(player)

    #to calculate reword function needs sorted players list according to a score with descending order and then according to input stack with ascending order
    player_list.sort(key=operator.attrgetter('input_stack'))
    player_list.sort(key=operator.attrgetter('score'), reverse=True)
    n = len(player_list)
    player_score, input_stack = [], []

    for player in player_list:
        player_score.append(player.score)
        input_stack.append(player.input_stack)

    win_list = [0] * n
    input_in_game = [0] * n

    #calculates how many players will be given back the chips they have put into the main pot
    for i in range(n):
        if player_score[i] == max(player_score):
            input_in_game[i] = input_stack[i]
        else:
            aux = [0] * n
            new_input = [0] * n
            for j in range(n):
                if player_score[j] != player_score[i]:
                    aux[j] = 1
            for j in range(n):
                new_input[j] = aux[j] * input_stack[j]
            if input_stack[i] - max(new_input[0:i]) < 0:
                input_in_game[i] = 0
            else:
                input_in_game[i] = input_stack[i] - max(new_input[0:i])

    #calculates how many each player wins the chips
    for i in range(n):
        number_division = player_score[i:].count(player_score[i])
        for j in range(i + 1, n):
            if player_score[i] > player_score[j]:
                if input_stack[i] >= input_stack[j]:
                    win_list[i] += input_stack[j] / number_division
                    input_stack[j] = 0
                elif input_stack[i] < input_stack[j]:
                    win_list[i] += input_stack[i] / number_division
                    input_stack[j] -= input_stack[i]
        if number_division > 1:
            for k in range(i + 1, n):
                if player_score[i] == player_score[k]:
                    win_list[k] = win_list[i]
                    input_stack[k] -= input_stack[i]

    #sum of chips returned and won
    list_winner = []
    for i in range(n):
        win_value = input_in_game[i] + win_list[i]
        list_winner.append((player_list[i], int(win_list[i])))
        player_list[i].win(win_value)

    return list_winner


def one_player_win():
    #function changing player stack who win, and return list tuple who win and how much
    from app.player_class import Player
    player_list = Player.player_list_chair.copy()
    list_winner = []
    for player in player_list:
        if player.live or player.alin:
            win_value = sum([player.input_stack for player in player_list])
            player.win(win_value)
            list_winner.append((player, win_value - player.input_stack))
    return list_winner


def change_players_positions(shift):
    """
    Function change each player position
    order in Player.player_list are changed
    :param shift:
    :return: change each player position
    """

    import operator
    from app.player_class import Player
    player_list = Player.player_list
    number_players = len(player_list)
    for player in player_list:
        player.position = (player.position + shift) % number_players
    player_list.sort(key=operator.attrgetter('position'))