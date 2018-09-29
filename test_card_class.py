# This short script simply tests the card class and the methods inside the class to ensure they are working

from Card import Card

newCard = Card("spade", "A")
string_representation_array = newCard.get_string_array()
for element in string_representation_array:
    print(element)
print(newCard.get_denomination())
print(newCard.get_suit())
print(newCard.get_values())

string_representation_array_empty = newCard.get_string_array_empty()
for element in string_representation_array_empty:
    print(element)
