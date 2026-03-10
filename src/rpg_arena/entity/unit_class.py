from enum import Enum

class UnitClass(Enum):
    """
    Enum representing the different possible classes a unit can have.

    Each class defines a unique archetype for units, which can influence
    base stats, growth rates, and available weapons.

    Members:
        FIGHTER (str): Fighter class.
        MAGE (str): Mage class.
        MERCENARY (str): Mercenary class.
        KNIGHT (str): Knight class.
        SWORDMASTER (str): Sword Master class.
        BERSERKER (str): Berserker class.
        THIEF (str): Thief class.
        SOLIDER (str): Solider class.
        ARCHER (str): Archer class.
        PALADIN (str): Paladin class.
        PALADIN (str): "Paladin"
        WARRIOR (str): "Warrior"
        MAGEKNIGHT (str): "Mage Knight"
        SAGE (str): "Sage"
    """

    FIGHTER = "Fighter"
    MAGE = "Mage"
    MERCENARY = "Mercenary"
    KNIGHT = "Knight"
    SWORDMASTER = "Sword Master"
    BERSERKER = "Berserker"
    THIEF = "Thief"
    SOLDIER = "Solider"
    ARCHER = "Archer"
    PALADIN = "Paladin"
    WARRIOR = "Warrior"
    MAGEKNIGHT = "Mage Knight"
    SAGE = "Sage"