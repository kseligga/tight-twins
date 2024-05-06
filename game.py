import random

from settings import Difficulty, Display

def alphabet(display, len): # funkcja do tworzenia alfabetu (listy) na podstawie ustawien
    if display == Display.NUMBERS:
        return list(range(1,len+1))
    if display == Display.LETTERS:
        return list(map(chr, range(97, 97+len)))
    if display == Display.EMOJI:
        return # nie uzywac, cos tu grzebalem ale nie moge zrobic na szybko tego co chce zrobic
    if display == Display.MIXED:
        return # to samo

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
        print("-----------------------------------------")
        w = self.current_word
        self.current_word_length = len(str(w))

        display_word = ' _' + '_'.join(list(str(w))) + '_ '
        print(display_word)

        display_gaps = ' ' + ' '.join(str(i) for i in range(1, len(str(w)) + 2))
        print(display_gaps)

        print("")
        print("Obecna długość słowa: ", self.current_word_length)
        if self.moves_to_end>=0:
            print("Komputer zwycięży za ", self.moves_to_end," kolejek bez ciasnych bliźniaków")


    def player_move(self):
        self.curr_chosen_place = int(input("Wybierz miejsce, gdzie komputer ma wstawić literę: "))
        while self.curr_chosen_place not in range(1, self.current_word_length + 2):
            print("Wybierz prawidłową wartość.")
            self.curr_chosen_place = int(input("Wybierz miejsce, gdzie komputer ma wstawić literę: "))


    def computer_move(self):
        # inteligentny_algorytm(self.current_word, self.curr_chosen_place) #TODO algorytmy dla komputera
        self.glupi_algorytm()

    def glupi_algorytm(self): # wstawia losowa litere
        idx = self.curr_chosen_place
        s = str(self.current_word)
        new_letter = str(random.choice(self.alphabet))
        self.current_word = s[:idx-1] + new_letter + s[idx-1:]


    def check_game_state(self):
        if self.current_word == "xxx": # TODO tu warunek na wystąpienie ciasnych bliźniaków w słowie
            self.game_state = 1 # wystapil blizniak - wygrywa gracz

        if self.moves_to_end <= 0:
            self.game_state = -1 # skonczyl sie czas - wygral komputerek

    def play(self):
        self.current_word = random.choice(self.alphabet) # pierwsza litera losowa

        while self.game_state==0: # rozgrywka w pętli póki nie ma wygranego
            self.check_game_state() # patrzymy czy to nie koniec
            self.moves_to_end -= 1

            self.display_current_state()


            if self.game_state==1:
                print("Brawo graczu! Wygrales! （〜^∇^ )〜")
                break
            if self.game_state==-1:
                print("Przegrales graczu (╯°□°)╯︵ ┻━┻ ale za to komputer wygral")
                break


            self.player_move()
            self.computer_move()

        return(self.game_state)



