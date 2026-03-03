from rpg_arena.entity.unit_class import UnitClass
from rpg_arena.entity.fighter import Fighter
from rpg_arena.service.data.names import fighter_names, enemy_names
from rpg_arena.service.data.weapon_data import WEAPONS, CLASS_WEAPON_MAP
import random

class RosterService:
    def __init__(self, root_service: "RootService"):
        self.root_service = root_service

    def modify_unit_values(self, unit: "Fighter", is_enemy: bool):

        unit.hp += self.generate_unit_stat_value() + 15
        unit.max_hp = unit.hp
        unit.strength += self.generate_unit_stat_value()
        unit.magic += self.generate_unit_stat_value()
        unit.skill += self.generate_unit_stat_value()
        unit.speed += self.generate_unit_stat_value()
        unit.luck += self.generate_unit_stat_value()
        unit.defense += self.generate_unit_stat_value()
        unit.res += self.generate_unit_stat_value()

        unit.hp_growth += self.generate_unit_growth_value()
        unit.strength_growth += self.generate_unit_growth_value()
        unit.magic_growth += self.generate_unit_growth_value()
        unit.skill_growth += self.generate_unit_growth_value()
        unit.speed_growth += self.generate_unit_growth_value()
        unit.luck_growth += self.generate_unit_growth_value()
        unit.defense_growth += self.generate_unit_growth_value()
        unit.res_growth += self.generate_unit_growth_value()

        return unit

    def generate_unit_growth_value(self):

        # growths should be random between 0.05 and 0.5; but with a tendency to the center of 0.25
        possible_growths = [i * 0.05 for i in range(1, 11)]

        weights = []
        for value in possible_growths:
            distance = abs(value - 0.25)
            weight = 1 / (1 + distance * 10)
            weights.append(weight)

        return random.choices(possible_growths, weights=weights, k=1)[0]

    def generate_unit_stat_value(self):

        # stats should be random between 0 and 15; but with a tendency to 5
        possible_growths = [i * 0.05 for i in range(1, 11)]

        possible_values = list(range(0, 16))  # 0 bis 15
        weights = []
        for value in possible_values:
            # Abstand zur Mitte (5)
            distance = abs(value - 5)

            weight = 1 / (1 + distance)
            weights.append(weight)

        return random.choices(possible_values, weights=weights, k=1)[0]

    def generate_random_unit(self, is_enemy: bool):
        random_class = random.choice(list(UnitClass))
        new_fighter = Fighter(random_class)
        new_fighter = self.modify_unit_values(new_fighter, is_enemy)

        random_weapon = self.random_weapon(random_class)
        new_fighter.items.append(random_weapon)
        new_fighter.equipped_weapon = random_weapon

        return new_fighter

    def random_weapon(self, unit_class: "Class"):
        allowed_types = CLASS_WEAPON_MAP[unit_class]

        possible_weapons = [
            w for w in WEAPONS.values() if w.weapon_type in allowed_types
        ]

        return random.choice(possible_weapons)

    def generate_initial_units(self):
        units = [self.generate_random_unit(is_enemy= False) for _ in range(5)]
        names = random.sample(fighter_names, 5)
        for i in range(0,5):
            units[i].name = names[i]
        return units

    def generate_enemy_units(self):
        units = [self.generate_random_unit(is_enemy=True) for _ in range(3)]
        names = random.sample(fighter_names, 3)
        for i in range(0,3):
            self.level_enemy_unit(units[i], i)
            units[i].name = "Gladiator"
        return units

    def level_enemy_unit(self, unit: Fighter, strength: int):
        round_ = self.root_service.current_game.round

        match strength:
            case 0:
                level = round(random.uniform(1, round_))
                unit.level_enemy(level)
                base_gold = round_ * 100
                unit.gold = max(50, int(base_gold  + random.normalvariate(0, base_gold * 0.1)))
            case 1:
                level = round(random.uniform(round_, round_ + 2))
                unit.level_enemy(level)
                base_gold = round_ * 250
                unit.gold = max(250, int(base_gold + random.normalvariate(0, base_gold * 0.05)))
            case 2:
                level = round(random.uniform(round_ + 2, round_ + 4))
                unit.level_enemy(level)
                base_gold = round_ * 500
                unit.gold = max(500, int(base_gold + random.normalvariate(0, base_gold * 0.1)))
