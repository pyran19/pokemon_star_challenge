import pandas as pd
import numpy as np
import math
from type_relation import type_relations
from typing import List, Optional

class Pool:
    def __init__(self):
        self.pokemons = pd.DataFrame()
    
    def read_csv(self, path: str) -> pd.DataFrame:
        df = pd.read_csv(path)
        df.fillna("",inplace=True)
        self.pokemons["name"] = df["ポケモン"]
        type_list = [i for i in zip(df["タイプ1"],df["タイプ2"])]
        self.pokemons["type"] = pd.Series(type_list)

    def calc_type_effectiveness(self, attacker_types: List[Optional[str]], defender_types: List[Optional[str]], theta: float = 0.0) -> float:
        effectiveness_list = [1/3]
        for attacker_type in attacker_types:
            if attacker_type == "":
                effectiveness_list.append(1/3)
                continue
            effectiveness = 1
            for defender_type in defender_types:
                if defender_type == "":
                    continue
                effectiveness *= type_relations.get_effectiveness_value(attacker_type, defender_type)
            effectiveness_list.append(effectiveness)
        
        effectiveness_list = sorted(effectiveness_list,reverse=True)
        total_effectiveness = (1-theta)*effectiveness_list[0] + theta*effectiveness_list[1]

        return total_effectiveness

    def calc_pokemon_effectiveness(self, attacker: str, defender: str,theta: float = 0.0) -> float:
        attacker_types = self.pokemons[self.pokemons["name"] == attacker]["type"].values[0]
        defender_types = self.pokemons[self.pokemons["name"] == defender]["type"].values[0]
        pokemon_effectiveness = self.calc_type_effectiveness(attacker_types, defender_types,theta)
        return pokemon_effectiveness

    def get_pokemons(self) -> pd.DataFrame:
        return self.pokemons


    def mutchup_by_type(self, pokemon1: str, pokemon2: str,theta: float = 0.0) -> float:
        e12=self.calc_pokemon_effectiveness(pokemon1, pokemon2,theta)
        e21=self.calc_pokemon_effectiveness(pokemon2, pokemon1,theta)
        return math.log(e12/e21,2)

    def make_relation_by_type(self,theta: float = 0.0) -> np.ndarray:
        self.relation = np.zeros((self.pokemons.shape[0],self.pokemons.shape[0]))
        n = self.pokemons.shape[0]
        for i in range(n):
            for j in range(i,n):
                self.relation[i,j] = self.mutchup_by_type(
                    self.pokemons.iloc[i]["name"],
                    self.pokemons.iloc[j]["name"],
                    theta=theta
                    )
                self.relation[j,i] = -self.relation[i,j]
        return self.relation
    
    def save_relation(self,path: str):
        np.savetxt(path,self.relation,delimiter=",")
    
    def load_relation(self,path: str):
        self.relation = np.loadtxt(path,delimiter=",")
        
    def extract_team_by_index(self,my_team_index: List[int],op_team_index: List[int]) -> np.ndarray:
        extracted_relation = self.relation[my_team_index, :][:, op_team_index]
        return extracted_relation
    
    def extract_team_by_name(self,my_team: List[str],op_team: List[str]) -> np.ndarray:
        my_team_index = [self.pokemons[self.pokemons["name"] == pokemon].index.values[0] for pokemon in my_team]
        op_team_index = [self.pokemons[self.pokemons["name"] == pokemon].index.values[0] for pokemon in op_team]
        extracted_relation = self.extract_team_by_index(my_team_index,op_team_index)
        return extracted_relation


if __name__ == "__main__":
    pool = Pool()
    pool.read_csv("input/pool.csv")
    pool.make_relation_by_type(theta=0.3)
    pool.save_relation("output/relation.csv")

