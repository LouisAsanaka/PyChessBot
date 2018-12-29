from gui.gui import GUI
from bot.bot import Bot
from board.chessboard import Chessboard
from board.scanner import Scanner
from board.analyzer import BoardAnalyzer
import chess
import sys
import os

TASK_REPEAT_INTERVAL = 100


class Main:

    def __init__(self):
        if not os.path.isdir("../bin"):
            os.mkdir("../bin")
        if not os.path.isfile("../bin/engine.exe"):
            print("Error: Engine not found!")
            print("Place engine.exe in " + os.path.join(os.path.dirname(os.path.abspath(".")), "bin"))
            sys.exit()

        self.board: Chessboard = None
        self.analyzer: BoardAnalyzer = None
        self.bot: Bot = None

        # Instantiate the GUI
        self.interface = GUI(self.toggle_color, self.set_coordinates)
        self.interface.create_window()

        # Instantiate the scanner
        self.scanner = Scanner(self.interface)

        # Retrieve the coordinates of the board from mouse input
        self.scanner.retrieve_coordinates(self.set_coordinates)

        # Required main loop for any tkinter application
        self.interface.window.mainloop()

    def set_coordinates(self, width, height, top_left):
        self.interface.loaded = True  # Funky hack
        if self.scanner.task_id != -1:
            self.interface.cancel_task(self.scanner.task_id)
        self.scanner = None
        self.wait_for_start(self.initialize_bot, width, height, top_left)

    def initialize_bot(self, width, height, top_left):
        # Instantiate a chessboard object (wrapper for a python-chess board)
        self.board = Chessboard(width, height, top_left, self.interface.color)
        self.analyzer = BoardAnalyzer(self.board, self.interface)
        self.bot = Bot(self.board, self.analyzer.square_centers)

        if self.board.color == chess.WHITE:
            self.bot.play_move()
            self.analyzer.set_previous_state()
            self.loop()
        else:
            self.loop_initial_check()

    def wait_for_start(self, callback, *args):
        if self.interface.running:
            callback(*args)
            return
        self.interface.delay_task(100, self.wait_for_start, callback, *args)

    def loop(self):
        if not self.interface.running:
            self.interface.delay_task(TASK_REPEAT_INTERVAL, self.loop)
            return
        if self.board.is_game_over():
            self.interface.log("Game over!")
            self.bot.terminate()
            return
        move = self.analyzer.analyze_changes(self.analyzer.detect_changes())
        if move is None:
            self.interface.delay_task(TASK_REPEAT_INTERVAL, self.loop)
            return
        self.board.play_move(move)

        self.bot.play_move()

        self.analyzer.set_previous_state()  # Take a shot AFTER the bot's own move

        self.interface.delay_task(TASK_REPEAT_INTERVAL, self.loop)

    def loop_initial_check(self):
        if not self.interface.running:
            self.interface.delay_task(TASK_REPEAT_INTERVAL, self.loop_initial_check)
            return
        move = self.analyzer.detect_initial_changes()
        if move is None:
            self.interface.delay_task(TASK_REPEAT_INTERVAL, self.loop_initial_check)
            return
        self.board.play_move(move)

        self.bot.play_move()
        self.analyzer.set_previous_state()

        self.loop()

    def toggle_color(self):
        if self.board is not None:
            self.board.color = not self.board.color


if __name__ == "__main__":
    Main()
