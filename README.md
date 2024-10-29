# pokemon_star_challenge
スター団チャレンジにおいて強い構築の探索を行う

## 概要
公式大会スター団チャレンジでは25匹という極端に少ないポケモンのプールから構築の作成を行う。
6匹構築から3匹を選出するゲームのゲーム理論を用いて構築同士の優劣を計算し、強い構築の探索・考察を行う

## ディレクトリ構造
```
.
├── README.md
├── src
│   ├── __init__.py
│   ├── pokemon.py
│   ├── selection.py
│   └── selection_test.py
├── input
│   └── pool.csv
│   └── relation.csv
├── output
│   └── result.csv
```

## 導入
```
pip install -r doc/requirements.txt
```

## 使用方法
```
python src/main.py
```


