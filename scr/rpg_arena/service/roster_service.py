from rpg_arena.entity.unit_class import UnitClass
from rpg_arena.entity.fighter import Fighter
from rpg_arena.service.data.names import fighter_names, enemy_names
from rpg_arena.service.data.weapon_data import WEAPONS, CLASS_WEAPON_MAP, WEAK_WEAPONS, STRONG_WEAPONS, MEDIUM_WEAPONS
import random

class RosterService:
    def __init__(self, root_service: "RootService"):
        self.root_service = root_service

    def modify_unit_values(self, unit: "Fighter", type_: int):

        unit.hp += self.generate_unit_stat_value(type_) + 15
        unit.max_hp = unit.hp
        unit.strength += self.generate_unit_stat_value(type_)
        unit.magic += self.generate_unit_stat_value(type_)
        unit.skill += self.generate_unit_stat_value(type_)
        unit.speed += self.generate_unit_stat_value(type_)
        unit.luck += self.generate_unit_stat_value(type_)
        unit.defense += self.generate_unit_stat_value(type_)
        unit.res += self.generate_unit_stat_value(type_)

        unit.hp_growth += self.generate_unit_growth_value(type_)
        unit.strength_growth += self.generate_unit_growth_value(type_)
        unit.magic_growth += self.generate_unit_growth_value(type_)
        unit.skill_growth += self.generate_unit_growth_value(type_)
        unit.speed_growth += self.generate_unit_growth_value(type_)
        unit.luck_growth += self.generate_unit_growth_value(type_)
        unit.defense_growth += self.generate_unit_growth_value(type_)
        unit.res_growth += self.generate_unit_growth_value(type_)

        return unit

    def generate_unit_growth_value(self, type_: int) -> float:
        """
        Generate a random growth value based on type:
        type_ == 1: player units (0.05 - 0.50, tendency to 0.25)
        type_ == 2: weaker enemies (0.00 - 0.25, tendency to 0.15)
        type_ == 3: stronger enemies (0.25 - 0.70, tendency to 0.35)
        """
        match type_:
            case 1:
                range_ = range(1, 11)  # 0.05 .. 0.50
                center = 0.25
            case 2:
                range_ = range(0, 6)  # 0.00 .. 0.25
                center = 0.15
            case 3:
                range_ = range(5, 15)  # 0.25 .. 0.70
                center = 0.35
            case _:
                range_ = range(1, 11)
                center = 0.25

        possible_growths = [i * 0.05 for i in range_]

        weights = []
        for value in possible_growths:
            distance = abs(value - center)
            weight = 1 / (1 + distance * len(range_))
            weights.append(weight)

        return random.choices(possible_growths, weights=weights, k=1)[0]

    def generate_unit_stat_value(self, type_: int) -> int:
        """
        Generate a random base stat value for a unit.
        type_ == 1: player units (0-15, tendency to 5)
        type_ == 2: weaker enemies (0-10, tendency to 3)
        type_ == 3: stronger enemies (5-15, tendency to 8)
        """
        match type_:
            case 1:
                possible_values = list(range(0, 16))
                center = 5
            case 2:
                possible_values = list(range(0, 11))
                center = 3
            case 3:
                possible_values = list(range(5, 16))
                center = 8
            case _:
                possible_values = list(range(0, 16))
                center = 5

        weights = [1 / (1 + abs(value - center)) for value in possible_values]

        return random.choices(possible_values, weights=weights, k=1)[0]

    def generate_random_unit(self, type_: int):
        random_class = random.choice(list(UnitClass))
        new_fighter = Fighter(random_class)
        new_fighter = self.modify_unit_values(new_fighter, type_)

        random_weapon = self.random_weapon(random_class, type_)
        new_fighter.items.append(random_weapon)
        new_fighter.equipped_weapon = random_weapon

        return new_fighter

    def random_weapon(self, unit_class: "Class", type_: int):
        round_ = self.root_service.current_game.round
        allowed_types = CLASS_WEAPON_MAP[unit_class]

        possible_weapons = [
            w for w in WEAPONS.values() if w.weapon_type in allowed_types
        ]

        match type_:
            case 1:
                modificator = round_
            case 2:
                modificator = round_ * 2
            case 3:
                modificator = round_ * 0.25
            case _:
                modificator = round_

        if random.random() < 0.05 * modificator:
            weapons = [w for w in possible_weapons if w in STRONG_WEAPONS]

        elif random.random() < 0.25 * modificator:
            weapons = [w for w in possible_weapons if w in MEDIUM_WEAPONS]
        else:
            weapons = [w for w in possible_weapons if w in WEAK_WEAPONS]

        return random.choice(weapons)

    def generate_initial_units(self):
        units = [self.generate_random_unit(1) for _ in range(5)]
        names = random.sample(fighter_names, 5)
        for i in range(0,5):
            units[i].name = names[i]
        return units

    def generate_enemy_units(self):
        easy_enemy = self.generate_random_unit(2)
        normal_enemy = self.generate_random_unit(1)
        hard_enemy =self.generate_random_unit(3)

        units = [easy_enemy, normal_enemy, hard_enemy]
        for i in range(0,3):
            self.level_enemy_unit(units[i], i)
            units[i].name = "Gladiator"
        return units

    def level_enemy_unit(self, unit: Fighter, strength: int):
        round_ = self.root_service.current_game.round

        match strength:
            case 0:
                level = round_ - 1 if round_ > 1 else round_
                unit.level_enemy(level)
                base_gold = round_ * 100
                unit.gold = max(50, int(base_gold  + random.normalvariate(0, base_gold * 0.1)))
                unit.exp = 50
            case 1:
                level = round(random.uniform(round_, round_ + 2))
                unit.level_enemy(level)
                base_gold = round_ * 250
                unit.gold = max(250, int(base_gold + random.normalvariate(0, base_gold * 0.05)))
                unit.exp = 100
            case 2:
                level = round(random.uniform(round_ + 2, round_ + 4))
                unit.level_enemy(level)
                base_gold = round_ * 500
                unit.gold = max(500, int(base_gold + random.normalvariate(0, base_gold * 0.1)))
                unit.exp = 150
