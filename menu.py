import subprocess
import os
from enum import Enum
from time import sleep

import title
from game import Game
from settings import Difficulty, Display

# tutaj cale menu i wywolanie gry
class Menu:
    def __init__(self):
        self.score = [0, 0]
        self.settings = {
            'difficulty': Difficulty.EASY,
            'display': Display.LETTERS,
            'games_to_win': 1
        }

    def display_menu(self):
        print("-----------------------------------------")
        print("1. Instrukcja gry")
        print("2. Ustawienia gry")
        print("3. Graj")
        print("4. Wyjdź")
        print("-----------------------------------------")

    def display_instructions(self):
        print("-----------------------------------------")
        print("Tutaj będą wyświetlane instrukcje gry...") # TODO instrukcja
        input("Wpisz dowolną wartość aby kontynuować...")

    def change_settings(self):
        print("-----------------------------------------")
        print("1. Zmień poziom trudności")
        print("2. Zmień ustawienia wyświetlania")
        print("3. Zmień do ilu wygranych gier")
        print("4. Powrót")
        print("-----------------------------------------")
        choice = input("Wybierz opcję: ")
        print("-----------------------------------------")
        if choice == '1':
            while True:
                print("Obecny poziom trudności: ", self.settings['difficulty'].value)
                try:
                    difficulty_set = Difficulty(input("Podaj nowy poziom trudności [easy/medium/hard]: "))
                    self.settings['difficulty'] = difficulty_set
                    print("Zmieniono poziom trudności na: ", difficulty_set.value)
                    break
                except:
                    print("X Nieprawidłowy poziom. Spróbuj ponownie.")
                    continue
        elif choice == '2':
            print("Obecne ustawienie wyświetlania: ", self.settings['display'].value)
            while True:
                try:
                    display_set = Display(input("Podaj nowe ustawienia wyświetlania [numbers/letters/emoji/mixed]: "))
                    self.settings['display'] = display_set
                    print("Zmieniono wyświetlanie na: ", display_set.value)
                    break
                except:
                    print("X Nieprawidłowe ustawienia. Spróbuj ponownie.")
                    continue
        elif choice == '3':
            print("Obecna liczba rund potrzebna do wygrania: ", self.settings['games_to_win'])
            while True:
                tw = input("Podaj nową liczbę gier do wygrania: ")
                try:
                    towin_set = int(tw)
                    if towin_set >= 1:
                        self.settings['games_to_win'] = towin_set
                        print("Zmieniono liczbę rund do wygrania na: ", towin_set)
                        break
                    else:
                        print("Wpisz liczbę większą lub równą od 1.")
                        continue
                except:
                    print("X Nieprawidłowe ustawienia. Spróbuj ponownie.")
                    continue
        elif choice == '4':
            pass
        else:
            print("X Nieznana opcja, spróbuj ponownie.")
        if choice!='4':
            input("Wpisz dowolną wartość aby kontynuować...")

    def display_settings(self):
        print(f"Poziom trudności: {self.settings['difficulty'].value}")
        print(f"Ustawienia wyświetlania: {self.settings['display'].value}")
        print(f"Do ilu wygranych gier: {self.settings['games_to_win']}")

    def play_game(self):
        print("-----------------------------------------")
        print("Rozpoczynamy grę!")
        self.score = [0, 0]
        while True:
            a = input("Podaj długość używanego alfabetu: ")
            try:
                a = int(a)
                if a <= 1:
                    print("Wpisz wartość większą od 1.")
                    continue
                else:
                    alphabet_len = a
                    if alphabet_len > 26 and self.settings['display']== Display.LETTERS:
                        print("Duża długość alfabetu - automatycznie zmieniono ustawienia wyświetlania")
                        self.settings['display'] = Display.NUMBERS
                    break
            except:
                print("Wpisz prawidłową wartość")
                continue

        while True:
            e = input("Podaj długość słowa, po której przekroczeniu wygra komputer: ")
            try:
                e = int(e)
                if e <= 0:
                    print("Wpisz dodatnią wartość")
                    continue
                else:
                    end_len = e
                    break
            except:
                print("Wpisz prawidłową wartość")
                continue

        # gramy
        while all(x < self.settings['games_to_win'] for x in self.score):
            current_game = Game(self.settings, alphabet_len, end_len)
            res = current_game.play() # tu zaczynamy grac - cala gra w game.py
            if res == 1:
                self.score[0] += 1
            elif res == -1:
                self.score[1] += 1
            if self.settings['games_to_win'] > 1:  # dla jednorundowej gry bez obsługi rund
                print("Obecny wynik: Gracz ", str(self.score[0]), "-", str(self.score[1]), " Komputer")
                input("Wpisz dowolną wartość aby kontynuować...")

        print("Gra skończona!")
        again = input("Jeśli chcesz zagrać znowu z tymi samymi ustawieniami, wpisz 1. Aby wrócić do menu, "
                      "wpisz dowolną inną wartość:")
        if again == '1':
            self.play_game()

    def start(self):
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')  # obsługa win i linuxa
            title.display()

            self.display_menu()
            choice = input("Wybierz opcję: ")
            if choice == '1':
                self.display_instructions()
            elif choice == '2':
                self.change_settings()
            elif choice == '3':
                self.play_game()
            elif choice == '4':
                exit()
            else:
                print("X Nieznana opcja, spróbuj ponownie.")
                input("Wpisz dowolną wartość aby kontynuować...")

if __name__ == "__main__":
    menu = Menu()
    menu.start()
