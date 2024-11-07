import pytest
import numpy as np
from app import make_relation,play_game

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
    return A

# パラメータを受け取ってポケモン間の関係を表す行列を作成する
def test_make_relation():
    data={"theta":0.0}
    result=make_relation(data)
    assert result["status"]=="成功"
    assert len(result["pokemon"])==25
    pokemon=["プクリン","オコリザル","ウインディ","ベトベトン","マリルリ","ヘルガー","コータス","ノクタス","ドンカラス","スカタンク","ルカリオ","ドクロッグ","ワルビアル","ドラミドロ","クレッフィ","ドヒドイデ","ナゲツケザル","セキタンザン","ブリムオン","バウッチェル","グレンアルマ","マフィティフ","ブロロローム","コノヨザル","ドドゲザン"]
    assert result["pokemon"]==pokemon
    assert isinstance(result["relation"], list)
    assert len(result["relation"])==25
    assert len(result["relation"][0])==25
    for i in range(25):
        assert result["relation"][i][i]==0
        for j in range(i+1,25):
            assert result["relation"][i][j]==-result["relation"][j][i]
    assert result["relation"][0][1]==1
    assert result["relation"][0][2]==0
    assert result["relation"][1][3]==-1


# 任意の6×6行列を受け取ってゲームを実行する
def test_play_game(game_data_A):
    data={"relation":game_data_A}
    result=play_game(data)
    assert result["status"]=="成功"
    assert result["evaluation"]==0
    assert result["selection"]==[1.,1.,1.,0.,0.,0.]
