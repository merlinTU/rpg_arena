from .weapon_type import WeaponType
from .item import Item

class Weapon(Item):
    """
    Represents a weapon item that can be equipped by a unit.

    Attributes:
        name (str): Name of the weapon (inherited from Item).
        usable (bool): Whether the item is usable (False for weapons).
        price (int): Price of the weapon (inherited from Item).
        weapon_type (WeaponType): Type of the weapon (e.g., Sword, Axe, Lance).
        strength (int): Weapon's attack power.
        accuracy (int): Weapon's hit chance modifier.
        uses (int): Number of times the weapon can be used before breaking.
        crit (int): Weapon's critical hit chance.
        weight (int): Weight of the weapon, affecting the wielder's speed.
    Methods:
        copy(): Returns a new Weapon instance with the same stats.
        __str__(index=None): Returns a formatted string representation of the weapon.
    """

    def __init__(self, name, weapon_type: WeaponType, strength: int, accuracy: int,
                 uses: int, crit: int, weight: int, price: int):
        """
        Initialize a Weapon instance with stats, type, and price.

        Args:
            name (str): Name of the weapon.
            weapon_type (WeaponType): Type of the weapon.
            strength (int): Attack power of the weapon.
            accuracy (int): Hit chance of the weapon.
            uses (int): Durability of the weapon (number of uses).
            crit (int): Critical hit chance of the weapon.
            weight (int): Weight affecting user's speed.
            price (int): Purchase price of the weapon.

        Returns:
            None
        """
        super().__init__(name, False, price)
        self.weapon_type = weapon_type
        self.strength = strength
        self.accuracy = accuracy
        self.uses = uses
        self.crit = crit
        self.weight = weight

    def copy(self):
        """
        Create a copy of this Weapon instance.

        Returns:
            Weapon: A new Weapon instance with identical attributes.
        """
        return Weapon(
            name=self.name,
            weapon_type=self.weapon_type,
            strength=self.strength,
            accuracy=self.accuracy,
            uses=self.uses,
            crit=self.crit,
            weight=self.weight,
            price=self.price
        )

    def __str__(self, index=None):
        """
        Return a formatted string representation of the weapon.

        Args:
            index (int | None, optional): Optional index to display before the weapon name.

        Returns:
            str: Formatted string showing weapon stats.
        """
        name_width = 20
        stat_width = 6
        index_str = f"{index}) " if index is not None else ""
        name_width = name_width - len(index_str)

        return (
            f"{index_str}{self.name:<{name_width}} | "
            f"STR: {self.strength:>{stat_width}} | "
            f"ACC: {self.accuracy:>{stat_width}} | "
            f"CRIT: {self.crit:>{stat_width}} | "
            f"WEIGHT: {self.weight:>{stat_width}} | "
            f"USES: {self.uses:>{stat_width}} |"
        )