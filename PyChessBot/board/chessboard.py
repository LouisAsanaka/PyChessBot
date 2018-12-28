import chess


class Chessboard:
    LEGAL_FIRST_MOVES = (
        "Nh3", "Nf3", "Nc3", "Na3", "h3", "g3", "f3", "e3", "d3", "c3",
        "b3", "a3", "h4", "g4", "f4", "e4", "d4", "c4", "b4", "a4"
    )
    LEGAL_FIRST_MOVES_UCI = (
        "g1h3", "g1f3", "b1c3", "b1a3", "h2h3", "g2g3", "f2f3", "e2e3", "d2d3", "c2c3",
        "b2b3", "a2a3", "h2h4", "g2g4", "f2f4", "e2e4", "d2d4", "c2c4", "b2b4", "a2a4"
    )

    def __init__(self, width, height, top_left, color=chess.WHITE):
        # Instantiate an internal board object
        self.internal_board = chess.Board()

        self.width = width
        self.height = height

        self.square_width = width // 8
        self.square_height = height // 8

        self.coord = top_left

        self.color = color

    def set_color(self, color):
        self.color = color

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
        return self.internal_board.is_game_over(claim_draw=False)

    @staticmethod
    def mirror(square, color=chess.WHITE):
        if color == chess.WHITE:
            return square ^ 0x38
        else:
            return square ^ 0x7

    @staticmethod
    def get_square(rank, file, color=chess.WHITE):
        return Chessboard.mirror(chess.square(file, rank), color)

    @staticmethod
    def get_square_name(square, color=chess.WHITE):
        return chess.square_name(Chessboard.mirror(square, color))

    @staticmethod
    def get_true_rank(square, color=chess.WHITE):
        rank = chess.square_rank(square)
        return 7 - rank if color == chess.WHITE else rank

    @staticmethod
    def get_true_file(square, color=chess.WHITE):
        file = chess.square_file(square)
        return file if color == chess.WHITE else 7 - file

    def play_move(self, move):
        self.internal_board.push(move)
