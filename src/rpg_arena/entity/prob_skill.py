from rpg_arena.entity.skill import Skill
import random


class ProbSkill(Skill):
    def __init__(self, name, price, target, value, type_, description):
        super().__init__(name, price, description)
        self.target = target
        self.type_ = type_ # at attack or defense
        self.value = value

    def __str__(self, index=None):
        """
        Return a formatted string for displaying the skill in the shop.

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
            f"{getattr(self, 'description', '')}"
        )

    def activate(self, value_to_modify, target_type, attack_type, unit):
        if target_type != self.target or attack_type != self.type_:
            return value_to_modify

        if random.random() < unit.skill / 100:
            return value_to_modify // self.value
        else:
            return value_to_modify