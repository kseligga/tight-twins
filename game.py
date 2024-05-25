import os
import random
import subprocess
import copy

import numpy as np

from settings import Difficulty, Display


def alphabet(display, len):  # funkcja do tworzenia alfabetu (listy) na podstawie ustawien
    if display == Display.NUMBERS:
        return list(range(1, len + 1))
    if display == Display.LETTERS:
        return list(map(chr, range(97, 97 + len)))
    if display == Display.EMOJI:
        return  # nie uzywac, cos tu grzebalem ale nie moge zrobic na szybko tego co chce zrobic
    if display == Display.MIXED:
        return  # to samo


# przebieg pojedynczej gry
class Game():
    def __init__(self, settings, alphabet_len, end_len):
        self.difficulty = settings['difficulty']
        self.end_len = end_len
        self.alphabet = alphabet(settings['display'], alphabet_len)

        self.current_word = ""
        self.current_word_length = 0
        self.moves_to_end = self.end_len - self.current_word_length

        self.game_state = 0

        self.curr_chosen_place = None

    def display_current_state(self):
        os.system('cls')  # trzeba startować z terminala, żeby ładnie czyściło (dla linux trzeba 'clear')
        subprocess.call(["python", "silly-title.py"])
        print("-----------------------------------------")
        w = self.current_word
        self.current_word_length = len(str(w))

        display_word = ' _' + '_'.join(list(str(w))) + '_ '
        print(display_word)

        display_gaps = ' ' + ' '.join(str(i) for i in range(1, len(str(w)) + 2))
        print(display_gaps)

        print("")
        print("Obecna długość słowa: ", self.current_word_length)
        if self.moves_to_end >= 0:
            print("Komputer zwycięży za ", self.moves_to_end, " kolejek bez ciasnych bliźniaków")

    def player_move(self):
        self.curr_chosen_place = int(input("Wybierz miejsce, gdzie komputer ma wstawić literę: "))
        while self.curr_chosen_place not in range(1, self.current_word_length + 2):
            print("Wybierz prawidłową wartość.")
            self.curr_chosen_place = int(input("Wybierz miejsce, gdzie komputer ma wstawić literę: "))

    def computer_move(self):
        # inteligentny_algorytm(self.current_word, self.curr_chosen_place) #TODO algorytmy dla komputera
        self.dumb_algorithm()

    def dumb_algorithm(self):  # wstawia losowa litere
        idx = self.curr_chosen_place - 1
        s = str(self.current_word)
        new_letter = str(random.choice(self.alphabet))
        self.current_word = s[:idx] + new_letter + s[idx:]

    def algorithm_1(self):
        # Próbuje wstawić losowo literę, jeśli tworzy to bliźniaka to losuje ponownie
        idx = self.curr_chosen_place - 1
        s = str(self.current_word)
        letters = copy.deepcopy(self.alphabet)
        random.shuffle(letters)
        i = 0
        while i < len(letters) and self.is_twin(idx, str(letters[i])):
            i += 1
        if i == len(letters):
            i = 0
        self.current_word = s[:idx] + str(letters[i]) + s[idx:]

    def algorithm_2(self):
        '''
        Próbuje tak wstawić literę aby nie utworzyć żadnego podciągu w którym każda litera występuje parzystą ilość razy
        jeśli się nie da działa zgodnie ze strategią z 'easy_algorithm'
        '''
        idx = self.curr_chosen_place - 1
        s = str(self.current_word)
        letters = copy.deepcopy(self.alphabet)
        random.shuffle(letters)
        for letter in letters:
            flag = False
            word = s[:idx] + str(letter) + s[idx:]
            for i in range(len(word)):
                for j in range(i + 1, len(word) + 1):
                    flag = Game.chars_even(word[i:j])
                    if flag:
                        break
                if flag:
                    break
            if not flag:
                self.current_word = s[:idx] + str(letter) + s[idx:]
                return
        self.algorithm_1()


    def algorithm_3(self):
        '''
        Wybiera taką literę aby była jak najbardziej oddalona od innych jej miejsc w słowie i jednocześnie sprawdza czy nie tworzy się bliźniak
        '''
        idx = self.curr_chosen_place - 1
        s = str(self.current_word)
        letters = copy.deepcopy(self.alphabet)
        dists = [0 for i in range(len(letters))]
        for i in range(len(letters)):
            l = str(letters[i])
            if l not in s:
                dists[i] = -1
                continue
            positions = [i for i, letter in enumerate(s) if letter == l]
            dists[i] = min(abs(idx - 0.5 - p) + 0.5 for p in positions)
        while True:
            try:
                pos = dists.index(-1)
            except:
                pos = np.argmax(dists)
            if self.is_twin(idx, str(letters[pos])):
                dists.pop(pos)
                if len(dists) == 0:
                    self.current_word = s[:idx] + str(letters[0]) + s[idx:]
                    return 
                continue
            else:
                self.current_word = s[:idx] + str(letters[pos]) + s[idx:]
                return






    def is_twin(self, add_pos=-1, add_letter=""):
        word = self.current_word
        if type(add_pos) == int and add_pos >= 0:
            word = word[:add_pos] + add_letter + word[add_pos:]
        if type(add_pos) == tuple:
            for i in range(len(add_pos)):
                word = word[:add_pos[i]] + add_letter[i] + word[add_pos[i]:]
        return self.twin_exist(word)

    @staticmethod
    def chars_even(subword):
        '''
        :return: True jeśli wszystkie znaki występują przystą ilość razy
        '''
        counters = {}
        for el in subword:
            if el in counters:
                counters[el] += 1
            else:
                counters[el] = 1
        flag = False
        for count in counters.values():
            if count % 2 == 1:
                flag = True
                break
        return not flag

    @staticmethod
    def twin_exist(word):
        for i in range(len(word)):
            for j in range(i + 1, len(word) + 1):
                flag = Game.chars_even(word[i:j])
                if not flag:
                    continue
                # Autorski algorytm sprawdzania czy w słowie istnieją bliźniaki (jeśli kazdy znak występuje parzystą ilość razy)                
                choiceList = [0 for _ in range(len(subword))]
                '''
                0 - domyślnie i wstawione do 1 słowa bez mozliwości wyboru 
                1 - wstawione do 1 słowa gdy był wybór 
                2 - wstawione do 2 słowa gdy był wybór
                -2 - wstawione do 2 słowa gdy nie było innej opcji
                '''
                flag2 = True
                s1 = subword[0]
                s2 = ""
                while flag2:
                    for i in range(len(s1) + len(s2), len(subword)):
                        letter = subword[i]
                        k = len(s2)
                        neededLetter = s1[k]
                        if letter == neededLetter:  # Mozna dodać literę do 2 słowa
                            s2 += letter
                            if s1.count(letter) < counters[letter] / 2:
                                choiceList[i] = 2
                            else:
                                choiceList[i] = -2
                        elif s1.count(letter) < counters[letter] / 2:  # Mozna dodać literę do 1 słowa
                            s1 += letter
                        elif 2 in choiceList:  # Nie mozna dodać litery do zadnego ze słów - przygotowanie do kolejnej iteracji
                            last2Index = max(i for i in reversed(range(len(choiceList))) if choiceList[i] == 2)
                            newLengthS2 = len(s2) - choiceList[last2Index:].count(-2) - 1
                            newLengthS1 = last2Index - newLengthS2  # chyba git ale moze byc zle
                            s1 = s1[:newLengthS1] + subword[last2Index]
                            s2 = s2[:newLengthS2]
                            choiceList[last2Index] = 1
                            for j in range(last2Index + 1, len(choiceList)):
                                choiceList[j] = 0
                            break
                        else:
                            flag2 = False  # Nie mozna dodać litery do zadnego ze słów oraz nie ma juz gdzie się cofnąć
                            break
                    if s1 == s2:
                        '''
                        pos:
                        0 jeśli nie jest elementem należącym do bliźniaków
                        1 jeśli należy do pierwszego bliźniaka
                        2 jeśli należy do drugiego bliźniaka
                        '''
                        pos = [0 for i in range(len(word))]
                        for e in range(i, j):
                            pos[e] = self.decode(choiceList[e - i])
                        return True, pos
        return False, None

    @staticmethod
    def decode(x):
        match x:
            case 0 | 1:
                return 1
            case 2 | -1:
                return 2
            case _:
                return 0

    def check_game_state(self):
        if self.is_twin() == True:  # TODO tu warunek na wystąpienie ciasnych bliźniaków w słowie
            self.game_state = 1  # wystapil blizniak - wygrywa gracz

        if self.moves_to_end <= 0:
            self.game_state = -1  # skonczyl sie czas - wygral komputerek

    def play(self):
        self.current_word = random.choice(self.alphabet)  # pierwsza litera losowa

        while self.game_state == 0:  # rozgrywka w pętli póki nie ma wygranego
            self.check_game_state()  # patrzymy czy to nie koniec
            self.moves_to_end -= 1

            self.display_current_state()

            if self.game_state == 1:
                print("Brawo graczu! Wygrales! （〜^∇^ )〜")
                input("Wciśnij dowolny przycisk, aby kontynuować...")
                break
            if self.game_state == -1:
                print("Przegrales graczu (╯°□°)╯︵ ┻━┻ ale za to komputer wygral")
                input("Wciśnij dowolny przycisk, aby kontynuować...")
                break

            self.player_move()
            self.computer_move()

        return (self.game_state)
