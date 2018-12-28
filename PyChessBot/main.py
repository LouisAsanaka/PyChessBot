from gui.gui import GUI
from board.chessboard import Chessboard
from board.scanner import Scanner
from board.analyzer import BoardAnalyzer
from engine.chessengine import ChessEngine


class Main:

    def __init__(self):
        self.board = None
        self.engine = None
        self.analyzer = None

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
        self.engine = ChessEngine()
        self.analyzer = BoardAnalyzer(self.board)


if __name__ == "__main__":
    Main()
