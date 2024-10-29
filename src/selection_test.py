import unittest
import numpy as np
from selection import Game

class Test6on3(unittest.TestCase):
    def setUp(self):
        self.A=np.array([
            [ 0, -1,  1,  1,  1,  1],  #a
            [ 1,  0, -1,  1,  1,  1],  #b
            [-1,  1,  0,  1,  1,  1],  #c
            [ -1,  -1,  -1,  0,  0,  0],  #d
            [ -1,  -1,  -1,  0,  0,  0],  #e
            [ -1,  -1,  -1,  0,  0,  0]   #f
        ])
        self.pokemon_name_A_my=["グー","チョキ","パー","モブ1","モブ2","モブ3"]
        self.pokemon_name_A_op=["グー","チョキ","パー","モブ1","モブ2","モブ3"]
        self.pokemon_name_B_my=["12","13","23","34","45","56"]
        self.pokemon_name_B_op=["かませ1","かませ2","かませ3","あくま4","あくま5","あくま6"]
        self.B=np.array([
            [ 1,  1,  0,  0,  0,  0],  #12
            [ 1,  0,  1,  0,  0,  0],  #13
            [ 0,  1,  1,  0,  0,  0],  #23
            [ 0,  0,  1,  1,  0,  0],  #34
            [ 0,  0,  0,  1,  1,  0],  #45
            [ 0,  0,  0,  0,  1,  1]   #56
        ])
    def check_testself_AB(self):
        self.assertEqual(self.A.shape[0], 6)
        self.assertEqual(self.A.shape[1], 6)
        self.assertEqual(self.B.shape[0], 6)
        self.assertEqual(self.B.shape[1], 6)
        self.assertEqual(self.A[0][1], -1)
        self.assertEqual(self.B[0][1], 1)
        self.assertEqual(self.A[1][0], 1)
        self.assertEqual(self.B[3][5], 0)
    def test_game(self):
        game = Game(self.A,self.pokemon_name_A_my,self.pokemon_name_A_op)
        game.play()
        result = game.get_result()
        
        self.assertEqual(result["evaluation"], 0)
        np.testing.assert_array_equal(result["selection"], np.array([1,1,1,0,0,0]))
    def test_game2(self):
        game = Game(self.B,self.pokemon_name_B_my,self.pokemon_name_B_op)
        game.play()
        result = game.get_result()
        
        self.assertEqual(result["evaluation"], 3)
        np.testing.assert_array_equal(result["selection"], np.array([1,0,0,1,0,1]))
    def test_print_result(self):
        game = Game(self.B,self.pokemon_name_B_my,self.pokemon_name_B_op)
        game.play()
        game.print_result()

if __name__ == "__main__":
    unittest.main()

