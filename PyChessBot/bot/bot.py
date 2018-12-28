import chess
import pyautogui
import time
from board.chessboard import Chessboard
from engine.chessengine import ChessEngine


class Bot:

    def __init__(self, board, square_centers):
        pyautogui.PAUSE = 0.1

        self.engine: ChessEngine = ChessEngine()
        self.board: Chessboard = board
        self.square_centers = square_centers

    def play_move(self):
        engine_move = self.engine.evaluate(self.board.internal_board)
        self.board.play_move(engine_move)

        move_from, move_to, promotion = engine_move.from_square, engine_move.to_square, engine_move.promotion

        start_x, start_y = self.square_centers[7 - chess.square_rank(move_from), chess.square_file(move_from)]
        to_x, to_y = self.square_centers[7 - chess.square_rank(move_to), chess.square_file(move_to)]

        pyautogui.moveTo(start_x, start_y)
        pyautogui.dragTo(to_x, to_y, 0.5, button='left')

        if promotion is not None:
            self.attempt_promotion(promotion)

    def attempt_promotion(self, promotion):
        try:
            # This is purely for chess.com
            # Promotion list: Queen Knight Rook Bishop
            promotion_list = [
                chess.QUEEN,
                chess.KNIGHT,
                chess.ROOK,
                chess.BISHOP
            ]
            if promotion in promotion_list:
                multiplier = promotion_list.index(promotion)
                relative_distance = self.board.square_height * multiplier
                if relative_distance == 0:
                    time.sleep(0.5)
                    pyautogui.click()
                else:
                    pyautogui.moveRel(yOffset=relative_distance, duration=0.5)
                    pyautogui.click()
        except NameError:
            pass
