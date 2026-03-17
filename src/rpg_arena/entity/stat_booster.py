import time
from .item import Item

class StatBooster(Item):
    """
    Represents a consumable item that permanently boosts a specific stat
    of a Fighter when used.

    Attributes:
        name (str): Name of the item (inherited from Item).
        usable (bool): Whether the item is usable (always True for StatBooster).
        price (int): Price of the item (inherited from Item).
        status (str): The stat to be boosted (e.g., "HP", "STR", "MAG", "SKL", "SPD", "LUCK", "DEF", "RES").
        boost (int): The amount by which the stat is increased.
        uses (int): Number of times the item can be used (default 1).
    """

    def __init__(self, name, status: str, boost: int, price):
        """
        Initialize a StatBooster with a stat type, boost amount, and price.

        Args:
            name (str): The name of the stat booster.
            status (str): The stat to increase (e.g., "HP", "STR", "MAG", etc.).
            boost (int): Amount to increase the stat by.
            price (int): The price of the item.

        Returns:
            None
        """
        super().__init__(name, True, price)
        self.status = status
        self.boost = boost
        self.uses = 1
        self.max_uses = 1

    def __str__(self, index=None):
        """
        Return a formatted string representation of the StatBooster.

        Args:
            index (int | None, optional): Optional index to display before the name.

        Returns:
            str: Formatted string including name, remaining uses, and boost info.
        """
        name_width = 20
        value_width = 5
        index_str = f"{index}) " if index is not None else ""
        name_width = name_width - len(index_str)

        line = (
            f"{index_str}{self.name:<{name_width}} | "
            f"Uses: {self.uses:>{value_width}} | "
            f"{self.status:<8} +{self.boost:<1} | "
        )

        return f"{line}"

    def copy(self):
        """
        Create a copy of this StatBooster instance.

        Returns:
            StatBooster: A new instance with the same name, status, boost, and price.
        """
        return StatBooster(
            name=self.name,
            status=self.status,
            boost=self.boost,
            price=self.price
        )

    def use(self, player_unit, game, in_convoy=False):
        """
        Apply the stat boost to a Fighter and update inventory or convoy.

        Args:
            player_unit (Fighter): The unit using the item.
            game (Game): The current game instance, to modify global state if needed.
            in_convoy (bool, optional): If True, remove from convoy instead of player items.

        Returns:
            None
        """
        match self.status:
            case "HP":
                player_unit.hp += self.boost
                player_unit.max_hp += self.boost
            case "STR":
                player_unit.strength += self.boost
            case "MAG":
                player_unit.magic += self.boost
            case "SKL":
                player_unit.skill += self.boost
            case "SPD":
                player_unit.speed += self.boost
            case "LUCK":
                player_unit.luck += self.boost
            case "DEF":
                player_unit.defense += self.boost
            case "RES":
                player_unit.resistance += self.boost
            case _:
                print("Invalid stat type.")
                return

        self.uses -= 1
        if self.uses > 0:
            return

        if not in_convoy:
            player_unit.items.remove(self)
        else:
            game.convoy.remove(self)

        print(f"{player_unit.name}'s {self.status} increased by {self.boost}!")
        time.sleep(1)

    def update_price(self):
        """
        Updates the price of the item based on its remaining durability.
        """
        self.price = int(self.price * self.uses / self.max_uses)