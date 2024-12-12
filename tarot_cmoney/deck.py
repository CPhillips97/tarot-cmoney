import json
import os
import random
from argparse import ArgumentError

from card import Card, CardRaw
from exceptions import NoCardsRemainingError


class Deck:
    __card_directory = 'cards'

    def __init__(self):
        self.__cards: list[CardRaw] = list()
        self.reset()

    @property
    def count(self) -> int:
        return len(self.__cards)

    def draw_card(self, force_upright: bool = False, force_reverse: bool = False) -> Card:
        if self.count == 0:
            raise NoCardsRemainingError()

        if force_upright and force_reverse:
            raise ArgumentError(message='A card cannot be forced to be drawn in both upright and reverse positions.')

        raw_card = self.__cards.pop(random.randrange(self.count))

        if force_upright:
            return Card(raw_card, 'upright')

        if force_reverse:
            return Card(raw_card, 'reversed')

        return Card(raw_card)

    def reset(self) -> None:
        self.__cards = list()
        self.__load_deck()

    def __load_deck(self) -> None:
        for file in os.listdir(self.__card_directory):
            if file.endswith('.json'):
                with open(os.path.join(self.__card_directory, file), 'r') as f:
                    self.__cards.append(CardRaw(**json.load(f)))
