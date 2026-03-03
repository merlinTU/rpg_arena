from rpg_arena.entity.weapon import Weapon
from rpg_arena.entity.weapon_type import WeaponType
from rpg_arena.entity.unit_class import UnitClass


iron_sword = Weapon(
    name="Iron Sword",
    weapon_type=WeaponType.SWORD,
    strength=8,
    accuracy=100,
    uses=40,
    crit=5,
    weight=5.0,
    price=100
)

iron_axe = Weapon(
    name="Iron Axe",
    weapon_type=WeaponType.AXE,
    strength=12,
    accuracy=85,
    uses=35,
    crit=5,
    weight=7,
    price=120
)

iron_bow = Weapon(
    name="Iron Bow",
    weapon_type=WeaponType.BOW,
    strength=7,
    accuracy=115,
    uses=30,
    crit=5,
    weight=4,
    price=90
)

fire_magic = Weapon(
    name="Fire",
    weapon_type=WeaponType.MAGIC,
    strength=5,
    accuracy=100,
    uses=25,
    crit=5,
    weight=0,
    price=150
)

iron_lance = Weapon(
    name="Iron Lance",
    weapon_type=WeaponType.LANCE,
    strength=10,
    accuracy=90,
    uses=35,
    crit=5,
    weight=6,
    price=110
)

steel_sword = Weapon(
    name="Steel Sword",
    weapon_type=WeaponType.SWORD,
    strength=12,
    accuracy=100,
    uses=35,
    crit=10,
    weight=5,
    price=300
)

steel_axe = Weapon(
    name="Steel Axe",
    weapon_type=WeaponType.AXE,
    strength=16,
    accuracy=85,
    uses=30,
    crit=10,
    weight=7,
    price=320
)

steel_lance = Weapon(
    name="Steel Lance",
    weapon_type=WeaponType.LANCE,
    strength=14,
    accuracy=90,
    uses=30,
    crit=10,
    weight=6,
    price=310
)

steel_bow = Weapon(
    name="Steel Bow",
    weapon_type=WeaponType.BOW,
    strength=11,
    accuracy=115,
    uses=25,
    crit=10,
    weight=4,
    price=290
)

thunder = Weapon(
    name="Thunder",
    weapon_type=WeaponType.MAGIC,
    strength=8,
    accuracy=100,
    uses=20,
    crit=5,
    weight=0,
    price=350
)

silver_sword = Weapon(
    name="Silver Sword",
    weapon_type=WeaponType.SWORD,
    strength=18,
    accuracy=100,
    uses=30,
    crit=15,
    weight=6,
    price=600
)

silver_axe = Weapon(
    name="Silver Axe",
    weapon_type=WeaponType.AXE,
    strength=22,
    accuracy=85,
    uses=25,
    crit=15,
    weight=8,
    price=650
)

silver_lance = Weapon(
    name="Silver Lance",
    weapon_type=WeaponType.LANCE,
    strength=20,
    accuracy=90,
    uses=25,
    crit=15,
    weight=7,
    price=620
)

silver_bow = Weapon(
    name="Silver Bow",
    weapon_type=WeaponType.BOW,
    strength=16,
    accuracy=115,
    uses=20,
    crit=15,
    weight=5,
    price=610
)

dire_thunder = Weapon(
    name="Dire Thunder",
    weapon_type=WeaponType.MAGIC,
    strength=15,
    accuracy=95,
    uses=5,
    crit=15,
    weight=8,
    price=700
)


WEAPONS = { "Iron Sword": iron_sword,
            "Iron Axe": iron_axe,
            "Iron Bow": iron_bow,
            "Fire": fire_magic,
            "Iron Lance": iron_lance,
            "Steel Sword": steel_sword,
            "Steel Axe": steel_axe,
            "Steel Lance": steel_lance,
            "Steel Bow": steel_bow,
            "Thunder": thunder,
            "Silver Sword": silver_sword,
            "Silver Axe": silver_axe,
            "Silver Lance": silver_lance,
            "Silver Bow": silver_bow,
            "Dire Thunder": dire_thunder
            }

CLASS_WEAPON_MAP = {
    UnitClass.FIGHTER: [WeaponType.BOW, WeaponType.AXE],
    UnitClass.MERCENARY: [WeaponType.SWORD, WeaponType.AXE],
    UnitClass.MAGE: [WeaponType.MAGIC]
}

WEAK_WEAPONS = [
    iron_sword,
    iron_axe,
    iron_lance,
    iron_bow,
    fire_magic
]

MEDIUM_WEAPONS = [
    steel_sword,
    steel_axe,
    steel_lance,
    steel_bow,
    thunder
]

STRONG_WEAPONS = [
    silver_sword,
    silver_axe,
    silver_lance,
    silver_bow,
    dire_thunder
]