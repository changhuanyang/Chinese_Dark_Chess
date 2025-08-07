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
            assert type == FLIP
    
    # def test_(self):
    #     self.assertTrue('FOO'.isupper())
    #     self.assertFalse('Foo'.isupper())

    # def test_split(self):
    #     s = 'hello world'
    #     self.assertEqual(s.split(), ['hello', 'world'])
    #     # check that s.split fails when the separator is not a string
    #     with self.assertRaises(TypeError):
    #         s.split(2)

if __name__ == '__main__':
    unittest.main()