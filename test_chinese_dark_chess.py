import unittest
from chinese_dark_chess import *

class TestStringMethods(unittest.TestCase):

    def test_original_legal_moves(self):
        new_game = ChineseDarkGame()
        legal_moves = new_game.get_legal_moves()
        # should be only flip
        assert len(legal_moves) == 32
        for legal_move in legal_moves:
            type, _, _ = legal_move
            self.assertEqual(type,FLIP)
    
    def test_general_moves_and_captures(self):
        new_game = ChineseDarkGame()
        new_game.board = np.full((BOARD_ROWS,BOARD_COLS), EMPTY_SPACE,  dtype=np.uint8)
        new_game.board[0,0] = BLACK_GENERAL_PIECE
        new_game.board[0,1] = RED_GENERAL_PIECE
        new_game.current_player = 1
        new_game.current_player_color = BLACK_PLAYER

        legal_moves = new_game.get_legal_moves()
        self.assertEqual(len(legal_moves), 2)
        for legal_move in legal_moves:
            type, _, _,_, _ = legal_move
            self.assertEqual(type,MOVE)

    # def test_split(self):
    #     s = 'hello world'
    #     self.assertEqual(s.split(), ['hello', 'world'])
    #     # check that s.split fails when the separator is not a string
    #     with self.assertRaises(TypeError):
    #         s.split(2)

if __name__ == '__main__':
    unittest.main()