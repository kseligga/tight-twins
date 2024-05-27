from enum import Enum


class Difficulty(Enum):
    EASY = 'easy'
    MEDIUM = 'medium'
    HARD = 'hard'
    HARDER = 'harder'

class Display(Enum):
    LETTERS = 'letters'
    DIGITS = 'digits'
    CUSTOM = 'custom'
