from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from rpg_arena.entity.fighter import Fighter


class Item:
    """
    Represents an item in the game, which can be usable or non-usable
    and has an associated price.

    Attributes:
        name (str): Name of the item.
        usable (bool): Indicates whether the item can be used by a unit.
        price (int): Cost of the item in gold.
    """

    def __init__(self, name: str, usable: bool, price: int):
        """
        Initialize an Item with name, usability, and price.

        Args:
            name (str): The name of the item.
            usable (bool): Whether the item is usable by a unit.
            price (int): Cost of the item in gold.

        Returns:
            None
        """
        self.name = name
        self.usable = usable
        self.price = price

    def __str__(self, index=None):
        """
        Return a string representation of the item.

        Args:
            index (int | None, optional): Optional index to display before the name.

        Returns:
            str: The name of the item, optionally prefixed by an index.
        """
        return f"{self.name}"

    def use(self, player_unit: Fighter, game):
        """
        Use the item on a player unit or modify the game state.

        This method should implement the item's effect.

        Args:
            player_unit (Fighter): The unit using the item.
            game (Game): The game instance, for modifying global state if needed.

        Returns:
            None
        """
        pass