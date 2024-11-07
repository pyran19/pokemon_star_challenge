from flask import Flask, request, jsonify
from pool import Pool
from selection import Game
from timeout_decorator import timeout, TimeoutError
import numpy as np



app = Flask(__name__)

#バリデーション関数
def validate_relation(relation):
    if len(relation) != 6:
        return False
    for i in range(len(relation)):
        if len(relation[i]) != len(relation):
            return False
    for i in range(len(relation)):
        for j in range(len(relation)):
            try:
                float(relation[i][j])
            except ValueError:
                return False
    return True

def make_relation(data):
    theta=data["theta"]
    pool = Pool()
    pool.read_csv("input/pool.csv")
    pool.make_relation_by_type(theta=theta)
    pokemon=pool.pokemons["name"].tolist()
    relation=pool.relation.tolist()
    outputdata={"status":"成功","relation":relation,"pokemon":pokemon}
    return outputdata

def play_game(data):
    A = np.array([[float(element) for element in row] for row in data["relation"]])
    my_team=[]# ダミー（引数に設定したけど計算に不要だった）
    op_team=[]# ダミー（引数に設定したけど計算に不要だった）
    game = Game(A,my_team,op_team)
    game.play(my_required_index=0,op_required_index=0)
    result=game.get_result()
    outputdata={"status":"成功","evaluation":result["evaluation"],"selection":result["selection"].tolist()}
    return outputdata

@app.route('/make_relation', methods=['GET'])
def relation_api():
    try:
        theta = request.args.get('theta')  # URLパラメータからthetaを取得
        data = {"theta": float(theta)}  # thetaをデータに変換
    except:
        return jsonify({"status": "失敗", "error": "パラメータが正しくありません"}), 400  # 400エラーを返す
    try:
        result = make_relation_with_timeout(data)  # タイムアウト付きのプログラムの実行
    except TimeoutError:
        return jsonify({"status": "失敗", "error": "タイムアウトしました"}), 504  # タイムアウトエラーを返す
    return jsonify(result)  # JSONで結果を返す


@app.route('/play_game', methods=['POST'])
def game_api():
    data = request.json  # POSTデータを受け取る
    if not validate_relation(data["relation"]):
        return jsonify({"status": "失敗", "error": "入力された行列が正しくありません"}), 400  # 400エラーを返す
    try:
        data["relation"]=np.array(data["relation"])
        result = play_game_with_timeout(data)  # タイムアウト付きのプログラムの実行
    except TimeoutError:
        return jsonify({"status": "失敗", "error": "タイムアウトしました"}), 504  # タイムアウトエラーを返す
    return jsonify(result)  # JSONで結果を返す



@timeout(5)  # 5秒のタイムアウトを設定
def make_relation_with_timeout(data):
    return make_relation(data)
@timeout(30)  # 30秒のタイムアウトを設定
def play_game_with_timeout(data):
    return play_game(data)


if __name__ == '__main__':
    app.run(debug=True)
