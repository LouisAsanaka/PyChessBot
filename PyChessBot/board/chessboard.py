import chess


class Chessboard:
    def __init__(self):
        # Instantiate an internal board object
        self.internal_board = chess.Board()

        self.width = 0
        self.height = 0

    def set_dimensions(self, width, height):
        self.width = width
        self.height = height

    def get_dimensions(self):
        return self.width, self.height
