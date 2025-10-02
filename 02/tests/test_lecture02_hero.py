import unittest

from src import Hero


class TestHero(unittest.TestCase):
    def test_getHP_no_buf(self):
        hero = Hero("TestHero", hp=150)
        self.assertEqual(hero.getHP(), 150)
        hero2 = Hero("DefaultHero")
        self.assertEqual(hero2.getHP(), 100)  # デフォルトHP

    def test_getHP_with_buf(self):
        hero = Hero("TestHero", hp=150)
        Hero.buf_status["hp"] = -30  # デバフを設定
        self.assertEqual(hero.getHP(), 120)
        Hero.buf_status["hp"] = 0  # 以下のテストに影響しないようにbuf_statusをリセット

    def test_getDefaultHP(self):
        self.assertEqual(Hero.getDefaultHP(), 100)

    def test_damage(self):
        hero = Hero("TestHero", hp=150)
        hero2 = Hero("DefaultHero")
        hero.damage(hero2)  # NotImplementedErrorが発生することを確認
