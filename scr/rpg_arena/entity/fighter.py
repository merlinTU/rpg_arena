from .unit_class import UnitClass
import numpy as np

from ..service.data.class_data import CLASS_DATA


class Fighter:
    def __init__(self,  player_class: UnitClass):
        self.name = None
        self.player_class = player_class
        self.level = 1

        stats = CLASS_DATA[player_class]

        self.hp = stats.base_hp
        self.strength = stats.base_str
        self.magic = stats.base_magic
        self.skill = stats.base_skill
        self.speed = stats.base_speed
        self.luck = stats.base_luck
        self.defense = stats.base_defense
        self.res = stats.base_res

        self.hp_growth = stats.growth_hp
        self.strength_growth = stats.growth_str
        self.magic_growth = stats.growth_magic
        self.skill_growth = stats.growth_skill
        self.speed_growth = stats.growth_speed
        self.luck_growth = stats.growth_luck
        self.defense_growth = stats.growth_defense
        self.res_growth = stats.growth_res

        self.gold =0
        self.weapons = []

    def level_enemy(self, level: int):
        for _ in range(level):
            self.level += 1
            self.hp += self.hp_growth
            self.strength += self.strength_growth
            self.magic += self.magic_growth
            self.skill += self.skill_growth
            self.speed += self.speed_growth
            self.luck += self.luck_growth
            self.defense += self.defense_growth
            self.res_growth += self.res_growth

        self.hp = int(self.hp)
        self.strength = int(self.strength)
        self.magic = int(self.magic)
        self.skill = int(self.skill)
        self.speed = int(self.speed)
        self.luck = int(self.luck)
        self.defense = int(self.defense)
        self.res_growth = int(self.res_growth)