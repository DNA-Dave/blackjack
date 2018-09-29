'''
Created on 09/22/2018

This file contains the blackjack game class. Most of the mechanics of the game are encoded here.

@author: David Wu (dwwu16@stanford.edu)
'''


from Hand import Hand
from Deck import Deck
from Card import Card
import os
import math

class Blackjack(object):

    # Class Variables
    starting_money = None
    num_players = None
    array_pointer = None
    used_player_names = None
    map_player_to_money = None
    players_with_no_money = None

    NUM_DECKS = 6
    BLACKJACK_MULTIPLIER = 1.5
    PLAYER_MAX = 7
    PLAYER_MIN = 1
    MONEY_MIN = 1
    MONEY_MAX = 100000000
    GO_BACK_STRING = "go back"
    YES_STRING = "y"
    NO_STRING = "n"
    GO_BACK_INPUT = 0
    VALID_INPUT = 1
    NOT_VALID_INPUT = -1
    MAX_LEN_NAMES = 30
    MIN_BET = 1
    NUM_LINES_PER_CARD = 7
    DEALER_STAND_SCORE = 17
    INT_STAND = 1
    INT_HIT = 2
    INT_DOUBLE = 3
    INT_SPLIT = 4
    INT_BLACKJACK = 21

    all_moves = {
        1: "Stand",
        2: "Hit",
        4: "Split",
        3: "Double Down",
    }

    # After the players have entered the number of players, the starting money for each player, and the names of the
    # players, this method prints this information to the screen to confirm the choice
    def print_set_vals(self):
        print("")
        print("SUMMARY OF ENTERED INFORMATION")
        print("Starting money for each player: " + str(self.starting_money))
        print("Number of players: " + str(self.num_players))
        all_names = ""
        for i in range(len(self.used_player_names)):
            all_names += self.used_player_names[i]
            if i != len(self.used_player_names) - 1:
                all_names += ", "
        print("All names: " + all_names)

    # This method takes in a string that represents input from the user. The input should represent a name, and
    # this method validates that the input is a valid name (IE not empty, not longer than self.MAX_LEN_NAMES, and not
    # the string "go back" that goes back to the previous information entry method). Returns a integer that instructs the
    # calling method of the result of the validation
    def validate_input_str(self, string_input):
        if string_input == "" or len(string_input) > self.MAX_LEN_NAMES:
            return self.NOT_VALID_INPUT
        elif string_input == self.GO_BACK_STRING:
            return self.GO_BACK_INPUT
        elif string_input in self.used_player_names:
            return self.NOT_VALID_INPUT
        else:
            return self.VALID_INPUT

    # This method takes in a string that represents input from the user. The input should represent a number, and
    # this method validates that the input is a valid number input (IE not empty, no other characters other than digits,
    # and not the string "go back" that goes back to the previous information entry method). Also validates the input is
    # between the lower_bound and upper_bound parameters. Returns a integer that instructs the calling method of the
    # result of the validation
    def validate_input_int(self, num_players_input, lower_bound, upper_bound):
        if num_players_input.isdigit():
            integer_form = int(num_players_input)
            if lower_bound <= integer_form <= upper_bound:
                return self. VALID_INPUT
            else:
                return self.NOT_VALID_INPUT
        elif num_players_input == self.GO_BACK_STRING:
            return self.GO_BACK_INPUT
        else:
            return self.NOT_VALID_INPUT

    # Method called that gets input from the user on the number of players that are to be in the current game.
    # If use enters a invalid input, repeatedly prompts user until valid input is entered
    def get_num_players(self):
        print("")
        num_players_input_text = "Number of Players (1-7): "
        num_players_input = input(num_players_input_text)
        num_players_validated_output = self.validate_input_int(num_players_input, self.PLAYER_MIN, self.PLAYER_MAX)
        while num_players_validated_output == self.NOT_VALID_INPUT or num_players_validated_output == self.GO_BACK_INPUT:
            if num_players_validated_output == self.NOT_VALID_INPUT:
                print("Sorry, that is not a valid number of players. Please enter a valid number (digits only, 1-7)!")
            else:
                print("Sorry, this is the first setting! We cannot go back. Please enter a valid number (digits only, "
                      "1-7)")
            print("")
            num_players_input = input(num_players_input_text)
            num_players_validated_output = self.validate_input_int(num_players_input, self.PLAYER_MIN, self.PLAYER_MAX)
        self.num_players = int(num_players_input)

    # Method called that gets input from the user on the name of each player in the current game.
    # If use enters a invalid input, repeatedly prompts user until valid input is entered
    def get_player_names(self):
        self.used_player_names = list()
        print("")
        for i in range(1, self.num_players + 1):
            to_display_string = "Player " + str(i) + "'s " + "name (<30 characters long, cannot be \"go back\" and" \
                                                             " no duplicate names): "
            player_name = input(to_display_string)
            player_name_validated_output = self.validate_input_str(player_name)
            while player_name_validated_output == self.NOT_VALID_INPUT:
                print("")
                print("Sorry, that is not a valid player name. Please enter a valid name (<30 characters long, cannot "
                      "be \"Go back\" and no duplicate names)")
                player_name = input(to_display_string)
                player_name_validated_output = self.validate_input_str(player_name)
            if player_name_validated_output == self.GO_BACK_INPUT:
                self.array_pointer -= 2
                break
            else:
                self.used_player_names.append(player_name)

    # Method called that gets input from the user on the amount of money each player starts with in the current game.
    # If use enters a invalid input, repeatedly prompts user until valid input is entered
    def get_starting_money(self):
        print("")
        to_display_string = "Amount of money each player will start with (Between 1 and 100000000): "
        starting_amount = input(to_display_string)
        starting_amount_validated_output = self.validate_input_int(starting_amount, self.MONEY_MIN, self.MONEY_MAX)
        while starting_amount_validated_output == self.NOT_VALID_INPUT:
            print("")
            print("Sorry, that is not a valid amount of starting money. Please enter a valid amount (between 1 and "
                  "100000000)")
            starting_amount = input(to_display_string)
            starting_amount_validated_output = self.validate_input_int(starting_amount, self.MONEY_MIN, self.MONEY_MAX)
        if starting_amount_validated_output == self.GO_BACK_INPUT:
            self.array_pointer -= 2
        else:
            self.starting_money = int(starting_amount)

    # This method is called when all necessary information is entered, and prompts the users if they are ready to begin
    # playing. If not, brings users back to the prompt setting up the last parameter of the game
    def confirm(self):
        self.print_set_vals()
        print("")
        answer = input("Is this correct (y/n)? Pressing no will bring you back to setting the starting money each "
                       "player has: ")
        while answer != self.YES_STRING and answer != self.NO_STRING:
            print("Invalid answer! Please pick a valid answer!")
            answer = input("Is this correct (y/n)? Pressing no will bring you back to setting the starting money each "
                           "player has: ")
        if answer == self.YES_STRING:
            print("Okay, lets play! Enter q to quit at anytime!")
            for player in self.used_player_names:
                self.map_player_to_money[player] = self.starting_money
        else:
            self.array_pointer -= 2

    # Prints relevant information about the game is serves as the welcome message to the program. Also displays
    # information about the rules of the game
    def introduction(self):
        introduction_string = "Welcome to Blackjack! Before you get playing, we need some information. Enter \"Go " \
                              "back\" to reset the last value at any time. Press Ctrl+C at anytime to quit."
        print(introduction_string)
        rule_change_string = "The rules are exactly the same as regular blackjack, except for the fact that you can " \
                             "make any denomination bet, but your winnings will be rounded down to the nearest dollar!" \
                             "Additionally, cards are shuffled back into the deck after every turn, so good luck trying" \
                             "to count cards! :)"
        print(rule_change_string)
        self.array_pointer = 0
        getting_info_functions = [self.get_num_players, self.get_player_names, self.get_starting_money, self.confirm]
        while self.array_pointer != len(getting_info_functions):
            getting_info_functions[self.array_pointer]()
            self.array_pointer += 1

    # Repeatedly calls one_round until everyone has lost. one_round is the method that does the work of playing a single
    # round of blackjack.
    def play_game(self):
        while True:
            not_quit = False
            for player in self.used_player_names:
                if player not in self.players_with_no_money:
                    not_quit = True
            if not not_quit:
                break
            self.one_round()
        print("Everyone has lost! Resetting...")
        self.reset_vals()
        self.start_game()

    # Resets all of the user-entered values back to None so that user can re-enter these values at the start of the
    # next game
    def reset_vals(self):
        self.starting_money = None
        self.num_players = None
        self.array_pointer = None
        self.used_player_names = None
        self.map_player_to_money = None
        self.players_with_no_money = None

    # Validates that the bets that the user entered is a valid bet (not more than the user's money, and a number)
    # Returns whether or not the input is valid. Uses the lower_bound and upper_bound to determine the range of numbers
    # that is valid
    def validate_bet(self, num_players_input, lower_bound, upper_bound):
        if num_players_input.isdigit():
            integer_form = int(num_players_input)
            if lower_bound <= integer_form <= upper_bound:
                return self. VALID_INPUT
            else:
                return self.NOT_VALID_INPUT
        else:
            return self.NOT_VALID_INPUT

    # Prompts each player to enter in a valid bet for the round. Repeatedly prompts the user for this input until the
    # user has entered in a valid amount
    def get_bets(self, player_to_bets):
        print("Players money is the following:")
        for player in self.used_player_names:
            player_money = self.map_player_to_money[player]
            print(player + " has $" + str(player_money))
        for player in self.map_player_to_money:
            if player not in self.players_with_no_money:
                potential_bet = input(player + " please enter a bet: ")
                potential_bet_output = self.validate_bet(potential_bet, self.MIN_BET,
                                                               self.map_player_to_money[player])
                while potential_bet_output == self.NOT_VALID_INPUT:
                    print("That is not a valid bet! Please enter a number between 1 and your current balance")
                    potential_bet = input(player + " please enter a bet: ")
                    potential_bet_output = self.validate_bet(potential_bet, self.MIN_BET,
                                                             self.map_player_to_money[player])
                player_to_bets[player] = int(potential_bet)
                self.map_player_to_money[player] -= int(potential_bet)

    # Method to print to the screen the hands of each player and the current score of said hands.
    def print_all_hands(self, map_player_to_hands):
        print("Here are all of the hands so far...\n")
        for player in map_player_to_hands:
            to_print_array = list()
            for i in range(self.NUM_LINES_PER_CARD + 1):
                to_print_array.append("")
            print(player + "'s hands are:\n")
            for i in range(len(map_player_to_hands[player])):
                current_hand = map_player_to_hands[player][i]
                to_print_array[0] += "Hand " + str(i) + " with score of " + str(self.get_final_score(current_hand))
                for card in current_hand.get_cards():
                    string_representation_array = card.get_string_array()
                    for k in range(len(string_representation_array)):
                        to_print_array[k + 1] += string_representation_array[k]
                for k in range(len(to_print_array)):
                    to_print_array[k] += "         "
            for line in to_print_array:
                print(line)

    # Prints the hand of the dealer, and accepts a boolean parameter mystery that indicates whether or not to hide
    # all but one of the dealer's cards from the players
    def print_dealer_hand(self, dealer_hand, mystery):
        print_score = str(self.get_final_score(dealer_hand))
        if mystery:
            print_score = "???"
        print("\nDealer's hand with score of " + print_score)
        to_print_array = list()
        cards_in_hand = dealer_hand.get_cards()
        for i in range(self.NUM_LINES_PER_CARD):
            to_print_array.append("")
        for i in range(len(cards_in_hand)):
            card = cards_in_hand[i]
            if i == 0:
                string_representation_array = card.get_string_array()
            else:
                if mystery:
                    string_representation_array = card.get_string_array_empty()
                else:
                    string_representation_array = card.get_string_array()
            for k in range(len(string_representation_array)):
                to_print_array[k] += string_representation_array[k]
        for line in to_print_array:
            print(line)

    # If the dealer's face up card shows an ace, then this method is called in order to ask each player that can
    # afford insurance whether or not they want to make this side bet
    def ask_for_insurance(self, insurance_players, player_to_bets):
        for player in self.map_player_to_money:
            if player in self.players_with_no_money or self.map_player_to_money[player] < \
                    math.ceil(player_to_bets[player] * 0.5):
                continue
            potential_answer = input(player + ", do you want insurance (y/n, and insurance is half your bet)? ")
            while potential_answer != self.YES_STRING and potential_answer != self.NO_STRING:
                print("That is not a valid answer! Please enter y or n.")
                potential_answer = input(player + ", do you want insurance (y/n)? ")
            if potential_answer == self.YES_STRING:
                insurance_players[player] = math.ceil(player_to_bets[player] * 0.5)
                self.map_player_to_money[player] -= math.ceil(player_to_bets[player] * 0.5)

    # Clears the screen to remove clutter and prints all of the bets that the players have placed
    def print_bets(self, player_to_bets):
        os.system('cls' if os.name == 'nt' else 'clear')
        for player in self.used_player_names:
            if player not in self.players_with_no_money:
                print(player + " has bet " + str(player_to_bets[player]))
        print("\n")

    # For a particular hand, gives the players all possible options (from stand, hit, double down, and split) and plays
    # the hand until the player chooses to stop playing the hand or the player busts.
    def make_move(self, player, player_hand, curr_deck, player_to_hands, black_jacks, split_denom, hand_to_double_down,
                  busted_hands, player_to_bets, hands_already_done, can_blackjack):
        hand_is_over = False
        can_black_jack = can_blackjack

        while not hand_is_over: # while the hand is still playable (IE the hand has not bust)
            options = [self.INT_STAND, self.INT_HIT]
            options_str = [str(self.INT_STAND), str(self.INT_HIT)]
            can_split = False
            current_cards_in_hand = player_hand.get_cards()

            if len(current_cards_in_hand) == 2: # Determines whether the player can double down and/or split
                if self.map_player_to_money[player] >= player_to_bets[player]:
                    options.append(self.INT_DOUBLE)
                    options_str.append(str(self.INT_DOUBLE))

                if current_cards_in_hand[0].get_denomination() == current_cards_in_hand[1].get_denomination():
                    if split_denom is not None:
                        if split_denom == current_cards_in_hand[0].get_denomination() and \
                                self.map_player_to_money[player] >= player_to_bets[player]:
                            can_split = True
                    elif self.map_player_to_money[player] >= player_to_bets[player]:
                        can_split = True

            if can_split:
                options.append(self.INT_SPLIT)
                options_str.append(str(self.INT_SPLIT))

            # prints the current hand of the player and score as well asl the choices players can take.
            ask_for_move_string = player + ", you have several options for your hand of "
            for card in current_cards_in_hand:
                ask_for_move_string += card.get_non_graphic_string()
                if card != current_cards_in_hand[-1]:
                    ask_for_move_string += " and "
            ask_for_move_string += ". It's current value is " + str(self.get_final_score(player_hand)) + ". You can " \
                                                                                                         "either "
            for i in range(len(options)):
                number = options[i]
                ask_for_move_string += self.all_moves[number] + " (enter " + str(number) + ")"
                if i != len(options) - 1:
                    ask_for_move_string += ", "
            choice = input(ask_for_move_string + ": ")
            while choice not in options_str: # Repeatedly prompts user for choice until they enter a valid choice
                print("That is not a valid choice, please enter a valid choice!")
                choice = input(ask_for_move_string + ": ")
            choice = int(choice)
            if choice == self.INT_STAND: # if player stands
                hand_is_over = True
                if self.INT_BLACKJACK in player_hand.get_scores() and can_black_jack:
                    black_jacks.add(player_hand)
                hands_already_done.add(player_hand)
            elif choice == self.INT_HIT: # if player hits
                next_card = curr_deck.draw()
                player_hand.add_card(next_card)
                self.print_single_hand(player_hand)
                new_score = self.get_final_score(player_hand)
                if new_score == 0:
                    busted_hands.add(player_hand)
                    hand_is_over = True
                    hands_already_done.add(player_hand)
            elif choice == self.INT_SPLIT: # if player splits
                hand_1 = Hand()
                hand_2 = Hand()
                hand_1.add_card(current_cards_in_hand[0])
                hand_2.add_card(current_cards_in_hand[1])
                new_card_1 = curr_deck.draw()
                new_card_2 = curr_deck.draw()
                hand_1.add_card(new_card_1)
                hand_2.add_card(new_card_2)
                player_to_hands[player].remove(player_hand)
                player_to_hands[player].append(hand_1)
                player_to_hands[player].append(hand_2)
                self.print_all_hands(player_to_hands)
                self.map_player_to_money[player] -= player_to_bets[player]
                # Player's hand is split into two hands, then each hand is played out by a recursive call to make_move
                self.make_move(player, hand_1, curr_deck, player_to_hands, black_jacks, current_cards_in_hand[0].get_denomination(),
                               hand_to_double_down, busted_hands, player_to_bets, hands_already_done, False)
                self.make_move(player, hand_2, curr_deck, player_to_hands, black_jacks, current_cards_in_hand[0].get_denomination(),
                               hand_to_double_down, busted_hands, player_to_bets, hands_already_done, False)
                hand_is_over = True
            else: # choice is to double down
                next_card = curr_deck.draw()
                player_hand.add_card(next_card)
                hand_to_double_down.add(player_hand)
                new_score = self.get_final_score(player_hand)
                if new_score == 0:
                    busted_hands.add(player_hand)
                hand_is_over = True
                self.map_player_to_money[player] -= player_to_bets[player]
                hands_already_done.add(player_hand)
            can_black_jack = False

    # Given a hand, prints the highest possible score of the hand under 21
    def get_final_score(self, player_hand):
        all_possible_scores = [score for score in player_hand.get_scores() if score <= self.INT_BLACKJACK]
        if len(all_possible_scores) == 0:
            return 0
        else:
            return max(all_possible_scores)

    # prints the cards of a hand in graphic format for parameter hand
    def print_single_hand(self, hand):
        to_print_array = list()
        cards_in_hand = hand.get_cards()
        for i in range(len(cards_in_hand)):
            card = cards_in_hand[i]
            if i == 0:
                to_print_array = card.get_string_array()
            else:
                string_representation_array = card.get_string_array()
                for j in range(len(string_representation_array)):
                    to_print_array[j] += "  " + string_representation_array[j]
        for line in to_print_array:
            print(line)

    # Method to play a single round of blackjack
    def one_round(self):
        player_to_bets = {}
        player_to_hands = {}
        hands_already_done = set()
        hand_to_double_down = set()
        insurance_players = dict()
        busted_hands = set()
        self.get_bets(player_to_bets)
        self.print_bets(player_to_bets)
        current_deck = Deck(self.NUM_DECKS)
        for player in self.used_player_names:
            if player not in self.players_with_no_money: # draws the first card for players
                card_drew = current_deck.draw()
                new_hand = Hand()
                new_hand.add_card(card_drew)
                player_to_hands[player] = [new_hand]
        dealer_first_card = current_deck.draw() # draws the first card for the dealer
        dealer_hand = Hand()
        dealer_hand.add_card(dealer_first_card)
        for player in self.used_player_names:
            if player not in self.players_with_no_money: # draws the second card for players
                card_drew = current_deck.draw()
                player_to_hands[player][0].add_card(card_drew)

        dealer_second_card = current_deck.draw() # draws the second card for dealer
        dealer_hand.add_card(dealer_second_card)
        dealer_black_jack = self.get_final_score(dealer_hand) == self.INT_BLACKJACK

        black_jacks = set()
        os.system('cls' if os.name == 'nt' else 'clear')
        self.print_all_hands(player_to_hands)
        self.print_dealer_hand(dealer_hand, True)

        if dealer_first_card.get_denomination() == "A":
            self.ask_for_insurance(insurance_players, player_to_bets)

        for player in self.used_player_names:
            if player not in self.players_with_no_money:
                for hand in player_to_hands[player]:
                    if hand not in hands_already_done:
                        self.make_move(player, hand, current_deck, player_to_hands, black_jacks, None,
                                       hand_to_double_down, busted_hands, player_to_bets, hands_already_done, True)
        dealer_bust = self.dealer_move(dealer_hand, current_deck)
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Final hands (After Dealer has played, so if you busted or blackjacked they still played)")
        self.print_all_hands(player_to_hands)
        self.print_dealer_hand(dealer_hand, False)
        self.end_round(player_to_hands, player_to_bets, hand_to_double_down, insurance_players,
                       dealer_black_jack, black_jacks, dealer_bust, dealer_hand, busted_hands)

    # After all hands are finished playing, including the dealer, calculates the amount of money each player now has
    # according to rules of blackjack
    def end_round(self, player_to_hands, player_to_bets, hand_to_double_down, insurance_players,
                       dealer_black_jack, black_jacks, dealer_bust, dealer_hand, busted_hands):
        for player in self.used_player_names:
            if player in self.players_with_no_money:
                continue
            if dealer_black_jack and player in insurance_players:
                self.map_player_to_money[player] += insurance_players[player]
                self.map_player_to_money[player] += player_to_bets[player]
            for hand in player_to_hands[player]:
                player_win = False
                player_push = False
                if hand in busted_hands:
                    continue
                if dealer_bust:
                    player_win = True
                if not player_win:
                    if self.get_final_score(hand) > self.get_final_score(dealer_hand):
                        player_win = True
                    elif self.get_final_score(hand) == self.get_final_score(dealer_hand):
                        player_push = True
                if player_win:
                    winnings = player_to_bets[player]
                    if hand in black_jacks:
                        winnings += math.floor(player_to_bets[player] * 1.5)
                    else:
                        winnings += player_to_bets[player]
                    if hand in hand_to_double_down:
                        winnings += player_to_bets[player] * 2
                    self.map_player_to_money[player] += winnings
                elif player_push:
                    winnings = player_to_bets[player]
                    if hand in hand_to_double_down:
                        winnings += player_to_bets[player]
                    self.map_player_to_money[player] += winnings
        for player in self.used_player_names:
            if self.map_player_to_money[player] <= 0:
                self.players_with_no_money.add(player)

    # Simulates the dealer playing his hand (IE standing on a soft 17 and repeatingly
    # hitting on anything lower than soft 17)
    def dealer_move(self, dealer_hand, current_deck):
        while True:
            dealer_scores = dealer_hand.get_scores()
            dealer_values_17_thru_21 = [score for score in dealer_scores if
                                        self.INT_BLACKJACK >= score >= self.DEALER_STAND_SCORE]
            dealer_values_more_than_21 = [score for score in dealer_scores if score > self.INT_BLACKJACK]
            dealer_values_under_17 = [score for score in dealer_scores if score < self.DEALER_STAND_SCORE]
            if len(dealer_values_17_thru_21) != 0:
                break
            elif len(dealer_values_under_17) == 0 and len(dealer_values_more_than_21) != 0:
                break
            next_card = current_deck.draw()
            dealer_hand.add_card(next_card)
        dealer_values_21_and_under = [score for score in dealer_hand.get_scores() if score <= self.INT_BLACKJACK]
        if len(dealer_values_21_and_under) == 0:
            return True
        else:
            return False

    # Method to call from outside script to start a game of blackjack
    def start_game(self):
        self.players_with_no_money = set()
        self.map_player_to_money = dict()
        self.introduction()
        os.system('cls' if os.name == 'nt' else 'clear')
        self.play_game()