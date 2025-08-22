"""Chinese Dark Chess (Banqi) Game Engine.

This module implements a complete Chinese Dark Chess (Banqi) game engine with
game state management, move validation, and win condition detection.

Chinese Dark Chess is a traditional board game played on an 8x4 board where
pieces are initially placed face-down and revealed during play. Players take
turns flipping pieces or moving revealed pieces according to traditional
Chinese chess rules with modifications for the hidden information gameplay.

Piece Hierarchy (by power level):
    - General (將/帥): Power 6, can capture all except Soldier
    - Advisor (士/仕): Power 5
    - Elephant (象/相): Power 4
    - Horse (馬/俥): Power 3
    - Chariot (車/傌): Power 2
    - Cannon (包/砲): Power 1, can jump over pieces
    - Soldier (卒/兵): Power 0, can capture General

Example:
    game = ChineseDarkGame()
    legal_moves = game.get_legal_moves()
    game.flip(0, 0)  # Flip piece at position (0,0)
    game.change_player()
    
Constants:
    BOARD_ROWS: Board height (8)
    BOARD_COLS: Board width (4)
    BLACK_PIECES: List of black piece indices [2-8]
    RED_PIECES: List of red piece indices [9-15]
"""

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
                         5: "車", 
                         6: "馬"
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
    """Checks if a piece belongs to the red player.
    
    Args:
        piece_index: Integer representing the piece type (0-15).
            Red pieces have indices 9-15.
    
    Returns:
        bool: True if the piece is red (index >= 9), False otherwise.
    """
    if piece_index >= 9:
        return True
    else:
        return False

def is_black(piece_index):
    """Checks if a piece belongs to the black player.
    
    Args:
        piece_index: Integer representing the piece type (0-15).
            Black pieces have indices 2-8.
    
    Returns:
        bool: True if the piece is black (2 <= index <= 8), False otherwise.
    """
    if piece_index <= 8 and piece_index >=2:
        return True
    else:
        return False

def validate_row_col(func):
    """Decorator that validates row and column arguments for board methods.
    
    This decorator checks if the first two positional arguments (row, col)
    are valid board positions before calling the decorated function.
    
    Args:
        func: The function to be decorated. Should be a method that takes
            row and col as its first two arguments after self.
    
    Returns:
        function: The decorated function that validates position arguments.
        Returns False if position is invalid, otherwise calls original function.
    """
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
    """Main game engine for Chinese Dark Chess (Banqi).
    
    This class manages the complete game state including board configuration,
    piece positions, player turns, and win conditions. The game starts with
    all pieces face-down and players take turns either flipping pieces or
    moving revealed pieces according to traditional Chinese chess rules.
    
    Attributes:
        board: List representing the 8x4 board state with piece indices.
        board_face_down_: Shuffled list of actual piece values under face-down pieces.
        taken_pieces_black: List of black pieces that have been captured.
        taken_pieces_red: List of red pieces that have been captured.
        current_player: Current player number (1 or 2).
        current_player_color: Current player's color (RED_PLAYER, BLACK_PLAYER, or UNKNOWN_PLAYER).
        no_change_move: Counter for moves that don't result in captures (for draw detection).
    """
    
    def __init__(self):
        """Initializes a new Chinese Dark Chess game.
        
        Sets up the board with all pieces face-down in random positions,
        initializes empty capture lists, and sets the starting player.
        The first player's color is determined when they flip their first piece.
        """
        # express board as 8x4 2D array, using column major
        self.board = np.full((BOARD_ROWS,BOARD_COLS), FACE_DOWN_PIECE,  dtype=np.uint8)
        self.board_face_down_ = INIT_BOARD_FACE_UP # all
        np.random.shuffle(self.board_face_down_)
        self.taken_pieces_black = []
        self.taken_pieces_red = []
        self.current_player = 1
        self.current_player_color = UNKNOWN_PLAYER
        self.no_change_move = 0

    def restart(self):
        """Resets the game to initial state.
        
        Reshuffles all pieces face-down, clears capture lists, and resets
        player state to the beginning of a new game.
        """
        self.board = np.full((BOARD_ROWS,BOARD_COLS), FACE_DOWN_PIECE,  dtype=np.uint8)
        self.board_face_down_ = INIT_BOARD_FACE_UP
        np.random.shuffle(self.board_face_down_)
        self.taken_pieces_black = []
        self.taken_pieces_red = []
        self.current_player = 1
        self.current_player_color = UNKNOWN_PLAYER
    

    def get_board_state(self):
        """Gets the current board state as a 2D array.
        
        Returns:
            numpy.ndarray: 8x4 array representing the board state where each
                element contains a piece index (0=empty, 1=face-down, 2-15=pieces).
        """
        return np.copy(self.board)
    
    def is_valid_pos(self, row, col) -> bool:
        """Checks if the given position is within board boundaries.
        
        Args:
            row: Row index (0-7).
            col: Column index (0-3).
            
        Returns:
            bool: True if position is valid, False otherwise.
        """
        if row < 0 or row >= BOARD_ROWS: # check row
            return False
        if col < 0 or col >= BOARD_COLS: # check col
            return False
        return True
    def who_win(self):
        """Determines the winner of the current game state.
        
        Checks for win conditions including elimination of all pieces of one color,
        draw due to lack of progress, or ongoing game status.
        
        Returns:
            int: Game outcome constant:
                - DRAW (3): Game is a draw (20+ moves without captures)
                - RED_WIN (1): Red player wins (no black pieces remain)
                - BLACK_WIN (2): Black player wins (no red pieces remain)
                - UNKNOWN (0): Game is still ongoing
        """
        if self.no_change_move >= 20:
            return DRAW
        # all black in taken pieces
        black_pieces = 0
        red_pieces = 0
        face_down_piece = 0
        for piece in np.nditer(self.board):
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
        """Adds a captured piece to the appropriate taken pieces list.
        
        Args:
            piece: Integer representing the captured piece (2-15).
                Black pieces (2-8) go to taken_pieces_black.
                Red pieces (9-15) go to taken_pieces_red.
                
        Raises:
            RuntimeError: If attempting to add EMPTY_SPACE or FACE_DOWN_PIECE.
        """
        if piece == EMPTY_SPACE:
            raise RuntimeError("Try to add Empty piece in to taken pieces")
        if piece == FACE_DOWN_PIECE:
            raise RuntimeError("Try to add face down piece in to taken pieces")
        if piece in BLACK_PIECES:
            self.taken_pieces_black.append(piece)
        else:
            self.taken_pieces_red.append(piece)

    def get_legal_moves(self):
        """Generates all legal moves for the current game state.
        
        Examines the board to find all valid flip and move actions available
        to the current player. Flip moves are available for face-down pieces,
        while move actions are available for revealed pieces according to
        movement and capture rules.
        
        Returns:
            list: List of tuples representing legal moves:
                - Flip moves: (FLIP, row, col)
                - Move actions: (MOVE, from_row, from_col, to_row, to_col)
        """
        legal_moves = []
        # check flip
        for r in range(8):
            for c in range(4):
                if self.can_flip(r, c):
                    legal_moves.append((FLIP, r, c))

        #Player can only move an existing face-up same color piece to other place that are empty or other color.
        if (self.current_player_color == UNKNOWN_PLAYER):
            return legal_moves
        
        # move can only from existing piece to some place
        start_pos_list = [None] * 32
        end_pos_list = [None] * 32
        start_pos_count = 0
        end_pos_list_count = 0
        for r in range(8):
            for c in range(4):
                if self.current_player_color==RED_PLAYER:
                    piece = self.board[r,c]
                    if piece == FACE_DOWN_PIECE:
                        continue
                    elif is_red(piece):
                        start_pos_list[start_pos_count] = (r,c)
                        start_pos_count = start_pos_count + 1
                    else: # is_black or empty
                        end_pos_list[end_pos_list_count] = (r,c)
                        end_pos_list_count = end_pos_list_count + 1
                
                if self.current_player_color==BLACK_PLAYER:
                    piece = self.board[r,c]
                    if piece == FACE_DOWN_PIECE:
                        continue
                    elif is_black(piece):
                        start_pos_list[start_pos_count]= (r,c)
                        start_pos_count = start_pos_count + 1
                    else: # is_red or empty
                        end_pos_list[end_pos_list_count]= (r,c)
                        end_pos_list_count = end_pos_list_count + 1
        for start_pos in start_pos_list:
            for end_pos in end_pos_list:
                if start_pos and end_pos:
                    if self.can_move(start_pos[0], start_pos[1], end_pos[0], end_pos[1]):
                        legal_moves.append((MOVE, start_pos[0], start_pos[1], end_pos[0], end_pos[1]))

        return legal_moves

    def can_flip(self, row, col) -> bool:
        """Checks if a piece at the given position can be flipped.
        
        Args:
            row: Row index (0-7).
            col: Column index (0-3).
            
        Returns:
            bool: True if there is a face-down piece at this position, False otherwise.
        """
        if self.board[row, col] != FACE_DOWN_PIECE:  # can only flip face_down
            return False
        else:
            return True
    
    def can_move(self, row, col, next_row, next_col) -> bool:
        """Checks if a piece can be moved from one position to another.
        
        Validates all movement rules including:
        - Player ownership of the piece
        - Basic movement constraints (orthogonal only)
        - Capture rules based on piece hierarchy
        - Special cannon jumping rules
        - General vs Soldier special interaction
        
        Args:
            row: Starting row position (0-7).
            col: Starting column position (0-3).
            next_row: Target row position (0-7).
            next_col: Target column position (0-3).
            
        Returns:
            bool: True if the move is valid according to game rules, False otherwise.
        """
        if row == next_row and col == next_col:
            return False
        if (row != next_row ) and (col != next_col):
            return False
        pos = row*BOARD_COLS + col
        next_pos = next_row*BOARD_COLS + next_col
        cur_piece_index = self.board[row, col]
        next_piece_index = self.board[next_row, next_col]
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
                    if self.board[row, c] != EMPTY_SPACE:
                        count += 1
            else:
                count = 0
                for r in range(min_row+1, max_row):
                    if self.board[r, col] != EMPTY_SPACE:
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
        """Flips a face-down piece to reveal its identity.
        
        When a piece is flipped, it reveals the actual piece underneath and
        may determine the current player's color if this is their first move.
        Resets the no-change move counter.
        
        Args:
            row: Row position of the piece to flip (0-7).
            col: Column position of the piece to flip (0-3).
            
        Returns:
            bool: True if flip was successful, False if invalid position or
                piece cannot be flipped.
        """
        if self.can_flip(row, col):
            pos = row*BOARD_COLS + col
            self.board[row, col] = self.board_face_down_[pos]
            piece_index = self.board[row, col]
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
        """Moves a piece from one position to another.
        
        Executes a validated move, handling captures, cannon jumps, and special
        rules. Updates board state, manages captured pieces, and tracks move
        counters for draw detection.
        
        Args:
            row: Starting row position (0-7).
            col: Starting column position (0-3).
            next_row: Target row position (0-7).
            next_col: Target column position (0-3).
            
        Returns:
            bool: True if move was executed successfully, False if invalid.
            
        Raises:
            RuntimeError: If move validation passed but execution failed.
        """
        if not self.can_move(row, col, next_row, next_col):
            return False
        pos = row*BOARD_COLS + col
        next_pos = next_row*BOARD_COLS + next_col
        cur_piece_index = self.board[row, col]
        next_piece_index = self.board[next_row, next_col]
        if (abs(next_row-row) + abs(next_col-col)) != 1:
            self.board[next_row, next_col] = cur_piece_index
            self.board[row, col] = EMPTY_SPACE
            self.add_taken_pieces(next_piece_index)
            self.no_change_move = 0
            return True
        else: # move distance = 1 case. Cannon jump is not included.
            if next_piece_index == EMPTY_SPACE:
                # Swap the values in the two poses
                self.board[next_row, next_col] = self.board[row, col]
                self.board[row, col] = EMPTY_SPACE
                self.no_change_move = self.no_change_move + 1
                return True
            if PIECE_POWER[cur_piece_index] == 0 and PIECE_POWER[next_piece_index] == 6: # 兵 能吃 將
                self.board[next_row, next_col] = cur_piece_index
                self.board[row, col] = EMPTY_SPACE
                self.add_taken_pieces(next_piece_index)
                self.no_change_move = 0
                return True
            if (PIECE_POWER[cur_piece_index] >= PIECE_POWER[next_piece_index]):
                print(f"{INDEX_TO_CHINESE_MAP[cur_piece_index]} 吃 {INDEX_TO_CHINESE_MAP[next_piece_index]} !")
                self.board[next_row, next_col] = cur_piece_index
                self.board[row, col] = EMPTY_SPACE
                self.add_taken_pieces(next_piece_index)
                self.no_change_move = 0
                return True
            raise RuntimeError("move failed ??")
            
    def change_player(self):
        """Switches to the next player's turn.
        
        Alternates between player 1 and player 2, and swaps the active color
        between red and black. Cannot be called if current player color is
        still unknown (before any pieces are flipped).
        
        Returns:
            bool: True if player change was successful, False if current
                player color is still unknown.
        """
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


