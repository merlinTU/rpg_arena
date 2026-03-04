from .item import Item

class HealingPotion(Item):
    def __init__(self, name, heal_amount, uses, price):
        super().__init__(name, True, price)
        self.heal_amount = heal_amount
        self.uses = uses

    def __str__(self):
        name_width = 20
        value_width = 6

        line = (
            f"{self.name:<{name_width}} | "
            f"Uses: {self.uses:>{value_width}} | "
            f"Heal: +{self.heal_amount:>{value_width}} HP"
        )

        return f"{line}"

    def use(self, player_unit, game):
        if player_unit.health == player_unit.max_health:
            return -1
        else:
            player_unit.health += self.heal_amount
            self.uses -= 1
            if self.uses == 0:
                player_unit.items.remove(self)
            return 1

    def copy(self):
        """Return a new HealingPotion instance with the same stats."""
        return HealingPotion(
            name=self.name,
            heal_amount=self.heal_amount,
            uses=self.uses,
            price=self.price
        )