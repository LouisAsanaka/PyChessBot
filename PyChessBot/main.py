from gui.gui import GUI
from bot.bot import Bot
from board.chessboard import Chessboard
from board.scanner import Scanner
from board.analyzer import BoardAnalyzer


class Main:

    def __init__(self):
        self.board: Chessboard = None
        self.analyzer: BoardAnalyzer = None
        self.bot: Bot = None

        # Instantiate the GUI
        self.interface = GUI()
        self.interface.create_window()

        # Instantiate the scanner
        scanner = Scanner(self.interface)

        # Retrieve the coordinates of the board from mouse input
        scanner.retrieve_coordinates(self.initialize_bot)

        # Required main loop for any tkinter application
        self.interface.window.mainloop()

    def initialize_bot(self, width, height, top_left):
        # Instantiate a chessboard object (wrapper for a python-chess board)
        self.board = Chessboard(width, height, top_left)
        self.analyzer = BoardAnalyzer(self.board, self.interface)
        self.bot = Bot(self.board, self.analyzer.square_centers)

        self.bot.play_move()
        self.analyzer.set_previous_state()

        self.loop()

    def loop(self):
        if self.board.is_game_over():
            self.interface.log("Game over!")
            return
        move = self.analyzer.analyze_changes(self.analyzer.detect_changes())
        if move is None:
            self.interface.delay_task(100, self.loop)
            return
        self.board.play_move(move)

        self.bot.play_move()

        self.analyzer.set_previous_state()  # Take a shot AFTER the bot's own move

        self.interface.delay_task(100, self.loop)


if __name__ == "__main__":
    Main()
