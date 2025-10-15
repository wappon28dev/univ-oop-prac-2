import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Final, Protocol, Self

CWD: Final = Path(__file__).parent


class Model(Protocol):
    @classmethod
    def from_str(cls, row: list[str]) -> Self: ...


@dataclass
class ModelLoader[T: Model]:
    model: type[T]

    def csv(self, filename: Path) -> list[T]:
        with filename.open(encoding="utf-8") as file:
            reader = csv.reader(file)
            _ = next(reader)
            return [self.model.from_str(row) for row in reader]


@dataclass
class Weapon(Model):
    id: int
    name: str
    hp: int
    mp: int
    atk: int
    def_: int
    age: int

    @classmethod
    def from_str(cls, row: list[str]) -> Self:
        [id_, name, hp, mp, atk, def_, age] = row
        return cls(
            id=int(id_),
            name=name,
            hp=int(hp),
            mp=int(mp),
            atk=int(atk),
            def_=int(def_),
            age=int(age),
        )

    def __str__(self) -> str:
        return (
            f"{self.name}のステータスは"
            f"HP:{self.hp},MP:{self.mp},Atk:{self.atk},Def:{self.def_},Age:{self.age}"
        )


@dataclass
class Hero(Model):
    id: int
    name: str
    hp: int
    mp: int
    atk: int
    def_: int
    age: int
    weapon: int

    applied_weapon: Weapon | None = None

    @classmethod
    def from_str(cls, row: list[str]) -> Self:
        [id_, name, hp, mp, atk, def_, age, weapon] = row
        return cls(
            id=int(id_),
            name=name,
            hp=int(hp),
            mp=int(mp),
            atk=int(atk),
            def_=int(def_),
            age=int(age),
            weapon=int(weapon),
        )

    def subject(self) -> str:
        match self.applied_weapon:
            case None:
                return self.name
            case Weapon():
                return f"{self.applied_weapon.name}を装備した{self.name}"

    def __str__(self) -> str:
        return (
            f"{self.subject()}のステータスは"
            f"HP:{self.hp},MP:{self.mp},Atk:{self.atk},Def:{self.def_},Age:{self.age}"
        )

    def set_weapon(self, weapons: list[Weapon]) -> None:
        weapon: Final = next(
            filter(lambda w: w.id == self.weapon, weapons),
            None,
        )

        if weapon is None:
            raise ValueError(f"Weapon id `{self.weapon}` not found for hero `{self.name}`")

        self.applied_weapon = weapon

        self.hp += weapon.hp
        self.mp += weapon.mp
        self.atk += weapon.atk
        self.def_ += weapon.def_
        self.age += weapon.age


loader_hero_csv: Final = ModelLoader(Hero).csv
loader_weapon_csv: Final = ModelLoader(Weapon).csv


def lecture02_01_printHeroStatus() -> None:  # noqa: N802
    heros: Final = loader_hero_csv(CWD / "lecture02_Hero.csv")

    target_hero_id: Final = 1
    target_hero: Final = next(filter(lambda h: h.id == target_hero_id, heros), None)
    print(target_hero)


def lecture02_01_printWeaponStatus() -> None:  # noqa: N802
    weapons: Final = loader_weapon_csv(CWD / "lecture02_Weapon.csv")

    target_weapon_id: Final = 1
    target_weapon: Final = next(filter(lambda w: w.id == target_weapon_id, weapons), None)
    print(target_weapon)


def _lecture02_01_printHeroStatusWithWeapon() -> None:  # noqa: N802
    heros: Final = loader_hero_csv(CWD / "lecture02_Hero.csv")
    weapons: Final = loader_weapon_csv(CWD / "lecture02_Weapon.csv")

    target_hero_id: Final = 1
    target_hero: Final = next(filter(lambda h: h.id == target_hero_id, heros), None)

    if target_hero is None:
        raise ValueError(f"Hero id `{target_hero_id}` not found")

    target_hero.set_weapon(weapons)
    print(target_hero)


def lecture02_01_printHeroStatusWithWeapon() -> None:  # noqa: N802
    heros: Final = loader_hero_csv(CWD / "lecture02_Hero.csv")
    weapons: Final = loader_weapon_csv(CWD / "lecture02_Weapon.csv")

    target_hero_id: Final = 1
    target_hero: Final = next(filter(lambda h: h.id == target_hero_id, heros), None)

    if target_hero is None:
        raise ValueError(f"Hero id `{target_hero_id}` not found")

    ### 変数名の指定 ###
    hero_name = target_hero.name
    hero_hp = int(target_hero.hp)
    hero_mp = int(target_hero.mp)
    hero_atk = int(target_hero.atk)
    hero_def = int(target_hero.def_)
    hero_age = int(target_hero.age)
    hero_weapon = int(target_hero.weapon)
    ###

    target_hero.set_weapon(weapons)
    target_weapon = target_hero.applied_weapon

    if target_weapon is None:
        raise ValueError(f"Weapon id `{hero_weapon}` not found for hero `{hero_name}`")

    ### 変数名の指定 ###
    # NOTE: `weapn` in spec is typo.
    weapn_name = target_weapon.name
    weapon_hp = int(target_weapon.hp)
    weapon_mp = int(target_weapon.mp)
    weapon_atk = int(target_weapon.atk)
    weapon_def = int(target_weapon.def_)
    weapon_age = int(target_weapon.age)

    total_hp = hero_hp + weapon_hp
    total_mp = hero_mp + weapon_mp
    total_atk = hero_atk + weapon_atk
    total_def = hero_def + weapon_def
    total_age = hero_age + weapon_age
    ###

    print(
        f"{weapn_name}を装備した{hero_name}のステータスは"
        f"HP:{total_hp},MP:{total_mp},Atk:{total_atk},Def:{total_def},Age:{total_age}",
    )


if __name__ == "__main__":
    lecture02_01_printHeroStatus()
    lecture02_01_printWeaponStatus()
    lecture02_01_printHeroStatusWithWeapon()
