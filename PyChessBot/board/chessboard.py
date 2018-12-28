import chess


class Chessboard:
    def __init__(self, width=0, height=0, top_left=(0, 0)):
        # Instantiate an internal board object
        self.internal_board = chess.Board()

        self.width = width
        self.height = height

        self.square_width = width // 8
        self.square_height = height // 8

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

    def get_square_corner(self, rank, file):
        return self.coord[0] + self.square_width * file, self.coord[1] + self.square_height * rank

    def get_square_center(self, corner):
        return corner[0] + self.square_width // 2, corner[1] + self.square_height // 2

    def piece_type_at(self, square):
        return self.internal_board.piece_type_at(square)

    def get_legal_moves(self):
        return self.internal_board.legal_moves

    def is_game_over(self):
        return self.internal_board.is_game_over(claim_draw=True)

    @staticmethod
    def get_square(rank, file):
        return chess.square_mirror(chess.square(file, rank))

    def play_move(self, move):
        self.internal_board.push(move)
