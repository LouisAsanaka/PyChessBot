import chess


class Chessboard:
    def __init__(self, width=0, height=0, top_left=(0, 0)):
        # Instantiate an internal board object
        self.internal_board = chess.Board()

        self.width = width
        self.height = height

        self.coord = top_left

    def set_dimensions(self, width, height):
        self.width = width
        self.height = height

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def set_coordinates(self, top_left):
        self.coord = top_left

    def get_coordinates(self):
        return self.coord
