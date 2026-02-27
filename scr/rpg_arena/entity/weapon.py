from .weapon_type import WeaponType

class Weapon:
    def __init__(self,
                 name: str,
                 weapon_type: WeaponType,
                 strength: int,
                 accuracy: int,
                 uses: int,
                 crit: int,
                 weight: float,
                 price: int):
        self.name = name
        self.weapon_type = weapon_type
        self.strength = strength
        self.accuracy = accuracy
        self.uses = uses
        self.crit = crit
        self.weight = weight
        self.price = price

    def __str__(self):
        return (f"{self.name} ({self.weapon_type.name}) - STR:{self.strength} "
                f"ACC:{self.accuracy} CRIT:{self.crit} USES:{self.uses} "
                f"WGT:{self.weight} PRICE:{self.price}")