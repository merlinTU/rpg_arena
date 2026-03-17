from rpg_arena.entity import WeaponType
from rpg_arena.entity.skill import Skill


class WeaponSkill(Skill):
    def __init__(self, name, price, weapon_type : WeaponType, description):
        super().__init__(name, price, description)
        self.weapon_type = weapon_type

    def __str__(self, index=None):
        """
        Return a formatted string for displaying the weapon skill in the shop.

        Args:
            index (int | None, optional): Optional index number before the skill name.

        Returns:
            str: Formatted string with skill info.
        """
        index_str = f"{index}) " if index is not None else ""
        name_width = 20 - len(index_str)
        stat_width = 6

        return (
            f"{index_str}{self.name:<{name_width}} | "
            f"Price: {self.price:>{stat_width}} | "
            f"{getattr(self, 'description', '')}")
