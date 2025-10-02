from src.lecture02_hero import Hero


# Heroクラスを継承したMagicianクラスを宣言
class Magician(Hero):
    """Magicianクラス

    Attributes
    ----------
    name : str
        Heroの名前　インスタンス作成時に指定する
    hp : int, default is __DEFAULT_HP = 100
        Heroの初期HP　指定しない場合はデフォルト値となる
    mp : int, default is __DEFAULT_MP = 100
        Magicianの初期MP　指定しない場合はデフォルト値となる

    """

    __DEFAULT_MP = 100

    # コンストラクタ
    # 親クラスのコンストラクタをsuper().__init__()で呼び出すことができる
    # 親クラスのprivate変数にアクセスする方法１としてDEFAULT_HPのゲッター関数を呼び出している
    def __init__(self, name=None, hp=Hero.getDefaultHP(), mp=__DEFAULT_MP):
        super().__init__(name, hp)
        self.mp = mp

    # 特殊な関数の宣言(上書き)
    def __str__(self):
        return f'"名前": "{self.name}", "HP": {self.hp + self.buf_status["hp"]}, "MP": {self.mp}'

    # 親クラスのprivate変数へのアクセス
    def printDefaultHP(self):
        # 親クラスのprivate変数にアクセスする方法2
        print(f"親クラスのプライベート変数にアクセス: DEFAULT_HP={Hero._Hero__DEFAULT_HP}")

    # 魔法攻撃
    def magic_attack(self, enemy: Hero) -> None:
        mp_cost = 10
        if self.mp < mp_cost:
            print(f"{self.name}のMPが足りない")
            return
        self.mp -= mp_cost
        print(f"{self.name}は{enemy.name}に魔法攻撃をした")
        # enemy.damage(damage) # damageメソッドは未実装なのでコメントアウト
        print(f"{self.name}の残りMPは{self.mp}")


if __name__ == "__main__":
    hero1 = Hero("愛知太郎")  # Heroクラスのインスタンスを生成
    print(f"hero1={hero1!s}")  # 文字列に変換
    hero2 = Magician(name="愛知花子", hp=200, mp=200)  # 引数名を指定してコンストラクタを呼び出し
    print(f"hero2={hero2!s}")  # 文字列に変換
    hero2.printDefaultHP()
    print(type(hero1))  # <class 'my_module.lecture03_hero.Hero'>
    print(type(hero2))  # <class '__main__.Magician'>
    if type(hero1) is Hero:
        print("hero1はHero")
    if type(hero2) is not Hero:
        print("hero2とはHeroではない")
    if isinstance(hero1, Hero):
        print("hero1はHeroクラスのインスタンス")
    if isinstance(hero2, Hero):
        print("hero2もHeroクラスのインスタンス")
