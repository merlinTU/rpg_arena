from .class_enitity import Class
import numpy as np

class Fighter:
    def __init__(self, name: str, player_class: Class):
        self.name = name
        self.player_class = player_class
        self.level = 1

        self.hp = player_class.base_hp
        self.strength = player_class.base_str
        self.magic = player_class.base_magic
        self.skill = player_class.base_skill
        self.speed = player_class.base_speed
        self.luck = player_class.base_luck
        self.defense = player_class.base_defense
        self.res = player_class.base_res

    def level_up(self):
        self.level += 1
        self.hp += np.random.binomial(n=1, p=self.player_class.growth_hp)
        self.strength += np.random.binomial(n=1, p=self.player_class.growth_str)
        self.magic += np.random.binomial(n=1, p=self.player_class.growth_magic)
        self.skill += np.random.binomial(n=1, p=self.player_class.growth_skill)
        self.speed += np.random.binomial(n=1, p=self.player_class.growth_speed)
        self.luck += np.random.binomial(n=1, p=self.player_class.growth_luck)
        self.defense += np.random.binomial(n=1, p=self.player_class.growth_defense)

    def level_enemy(self, level: int):
        pass


