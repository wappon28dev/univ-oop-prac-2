import random
from datetime import datetime

from flask import Flask, render_template, request

app = Flask(__name__)


# 1. プロジェクトのトップ（じゃんけんアプリや、課題のアプリへのリンクを配置するだけ）
@app.route("/")
def index():
    return render_template("index.html")


# 2. じゃんけんアプリの入力フォーム
@app.route("/janken")
def janken():
    # じゃんけんの入力画面のテンプレートを呼び出し
    return render_template("janken_form.html")


@app.route("/janken/play", methods=["POST"])
def janken_play() -> str:
    # <input type="text" id="your_name" name="name">
    name = request.form.get("name")
    if not name:
        name = "名無しさん"

    # <input type="radio" id="hand_rock" value="rock" name="hand">
    # <input type="radio" id="hand_scissor" value="scissor" name="hand">
    # <input type="radio" id="hand_paper" value="paper" name="hand">
    hand = request.form.get("hand", None)
    is_settai = request.form.get("is_settai")

    # リストの中からランダムに選ぶ
    cpu = random.choice(["rock", "scissor", "paper"])

    # 接待モードの場合、CPUは絶対に負ける
    if is_settai:
        if hand == "rock":
            cpu = "scissor"
        elif hand == "scissor":
            cpu = "paper"
        elif hand == "paper":
            cpu = "rock"

    # じゃんけん処理
    result_status = "draw"
    if hand == cpu:
        result_message = "あいこ"
        result_status = "draw"
    elif hand == "rock":
        if cpu == "scissor":
            result_message = f"{name}の勝ち"
            result_status = "win"
        else:
            result_message = f"{name}の負け"
            result_status = "lose"
    elif hand == "scissor":
        if cpu == "paper":
            result_message = f"{name}の勝ち"
            result_status = "win"
        else:
            result_message = f"{name}の負け"
            result_status = "lose"
    elif hand == "paper":
        if cpu == "rock":
            result_message = f"{name}の勝ち"
            result_status = "win"
        else:
            result_message = f"{name}の負け"
            result_status = "lose"
    else:
        result_message = "後出しはダメです。"
        result_status = "lose"

    # 渡したいデータを先に定義しておいてもいいし、テンプレートを先に作っておいても良い
    return render_template(
        "janken_play.html",
        result_message=result_message,
        result_status=result_status,
        name=name,
        hand=hand,
        cpu=cpu,
    )


# 3. 占いアプリの入力フォーム
@app.route("/uranai")
def uranai():
    return render_template("uranai_form.html")


@app.route("/uranai/play", methods=["POST"])
def uranai_play() -> str:
    name = request.form.get("name")
    birthday_str = request.form.get("birthday")

    # 入力チェック
    if not name or not birthday_str:
        return render_template(
            "uranai_result.html",
            result=1,
            message="入力不備で占えませんでした",
        )

    try:
        # 生年月日を日付オブジェクトに変換 (yyyy-mm-dd形式を想定)
        birthday = datetime.strptime(birthday_str, "%Y-%m-%d")
    except ValueError:
        return render_template(
            "uranai_result.html",
            result=1,
            message="入力不備で占えませんでした",
        )

    # 現在日付を数値化 (yyyyMMdd)
    now = datetime.now()
    now_int = int(now.strftime("%Y%m%d"))

    # 生年月日を数値化 (yyyyMMdd)
    birthday_int = int(birthday.strftime("%Y%m%d"))

    # 計算式
    # 1. 現在日付から生年月日を減算し、絶対値を算出
    diff = abs(now_int - birthday_int)

    # 2. 減算結果の絶対値と名前の文字数を掛け算
    calc_result = diff * len(name)

    # 3. 掛け算結果を5で割った余りを算出
    remainder = calc_result % 5

    # 4. List:[5, 1, 3, 2, 4]のインデックスとして使用
    result_list = [5, 1, 3, 2, 4]
    uranai_result = result_list[remainder]

    # メッセージの決定
    messages = {
        5: "最高の一日になりそうです！何をやってもうまくいきます。",
        4: "とても良い運勢です。新しいことに挑戦してみましょう。",
        3: "普通の運勢です。いつも通りの一日を過ごしましょう。",
        2: "少し注意が必要です。慎重に行動しましょう。",
        1: "今日はあまりついていないかもしれません。無理せず過ごしましょう。",
    }
    message = messages.get(uranai_result, "運勢判定不能")

    return render_template(
        "uranai_result.html",
        result=uranai_result,
        message=message,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
