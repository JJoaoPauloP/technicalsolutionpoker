import itertools

def hand(composition):
    """
    Calculates the score of a hand composition based on the poker hand ranking.
    
    The scoring system is relative, where better hands receive higher scores. 
    It evaluates various types of poker hands including Royal Flush, Straight Flush, 
    Four of a Kind, Full House, Flush, Straight, Three of a Kind, Two Pair, Pair, 
    and High Card. 

    :param composition: A list of five cards (strings) to evaluate. For example, 
                        ['2D', '3C', 'AH', 'AC', '7D']
    :return: A tuple containing the score and the name of the hand ranking. 
             For example, (180, 'Royal flush').
    """
    #split card figures and colors
    handfigure = [card[0] for card in composition]
    handcolor = [card[1] for card in composition]

    #convert face card figures to numbers
    dict_figure = {'T': '10', 'J': '11', 'Q': '12', 'K': '13', 'A': '14'}
    handfigure = [dict_figure.get(handfigure[i], handfigure[i]) for i in range(5)]

    #sort the figures numerically
    handfigure = sorted([int(handfigure[i]) for i in range(5)])

    #check for a straight (consecutive cards)
    if [handfigure[i] - handfigure[0] for i in range(5)] == [0, 1, 2, 3, 4] or handfigure == [2, 3, 4, 5, 14]:
        straight = True
    else:
        straight = False

    #condition for Royal Flush
    if handfigure == [10, 11, 12, 13, 14] and len(set(handcolor)) == 1:
        score = 180
        name_poker_hand = 'Royal flush'

    #condition for Straight Flush
    elif straight is True and len(set(handcolor)) == 1:
        score = 160 + handfigure[4]
        name_poker_hand = "Straight Flush"

    #condition for Four of a Kind
    elif handfigure.count(handfigure[2]) == 4:
        if handfigure.count(handfigure[0]) == 1:
            score = 140 + handfigure[1] + handfigure[0] / 100
        else:
            score = 140 + handfigure[0] + handfigure[4] / 100
        name_poker_hand = 'Four of kind'

    #condition for Full House
    elif len(set(handfigure)) == 2 and handfigure.count(handfigure[2]) != 4:
        if handfigure.count(handfigure[0]) == 2:
            score = 120 + handfigure[2] + handfigure[0] / 100
        else:
            score = 120 + handfigure[0] + handfigure[3] / 100
        name_poker_hand = "Full house"

    #condition for Flush
    elif len(set(handcolor)) == 1:
        score = 100 + handfigure[4] / 10 + handfigure[3] / 100 + handfigure[2] / 1000 + handfigure[1] / 10000 + handfigure[0] / 100000
        name_poker_hand = "Flush"

    #condition for Straight
    elif straight is True:
        if handfigure == [2, 3, 4, 5, 14]:
            score = 80
        else:
            score = 80 + handfigure[4]
        name_poker_hand = "Straight"

    #condition for Three of a Kind
    elif handfigure.count(handfigure[2]) == 3 and len(set(handfigure)) == 3:
        handfigure_set = list(set(handfigure))
        handfigure_set.remove(handfigure[2])
        score = 60 + handfigure[2] + handfigure_set[1] / 100 + handfigure_set[0] / 1000
        name_poker_hand = 'Three of kind'

    #condition for Two Pair
    elif handfigure.count(handfigure[1]) == 2 and handfigure.count(handfigure[3]) == 2:
        handfigure_set = list(set(handfigure))
        handfigure_set.remove(handfigure[1])
        handfigure_set.remove(handfigure[3])
        score = 40 + handfigure[3] + handfigure[1] / 10 + handfigure_set[0] / 100
        name_poker_hand = "Two pair"

    #condition for Pair
    elif len(set(handfigure)) == 4:
        if handfigure.count(handfigure[1]) == 2:
            handfigure_set = list(set(handfigure))
            handfigure_set.remove(handfigure[1])
            score = 20 + handfigure[1] + handfigure_set[2] / 100 + handfigure_set[1] / 10000 + handfigure_set[0] / 100000
        elif handfigure.count(handfigure[3]) == 2:
            handfigure_set = list(set(handfigure))
            handfigure_set.remove(handfigure[3])
            score = 20 + handfigure[3] + handfigure_set[2] / 100 + handfigure_set[1] / 10000 + handfigure_set[0] / 100000
        name_poker_hand = "Pair"

    #condition for High Card
    elif len(set(handfigure)) == 5:
        score = handfigure[4] + handfigure[3] / 10 + handfigure[2] / 100 + handfigure[1] / 1000 + handfigure[0] / 10000
        name_poker_hand = "High card"

    return score, name_poker_hand


def players_score(player_list, common_cards):
    """
    Calculates and assigns the best hand score for each player based on their cards 
    and the common cards.

    This function evaluates all possible 5-card combinations of the player's hand 
    and the common cards to determine the best hand.

    :param player_list: A list of player objects for whom the scores will be calculated.
    :param common_cards: A list of community cards shared by all players. 
                          These cards are used in combination with the player's hand.
    :return: None. The function modifies the player objects, assigning them a score 
             and the name of their hand ranking.
    """
    for player in player_list:
        best_score, best_hand = 0, ''
        cards_combinations = list(itertools.combinations(common_cards + player.cards, 5))
        
        #evaluate each combination of player's cards and common cards
        for combination in cards_combinations:
            combination_score, combination_name = hand(combination)
            if combination_score > best_score:
                best_score = combination_score
                player.score, player.hand = best_score, combination_name
