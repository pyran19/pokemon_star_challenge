import pulp
import numpy as np

#線形計画法
class Game:
    def __init__(self,A,my_pokemon,opponent_pokemon):
        self.A=A
        self.my_pokemon=my_pokemon
        self.opponent_pokemon=opponent_pokemon
        self.nPT=6
    def play(self):
        lp = pulp.LpProblem(sense=pulp.LpMaximize)
        v = pulp.LpVariable("v") 
        x = [ pulp.LpVariable("x_"+str(i)) for i in range(self.nPT) ]
        for i in range(self.nPT):
            for j in range(i+1,self.nPT):
                for k in range(j+1,self.nPT):
                    lp += v <= pulp.lpDot(self.A[:,i], x)+pulp.lpDot(self.A[:,j], x)+pulp.lpDot(self.A[:,k], x)
        for i in range(self.nPT):
            lp += x[i] >= 0
            lp += x[i] <= 1
        lp += pulp.lpSum(x) == 3
        lp += v
        lp.solve(pulp.PULP_CBC_CMD(msg=False))
        self.x = np.array([ x[i].value() for i in range(self.nPT) ])
        self.v = v.value()
    def get_result(self):
        self.result={}
        self.result["evaluation"]=self.v
        self.result["selection"]=self.x
        return self.result
    def print_result(self):
        print("選出率")
        for i in range(self.nPT):
            print(self.my_pokemon[i]+"の選出率: ",100*self.x[i],"%")
        print("構築評価: ",self.v)
