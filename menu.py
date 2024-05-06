import subprocess
from enum import Enum

from game import Game
from settings import Difficulty, Display

# tutaj cale menu i wywolanie gry
class Menu:
    def __init__(self):
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

    def display_instructions(self):
        print("Tutaj będą wyświetlane instrukcje gry...") # TODO instrukcja

    def change_settings(self):
        print("-----------------------------------------")
        print("1. Zmień poziom trudności")
        print("2. Zmień ustawienia wyświetlania")
        print("3. Zmień do ilu wygranych gier")
        choice = input("Wybierz opcję: ")
        if choice == '1':
            print("Obecny poziom trudności: ", self.settings['difficulty'])  # TODO repr jakis z tego enuma
            try:
                difficulty_set = Difficulty(input("Podaj nowy poziom trudności [easy/medium/hard]: "))
                self.settings['difficulty'] = difficulty_set
                print("Zmieniono poziom trudności na ", difficulty_set)
            except:
                print("❌ Nieprawidłowy poziom. Spróbuj ponownie.")
        elif choice == '2':
            print("Obecne ustawienie wyświetlania: ", self.settings['display'])
            try:
                display_set = Display(input("Podaj nowe ustawienia wyświetlania [numbers/letters/emoji/mixed]: "))
                self.settings['display'] = display_set
                print("Zmieniono wyświetlanie na ", display_set)
            except:
                print("❌ Nieprawidłowe ustawienia. Spróbuj ponownie.")
        elif choice == '3':
            print("Obecna liczba gier potrzebna do wygrania: ", self.settings['games_to_win'])
            try:
                towin_set = int(input("Podaj nową liczbę gier do wygrania: "))
                self.settings['games_to_win'] = towin_set
                print("Zmieniono liczbę gier do wygrania na ", towin_set)
            except:
                print("❌ Nieprawidłowe ustawienia. Spróbuj ponownie.")
        else:
            print("❌ Nieznana opcja, spróbuj ponownie.")

    def display_settings(self):
        print(f"Poziom trudności: {self.settings['difficulty'].value}")
        print(f"Ustawienia wyświetlania: {self.settings['display'].value}")
        print(f"Do ilu wygranych gier: {self.settings['games_to_win']}")

    def play_game(self):
        print("-----------------------------------------")
        print("Rozpoczynamy grę!")
        try:
            alphabet_len = int(input("Podaj długość używanego alfabetu: "))
            end_len = int(input("Podaj długość słowa, po której przekroczeniu wygra komputer: "))
        except:
            print("Wpisz prawidłową wartość")
        current_game = Game(self.settings, alphabet_len, end_len)
        current_game.play() # tu zaczynamy grac - cala gra w game.py


    def start(self):
        subprocess.call(["python", "silly-title.py"])
        while True:
            self.display_menu()
            choice = input("Wybierz opcję: ")
            if choice == '1':
                self.display_instructions()
            elif choice == '2':
                self.change_settings()
            elif choice == '3':
                self.play_game()
            else:
                print("❌ Nieznana opcja, spróbuj ponownie.")

if __name__ == "__main__":
    menu = Menu()
    menu.start()
