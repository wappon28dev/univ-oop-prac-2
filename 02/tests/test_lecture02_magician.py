import unittest

from src import Hero, Magician


class TestMagician(unittest.TestCase):
    def test_magician_inheritance(self):
        magician = Magician("TestMagician", hp=150, mp=80)
        self.assertEqual(magician.name, "TestMagician")
        self.assertEqual(magician.getHP(), 150)
        self.assertEqual(magician.mp, 80)

    def test_magic_attack_with_sufficient_mp(self):
        magician = Magician("TestMagician", mp=50)
        enemy = Hero("EnemyHero", hp=100)
        magician.magic_attack(enemy)
        self.assertEqual(magician.mp, 40)  # MPは10減る

    def test_magic_attack_with_insufficient_mp(self):
        magician = Magician("TestMagician", mp=5)
        enemy = Hero("EnemyHero", hp=100)
        magician.magic_attack(enemy)
        self.assertEqual(magician.mp, 5)  # MPは変わらない

    def test_printDefaultHP(self):
        magician = Magician("TestMagician")
        try:
            magician.printDefaultHP()  # 親クラスのprivate変数にアクセスできるか確認
        except Exception as e:
            self.fail(f"printDefaultHP raised an exception: {e}")
