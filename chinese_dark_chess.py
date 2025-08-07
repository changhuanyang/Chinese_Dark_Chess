# 象棋 英文代號
# 空 0
# 蓋牌 Unknown(N) 1 face down
# Black side / Red side
# 將/帥 General(G) 2 / 9 
# 士/仕 Advisor (A) 3 / 10
# 象/相(Elephant):Elephant or Bishop (常簡寫為E) 4 / 11
# 馬/碼(Horse):Horse (常簡寫為H) 5 / 12
# 車/俥(Chariot):Chariot or Rook (常簡寫為R) 6 / 13
# 包/砲(Cannon):Cannon (常簡寫為C) 7 / 14
# 卒/兵(Soldier):Soldier (常簡寫為S) 8/ 15

INIT_BOARD_FACE_UP = [2, 3, 3, 4, 4, 5,5,6,6,7,7,8,8,8,8,8, 9,10,10,11,11,12,12,13,13,14,14,15,15,15,15,15]
BLACK_PIECES = [2,3,4,5,6,7,8]
RED_PIECES = [9,10,11,12,13,14,15]

INDEX_TO_CHINESE_MAP = { 0: "", 
                         1: "?", 
                         2: u"將",  
                         3: u"士", 
                         4: u"象", 
                         5: u"車", 
                         6: u"馬", 
                         7: u"包", 
                         8: u"卒",
                         9: u"帥", 
                         10: u"仕",
                         11: u"相", 
                         12: u"傌", 
                         13: u"俥", 
                         14: u"砲", 
                         15: u"兵"}

import random
import numpy as np
from functools import wraps


BOARD_ROWS = 8
BOARD_COLS = 4
TOTAL_NUMBER_PIECES = BOARD_ROWS * BOARD_COLS

# Player
UNKNOWN_PLAYER = 0
RED_PLAYER = 1
BLACK_PLAYER = 2

# piece
EMPTY_SPACE = 0
FACE_DOWN_PIECE = 1
BLACK_GENERAL_PIECE = 2
BLACK_ADVISOR_PIECE = 3
BLACK_ELEPHANT_PIECE = 4
BLACK_HORSE_PIECE = 5
BLACK_CHARIOT_PIECE = 6
BLACK_CANNON_PIECE = 7
BLACK_SOLDIER_PIECE = 8

RED_GENERAL_PIECE = 9
RED_ADVISOR_PIECE = 10
RED_ELEPHANT_PIECE = 11
RED_HORSE_PIECE = 12
RED_CHARIOT_PIECE = 13
RED_CANNON_PIECE = 14
RED_SOLDIER_PIECE = 15


# 
UNKNOWN = 0
RED_WIN = 1
BLACK_WIN = 2
DRAW = 3


INIT_BOARD_FACE_UP = [2, 3, 3, 4, 4, 5,5,6,6,7,7,8,8,8,8,8, 9,10,10,11,11,12,12,13,13,14,14,15,15,15,15,15]
INDEX_TO_CHINESE_MAP = { 0: "", 
                         1: "?", 
                         2: "將",  
                         3: "士", 
                         4: "象", 
                         5: "馬", 
                         6: "車", 
                         7: "包", 
                         8: "卒",
                         9: "帥", 
                         10: "仕",
                         11: "相", 
                         12: "俥", 
                         13: "傌", 
                         14: "砲", 
                         15: "兵"}
PIECE_POWER = { 2: 6, 
                3: 5, 
                4: 4, 
                5: 3,
                6: 2,
                7: 1,
                8: 0,
                9: 6, 
                10: 5, 
                11: 4, 
                12: 3,
                13: 2,
                14: 1,
                15: 0 }

FLIP = 0
MOVE = 1


def is_red(piece_index):
    if piece_index >= 9:
        return True
    else:
        return False

def is_black(piece_index):
    if piece_index <= 8 and piece_index >=2:
        return True
    else:
        return False

def validate_row_col(func):
    
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        # Assuming 'a' and 'b' are the first two positional arguments
        row = args[0]
        col = args[1]
        if self.is_valid_pos(row, col):
            return func(self, *args, **kwargs)
        else:
            return False
    
    return wrapper



class ChineseDarkGame:
    def __init__(self):
        # express board as 8x4 2D array, using column major
        self.board = [FACE_DOWN_PIECE]* TOTAL_NUMBER_PIECES
        self.board_face_down_ = INIT_BOARD_FACE_UP # all 
        np.random.shuffle(self.board_face_down_)
        self.taken_pieces_black = []
        self.taken_pieces_red = []
        self.current_player = 1
        self.current_player_color = UNKNOWN_PLAYER
        self.no_change_move = 0

    def restart(self):
        self.board = [FACE_DOWN_PIECE]* TOTAL_NUMBER_PIECES
        self.board_face_down_ = INIT_BOARD_FACE_UP
        np.random.shuffle(self.board_face_down_)
        self.taken_pieces_black = []
        self.taken_pieces_red = []
        self.current_player = 1
        self.current_player_color = UNKNOWN_PLAYER

    def get_board_state(self):
        board_state = np.reshape(self.board, (8,4))
        return board_state
    
    def is_valid_pos(self, row, col) -> True:
        if row < 0 or row >= BOARD_ROWS: # check row
            return False
        if col < 0 or col >= BOARD_COLS: # check col
            return False
        return True
    def who_win(self):
        if self.no_change_move >= 20:
            return DRAW
        # all black in taken pieces
        black_pieces = 0
        red_pieces = 0
        face_down_piece = 0
        for piece in self.board:
            if piece in BLACK_PIECES:
                black_pieces = black_pieces + 1
            elif piece in RED_PIECES:
                red_pieces = red_pieces + 1
            elif piece == FACE_DOWN_PIECE:
                face_down_piece = face_down_piece + 1
        if face_down_piece != 0:
            return UNKNOWN
        if black_pieces == 0:
            return RED_WIN
        elif red_pieces == 0:
            return BLACK_WIN
        else:
            return UNKNOWN
    
    def add_taken_pieces(self, piece):
        if piece == EMPTY_SPACE:
            raise RuntimeError("Try to add Empty piece in to taken pieces")
        if piece == FACE_DOWN_PIECE:
            raise RuntimeError("Try to add face down piece in to taken pieces")
        if piece in BLACK_PIECES:
            self.taken_pieces_black.append(piece)
        else:
            self.taken_pieces_red.append(piece)

    def get_legal_moves(self):
        legal_moves = []
        # check flip
        for r in range(8):
            for c in range(4):
                if self.can_flip(r, c):
                    legal_moves.append((FLIP, r, c))

        # check move
        for r in range(8):
            for c in range(4):
                for next_r in range(8):
                    for next_c in range(4):
                        if self.can_move(r, c, next_r, next_c):
                            legal_moves.append((MOVE, r, c,next_r, next_c))

        return legal_moves

    def can_flip(self, row, col) -> bool:
        pos = row*BOARD_COLS + col
        if self.board[pos] != FACE_DOWN_PIECE:  # can only flip face_down
            return False
        else:
            return True
    
    def can_move(self, row, col, next_row, next_col) -> bool:
        if row == next_row and col == next_col:
            return False
        if (row != next_row ) and (col != next_col):
            return False
        pos = row*BOARD_COLS + col
        next_pos = next_row*BOARD_COLS + next_col
        cur_piece_index = self.board[pos]
        next_piece_index = self.board[next_pos]
        if self.current_player_color == RED_PLAYER and is_black(cur_piece_index):
            return False
        if self.current_player_color == BLACK_PLAYER and is_red(cur_piece_index):
            return False
        if cur_piece_index == FACE_DOWN_PIECE:
            return False
        if cur_piece_index == EMPTY_SPACE:
            return False
        if next_piece_index == FACE_DOWN_PIECE:
            return False
        if (is_red(cur_piece_index) and is_red(next_piece_index)) or (  is_black(cur_piece_index) and is_black(next_piece_index)): # same color
            return False
        if (abs(next_row-row) + abs(next_col-col)) != 1:
            if cur_piece_index != 7 and cur_piece_index != 14: # 不是砲
                return False
            # check if only one piece between the two pos
            max_col, min_col = max(col, next_col), min(col, next_col)
            max_row, min_row = max(row, next_row), min(row, next_row)
            count = 0
            if max_col != min_col:
                for c in range(min_col+1, max_col):
                    tmp_pos = row* BOARD_COLS + c
                    if self.board[tmp_pos] != EMPTY_SPACE:
                        count += 1
            else:
                count = 0
                for r in range(min_row+1, max_row):
                    tmp_pos = r* BOARD_COLS + col
                    if self.board[tmp_pos] != EMPTY_SPACE:
                        count += 1
            if count == 1:
                return True
            else:
                return False
        else: # move distance = 1 case. Cannon jump is not included.
            if next_piece_index == EMPTY_SPACE:
                return True
            if cur_piece_index == 7 or cur_piece_index == 14:
                return False
            if PIECE_POWER[cur_piece_index] == 6 and PIECE_POWER[cur_piece_index] == 0:# 將 不能吃 兵 
                return False
            if PIECE_POWER[cur_piece_index] == 0 and PIECE_POWER[next_piece_index] == 6: # 兵 能吃 將 
                return True
            if (PIECE_POWER[cur_piece_index] >= PIECE_POWER[next_piece_index]):
                return True
            else:
                return False


    @validate_row_col
    def flip(self, row, col) -> bool:
        if self.can_flip(row, col):
            pos = row*BOARD_COLS + col
            self.board[pos] = self.board_face_down_[pos]
            piece_index = self.board[pos]
            if self.current_player_color == UNKNOWN_PLAYER:
                if is_red(piece_index):
                    self.current_player_color = RED_PLAYER
                else:
                    self.current_player_color = BLACK_PLAYER
            self.no_change_move = 0
            return True
        else:
            return False

    @validate_row_col
    def move(self, row, col, next_row, next_col) -> bool:
        if not self.can_move(row, col, next_row, next_col):
            return False
        pos = row*BOARD_COLS + col
        next_pos = next_row*BOARD_COLS + next_col
        cur_piece_index = self.board[pos]
        next_piece_index = self.board[next_pos]
        if (abs(next_row-row) + abs(next_col-col)) != 1:
            self.board[next_pos] = cur_piece_index
            self.board[pos] = EMPTY_SPACE
            self.add_taken_pieces(next_piece_index)
            self.no_change_move = 0
            return True
        else: # move distance = 1 case. Cannon jump is not included.
            if next_piece_index == EMPTY_SPACE:
                # Swap the values in the two poses
                self.board[next_pos] = self.board[pos]
                self.board[pos] = EMPTY_SPACE
                self.no_change_move = self.no_change_move + 1
                return True
            if PIECE_POWER[cur_piece_index] == 0 and PIECE_POWER[next_piece_index] == 6: # 兵 能吃 將 
                self.board[next_pos] = cur_piece_index
                self.board[pos] = EMPTY_SPACE
                self.add_taken_pieces(next_piece_index)
                self.no_change_move = 0
                return True
            if (PIECE_POWER[cur_piece_index] >= PIECE_POWER[next_piece_index]):
                print(f"{INDEX_TO_CHINESE_MAP[cur_piece_index]} 吃 {INDEX_TO_CHINESE_MAP[next_piece_index]} !")
                self.board[next_pos] = cur_piece_index
                self.board[pos] = EMPTY_SPACE
                self.add_taken_pieces(next_piece_index)
                self.no_change_move = 0
                return True
            raise RuntimeError("move failed ??")
    def change_player(self):
        if self.current_player_color == UNKNOWN_PLAYER:
            return False
        if self.current_player == 1:
            self.current_player = 2
        else:
            self.current_player = 1
        
        if self.current_player_color == BLACK_PLAYER:
            self.current_player_color = RED_PLAYER
        else:
            self.current_player_color = BLACK_PLAYER
        
        return True


