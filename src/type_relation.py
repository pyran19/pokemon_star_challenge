from enum import Enum
from typing import Dict, Optional
import numpy as np

class Effectiveness(Enum):
    """技の効果を表す列挙型"""
    SUPER_EFFECTIVE = "○"      # 効果抜群
    NOT_VERY_EFFECTIVE = "△"  # 効果今ひとつ
    NO_EFFECT = "×"           # 効果なし
    NORMAL = None             # 通常

class TypeRelations:
    """タイプ関係を管理するクラス"""
    def __init__(self):
        # 全タイプのリスト
        self.types = [
            "ノーマル", "ほのお", "みず", "でんき", "くさ", "こおり",
            "かくとう", "どく", "じめん", "ひこう", "エスパー", "むし",
            "いわ", "ゴースト", "ドラゴン", "あく", "はがね", "フェアリー"
        ]
        
        # タイプ相性を初期化
        self.relations: Dict[str, Dict[str, Optional[Effectiveness]]] = {
            attacker: {defender: Effectiveness.NORMAL for defender in self.types}
            for attacker in self.types
        }

        # タイプ相性データを設定
        self._initialize_relations()

    def _initialize_relations(self):
        """タイプ相性データを初期化"""
        
        # ノーマル
        self._set_relation("ノーマル", "いわ", Effectiveness.NOT_VERY_EFFECTIVE)
        self._set_relation("ノーマル", "ゴースト", Effectiveness.NO_EFFECT)
        self._set_relation("ノーマル", "はがね", Effectiveness.NOT_VERY_EFFECTIVE)

        # ほのお
        self._set_relation("ほのお", "ほのお", Effectiveness.NOT_VERY_EFFECTIVE)
        self._set_relation("ほのお", "みず", Effectiveness.NOT_VERY_EFFECTIVE)
        self._set_relation("ほのお", "くさ", Effectiveness.SUPER_EFFECTIVE)
        self._set_relation("ほのお", "こおり", Effectiveness.SUPER_EFFECTIVE)
        self._set_relation("ほのお", "むし", Effectiveness.SUPER_EFFECTIVE)
        self._set_relation("ほのお", "いわ", Effectiveness.NOT_VERY_EFFECTIVE)
        self._set_relation("ほのお", "ドラゴン", Effectiveness.NOT_VERY_EFFECTIVE)
        self._set_relation("ほのお", "はがね", Effectiveness.SUPER_EFFECTIVE)

        # みず
        self._set_relation("みず", "ほのお", Effectiveness.SUPER_EFFECTIVE)
        self._set_relation("みず", "みず", Effectiveness.NOT_VERY_EFFECTIVE)
        self._set_relation("みず", "くさ", Effectiveness.NOT_VERY_EFFECTIVE)
        self._set_relation("みず", "じめん", Effectiveness.SUPER_EFFECTIVE)
        self._set_relation("みず", "いわ", Effectiveness.SUPER_EFFECTIVE)
        self._set_relation("みず", "ドラゴン", Effectiveness.NOT_VERY_EFFECTIVE)

        # でんき
        self._set_relation("でんき", "みず", Effectiveness.SUPER_EFFECTIVE)
        self._set_relation("でんき", "でんき", Effectiveness.NOT_VERY_EFFECTIVE)
        self._set_relation("でんき", "くさ", Effectiveness.NOT_VERY_EFFECTIVE)
        self._set_relation("でんき", "じめん", Effectiveness.NO_EFFECT)
        self._set_relation("でんき", "ひこう", Effectiveness.SUPER_EFFECTIVE)
        self._set_relation("でんき", "ドラゴン", Effectiveness.NOT_VERY_EFFECTIVE)

        # くさ
        self._set_relation("くさ", "ほのお", Effectiveness.NOT_VERY_EFFECTIVE)
        self._set_relation("くさ", "みず", Effectiveness.SUPER_EFFECTIVE)
        self._set_relation("くさ", "くさ", Effectiveness.NOT_VERY_EFFECTIVE)
        self._set_relation("くさ", "じめん", Effectiveness.SUPER_EFFECTIVE)
        self._set_relation("くさ", "ひこう", Effectiveness.NOT_VERY_EFFECTIVE)
        self._set_relation("くさ", "むし", Effectiveness.NOT_VERY_EFFECTIVE)
        self._set_relation("くさ", "ドラゴン", Effectiveness.NOT_VERY_EFFECTIVE)
        self._set_relation("くさ", "はがね", Effectiveness.NOT_VERY_EFFECTIVE)

        # こおり
        self._set_relation("こおり", "みず", Effectiveness.NOT_VERY_EFFECTIVE)
        self._set_relation("こおり", "くさ", Effectiveness.SUPER_EFFECTIVE)
        self._set_relation("こおり", "こおり", Effectiveness.NOT_VERY_EFFECTIVE)
        self._set_relation("こおり", "ひこう", Effectiveness.SUPER_EFFECTIVE)
        self._set_relation("こおり", "じめん", Effectiveness.SUPER_EFFECTIVE)
        self._set_relation("こおり", "ドラゴン", Effectiveness.SUPER_EFFECTIVE)
        self._set_relation("こおり", "はがね", Effectiveness.NOT_VERY_EFFECTIVE)

        # かくとう
        self._set_relation("かくとう", "ノーマル", Effectiveness.SUPER_EFFECTIVE)
        self._set_relation("かくとう", "こおり", Effectiveness.SUPER_EFFECTIVE)
        self._set_relation("かくとう", "どく", Effectiveness.NOT_VERY_EFFECTIVE)
        self._set_relation("かくとう", "ひこう", Effectiveness.NOT_VERY_EFFECTIVE)
        self._set_relation("かくとう", "エスパー", Effectiveness.NOT_VERY_EFFECTIVE)
        self._set_relation("かくとう", "むし", Effectiveness.NOT_VERY_EFFECTIVE)
        self._set_relation("かくとう", "いわ", Effectiveness.SUPER_EFFECTIVE)
        self._set_relation("かくとう", "ゴースト", Effectiveness.NO_EFFECT)
        self._set_relation("かくとう", "はがね", Effectiveness.SUPER_EFFECTIVE)
        self._set_relation("かくとう", "フェアリー", Effectiveness.NOT_VERY_EFFECTIVE)

        # どく
        self._set_relation("どく", "くさ", Effectiveness.SUPER_EFFECTIVE)
        self._set_relation("どく", "どく", Effectiveness.NOT_VERY_EFFECTIVE)
        self._set_relation("どく", "じめん", Effectiveness.NOT_VERY_EFFECTIVE)
        self._set_relation("どく", "いわ", Effectiveness.NOT_VERY_EFFECTIVE)
        self._set_relation("どく", "ゴースト", Effectiveness.NOT_VERY_EFFECTIVE)
        self._set_relation("どく", "はがね", Effectiveness.NO_EFFECT)
        self._set_relation("どく", "フェアリー", Effectiveness.SUPER_EFFECTIVE)

        # じめん
        self._set_relation("じめん", "ほのお", Effectiveness.SUPER_EFFECTIVE)
        self._set_relation("じめん", "でんき", Effectiveness.SUPER_EFFECTIVE)
        self._set_relation("じめん", "くさ", Effectiveness.NOT_VERY_EFFECTIVE)
        self._set_relation("じめん", "どく", Effectiveness.SUPER_EFFECTIVE)
        self._set_relation("じめん", "ひこう", Effectiveness.NO_EFFECT)
        self._set_relation("じめん", "むし", Effectiveness.NOT_VERY_EFFECTIVE)
        self._set_relation("じめん", "いわ", Effectiveness.SUPER_EFFECTIVE)
        self._set_relation("じめん", "はがね", Effectiveness.SUPER_EFFECTIVE)

        # ひこう
        self._set_relation("ひこう", "でんき", Effectiveness.NOT_VERY_EFFECTIVE)
        self._set_relation("ひこう", "くさ", Effectiveness.SUPER_EFFECTIVE)
        self._set_relation("ひこう", "かくとう", Effectiveness.SUPER_EFFECTIVE)
        self._set_relation("ひこう", "むし", Effectiveness.SUPER_EFFECTIVE)
        self._set_relation("ひこう", "いわ", Effectiveness.NOT_VERY_EFFECTIVE)
        self._set_relation("ひこう", "はがね", Effectiveness.NOT_VERY_EFFECTIVE)

        # エスパー
        self._set_relation("エスパー", "かくとう", Effectiveness.SUPER_EFFECTIVE)
        self._set_relation("エスパー", "どく", Effectiveness.SUPER_EFFECTIVE)
        self._set_relation("エスパー", "エスパー", Effectiveness.NOT_VERY_EFFECTIVE)
        self._set_relation("エスパー", "はがね", Effectiveness.NO_EFFECT)
        self._set_relation("エスパー", "あく", Effectiveness.NOT_VERY_EFFECTIVE)

        # むし
        self._set_relation("むし", "ほのお", Effectiveness.NOT_VERY_EFFECTIVE)
        self._set_relation("むし", "くさ", Effectiveness.SUPER_EFFECTIVE)
        self._set_relation("むし", "かくとう", Effectiveness.NOT_VERY_EFFECTIVE)
        self._set_relation("むし", "どく", Effectiveness.NOT_VERY_EFFECTIVE)
        self._set_relation("むし", "ひこう", Effectiveness.NOT_VERY_EFFECTIVE)
        self._set_relation("むし", "エスパー", Effectiveness.SUPER_EFFECTIVE)
        self._set_relation("むし", "ゴースト", Effectiveness.NOT_VERY_EFFECTIVE)
        self._set_relation("むし", "あく", Effectiveness.SUPER_EFFECTIVE)
        self._set_relation("むし", "はがね", Effectiveness.NOT_VERY_EFFECTIVE)
        self._set_relation("むし", "フェアリー", Effectiveness.NOT_VERY_EFFECTIVE)

        # いわ
        self._set_relation("いわ", "ほのお", Effectiveness.SUPER_EFFECTIVE)
        self._set_relation("いわ", "こおり", Effectiveness.SUPER_EFFECTIVE)
        self._set_relation("いわ", "かくとう", Effectiveness.NOT_VERY_EFFECTIVE)
        self._set_relation("いわ", "じめん", Effectiveness.NOT_VERY_EFFECTIVE)
        self._set_relation("いわ", "ひこう", Effectiveness.SUPER_EFFECTIVE)
        self._set_relation("いわ", "むし", Effectiveness.SUPER_EFFECTIVE)
        self._set_relation("いわ", "はがね", Effectiveness.NOT_VERY_EFFECTIVE)

        # ゴースト
        self._set_relation("ゴースト", "ノーマル", Effectiveness.NO_EFFECT)
        self._set_relation("ゴースト", "エスパー", Effectiveness.SUPER_EFFECTIVE)
        self._set_relation("ゴースト", "ゴースト", Effectiveness.SUPER_EFFECTIVE)
        self._set_relation("ゴースト", "あく", Effectiveness.NOT_VERY_EFFECTIVE)

        # ドラゴン
        self._set_relation("ドラゴン", "ドラゴン", Effectiveness.SUPER_EFFECTIVE)
        self._set_relation("ドラゴン", "はがね", Effectiveness.NOT_VERY_EFFECTIVE)
        self._set_relation("ドラゴン", "フェアリー", Effectiveness.NO_EFFECT)

        # あく
        self._set_relation("あく", "かくとう", Effectiveness.NOT_VERY_EFFECTIVE)
        self._set_relation("あく", "エスパー", Effectiveness.SUPER_EFFECTIVE)
        self._set_relation("あく", "ゴースト", Effectiveness.SUPER_EFFECTIVE)
        self._set_relation("あく", "あく", Effectiveness.NOT_VERY_EFFECTIVE)
        self._set_relation("あく", "フェアリー", Effectiveness.NOT_VERY_EFFECTIVE)

        # はがね
        self._set_relation("はがね", "ノーマル", Effectiveness.NOT_VERY_EFFECTIVE)
        self._set_relation("はがね", "ほのお", Effectiveness.NOT_VERY_EFFECTIVE)
        self._set_relation("はがね", "くさ", Effectiveness.SUPER_EFFECTIVE)
        self._set_relation("はがね", "こおり", Effectiveness.SUPER_EFFECTIVE)
        self._set_relation("はがね", "いわ", Effectiveness.SUPER_EFFECTIVE)
        self._set_relation("はがね", "はがね", Effectiveness.NOT_VERY_EFFECTIVE)
        self._set_relation("はがね", "フェアリー", Effectiveness.SUPER_EFFECTIVE)

        # フェアリー
        self._set_relation("フェアリー", "かくとう", Effectiveness.SUPER_EFFECTIVE)
        self._set_relation("フェアリー", "どく", Effectiveness.NOT_VERY_EFFECTIVE)
        self._set_relation("フェアリー", "ドラゴン", Effectiveness.SUPER_EFFECTIVE)
        self._set_relation("フェアリー", "あく", Effectiveness.SUPER_EFFECTIVE)
        self._set_relation("フェアリー", "はがね", Effectiveness.NOT_VERY_EFFECTIVE)
    def _set_relation(self, attacker: str, defender: str, effectiveness: Effectiveness):
        """タイプ相性を設定するヘルパーメソッド"""
        self.relations[attacker][defender] = effectiveness

    def get_effectiveness(self, attacker: str, defender: str) -> Effectiveness:
        """攻撃タイプと防御タイプの相性を取得"""
        if attacker not in self.types or defender not in self.types:
            raise ValueError("Invalid type specified")
        return self.relations[attacker][defender]

    def print_effectiveness(self, attacker: str, defender: str):
        """タイプ相性を表示"""
        effectiveness = self.get_effectiveness(attacker, defender)
        if effectiveness == Effectiveness.SUPER_EFFECTIVE:
            print(f"{attacker}は{defender}に対して効果抜群です")
        elif effectiveness == Effectiveness.NOT_VERY_EFFECTIVE:
            print(f"{attacker}は{defender}に対して効果今ひとつです")
        elif effectiveness == Effectiveness.NO_EFFECT:
            print(f"{attacker}は{defender}に対して効果がありません")
        else:
            print(f"{attacker}は{defender}に対して通常の効果です")
    def get_relation_matrix(self,super_effective:float,not_very_effective:float,no_effect:float,normal:float=1.):
        """相性を数値で置換して行列の形にする"""
        self.matrix = np.full((len(self.types), len(self.types)), normal)
        for i, attacker in enumerate(self.types):
            for j, defender in enumerate(self.types):
                effectiveness = self.get_effectiveness(attacker, defender)
                if effectiveness == Effectiveness.SUPER_EFFECTIVE:
                    self.matrix[i, j] = super_effective
                elif effectiveness == Effectiveness.NOT_VERY_EFFECTIVE:
                    self.matrix[i, j] = not_very_effective
                elif effectiveness == Effectiveness.NO_EFFECT:
                    self.matrix[i, j] = no_effect
                else:
                    self.matrix[i, j] = normal

        return self.matrix

# 使用例
def main():
    type_relations = TypeRelations()

    # タイプ相性の例を表示
    test_cases = [
        ("ゴースト", "ノーマル"),
        ("ほのお", "くさ"),
        ("みず", "ほのお")
    ]
    
    for attacker, defender in test_cases:
        type_relations.print_effectiveness(attacker, defender)

    # タイプ相性行列を表示
    print(type_relations.get_relation_matrix(2,0.5,0,1))

if __name__ == "__main__":
    main()