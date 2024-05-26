from enum import Enum


class Difficulty(Enum):
    SILLY = 'silly'
    EASY = 'easy'
    MEDIUM = 'medium'
    HARD = 'hard'

class Display(Enum):
    LETTERS = 'letters'
    DIGITS = 'digits'
    CUSTOM = 'custom'
