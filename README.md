# pokemon_star_challenge
スター団チャレンジにおいて強い構築の探索を行う

## 概要
公式大会スター団チャレンジでは25匹という極端に少ないポケモンのプールから構築の作成を行う。

これだけ少ないとポケモン間の相性を書きだすことが現実的なため、どのポケモンがどのポケモンに対してどの程度有利かを仮定し、その過程に基づいて構築同士の相性比較を行う。

構築同士の比較には6匹構築から3匹を選出するゲームのミニマックス計算をおこなう。

## ディレクトリ構造
```
.
├── README.md
├── src/
│   ├── pokemon.py
│   ├── selection.py
│   ├── type_relation.py
│   └── pool.py
├── input/
│   ├── pool.csv
│   └── relation.csv
├── output/
│   └── relation.csv
├── doc/
│   └── requirement.txt
└── tests/
    ├── selection_test.py
    ├── pokemon_test.py
    ├── conftest.py
    └── prepare_test.py
```

## セットアップ
```bash
pip install -r doc/requirements.txt
```

## 使用方法

### 1. ポケモン間の相性を計算する
pool.pyのthetaパラメータを調整することで、相性計算における二つ目のタイプの考慮度を変更できます。
- theta = 0: タイプ一致技の中で効果抜群な技のみを使用
- theta > 0: 効果抜群でない技も考慮して計算

```bash
python src/pool.py
```

### 2. CSVファイルの手動調整
タイプ相性だけでなく、実際の対戦を考慮して主要なポケモン間の関係を調整します：
1. output/relation.csvを確認
2. 必要な調整を加える
3. input/relation.csvとして保存

### 3. 構築同士の相性計算
main.pyで以下の設定が可能です：
- my_team, op_team: 自分と相手の構築を指定
- CSVファイルの選択: プログラム上部でファイルパスを指定

```bash
python src/main.py
```

### クイックスタート
計算済みファイルが用意されているため、main.pyで構築を指定するだけですぐに実行できます：
```bash
python src/main.py
```
