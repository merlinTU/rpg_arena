from rpg_arena.entity.weapon import Weapon
from rpg_arena.entity.weapon_type import WeaponType
from rpg_arena.entity.unit_class import UnitClass


iron_sword = Weapon(
    name="Iron Sword",
    weapon_type=WeaponType.SWORD,
    strength=4,
    accuracy=100,
    uses=15,
    crit=5,
    weight=5,
    price=100
)

master_sword = Weapon(
    name="Master Sword",
    weapon_type=WeaponType.SWORD,
    strength=6,
    accuracy=100,
    uses=10,
    crit=30,
    weight=8,
    price=500
)

master_lance = Weapon(
    name="Master Lance",
    weapon_type=WeaponType.LANCE,
    strength=9,
    accuracy=90,
    uses=10,
    crit=25,
    weight=10,
    price=500
)

master_bow = Weapon(
    name="Master Bow",
    weapon_type=WeaponType.BOW,
    strength=5,
    accuracy=100,
    uses=10,
    crit=35,
    weight=10,
    price=500
)


master_axe = Weapon(
    name="Master Axe",
    weapon_type=WeaponType.AXE,
    strength=10,
    accuracy=80,
    uses=10,
    crit=20,
    weight=14,
    price=500
)

iron_axe = Weapon(
    name="Iron Axe",
    weapon_type=WeaponType.AXE,
    strength=8,
    accuracy=85,
    uses=15,
    crit=0,
    weight=7,
    price=120
)

iron_bow = Weapon(
    name="Iron Bow",
    weapon_type=WeaponType.BOW,
    strength=3,
    accuracy=115,
    uses=15,
    crit=5,
    weight=4,
    price=90
)

fire_magic = Weapon(
    name="Fire",
    weapon_type=WeaponType.MAGIC,
    strength=5,
    accuracy=100,
    uses=15,
    crit=0,
    weight=0,
    price=150,
    is_magical= True
)

iron_lance = Weapon(
    name="Iron Lance",
    weapon_type=WeaponType.LANCE,
    strength=6,
    accuracy=90,
    uses=15,
    crit=0,
    weight=6,
    price=110
)

steel_sword = Weapon(
    name="Steel Sword",
    weapon_type=WeaponType.SWORD,
    strength=8,
    accuracy=90,
    uses=10,
    crit=5,
    weight=8,
    price=300
)

steel_axe = Weapon(
    name="Steel Axe",
    weapon_type=WeaponType.AXE,
    strength=16,
    accuracy=75,
    uses=10,
    crit=5,
    weight=12,
    price=320
)

steel_lance = Weapon(
    name="Steel Lance",
    weapon_type=WeaponType.LANCE,
    strength=12,
    accuracy=85,
    uses=10,
    crit=5,
    weight=10,
    price=310
)

steel_bow = Weapon(
    name="Steel Bow",
    weapon_type=WeaponType.BOW,
    strength=6,
    accuracy=115,
    uses=15,
    crit=10,
    weight=9,
    price=290
)

thunder = Weapon(
    name="Thunder",
    weapon_type=WeaponType.MAGIC,
    strength=8,
    accuracy=100,
    uses=10,
    crit=5,
    weight=5,
    price=350,
    is_magical= True
)

silver_sword = Weapon(
    name="Silver Sword",
    weapon_type=WeaponType.SWORD,
    strength=12,
    accuracy=100,
    uses=5,
    crit=0,
    weight=10,
    price=600
)

silver_axe = Weapon(
    name="Silver Axe",
    weapon_type=WeaponType.AXE,
    strength=24,
    accuracy=85,
    uses=5,
    crit=0,
    weight=16,
    price=650
)

silver_lance = Weapon(
    name="Silver Lance",
    weapon_type=WeaponType.LANCE,
    strength=18,
    accuracy=90,
    uses=5,
    crit=0,
    weight=14,
    price=620
)

silver_bow = Weapon(
    name="Silver Bow",
    weapon_type=WeaponType.BOW,
    strength=9,
    accuracy=120,
    uses=5,
    crit=15,
    weight=12,
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
    price=700,
    is_magical= True
)

thunder_sword = Weapon(
    name="Thunder Sword",
    weapon_type=WeaponType.SWORD,
    strength=10,
    accuracy=95,
    uses=10,
    crit=0,
    weight=9,
    price=500,
    is_magical= True
)

fire_lance = Weapon(
    name="Fire Lance",
    weapon_type=WeaponType.LANCE,
    strength=13,
    accuracy=80,
    uses=10,
    crit=0,
    weight=12,
    price=800,
    is_magical= True
)

ice_bow = Weapon(
    name="Ice Bow",
    weapon_type=WeaponType.BOW,
    strength=9,
    accuracy=105,
    uses=10,
    crit=5,
    weight=9,
    price=600,
    is_magical= True
)


WEAPONS = { "Iron Sword": iron_sword,
            "Steel Sword": steel_sword,
            "Master Sword" : master_sword,
            "Silver Sword": silver_sword,
            "Thunder Sword": thunder_sword,

            "Iron Axe": iron_axe,
            "Steel Axe": steel_axe,
            "Master Axe": master_axe,
            "Silver Axe": silver_axe,

            "Iron Bow": iron_bow,
            "Steel Bow": steel_bow,
            "Master Bow" : master_bow,
            "Silver Bow": silver_bow,
            "Ice Bow": ice_bow,

            "Fire": fire_magic,
            "Thunder": thunder,
            "Dire Thunder": dire_thunder,

            "Iron Lance": iron_lance,
            "Steel Lance": steel_lance,
            "Master Lance" : master_lance,
            "Silver Lance": silver_lance,
            "Fire Lance": fire_lance
            }

CLASS_WEAPON_MAP = {
    UnitClass.FIGHTER: [WeaponType.BOW, WeaponType.AXE],
    UnitClass.MERCENARY: [WeaponType.SWORD, WeaponType.AXE],
    UnitClass.MAGE: [WeaponType.MAGIC],
    UnitClass.KNIGHT: [WeaponType.SWORD, WeaponType.LANCE],
    UnitClass.SWORDMASTER: [WeaponType.SWORD],
    UnitClass.BERSERKER: [WeaponType.AXE],
    UnitClass.THIEF: [WeaponType.SWORD, WeaponType.MAGIC],
    UnitClass.SOLDIER: [WeaponType.LANCE],
    UnitClass.ARCHER: [WeaponType.BOW],
    UnitClass.PALADIN: [WeaponType.SWORD, WeaponType.AXE, WeaponType.LANCE]
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
    thunder,
    thunder_sword,
    fire_lance,
    ice_bow
]

STRONG_WEAPONS = [
    silver_sword,
    silver_axe,
    silver_lance,
    silver_bow,
    dire_thunder,
    master_axe,
    master_bow,
    master_lance,
    master_sword
]