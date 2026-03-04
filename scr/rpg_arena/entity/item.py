class Item:
    def __init__(self, name: str, usable: bool, price: int):
        self.name = name
        self.usable = usable
        self.price = price

    def __str__(self):
        return f"{self.name}"

    def use(self, player_unit: "Fighter", game):
        pass