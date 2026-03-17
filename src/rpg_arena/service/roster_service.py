from __future__ import annotations

import random
import numpy as np
from typing import TYPE_CHECKING

from rpg_arena.entity.unit_class import UnitClass
from rpg_arena.entity.fighter import Fighter
from rpg_arena.service.data.final_boss_data import BOSS_DATA
from rpg_arena.service.data.names import fighter_names
from rpg_arena.service.data.prob_skill_data import START_SKILLS
from rpg_arena.service.data.weapon_data import WEAPONS, CLASS_WEAPON_MAP, WEAK_WEAPONS, STRONG_WEAPONS, MEDIUM_WEAPONS
from rpg_arena.service.data.item_data import NORMAL_ITEMS, RARE_ITEMS

if TYPE_CHECKING:
    from rpg_arena.service.root_service import RootService

class RosterService:
    """
    Service responsible for generating, modifying, and managing units (player and enemy).

    Attributes:
        root_service (RootService): Reference to the central RootService for access to other services.

    Methods:
        modify_unit_values(unit, type_): Adjust unit stats and growth values based on type.
        generate_unit_growth_value(type_): Generate growth rate for a unit based on type.
        generate_unit_stat_value(type_): Generate base stat value for a unit based on type.
        generate_random_unit(type_): Create a new random Fighter with a weapon.
        random_weapon(unit_class, type_): Select a weapon for a unit based on class and type.
        random_item(): Generate a random item, rare or normal.
        generate_initial_units(): Generate initial player units.
        generate_enemy_units(): Generate enemy units for the arena.
        level_enemy_unit(unit, strength): Level an enemy unit and assign gold/experience.
    """

    def __init__(self, root_service: RootService):
        """
        Initialize the RosterService with a reference to RootService.

        Args:
            root_service (RootService): Central service managing all sub-services.

        Returns:
            None
        """
        self.root_service = root_service

    def modify_unit_values(self, unit: "Fighter", type_: int) -> "Fighter":
        """
        Modify the unit's stats and growth values according to its type.

        Args:
            unit (Fighter): Unit to modify.
            type_ (int): Type of unit (1=player, 2=weaker enemy, 3=stronger enemy).

        Returns:
            Fighter: Modified unit.
        """
        unit.hp += self.generate_unit_stat_value(type_) + 15
        unit.max_hp = unit.hp
        unit.strength += self.generate_unit_stat_value(type_)
        unit.magic += self.generate_unit_stat_value(type_)
        unit.skill += self.generate_unit_stat_value(type_)
        unit.speed += self.generate_unit_stat_value(type_)
        unit.luck += self.generate_unit_stat_value(type_)
        unit.defense += self.generate_unit_stat_value(type_)
        unit.res += self.generate_unit_stat_value(type_)

        unit.hp_growth += self.generate_unit_growth_value(type_) + 0.3
        unit.strength_growth += self.generate_unit_growth_value(type_)
        unit.magic_growth += self.generate_unit_growth_value(type_)
        unit.skill_growth += self.generate_unit_growth_value(type_)
        unit.speed_growth += self.generate_unit_growth_value(type_)
        unit.luck_growth += self.generate_unit_growth_value(type_)
        unit.defense_growth += self.generate_unit_growth_value(type_)
        unit.res_growth += self.generate_unit_growth_value(type_)

        # set negative attributes to 0
        for attr, value in vars(unit).items():
            if isinstance(value, (int, float)) and value < 0:
                setattr(unit, attr, 0)
        return unit

    @staticmethod
    def generate_unit_growth_value(type_: int) -> float:
        """
        Generate a random growth rate for a unit based on type.

        Args:
            type_ (int): Type of unit (1=player, 2=weaker enemy, 3=stronger enemy).

        Returns:
            float: Growth rate between 0.0 and 1.0.
        """
        match type_:
            # player unit and normal enemy
            case 1:
                range_ = range(1, 11)
                center = 0.25
            # weak enemy
            case 2:
                range_ = range(0, 6)
                center = 0.10
            # normal enemy
            case 3:
                range_ = range(1, 8)
                center = 0.20
            # strong enemy
            case 4:
                range_ = range(5, 12)
                center = 0.35
            case _:
                range_ = range(1, 11)
                center = 0.25

        possible_growths = [i * 0.05 for i in range_]
        weights = [np.exp(-abs(value - center) / 1.7) for value in possible_growths]
        return random.choices(possible_growths, weights=weights, k=1)[0]

    @staticmethod
    def generate_unit_stat_value(type_: int) -> int:
        """
        Generate a base stat value for a unit based on its type.

        Args:
            type_ (int): Type of unit (1=player, 2=weaker enemy, 3=stronger enemy).

        Returns:
            int: Base stat value.
        """
        match type_:
            # player unit
            case 1:
                possible_values = list(range(3, 7))
                center = 5
            # weak enemy
            case 2:
                possible_values = list(range(0, 3))
                center = 3
            # normal enemy
            case 3:
                possible_values = list(range(2, 5))
                center = 3
            # strong enemy
            case 4:
                possible_values = list(range(5, 9))
                center = 6
            case _:
                possible_values = list(range(3, 7))
                center = 5

        # try to use exp distribution to make more balance; more extreme stats should be less likely
        weights = [np.exp(-abs(value - center) / 1.7) for value in possible_values]
        return random.choices(possible_values, weights=weights, k=1)[0]

    def generate_random_unit(self, type_: int) -> "Fighter":
        """
        Generate a random Fighter unit with appropriate weapon.

        Args:
            type_ (int): Type of unit (1=player, 2=weaker enemy, 3=stronger enemy).

        Returns:
            Fighter: New randomly generated Fighter unit.
        """
        # exclude boss classes for player and non-boss enemies
        excluded_classes = {UnitClass.MAGEKNIGHT, UnitClass.SAGE, UnitClass.WARRIOR}
        available_classes = [cls for cls in UnitClass if cls not in excluded_classes]
        random_class = random.choice(available_classes)

        new_fighter = Fighter(random_class)
        new_fighter = self.modify_unit_values(new_fighter, type_)
        random_weapon = self.random_weapon(random_class, type_)
        new_fighter.items.append(random_weapon)
        new_fighter.equipped_weapon = random_weapon
        return new_fighter

    def random_weapon(self, unit_class: "UnitClass", type_: int):
        """
        Generate a random weapon for a unit based on class and type.

        Args:
            unit_class (UnitClass): Unit's class.
            type_ (int): Type of unit (1=player, 2=weaker enemy, 3=stronger enemy).

        Returns:
            Weapon: Randomly selected weapon.
        """
        round_ = self.root_service.current_game.round
        allowed_types = CLASS_WEAPON_MAP[unit_class]
        possible_weapons = [w for w in WEAPONS.values() if w.weapon_type in allowed_types]

        match type_:
            # normal unit
            case 1 | 3:
                base_strong = 0.05
                base_medium = 0.25
            # weak unit
            case 2:
                base_strong = 0
                base_medium = 0.05
            # strong enemy
            case 4:
                base_strong= 0.2
                base_medium = 0.5
            case _:
                base_strong = 0.05
                base_medium = 0.25

        scale = min(round_ / 20, 1)
        strong_chance = base_strong + scale * 0.15
        medium_chance = base_medium + scale * 0.15
        roll = random.random()

        if roll < strong_chance:
            weapons = [w for w in possible_weapons if w in STRONG_WEAPONS]
        elif roll < strong_chance + medium_chance:
            weapons = [w for w in possible_weapons if w in MEDIUM_WEAPONS]
        else:
            weapons = [w for w in possible_weapons if w in WEAK_WEAPONS]

        return random.choice(weapons).copy()

    @staticmethod
    def random_item():
        """
        Generate a random item (normal or rare).

        Returns:
            Item: A copy of a randomly selected item.
        """
        if random.random() < 0.05:
            item = random.choice(RARE_ITEMS)
        else:
            item = random.choice(NORMAL_ITEMS)
        return item.copy()

    def generate_initial_units(self) -> list["Fighter"]:
        """
        Generate 5 initial player units with names, weapons, and items.

        Returns:
            list[Fighter]: List of 5 initialized player units.
        """
        units = [self.generate_random_unit(1) for _ in range(5)]
        names = random.sample(fighter_names, 5)

        for i in range(5):
            units[i].name = names[i]
            self.give_random_skill(units[i])
            if random.random() < 0.15:
                units[i].items.append(self.random_weapon(units[i].player_class, type_=1))
            if random.random() < 0.15:
                units[i].items.append(self.random_item())
            if random.random() < 0.5:
                units[i].items.append(self.random_item())
        return units

    @staticmethod
    def give_random_skill(unit):
        if random.random() < 0.2:
            unit.skills.append(random.choice(START_SKILLS))

    def generate_enemy_units(self) -> list["Fighter"]:
        """
        Generate 3 enemy units: easy, normal, and hard.

        Returns:
            list[Fighter]: List of 3 enemy units.
        """
        easy_enemy = self.generate_random_unit(2)
        normal_enemy = self.generate_random_unit(3)
        hard_enemy = self.generate_random_unit(4)

        units = [easy_enemy, normal_enemy, hard_enemy]
        for i, unit in enumerate(units):
            self.level_enemy_unit(unit, i)
            unit.name = "Gladiator"
        return units

    def level_enemy_unit(self, unit: Fighter, strength: int):
        """
        Level an enemy unit based on strength and current round, assign gold and experience.

        Args:
            unit (Fighter): Enemy unit to level.
            strength (int): Strength tier (0=easy, 1=medium, 2=hard).

        Returns:
            None
        """
        round_ = self.root_service.current_game.round

        match strength:
            # easy enemy
            case 0:
                level = max(1, round_ - 1)
                if round_ > 1:
                    unit.level_enemy(level)
                # scale gold slowly
                base_gold = 50 + round_ * 20
                unit.gold = max(50, int(base_gold + random.normalvariate(0, base_gold * 0.1)))
                unit.exp = 50

            # medium enemy
            case 1:
                level = max(1, round_ + random.randint(-1, 1))
                unit.level_enemy(level)
                base_gold = 100 + round_ * 50
                unit.gold = max(100, int(base_gold + random.normalvariate(0, base_gold * 0.05)))
                unit.exp = 100

            # strong enemy
            case 2:
                level = max(1, round_ + random.randint(1, 4))
                unit.level_enemy(level)
                base_gold = 200 + round_ * 80
                unit.gold = max(200, int(base_gold + random.normalvariate(0, base_gold * 0.1)))
                unit.exp = 150

    def generate_boss_unit(self):
        """
        Generates a random boss as a Fighter object.

        Randomly selects an entry from the global BOSS_DATA list and creates
        a Fighter instance from it, including all stats, items, and the
        currently equipped weapon.

        Returns:
            Fighter: A fully configured boss as a Fighter object.
        """
        random_boss = random.randint(0, 2)

        boss = self.create_fighter_from_dict(BOSS_DATA[random_boss])
        return boss

    @staticmethod
    def create_fighter_from_dict(data: dict):
        """
        Creates a Fighter from a dictionary containing boss or unit data.

        This function initializes a Fighter with the specified UnitClass and
        then overwrites all base stats, level, items, and the currently
        equipped weapon according to the values in the dictionary.

        Args:
            data (dict): A dictionary containing the Fighter's data

        Returns:
            Fighter: A fully configured Fighter with stats, inventory, and
                     equipped weapon.
        """

        fighter = Fighter(player_class=data["unit_class"])

        fighter.name = data["name"]
        fighter.level = data["level"]
        fighter.max_hp = data["hp"]
        fighter.hp = data["hp"]
        fighter.strength = data["strength"]
        fighter.magic = data["magic"]
        fighter.skill = data["skill"]
        fighter.speed = data["speed"]
        fighter.luck = data["luck"]
        fighter.defense = data["defense"]
        fighter.res = data["res"]
        fighter.gold = data["gold"]

        fighter.items = data.get("items", [])
        fighter.equipped_weapon = data.get("equipped_weapon", None)

        return fighter
