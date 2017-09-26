import kivy
kivy.require('1.9.0')
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from time import sleep
from random import randint
from functools import partial
import threading


class SimonBoxLayout(BoxLayout):

    # reset all class variables
    def set_class_variables(self):

        # kivy button objects of the colored squares
        self.objcs = []

        # random new sequence that player will try replicate
        self.rand_list = []

        # player current attempt to replicate sequence
        self.player_moves = []

        # current biggest successful sequence replicate
        self.current_streak = 0

        # current longest registered sequence replicate
        self.longest_streak = 0

        # starting lenght of the sequence
        self.starting_size = 1

        # current game tracker for how many numbers in sequence
        self.move_counter = 0

        # game is still ongoing, used to continue looping game
        self.game_on = False

        # in seconds, how long before next blinking square
        self.speed = 1

        # used to lock player input while showing sequence
        self.players_turn = True

        # if this game broke previous record
        self.new_record_flag = False

        # kill_thread_flag is used to kill python loops after game closes
        self.kill_thread_flag = threading.Event()

    # binded to newgame button
    def setup(self, a, b, c, d):

        self.set_class_variables()

        # setup class variables
        self.objcs = [a, b, c, d]
        self.current_streak = 0
        self.longest_streak = self.load_record()
        self.move_counter = self.starting_size - 1
        self.rand_list = [randint(0, 3) for i in range(self.move_counter)]
        self.game_on = True

        # setup game screen
        display_streak = 'Current streak: ' + str(self.current_streak)
        display_record = 'Current record: ' + str(self.longest_streak)
        self.streak.text = display_streak
        self.record.text = display_record

        # start game loop
        threading.Thread(target=self.newgame).start()

    # game loop
    def newgame(self):
        while self.game_on:
            # check if program was closed
            if self.kill_thread_flag.is_set():
                # if yes kill loop
                return
            self.pattern()
            self.intakepattern()
            self.update_current()
        self.announce_gameover()

    # schedule the sequence
    def pattern(self):

        # increment lenght of the sequence
        self.move_counter += 1

        # add new value to sequence
        self.rand_list.append(randint(0, 3))

        # lock player input while sequence being shown
        self.change_turn()

        # in order to not move too fast:
        buff = self.speed / 4
        sleep(3 * buff)

        # list of functions to dim and turn back on
        # each button in sequence
        dim_list = []
        turnon_list = []
        for i in self.rand_list[:self.move_counter]:
            obj = self.objcs[i]
            partial_func1 = partial(self.showpattern_dim, obj)
            partial_func2 = partial(self.showpattern_high, obj)
            dim_list.append(partial_func1)
            turnon_list.append(partial_func2)

        # scheduling the time of execution of each function, in order
        # to create the sequence flow
        for i in range(len(dim_list)):
            Clock.schedule_once(dim_list[i], i * self.speed * 1.1)
            Clock.schedule_once(turnon_list[i], i * self.speed * 1.1 + 1)

        # unlock player input block, after entire sequence was shown
        Clock.schedule_once(self.change_turn, i * self.speed * 1.1 + 1 + buff)

    # dim button (recieves *args scheduling passes extra arg "dt")
    def showpattern_dim(self, obj, *args):
        obj.background_color[-1] = 0.2

    # brighten button (recieves *args scheduling passes extra arg "dt")
    def showpattern_high(self, obj, *args):
        obj.background_color[-1] = 1

    # update if it's player turn to play or not
    def change_turn(self, *args):
        self.players_turn = not self.players_turn
        if self.players_turn:
            self.turn.text = "YOUR TURN!"
        else:
            self.turn.text = ("REPEAT THIS SEQUENCE")

    # update if it's player turn to play or not
    def intakepattern(self, *args):

        # reset the players input from previous round, to get new one
        self.player_moves = []

        # wait for players turn to be True
        while not self.players_turn:

            # check if program was closed
            if self.kill_thread_flag.is_set():
                # if yes kill loop
                return

            # sleep and wait to check again
            sleep(1)

        # Player button clicks will append values to self.player_moves.
        # This loop will check and make sure every click matches sequence.
        # Will exit when player number of inputs equals the lenght of the
        # sequence.
        while len(self.player_moves) < self.move_counter:

            # check if program was closed
            if self.kill_thread_flag.is_set():
                # if yes kill loop
                return

            # check if lists are equal
            for x, y in zip(self.player_moves, self.rand_list):

                if x != y:
                    # if different, declare game over
                    self.game_on = False
                    return

            # wait a little before continuing loop
            sleep(0.1)

    # update screen after every turn
    def update_current(self):

        # if you failed to complete this last sequence lenght
        if not self.game_on:
            self.move_counter -= 1

        # update current streak
        self.current_streak = self.move_counter

        # if your streak is bigger than your record, update record
        if self.current_streak > self.longest_streak:
            self.new_record_flag = True
            self.longest_streak = self.current_streak

        # update the screen with your total streak and record
        streak = 'Current streak: ' + str(self.current_streak)
        record = 'Current record: ' + str(self.longest_streak)
        self.streak.text = streak
        self.record.text = record

    # load record from storage file
    def load_record(self):
        try:
            with open("kivy.dll") as f:
                data = f.readline()
                return int(data)
        except FileNotFoundError:
            with open("kivy.dll", mode="w") as f:
                f.write("0")
                return 0

    # if game is over, announce it
    def announce_gameover(self):

        # if there was a new record, update file, and congratulate
        if self.new_record_flag:
            with open("kivy.dll", mode="w") as f:
                f.write(str(self.current_streak))

            announce = "GAMEOVER\nCongratulations!\nYour new record is "
            announce += str(self.current_streak) + " repetitions."
            self.turn.text = (announce)
        else:
            announce = "GAMEOVER\nYour record remains "
            announce += str(self.longest_streak) + " repetitions."
            self.turn.text = (announce)

    # bound to colored buttons
    def click_append(self, color_number):
        # if its player turn, append to list else don't.
        try:
            if self.players_turn and self.game_on:
                self.player_moves.append(color_number)
        except AttributeError:
            self.set_class_variables()


class SimonGameApp(App):

    def on_stop(self):
        self.root.kill_thread_flag.set()

    def build(self):
        return SimonBoxLayout()


myapp = SimonGameApp()
myapp.run()
