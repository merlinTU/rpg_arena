from rpg_arena.entity.unit_class import UnitClass
from rpg_arena.entity.fighter import Fighter
from rpg_arena.service.data.names import fighter_names
import random

class RosterService:
    def __init__(self, root_service: "RootService"):
        self.root_service = root_service


    def modify_unit_values(self, unit: "Fighter", is_enemy: bool):
        for attr, value in vars(unit.player_class).items():
            # Base
            if attr.startswith("base_") and isinstance(value, int):
                delta = random.choice([-1, 0, 1])
                setattr(unit.player_class, attr, value + delta)
            # Growth
            elif attr.startswith("growth_") and isinstance(value, (float, int)):
                if is_enemy:
                    delta = random.uniform(-0.1, 0)
                else:
                    delta = random.uniform(-0.05, 0.15)
                new_value = max(0.0, min(1.0, value + delta))
                setattr(unit.player_class, attr, new_value)

        return unit

    def generate_random_unit(self, is_enemy: bool):
        random_class = random.choice(list(UnitClass))
        new_fighter = Fighter(random_class)
        new_fighter = self.modify_unit_values(new_fighter, is_enemy)

        return new_fighter

    def generate_initial_units(self):
        units = [self.generate_random_unit(is_enemy= False) for _ in range(5)]
        names = random.sample(fighter_names, 5)
        for i in range(0,5):
            units[i].name = names[i]
        return units

    def generate_enemy_units(self):
        units = [self.generate_random_unit(is_enemy=True) for _ in range(3)]
        for i in range(1,3):
            self.level_enemy_unit(units[i], i)
        return units

    def level_enemy_unit(self, unit: Fighter, strength: int):
        round_ = self.root_service.current_game.round

        match strength:
            case 1:
                level = round(random.uniform(1, round_))
                unit.level_enemy(level)
            case 2:
                level = round(random.uniform(round_, round_ + 2))
                unit.level_enemy(level)
            case 3:
                level = round(random.uniform(round_ + 2, round_ + 4))
                unit.level_enemy(level)
