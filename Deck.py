'''
Created on 09/20/2018

This file represents the deck of cards, and methods associated with a deck

@author: David Wu (dwwu16@stanford.edu)
'''

from Card import Card
from random import shuffle


class Deck(object):

    cards = []
    num_decks = None

    card_denominations = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]

    suits = ['spade', 'heart', 'diamond', 'club']

    def __init__(self, num_decks):
        # creates the deck by repeating adding single standard decks until the deck contains the correct number of cards
        self.num_decks = num_decks
        for i in range(num_decks):
            self.generate_single_deck()
        self.shuffle()

    def generate_single_deck(self):
        # adds a single standard deck to the current deck
        for suit in self.suits:
            for card_denominator in self.card_denominations:
                new_card = Card(suit, card_denominator)
                self.cards.append(new_card)

    def shuffle(self):
        # shuffles the completed deck
        shuffle(self.cards)

    def draw(self):
        # draws a card from the deck
        return self.cards.pop()

    def get_deck(self):
        #return all of the cards left in the deck
        return self.cards

    def Deck(self):
        return self