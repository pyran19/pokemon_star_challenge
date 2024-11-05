import pytest
import pandas as pd
import numpy as np
import os
from pool import Pool

@pytest.fixture
def mock_pool():
    pool = Pool()
    pool.pokemons = pd.DataFrame({
        "name": ["プクリン", "コノヨザル", "ドドゲザン"],
        "type": [["ノーマル", "フェアリー"], ["ゴースト", "かくとう"], ["はがね", "あく"]]
    })
    return pool
@pytest.fixture
def mock_pokemon_effectiveness():
    pool = Pool()
    effectiveness_map = {
        ("プクリン", "プクリン"): 1,
        ("プクリン", "コノヨザル"): 2,
        ("プクリン", "ドドゲザン"): 1,
        ("コノヨザル", "プクリン"): 1,
        ("コノヨザル", "コノヨザル"): 2,
        ("コノヨザル", "ドドゲザン"): 4,
        ("ドドゲザン", "プクリン"): 2,
        ("ドドゲザン", "コノヨザル"): 1,
        ("ドドゲザン", "ドドゲザン"): 0.5
    }
    
    def mock_calc_effectiveness(attacker, defender,theta):
        return effectiveness_map.get((attacker, defender))
    
    pool.calc_pokemon_effectiveness = mock_calc_effectiveness
    return pool


@pytest.fixture
def mock_relation():
    pool = Pool()
    pool.relation = np.array([[0,1,-1],[-1,0,2],[1,-2,0]])
    return pool

def test_read_csv():
    pool=Pool()
    pool.read_csv("input/pool.csv")
    pokemons = pool.get_pokemons()
    assert pokemons.shape[0] == 25
    assert pokemons.iloc[0]["name"] == "プクリン"
    assert set(pokemons.iloc[0]["type"]) == set(["ノーマル", "フェアリー"])
    assert pokemons.iloc[23]["name"] == "コノヨザル"
    assert set(pokemons.iloc[23]["type"]) == set(["ゴースト", "かくとう"])
    assert pokemons.iloc[24]["name"] == "ドドゲザン"
    assert set(pokemons.iloc[24]["type"]) == set(["はがね", "あく"])

def test_calc_type_effectiveness(mock_pool):
    # 計算方法を選択 通る方のタイプのみで計算する方式をモック
    theta=0.0 # 通る方のタイプのみで計算

    assert mock_pool.calc_type_effectiveness(["ノーマル", "フェアリー"], ["ノーマル", "フェアリー"],theta) == 1
    assert mock_pool.calc_type_effectiveness(["ノーマル", "フェアリー"], ["ゴースト", "かくとう"],theta) == 2
    assert mock_pool.calc_type_effectiveness(["ノーマル", "フェアリー"], ["はがね", "あく"],theta) == 1
    assert mock_pool.calc_type_effectiveness(["ゴースト", "かくとう"], ["ノーマル", "フェアリー"],theta) == 1
    assert mock_pool.calc_type_effectiveness(["ゴースト", "かくとう"], ["ゴースト", "かくとう"],theta) == 2
    assert mock_pool.calc_type_effectiveness(["ゴースト", "かくとう"], ["はがね", "あく"],theta) == 4
    assert mock_pool.calc_type_effectiveness(["はがね", "あく"], ["ノーマル", "フェアリー"],theta) == 2
    assert mock_pool.calc_type_effectiveness(["はがね", "あく"], ["ゴースト", "かくとう"],theta=0.) == 1 # キーワード引数での代入をテスト
    assert mock_pool.calc_type_effectiveness(["はがね", "あく"], ["はがね", "あく"]) == 0.5          # 引数省略での代入をテスト
    assert mock_pool.calc_type_effectiveness(["はがね", "あく"], ["でんき",""]) == 1
    assert mock_pool.calc_type_effectiveness(["でんき",""], ["でんき",""]) == 0.5          # 引数省略での代入をテスト
    assert mock_pool.calc_type_effectiveness(["でんき",""], ["どく","ひこう"]) == 2 
    assert mock_pool.calc_type_effectiveness(["みず",""], ["でんき","ほのお"]) == 2

def test_calc_type_effectiveness_cycle(mock_pool):
    theta=0.1 # サイクルパラメータが有限値を取る場合

    assert mock_pool.calc_type_effectiveness(["ノーマル", "フェアリー"], ["ノーマル", "フェアリー"],theta) == pytest.approx(1)
    assert mock_pool.calc_type_effectiveness(["ノーマル", "フェアリー"], ["ゴースト", "かくとう"],theta) == pytest.approx(1.8+1/30)
    assert mock_pool.calc_type_effectiveness(["ノーマル", "フェアリー"], ["はがね", "あく"],theta) == pytest.approx(0.95)
    assert mock_pool.calc_type_effectiveness(["ゴースト", "かくとう"], ["ノーマル", "フェアリー"],theta) == pytest.approx(0.9+1/30) 
    assert mock_pool.calc_type_effectiveness(["ゴースト", "かくとう"], ["ゴースト", "かくとう"],theta) == pytest.approx(1.8+1/30)
    assert mock_pool.calc_type_effectiveness(["ゴースト", "かくとう"], ["はがね", "あく"],theta) == pytest.approx(3.65)
    assert mock_pool.calc_type_effectiveness(["はがね", "あく"], ["ノーマル", "フェアリー"],theta) == pytest.approx(1.85)
    assert mock_pool.calc_type_effectiveness(["はがね", "あく"], ["ゴースト", "かくとう"],theta=theta) == pytest.approx(1) # キーワード引数での代入をテスト
    assert mock_pool.calc_type_effectiveness(["はがね", "あく"], ["はがね", "あく"],theta=theta) == pytest.approx(0.5)          # キーワード引数省略での代入をテスト

def test_calc_pokemon_effectiveness(mock_pool):
    assert mock_pool.calc_pokemon_effectiveness("プクリン", "プクリン") == mock_pool.calc_type_effectiveness(["ノーマル", "フェアリー"], ["ノーマル", "フェアリー"]) 
    assert mock_pool.calc_pokemon_effectiveness("プクリン", "コノヨザル") == mock_pool.calc_type_effectiveness(["ノーマル", "フェアリー"], ["ゴースト", "かくとう"])
    assert mock_pool.calc_pokemon_effectiveness("プクリン", "ドドゲザン") == mock_pool.calc_type_effectiveness(["ノーマル", "フェアリー"], ["はがね", "あく"])
    assert mock_pool.calc_pokemon_effectiveness("コノヨザル", "プクリン") == mock_pool.calc_type_effectiveness(["ゴースト", "かくとう"], ["ノーマル", "フェアリー"])
    assert mock_pool.calc_pokemon_effectiveness("コノヨザル", "コノヨザル") == mock_pool.calc_type_effectiveness(["ゴースト", "かくとう"], ["ゴースト", "かくとう"])
    assert mock_pool.calc_pokemon_effectiveness("コノヨザル", "ドドゲザン") == mock_pool.calc_type_effectiveness(["ゴースト", "かくとう"], ["はがね", "あく"])
    assert mock_pool.calc_pokemon_effectiveness("ドドゲザン", "プクリン") == mock_pool.calc_type_effectiveness(["はがね", "あく"], ["ノーマル", "フェアリー"])
    assert mock_pool.calc_pokemon_effectiveness("ドドゲザン", "コノヨザル") == mock_pool.calc_type_effectiveness(["はがね", "あく"], ["ゴースト", "かくとう"])
    assert mock_pool.calc_pokemon_effectiveness("ドドゲザン", "ドドゲザン") == mock_pool.calc_type_effectiveness(["はがね", "あく"], ["はがね", "あく"])

def test_mutchup_by_type(mock_pokemon_effectiveness):
    pool = mock_pokemon_effectiveness
    
    assert pool.mutchup_by_type("プクリン", "プクリン") == 0
    assert pool.mutchup_by_type("プクリン", "コノヨザル") == 1
    assert pool.mutchup_by_type("プクリン", "ドドゲザン") == -1
    assert pool.mutchup_by_type("コノヨザル", "プクリン") == -1
    assert pool.mutchup_by_type("コノヨザル", "コノヨザル") == 0
    assert pool.mutchup_by_type("コノヨザル", "ドドゲザン") == 2
    assert pool.mutchup_by_type("ドドゲザン", "プクリン") == 1
    assert pool.mutchup_by_type("ドドゲザン", "コノヨザル") == -2
    assert pool.mutchup_by_type("ドドゲザン", "ドドゲザン") == 0

def test_make_relation_by_type(mock_pool):
    n = mock_pool.pokemons.shape[0]
    relation = mock_pool.make_relation_by_type()
    
    assert relation.shape[0] == n
    assert relation.shape[1] == n
    expected_matrix = np.array([[0,1,-1],[-1,0,2],[1,-2,0]])
    assert np.array_equal(relation, expected_matrix)


def test_save_relation(mock_relation):
    mock_pool = mock_relation
    mock_pool.save_relation("output/relation.csv")
    assert os.path.exists("output/relation.csv")

