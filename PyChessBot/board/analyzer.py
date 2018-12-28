import numpy as np
import chess
from board.chessboard import Chessboard
from board.image import BoardImage
from gui.gui import GUI
from mss.screenshot import ScreenShot


class BoardAnalyzer:

    def __init__(self, board, interface):
        self.board: Chessboard = board
        self.image: BoardImage = BoardImage(board.get_coordinates(), board.get_width(), board.get_height())

        self.interface: GUI = interface

        self.square_corners = np.empty((8, 8), dtype=(int, 2))
        self.square_centers = np.empty((8, 8), dtype=(int, 2))

        # Units in pixels
        self.scan_region_size = 7
        self.scan_region_area = self.scan_region_size ** 2

        # Size by size area to check for pixel changes
        self.scan_region = np.empty((8, 8, self.scan_region_area, 2), dtype=int)

        self.current_state: ScreenShot = self.image.snap()
        self.previous_state: ScreenShot = self.current_state

        self.initialize_data()

    def set_previous_state(self, snap=None):
        if snap is None:
            self.previous_state = self.image.snap()
        else:
            self.previous_state = snap

    def initialize_data(self):
        for rank in range(8):
            for file in range(8):
                self.square_corners[rank, file] = corner = self.board.get_square_corner(rank, file)
                self.square_centers[rank, file] = center = self.board.get_square_center(corner)
                offset = self.scan_region_size // 2
                index = 0
                for x in range(center[0] - offset, center[0] + offset + 1):
                    for y in range(center[1] - offset, center[1] + offset + 1):
                        self.scan_region[rank, file, index] = (x, y)
                        index += 1

    def detect_changes(self):
        self.current_state = self.image.snap()
        if self.current_state.pixels == self.previous_state.pixels:
            self.interface.log("No changes")
            self.set_previous_state(self.current_state)
            return None

        changed_squares = []
        for rank in range(8):
            for file in range(8):
                coordinates = self.scan_region[rank, file]
                region_changes = 0
                for index in range(self.scan_region_area):
                    x, y = coordinates[index]
                    board_x, board_y = self.board.get_coordinates()
                    if self.current_state.pixel(x - board_x, y - board_y) != self.previous_state.pixel(x - board_x, y - board_y):
                        region_changes += 1
                if region_changes >= self.scan_region_area // 3:
                    self.interface.log("CHANGED")
                    changed_squares.append((rank, file))
        self.set_previous_state(self.current_state)
        if not changed_squares:
            self.interface.log("No changes")
            return None
        return changed_squares

    def analyze_changes(self, changed_squares):
        if changed_squares is None:
            return None
        changes = len(changed_squares)

        for square in changed_squares:
            print(chess.square_name(self.board.get_square(*square)))

        if changes == 4:  # Castling
            rook_index = None
            king_index = None
            for square in changed_squares:
                square_id = self.board.get_square(*square)
                piece_type = self.board.piece_type_at(square_id)
                if piece_type == chess.ROOK:
                    rook_index = square_id
                elif piece_type == chess.KING:
                    king_index = square_id

            assert rook_index is not None and king_index is not None
            print("rook index = " + str(rook_index))
            print("king index = " + str(king_index))
            assert king_index == 4 or king_index == 60

            distance = abs(king_index - rook_index)
            if distance == 3:  # Short castling
                target_index = king_index + 2
            elif distance == 4:
                target_index = king_index - 2
            else:
                raise RuntimeError("Castling calculation error")
            move = chess.Move.from_uci(chess.square_name(king_index) + chess.square_name(target_index))
            return move
        elif changes == 3:  # En passant
            pass
        elif changes == 2:  # Normal move
            sq1, sq2 = changed_squares
            sq1, sq2 = chess.square_name(self.board.get_square(*sq1)), chess.square_name(self.board.get_square(*sq2))
            first_move = chess.Move.from_uci(sq1 + sq2)
            second_move = chess.Move.from_uci(sq2 + sq1)

            legal_moves = self.board.get_legal_moves()
            if first_move in legal_moves:
                return first_move
            elif second_move in legal_moves:
                return second_move
            else:
                raise RuntimeError("Unknown error")
        else:
            self.interface.log("Invalid changes!")
