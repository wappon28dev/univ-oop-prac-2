from __future__ import annotations


# Python3.7以上ではfrom __future__ import annotationsを入れると型ヒントにクラス名を使える
class Hero:
    """HeroクラスはOOP2の学習のために作ったサンプルコードです

    Attributes
    ----------
    name : str
        Heroの名前　インスタンス作成時に指定する
    hp : int, default is __DEFAULT_HP = 100
        Heroの初期HP　指定しない場合はデフォルト値となる

    """

    # Javaでいうstatic変数
    # クラスのインスタンスを作らなくてもアクセスできる
    # 定数は大文字アルファベットなどルールを設けることが多い
    # 複数のHeroインスタンスのjob_statusは共通なのでHero職へのバフに使う
    # 例：Hero全体のステータスの向上はjob_status値を変更
    __DEFAULT_HP = 100
    buf_status = {"hp": 0}

    # コンストラクタ
    # デフォルト値を指定することもできる
    # なお，引数が異なるコンストラクタを定義することはできない
    def __init__(self, name: str, hp: int = __DEFAULT_HP):
        """コンストラクタ

        Parameters
        ----------
        name : str
            デフォルト値が設定されていないので必ず必要
        hp : int
            デフォルト値は全ヒーロー共通で__DEFAULT_HPとする

        """
        self.name = (
            name  # クラス内の変数を「self.変数名」で宣言する（コンストラクタ以外でも宣言可能）
        )
        self.hp = hp
        self.__weapon_id = None  # アンダーバーを2個つけるとprivate（武器は未実装）

    # デストラクタ
    def __del__(self):
        # 3項演算子（1行でif文を書く： 真のときの返り値 if 条件 else 偽のときの返り値）
        message = "一時パーティー離脱" if self.getHP() > 0 else "死亡のためパーティー離脱"
        print(f"{self.name}は{message}")

    # 特殊な関数の宣言
    def __str__(self):
        return f'"名前": "{self.name}", "HP": {self.getHP()}'

    # bufの影響を計算してhpを返すメソッド
    def getHP(self) -> int:
        """ヒーロのHPをbutを考慮して返す

        Returens
        --------
        hp : int
            HPに関係したbufが存在すればbufを加えてHPを返す
        returns : int
            HPに関係したbufが存在すればbufを加えてHPを返す
        """
        if "hp" in Hero.buf_status.keys():
            return self.hp + Hero.buf_status["hp"]
        return self.hp

    # DefaultHPのゲッター(selfを引数に入れないとstatic扱い)
    @staticmethod
    def getDefaultHP() -> int:
        """privateかつstaticな変数__DEFAULT_HPのゲッター"""
        return Hero.__DEFAULT_HP

    # 別のHeroクラスのインスタンスを受け取り，ダメージを与えるメソッド
    # 未開発です
    def damage(self, enemy: Hero) -> None:
        raise NotImplementedError
