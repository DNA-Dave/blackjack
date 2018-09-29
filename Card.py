'''
Created on 09/20/2018

This file encapsulates the card class, with method associated with cards

@author: David Wu (dwwu16@stanford.edu)
'''


class Card(object):

    suit = None
    values = None
    denomination = None
    denomination_to_values = {
        "A": [1, 11],
        "2": [2],
        "3": [3],
        "4": [4],
        "5": [5],
        "6": [6],
        "7": [7],
        "8": [8],
        "9": [9],
        "10": [10],
        "J": [10],
        "Q": [10],
        "K": [10]
    }
    suits = {
        'spade' : "♠",
        'heart' : "♥",
        'diamond' : "♦",
        'club' : "♣"
    }

    def __init__(self, suit, denomination):
        self.suit = self.suits[suit]
        self.denomination = denomination
        self.values = self.denomination_to_values[denomination]

    def Card(self):
        return self

    def get_suit(self):
        # returns the suit of the card
        return self.suit

    def get_values(self):
        # returns the possible scores of the card
        return self.values

    def get_denomination(self):
        # returns the denomination of the card
        return self.denomination

    def get_string_array(self):
        # Returns a card graphic comprised of characters to be printed to the screen in a array format so multiple cards
        # can be printed horizontally next to each other

        string_representation = list()

        string_representation.append('┌───────┐')
        string_representation.append((f'| {self.denomination:<2}    |'))
        string_representation.append('|       |')
        string_representation.append((f'|   {self.suit}   |'))
        string_representation.append('|       |')
        string_representation.append((f'|    {self.denomination:>2} |'))
        string_representation.append('└───────┘')

        return string_representation

    def get_string_array_empty(self):
        # Returns a card graphic without card info comprised of characters to be printed to the screen in a array format
        # so multiple cards can be printed horizontally next to each other

        string_representation = list()

        string_representation.append('┌───────┐')
        string_representation.append((f'| ?     |'))
        string_representation.append('|       |')
        string_representation.append((f'|   ?   |'))
        string_representation.append('|       |')
        string_representation.append((f'|     ? |'))
        string_representation.append('└───────┘')

        return string_representation

    def get_non_graphic_string(self):
        return self.get_denomination() + " of " + self.get_suit()


