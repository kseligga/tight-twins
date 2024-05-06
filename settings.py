from enum import Enum


class Difficulty(Enum):
    EASY = 'easy'
    MEDIUM = 'medium'
    HARD = 'hard'

class Display(Enum):
    LETTERS = 'letters'
    NUMBERS = 'numbers'
    EMOJI = 'emoji'
    MIXED = 'mixed'
