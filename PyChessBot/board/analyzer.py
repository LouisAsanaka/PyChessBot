from board.image import BoardImage


class BoardAnalyzer:

    def __init__(self, board):
        self.board = board
        self.image = BoardImage(board.get_coordinates(), board.get_width(), board.get_height())
