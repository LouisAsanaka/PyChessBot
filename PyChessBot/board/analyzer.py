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
        self.region_threshold = 10

        # Size by size area to check for pixel changes
        self.scan_region = np.empty((8, 8, self.scan_region_area, 2), dtype=int)

        self.board_x, self.board_y = self.board.get_coordinates()

        self.light_square_color = None
        self.dark_square_color = None

        self.current_state: ScreenShot = self.image.snap()
        self.previous_state: ScreenShot = self.current_state

        self.is_animating = False
        self.animating_state: ScreenShot = None

        self.initialize_data()

    def set_previous_state(self, snap=None):
        if snap is None:
            self.previous_state = self.image.snap()
        else:
            self.previous_state = snap

    def set_animating_state(self, snap=None):
        if snap is None:
            self.animating_state = self.image.snap()
        else:
            self.animating_state = snap

    def initialize_data(self):
        for rank in range(0, 8):
            for file in range(0, 8):
                self.square_corners[rank, file] = corner = self.board.get_square_corner(rank, file)
                self.square_centers[rank, file] = center = self.board.get_square_center(corner)
                offset = self.scan_region_size // 2
                index = 0
                for x in range(center[0] - offset, center[0] + offset + 1):
                    for y in range(center[1] - offset, center[1] + offset + 1):
                        self.scan_region[rank, file, index] = (x, y)
                        index += 1
        # Get the RGB values of the light and dark squares
        # 4, 0 and 4, 1 are arbitrary coordinates where we
        # are guaranteed to not have any pieces in the way
        light_sq_x, light_sq_y = self.square_centers[4, 0]
        self.light_square_color = self.current_state.pixel(light_sq_x - self.board_x, light_sq_y - self.board_y)
        dark_sq_x, dark_sq_y = self.square_centers[4, 1]
        self.dark_square_color = self.current_state.pixel(dark_sq_x - self.board_x, dark_sq_y - self.board_y)

    def detect_initial_changes(self):
        self.current_state = self.image.snap()
        for rank in range(2, 4):
            for file in range(0, 8):
                coordinates = self.scan_region[rank, file]
                region_changes = 0
                for index in range(self.scan_region_area):
                    x, y = coordinates[index]
                    pixel = self.current_state.pixel(x - self.board_x, y - self.board_y)
                    if BoardImage.is_close(pixel, self.light_square_color) or \
                            BoardImage.is_close(pixel, self.dark_square_color):
                        pass
                    else:
                        region_changes += 1
                print("-> ", (rank, file), region_changes)
                if region_changes >= self.region_threshold:
                    if self.is_animating:
                        if self.current_state.pixels == self.animating_state.pixels:
                            self.is_animating = False
                            self.set_animating_state(None)
                        else:
                            self.set_animating_state(self.current_state)
                            return None
                    else:
                        self.is_animating = True
                        self.set_animating_state(self.current_state)
                        return None
                    square_name = chess.square_name(Chessboard.get_square(rank, file, self.board.color))
                    if square_name in ("a3", "c3", "h3", "f3"):  # It might be a pawn move
                        x, y = self.square_centers[rank - 1, file]
                        pixel = self.current_state.pixel(x - self.board_x, y - self.board_y)
                        if BoardImage.is_close(pixel, self.light_square_color) or \
                                BoardImage.is_close(pixel, self.dark_square_color):
                            # Pawn move
                            move = square_name  # Did this just to remind myself
                        else:
                            # Knight move
                            move = "N" + square_name
                    elif square_name in Chessboard.LEGAL_FIRST_MOVES:
                        move = square_name  # Did this just to remind myself
                    else:
                        self.interface.log("Move detected was not a legal move.", level="error")
                        raise RuntimeError("Error: Move detected was not a legal move.")
                    self.interface.log(f"Opponent move: {move}")
                    uci_string = Chessboard.LEGAL_FIRST_MOVES_UCI[Chessboard.LEGAL_FIRST_MOVES.index(move)]
                    return chess.Move.from_uci(uci_string)

    def detect_changes(self):
        self.current_state = self.image.snap()
        if self.is_animating:
            if self.current_state.pixels == self.animating_state.pixels:
                self.is_animating = False
                self.set_animating_state(None)
                # self.image.save(self.current_state, "current")
                # self.image.save(self.previous_state, "previous")
                # self.image.save(self.animating_state, "anim")
            else:
                self.set_animating_state(self.current_state)
                return None
        else:
            if self.current_state.pixels == self.previous_state.pixels:
                self.set_previous_state(self.current_state)
                return None
            self.is_animating = True
            self.set_animating_state(self.current_state)
            return None

        changed_squares = []
        for rank in range(0, 8):
            for file in range(0, 8):
                coordinates = self.scan_region[rank, file]
                region_changes = 0
                for index in range(self.scan_region_area):
                    x, y = coordinates[index]
                    old_pixel = self.current_state.pixel(x - self.board_x, y - self.board_y)
                    new_pixel = self.previous_state.pixel(x - self.board_x, y - self.board_y)
                    if not BoardImage.is_close(old_pixel, new_pixel):
                        region_changes += 1
                # print((rank, file), region_changes)
                if region_changes >= self.region_threshold:
                    #print((rank, file), region_changes)
                    changed_squares.append((rank, file))
        self.set_previous_state(self.current_state)
        if not changed_squares:
            return None
        return changed_squares

    def analyze_changes(self, changed_squares: list):
        if changed_squares is None:
            return None
        changes = len(changed_squares)
        # print(changed_squares)
        print(self.board.internal_board)

        if changes == 4:  # Castling
            rook_index = None
            king_index = None
            for square in changed_squares:
                square_id = self.board.get_square(*square, self.board.color)
                piece_type = self.board.piece_type_at(square_id)
                if piece_type == chess.ROOK:
                    rook_index = square_id
                elif piece_type == chess.KING:
                    king_index = square_id

            assert rook_index is not None and king_index is not None
            assert king_index == 4 or king_index == 60

            distance = abs(king_index - rook_index)
            if distance == 3:  # Short castling
                target_index = king_index + 2
            elif distance == 4:
                target_index = king_index - 2
            else:
                self.interface.log("Castling calculation error", level="error")
                raise RuntimeError("Castling calculation error.")
            move = chess.Move.from_uci(chess.square_name(king_index) + chess.square_name(target_index))
            return move
        elif changes == 3:  # En passant
            squares = []
            for i in range(0, 3):
                squares.append(Chessboard.get_square(*changed_squares[i], self.board.color))
            if chess.square_file(squares[0]) == chess.square_file(squares[1]):
                attacking_pawn = 2
            elif chess.square_file(squares[1]) == chess.square_file(squares[2]):
                attacking_pawn = 1
            else:
                attacking_pawn = 1
            del changed_squares[attacking_pawn]

            attacking_pawn_rank = chess.square_rank(squares[attacking_pawn])
            if attacking_pawn_rank == chess.square_rank(squares[0]):
                target_square = squares[1]
            else:
                target_square = squares[0]
            return chess.Move.from_uci(
                Chessboard.get_square_name(squares[attacking_pawn], self.board.color) +
                Chessboard.get_square_name(target_square, self.board.color)
            )
        elif changes == 2:  # Normal move
            sq1, sq2 = changed_squares
            sq1 = chess.square_name(Chessboard.get_square(*sq1, self.board.color))
            sq2 = chess.square_name(Chessboard.get_square(*sq2, self.board.color))
            possible_moves = (sq1 + sq2, sq2 + sq1, sq1 + sq2 + "q", sq2 + sq1 + "q")

            legal_moves = self.board.get_legal_moves()
            for move_uci in possible_moves:
                move = chess.Move.from_uci(move_uci)
                if move in legal_moves:
                    return move
            self.interface.log("Unknown error occurred.", level="error")
            raise RuntimeError("Unknown error occurred.")
        else:
            self.interface.log("Invalid changes.", level="error")
            raise RuntimeError("Invalid changes.")
