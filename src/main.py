import numpy as np
from selection import Game
from pool import Pool

def get_pool():
    pool = Pool()
    pool.read_csv("input/pool.csv")
    pool.load_relation("input/relation_0_3.csv")
    return pool

def main(my_team,op_team):
    pool = get_pool()

    A = pool.extract_team_by_name(my_team,op_team)
    
    game = Game(A,my_team,op_team)
    game.play(my_required_index=0,op_required_index=0)
    result = game.get_result()
    game.print_result()

if __name__ == "__main__":
    my_team = ["ブロロローム","プクリン","オコリザル","ウインディ","コノヨザル","ワルビアル"]
    op_team = ["ブロロローム","プクリン","マリルリ","ウインディ","コノヨザル","ワルビアル"]
    main(my_team,op_team)

