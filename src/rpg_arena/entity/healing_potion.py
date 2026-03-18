from __future__ import annotations

from .item import Item

class HealingPotion(Item):
    """
    Represents a consumable healing item that restores HP to a Fighter.

    Attributes:
        name (str): Name of the item (inherited from Item).
        usable (bool): Whether the item is usable (always True for HealingPotion).
        price (int): Price of the item (inherited from Item).
        heal_amount (int): Amount of HP restored when used.
        uses (int): Number of times the potion can be used.

    Methods:
        __str__(index=None): Returns a formatted string representation of the potion.
        use(player_unit, game, in_convoy=False): Heals the player and updates inventory.
        copy(): Returns a new HealingPotion instance with the same attributes.
    """

    def __init__(self, name, heal_amount, uses, price):
        """
        Initialize a HealingPotion with a healing amount, number of uses, and price.

        Args:
            name (str): Name of the potion.
            heal_amount (int): Amount of HP the potion restores.
            uses (int): Number of times the potion can be used.
            price (int): Price of the potion.

        Returns:
            None
        """
        super().__init__(name, True, price)
        self.heal_amount = heal_amount
        self.uses = uses
        self.max_uses = uses

    def __str__(self, index=None):
        """
        Return a formatted string representation of the HealingPotion.

        Args:
            index (int | None, optional): Optional index to display before the item name.

        Returns:
            str: Formatted string showing name, remaining uses, and healing amount.
        """
        name_width = 20
        value_width = 5
        index_str = f"{index}) " if index is not None else ""
        name_width = name_width - len(index_str)

        heal_str = f"{self.heal_amount} HP"

        line = (
            f"{index_str}{self.name:<{name_width}} | "
            f"Uses: {self.uses:<{value_width}} | "
            f"Heal: {heal_str:<{value_width}} | "
        )

        return f"{line}"

    def use(self, player_unit, game, in_convoy=False):
        """
        Apply the healing effect to a player unit and update inventory.

        Args:
            player_unit (Fighter): The unit using the potion.
            game (Game): The game instance (for updating convoy if needed).
            in_convoy (bool, optional): If True, remove from convoy instead of player items.

        Returns:
            int: -1 if the unit is already at max HP, 1 if the potion was used successfully.
        """
        if player_unit.hp == player_unit.max_hp:
            return -1
        else:
            player_unit.hp += self.heal_amount
            player_unit.hp = min(player_unit.hp, player_unit.max_hp)

            self.uses -= 1
            if self.uses == 0 and not in_convoy:
                player_unit.items.remove(self)
            elif self.uses == 0 and in_convoy:
                game.convoy.remove(self)
            return 1

    def copy(self):
        """
        Create a copy of this HealingPotion instance.

        Returns:
            HealingPotion: A new HealingPotion instance with identical attributes.
        """
        return HealingPotion(
            name=self.name,
            heal_amount=self.heal_amount,
            uses=self.uses,
            price= self.price
        )

    def update_price(self):
        """
        Updates the price of the item based on its remaining durability.
        """
        self.price = int(self.price * self.uses / self.max_uses)