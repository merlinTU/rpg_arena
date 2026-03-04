import time

from .item import Item

class StatBooster(Item):
    def __init__(self, name, status: str, boost: int,  price):
        super().__init__(name, True, price)
        self.status = status
        self.boost = boost
        self.uses = 1

    def __str__(self):
        name_width = 20
        value_width = 6

        line = (
            f"{self.name:<{name_width}} | "
            f"Uses: {self.uses:>{value_width}} | "
            f"Boost: {self.status:<8} | "
            f"+{self.boost:>{value_width}}"
        )

        return f"{line}"

    def copy(self):
        """Return a new StatBooster instance with the same stats."""
        return StatBooster(
            name=self.name,
            status=self.status,
            boost=self.boost,
            price=self.price
        )

    def use(self, player_unit, game):

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

        if self in player_unit.items:
            player_unit.items.remove(self)
        else:
            game.convoy.remove(self)

        print(f"{player_unit.name}'s {self.status} increased by {self.boost}!")
        time.sleep(1)






