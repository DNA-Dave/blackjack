'''
Created on 09/22/2018

This class represents a hand in the game of blackjack, and contains methods associated with a hand

@author: David Wu (dwwu16@stanford.edu)
'''


class Hand(object):

    cards_in_hand = None
    curr_scores_of_hand = None

    def __init__(self):
        self.cards_in_hand = list()
        self.curr_scores_of_hand = list()

    def Hand(self):
        return self

    def add_card(self, new_card):
        # Adds new_card into the current hand and updates the scores of the hand
        self.cards_in_hand.append(new_card)
        card_values = new_card.get_values()
        if len(self.curr_scores_of_hand) == 0:
            self.curr_scores_of_hand = card_values
        else:
            new_scores_of_hand = []
            for card_value in card_values:
                for score in self.curr_scores_of_hand:
                    new_scores_of_hand.append(score + card_value)
            self.curr_scores_of_hand = new_scores_of_hand

    def get_cards(self):
        # returns the array of cards that make up the hand
        return self.cards_in_hand

    def get_scores(self):
        # returns the array of all possible scores of the hand
        return self.curr_scores_of_hand
