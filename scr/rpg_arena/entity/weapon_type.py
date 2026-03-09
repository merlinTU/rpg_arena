from enum import Enum, auto

class WeaponType(Enum):
    """
    Enum representing the different types of weapons available in the game.

    Each weapon type can influence which units can equip it,
    damage effectiveness, and combat interactions.

    Members:
        SWORD (int): Sword type weapon.
        AXE (int): Axe type weapon.
        BOW (int): Bow type weapon.
        MAGIC (int): Magic type weapon.
        LANCE (int): Lance type weapon.
    """
    SWORD = auto()
    AXE = auto()
    BOW = auto()
    MAGIC = auto()
    LANCE = auto()