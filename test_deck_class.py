from Deck import Deck
from Card import Card

newDeck = Deck(1)
cards_in_deck = newDeck.get_deck()
print(len(cards_in_deck))

new_deck_map = {}
new_deck_map_2 = {}

for card in cards_in_deck:
    hash_key = card.get_suit()
    if hash_key not in new_deck_map:
        new_deck_map[hash_key] = 1
    else:
        new_deck_map[hash_key] += 1
    hash_key = card.get_denomination()
    if hash_key not in new_deck_map_2:
        new_deck_map_2[hash_key] = 1
    else:
        new_deck_map_2[hash_key] += 1

for key in new_deck_map:
    print(key + "\t" + str(new_deck_map[key]))

for key in new_deck_map_2:
    print(key + "\t" + str(new_deck_map_2[key]))

drew = newDeck.draw()
print(str(drew.get_suit()) + "\t" + str(drew.get_denomination()))
after_draw = newDeck.get_deck()
print(len(after_draw))

removed_map = {}
removed_map_2 = {}

for card in after_draw:
    hash_key = card.get_suit()
    if hash_key not in removed_map:
        removed_map[hash_key] = 1
    else:
        removed_map[hash_key] += 1
    hash_key = card.get_denomination()
    if hash_key not in removed_map_2:
        removed_map_2[hash_key] = 1
    else:
        removed_map_2[hash_key] += 1

for key in removed_map:
    print(key + "\t" + str(removed_map[key]))

for key in removed_map_2:
    print(key + "\t" + str(removed_map_2[key]))