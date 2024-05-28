import os
import random
import subprocess
import copy
from time import sleep

import numpy as np

import title
from settings import Difficulty, Display


def alphabet(display, leng):  # funkcja do tworzenia alfabetu (listy) na podstawie ustawien
    if display == Display.DIGITS:  # do 10 cyfr
        return [str(i) for i in range(1, leng + 1)]

    if display == Display.LETTERS:
        if leng <= 26:
            return list(map(chr, range(97, 97 + leng)))
        elif leng <= 52:  # przy dużym alfabecie odróżniamy wielkie litery
            lowers = list(map(chr, range(97, 123)))
            uppers = list(map(chr, range(65, 65 + leng - 26)))
            return lowers + uppers
        else:  # przy bardzo dużym alfabecie włączamy też symbole
            return list(map(chr, range(33, 33 + leng)))

    if display == Display.CUSTOM:
        alphabet = str(input("Podaj własny alfabet (bez spacji i przecinków, np. 'abcdef'): "))
        while len(set(alphabet))<=1:
            alphabet = str(input("Podaj własny alfabet o długości powyżej 1: "))
        a = list(set([x for x in alphabet]))
        return a



# przebieg pojedynczej gry
class Game():
    def __init__(self, settings, alphabet_len, end_len):
        self.difficulty = settings['difficulty']
        self.end_len = end_len
        self.alphabet = alphabet(settings['display'], alphabet_len)
        self.skipsingles = settings['skipsingles']

        self.current_word = ""
        self.current_word_length = 0
        self.moves_to_end = self.end_len - self.current_word_length

        self.game_state = 0
        self.twin = []

        self.curr_chosen_place = None

    def display_current_state(self):
        # trzeba startować z terminala, żeby ładnie czyściło
        os.system('cls' if os.name == 'nt' else 'clear')  # obsługa win i linuxa
        title.display()
        print("-----------------------------------------")
        w = self.current_word
        self.current_word_length = len(str(w))

        display_word = ' _' + '_'.join(list(str(w))) + '_ '
        print(display_word)

        display_gaps = ' '+' '.join(str(i) if i < 10 else str(i // 10) for i in range(1, len(str(w)) + 2))
        print(display_gaps)
        if len(w)>=9:
            second_digit = ' '+' '.join(' ' if i < 10 else str(i % 10) for i in range(1, len(str(w)) + 2))
            print(second_digit)

        print("")
        print("Obecna długość słowa: ", self.current_word_length)
        if self.moves_to_end >= 0:
            print("Komputer zwycięży za ", self.moves_to_end, " kolejek bez ciasnych bliźniaków")

    def player_move(self):
        while True:
            try:
                self.curr_chosen_place = int(input("Wybierz miejsce, gdzie komputer ma wstawić literę: "))
                break
            except:
                print("Wpisz wartość liczbową")
        while self.curr_chosen_place not in range(1, self.current_word_length + 2):
            print("Wpisz liczbę z przedziału ( 1, ", str(self.current_word_length+1), ")")
            try:
                self.curr_chosen_place = int(input("Wybierz miejsce, gdzie komputer ma wstawić literę: "))
            except:
                print("Wpisz wartość liczbową")

    def computer_move(self):
        if self.difficulty == Difficulty.EASY:
            self.dumb_algorithm()
        elif self.difficulty == Difficulty.MEDIUM:
            self.algorithm_1()
        elif self.difficulty == Difficulty.HARD:
            self.algorithm_2()
        elif self.difficulty == Difficulty.HARDER:
            self.algorithm_3()

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
        while i < len(letters) and self.is_twin(idx, str(letters[i]))[0]:
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
                    flag = Game.chars_even(word[i:j])[0]
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
            if self.is_twin(idx, str(letters[pos]))[0]:
                dists.pop(pos)
                if len(dists) == 0:
                    self.current_word = s[:idx] + str(letters[0]) + s[idx:]
                    return
                continue
            else:
                self.current_word = s[:idx] + str(letters[pos]) + s[idx:]
                return



    def is_twin(self, add_pos=-1, add_letter=""):
        word = str(self.current_word)
        if type(add_pos) == int and add_pos >= 0:
            word = str(word[:add_pos]) + add_letter + str(word[add_pos:])
        if type(add_pos) == tuple:
            for i in range(len(add_pos)):
                word = str(word[:add_pos[i]]) + add_letter[i] + str(word[add_pos[i]:])
        return self.twin_exist(word, self.skipsingles)

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
        return not flag, counters

    @staticmethod
    def twin_exist(word, skipsingles):
        for i in range(len(word)):
            for j in range(i + 1, len(word) + 1):
                subword = word[i:j]
                if skipsingles and len(subword)<=2:
                    continue
                flag, counters = Game.chars_even(subword)
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
                    for v in range(len(s1) + len(s2), len(subword)):
                        letter = subword[v]
                        k = len(s2)
                        if skipsingles and len(s1)==1 and s1==s2:
                            continue
                        neededLetter = s1[k]
                        if letter == neededLetter:  # Mozna dodać literę do 2 słowa
                            s2 += letter
                            if s1.count(letter) < counters[letter] / 2:
                                choiceList[v] = 2
                            else:
                                choiceList[v] = -2
                        elif s1.count(letter) < counters[letter] / 2:  # Mozna dodać literę do 1 słowa
                            s1 += letter
                        elif 2 in choiceList:  # Nie mozna dodać litery do zadnego ze słów - przygotowanie do kolejnej iteracji
                            last2Index = max(x for x in range(len(choiceList)) if choiceList[x] == 2)
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
                        pos = [0 for _ in range(len(word))]
                        for e in range(i, j):
                            pos[e] = Game.decode(choiceList[e - i])
                        return True, pos
        return False, None

    @staticmethod
    def decode(x):
        match x:
            case 0 | 1:
                return 1
            case 2 | -2:
                return 2
            case _:
                return 0

    def check_game_state(self):
        is_twin, self.twin = self.is_twin()
        if is_twin == True:
            self.game_state = 1  # wystapil blizniak - wygrywa gracz

        if self.moves_to_end <= 0:
            self.game_state = -1  # skonczyl sie czas - wygral komputerek

    def printTwins(self):
        pos = self.twin
        word = str(self.current_word)
        s = ''
        for i in range(len(pos)):
            match pos[i]:
                case 0:
                    s+='_'
                case 1:
                    s+=word[i]
                case 2:
                    s+=word[i].upper()
        print("Końcowe słowo: " + word)
        print("    Bliźniaki: " + s)




    def play(self):
        self.current_word = random.choice(self.alphabet)  # pierwsza litera losowa

        while self.game_state == 0:  # rozgrywka w pętli póki nie ma wygranego
            self.check_game_state()  # patrzymy czy to nie koniec
            self.moves_to_end -= 1

            self.display_current_state()

            if self.game_state == 1:
                print("-----------------------------------------")
                print("Brawo graczu! Wygrałeś! (~^v^ )~")
                print("-----------------------------------------")
                self.printTwins()
                break
            if self.game_state == -1:
                print("-----------------------------------------")
                print("Przegrałeś graczu (╯°□°)╯ ┻━┻ Komputer był lepszy...")
                break

            self.player_move()
            self.computer_move()
            #sleep(3)

        return (self.game_state)
