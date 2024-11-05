import pytest
import numpy as np
from selection import Game

@pytest.fixture
def game_data_A():
    A = np.array([
        [ 0, -1,  1,  1,  1,  1],  #a
        [ 1,  0, -1,  1,  1,  1],  #b
        [-1,  1,  0,  1,  1,  1],  #c
        [ -1,  -1,  -1,  0,  0,  0],  #d
        [ -1,  -1,  -1,  0,  0,  0],  #e
        [ -1,  -1,  -1,  0,  0,  0]   #f
    ])
    pokemon_name_my = ["グー","チョキ","パー","モブ1","モブ2","モブ3"]
    pokemon_name_op = ["グー","チョキ","パー","モブ1","モブ2","モブ3"]
    return A, pokemon_name_my, pokemon_name_op

@pytest.fixture
def game_data_B():
    B = np.array([
        [ 1,  1,  0,  0,  0,  0],  #12
        [ 1,  0,  1,  0,  0,  0],  #13
        [ 0,  1,  1,  0,  0,  0],  #23
        [ 0,  0,  1,  1,  0,  0],  #34
        [ 0,  0,  0,  1,  1,  0],  #45
        [ 0,  0,  0,  0,  1,  1]   #56
    ])
    pokemon_name_my = ["12","13","23","34","45","56"]
    pokemon_name_op = ["かませ1","かませ2","かませ3","あくま4","あくま5","あくま6"]
    return B, pokemon_name_my, pokemon_name_op

def test_game(game_data_A):
    A, pokemon_name_my, pokemon_name_op = game_data_A
    game = Game(A, pokemon_name_my, pokemon_name_op)
    game.play()
    result = game.get_result()
    
    assert result["evaluation"] == 0
    np.testing.assert_array_equal(result["selection"], np.array([1,1,1,0,0,0]))

def test_game_required_selection(game_data_A):
    A, pokemon_name_my, pokemon_name_op = game_data_A
    game = Game(A, pokemon_name_my, pokemon_name_op)
    game.play(op_required_index=0)
    result = game.get_result()
    
    assert result["evaluation"] == 0
    np.testing.assert_array_almost_equal(result["selection"], np.array([1,1,1,0,0,0]), decimal=3)

def test_game_required_selection2(game_data_A):
    A, pokemon_name_my, pokemon_name_op = game_data_A
    game = Game(A, pokemon_name_my, pokemon_name_op)
    game.play(my_required_index=3,op_required_index=4)
    result = game.get_result()
    
    assert result["evaluation"] == 0
    np.testing.assert_array_almost_equal(result["selection"], np.array([2/3,2/3,2/3,1,0,0]), decimal=3)

def test_game2(game_data_B):
    B, pokemon_name_my, pokemon_name_op = game_data_B
    game = Game(B, pokemon_name_my, pokemon_name_op)
    game.play()
    result = game.get_result()
    
    assert result["evaluation"] == 3
    np.testing.assert_array_equal(result["selection"], np.array([1,0,0,1,0,1]))

def test_print_result(game_data_B):
    B, pokemon_name_my, pokemon_name_op = game_data_B
    game = Game(B, pokemon_name_my, pokemon_name_op)
    game.play()
    game.print_result()

