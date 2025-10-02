from src import Hero, Magician
from typing import Union

def print_heros(heros: list[Hero]) -> None:
    """
    ヒーローのリストを受け取り,1人ずつ表示する関数
    """
    print("パーティーの状態：")
    for hero in heros:
        print(hero)

def check_instance_type(heros : list[Union[Hero, Magician]]) -> None:
    for hero in heros:
        if type(hero) is Hero:
            print(f'{hero.name}はHero')
        elif type(hero) is Magician:
            print(f'{hero.name}はMagician')
        else:
            print(f'{hero.name}はHeroでもMagicianでもない')
        if isinstance(hero, Hero):
            print(f'{hero.name}はHeroクラスのインスタンス')
        elif isinstance(hero, Magician):
            print(f'{hero.name}はMagicianクラスのインスタンス')
        else:
            print(f'{hero.name}はHeroでもMagicianでもない')

if __name__ == '__main__':
    heros = []
    hero1 = Hero('愛知太郎') # Heroクラスのインスタンスを生成，後に()がついているのは関数呼び出しかクラスインスタンス生成
    hero2 = Hero(name='愛知花子', hp=200) # 引数名を指定してコンストラクタを呼び出し
    heros.append(hero1)
    heros.append(hero2)
    print_heros(heros) # ヒーローのリストを表示する関数を呼び出し

    # クラスメソッドの内，第1引数にselfが書かれているメソッドはインスタンスを作成して初めて呼び出せる
    print(f'hero1のHPは{hero1.getHP()}')

    # __DEFAULT_HPはPrivate変数なので直接アクセスするとエラーになる(↓の行のコメントを実行してみましょう)
    # print(Hero.__DEFAULT_HP) # private変数にアクセスできてしまうのであくまでもprivate扱いして欲しい変数
    # classの外からprivate変数にアクセスしたければアクセサー（get, set)を作ります
    print(Hero.getDefaultHP()) # static扱いの変数はインスタンス化しなくても実行可能

    # グループワーク内容
    # Heroクラスのインスタンスhero1，hero2を使ってフレーバーテキストを入れながらHPの変化とHero.buf_statusの変化を表示してください
    # hero1変数には，途中でMagicianクラスのインスタンスを代入してみましょう
    # heroのHPやMPが変化するようにフレバーテキストを入れて，実装してみましょう
    # Heroクラスのインスタンスを最後にdelで削除し, HPの値によって表示が変わることを確認してください
    print(f"{hero1.name}は冒険に出発した") # フレーバーテキスト
    print(f"{hero2.name}は{hero1.name}のパーティに合流した") # フレーバーテキスト
    print_heros(heros) # ヒーローのリストを表示する関数を呼び出し

    # 例１
    print("Hero全員のHPが下がるトラップ（デバフ）発動") # フレーバーテキスト
    # Hero.buf_status['hp']を変化させると良いのでは？
    Hero.buf_status['hp'] = -10
    print_heros(heros) # ヒーローのリストを表示する関数を呼び出し

    print(f"{hero1.name}は魔法使いに転職した") # フレーバーテキスト
    hero1 = Magician(name=hero1.name, hp=hero1.getHP(), mp=150) # Magicianクラスのインスタンスを生成，hpはgetHP()で取得
    heros[0] = hero1 # herosリストの最初の要素を更新
    check_instance_type(heros) # ヒーローのリストを表示する関数を呼び出し
    print_heros(heros) # ヒーローのリストを表示する関数を呼び出し

    # 例２
    print(f"{hero1.name}はHero全員のHPが下がる呪い（デバフ）をうけた") # フレーバーテキスト
    # hero1.buf_status['hp']を変化させると良いのでは？
    Hero.buf_status['hp'] = -30
    # print(f'Hero.buf_status = {Hero.buf_status}') # Heroクラスのjob_statusの値を確認
    print_heros(heros) # ヒーローのリストを表示する関数を呼び出し

    # 例３
    print(f"{hero1.name}は罠にかかって味方の{hero2.name}を魔法で攻撃してしまった") # フレーバーテキスト
    # hero1.magic_attack(hero2) # hero1がhero2に魔法攻撃
    hero1.buf_status['hp'] = -60
    print_heros(heros) # ヒーローのリストを表示する関数を呼び出し

    print(f"{hero1.name}と{hero2.name}の今日の冒険はここまで") # フレーバーテキスト
    print(f'hero1={str(hero1)}') # 文字列に変換
    del hero1 # インスタンスを削除
    print(f'hero2={str(hero2)}') # 文字列に変換
    del hero2 # インスタンスを削除