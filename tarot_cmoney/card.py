import random
from dataclasses import dataclass
from typing import Self

from .config import Config
from .exceptions import UnexpectedDirectionError


@dataclass
class CardRaw:
    suit: str
    name: str
    upright_meanings_1: list[str]
    upright_meanings_2: list[str]
    upright_love_meaning: list[str]
    upright_career_meaning: list[str]
    upright_finances_meaning: list[str]
    reverse_meanings_1: list[str]
    reverse_meanings_2: list[str]
    reverse_love_meaning: list[str]
    reverse_career_meaning: list[str]
    reverse_finances_meaning: list[str]


class Card:
    def __init__(self, raw_card: CardRaw, forced_direction: str = 'none'):
        self.config = Config()
        self.raw_card = raw_card
        self.__forcedDirection = forced_direction

        self.is_reversed: bool = self.__set_reversed_status()

    @property
    def name(self) -> str: return self.raw_card.name

    @property
    def suit(self) -> str: return self.raw_card.suit

    @property
    def meanings_summary1(self) -> list[str]:
        if self.is_reversed:
            return self.raw_card.reverse_meanings_1
        return self.raw_card.upright_meanings_1

    @property
    def meanings_summary2(self) -> list[str]:
        if self.is_reversed:
            return self.raw_card.reverse_meanings_2
        return self.raw_card.upright_meanings_2

    @property
    def meanings_love(self) -> list[str]:
        if self.is_reversed:
            return self.raw_card.reverse_love_meaning
        return self.raw_card.upright_love_meaning

    @property
    def meanings_career(self) -> list[str]:
        if self.is_reversed:
            return self.raw_card.reverse_career_meaning
        return self.raw_card.upright_career_meaning

    @property
    def meanings_finances(self) -> list[str]:
        if self.is_reversed:
            return self.raw_card.reverse_finances_meaning
        return self.raw_card.upright_finances_meaning

    def __set_reversed_status(self) -> bool:
        if self.__forcedDirection == 'none':
            if random.random() < self.config.reverse_probability:
                return True
            return False
        else:
            if self.__forcedDirection.lower() == 'upright':
                return False
            elif self.__forcedDirection.lower() == 'reversed':
                return True
            else:
                raise UnexpectedDirectionError(self.__forcedDirection)

    def get_card_in_other_direction(self) -> Self:
        direction = 'upright' if self.is_reversed else 'reversed'
        return Card(raw_card=self.raw_card, forced_direction=direction)

    def __str__(self):
        return self.name