from .class_enitity import Class
import numpy as np

class Fighter:
    def __init__(self,  player_class: Class):
        self.name = None
        self.player_class = player_class
        self.level = 1

        self.hp = 0
        self.strength = 0
        self.magic = 0
        self.skill = 0
        self.speed = 0
        self.luck = 0
        self.defense = 0
        self.res = 0

        self.hp_growth = 0
        self.strength_growth = 0
        self.magic_growth = 0
        self.skill_growth = 0
        self.speed_growth = 0
        self.luck_growth = 0
        self.defense_growth = 0
        self.res_growth = 0

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