from rpg_arena.entity import UnitClass, Weapon, WeaponType

# Boss weapons

great_axe = Weapon(
    name="Great Axe",
    weapon_type=WeaponType.AXE,
    strength=15,
    accuracy=100,
    uses=99,
    crit=0,
    weight=25,
    price=0
)

mjoelnir = Weapon(
    name="Mjölnir",
    weapon_type=WeaponType.MAGIC,
    strength=10,
    accuracy=80,
    uses=99,
    crit=30,
    weight=10,
    price=0
)

purgatio = Weapon(
    name="Purgatio",
    weapon_type=WeaponType.MAGIC,
    strength=15,
    accuracy=120,
    uses=99,
    crit=0,
    weight=10,
    price=0
)


BOSS_DATA = [
    {
        "name": "Gonzales the Giant",
        "unit_class": UnitClass.WARRIOR,
        "level": 20,
        "hp": 80,
        "strength": 20,
        "magic": 10,
        "skill": 20,
        "speed": 15,
        "luck": 20,
        "defense": 15,
        "res": 15,
        "gold": 0,
        "items": [great_axe],
        "equipped_weapon": great_axe
    },
    {
        "name": "Sarah the Saint",
        "unit_class": UnitClass.SAGE,
        "level": 20,
        "hp": 50,
        "strength": 5,
        "magic": 15,
        "skill": 20,
        "speed": 15,
        "luck": 5,
        "defense": 10,
        "res": 25,
        "gold": 0,
        "items": [purgatio],
        "equipped_weapon": purgatio
    },
    {
        "name": "Mercurius of the Thunder",
        "unit_class": UnitClass.MAGEKNIGHT,
        "level": 20,
        "hp": 60,
        "strength": 15,
        "magic": 10,
        "skill": 25,
        "speed": 25,
        "luck": 10,
        "defense": 15,
        "res": 15,
        "gold": 0,
        "items": [mjoelnir],
        "equipped_weapon": mjoelnir
    }
]