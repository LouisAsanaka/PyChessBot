from gui.gui import GUI
from bot.bot import Bot
from board.chessboard import Chessboard
from board.scanner import Scanner
from board.analyzer import BoardAnalyzer
import chess

TASK_REPEAT_INTERVAL = 100


class Main:

    def __init__(self):
        self.board: Chessboard = None
        self.analyzer: BoardAnalyzer = None
        self.bot: Bot = None

        # Instantiate the GUI
        self.interface = GUI(self.toggle_color)
        self.interface.create_window()

        # Instantiate the scanner
        scanner = Scanner(self.interface)

        # Retrieve the coordinates of the board from mouse input
        scanner.retrieve_coordinates(self.initialize_bot)

        # Required main loop for any tkinter application
        self.interface.window.mainloop()

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
        self.bot.terminate()

    def loop(self):
        if not self.interface.running:
            self.interface.delay_task(TASK_REPEAT_INTERVAL, self.loop)
            return
        if self.board.is_game_over():
            self.interface.log("Game over!")
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
