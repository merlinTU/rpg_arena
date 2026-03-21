
from .stat_modifier_skill import StatModifierSkill
from .unit_class import UnitClass
import random

from ..service.data.class_data import CLASS_DATA


class Fighter:
    """
    Represents a combat unit with stats, growth rates, equipment and level progression.

    A Fighter is initialized based on a given UnitClass. The base stats and
    growth rates are loaded from CLASS_DATA. The class also provides methods
    for leveling, calculating combat statistics, and managing equipment.


    Attributes:
        name (str | None): Name of the fighter.
        player_class (UnitClass): The class of the fighter determining base stats and growth rates.
        level (int): Current level of the fighter.

        max_hp (int): Maximum health points.
        hp (int): Current health points.
        strength (int): Physical attack stat.
        magic (int): Magical attack stat.
        skill (int): Accuracy and technical ability stat.
        speed (int): Determines attack speed and avoid.
        luck (int): Influences avoid and critical avoidance.
        defense (int): Physical damage reduction stat.
        res (int): Magical damage reduction stat.

        hp_growth (float): Growth rate for HP.
        strength_growth (float): Growth rate for strength.
        magic_growth (float): Growth rate for magic.
        skill_growth (float): Growth rate for skill.
        speed_growth (float): Growth rate for speed.
        luck_growth (float): Growth rate for luck.
        defense_growth (float): Growth rate for defense.
        res_growth (float): Growth rate for resistance.

        equipped_weapon (Weapon | None): Currently equipped weapon.
        gold (int): Amount of gold the fighter owns.
        exp (int): Current experience points.
        items (list): List of items carried by the fighter.
    """
    def __init__(self,  player_class: UnitClass):
        """
        Initialize a Fighter with base stats and growth rates from the given class.

        Args:
            player_class (UnitClass): The class of the fighter, which determines
                base stats and stat growth rates.

        Returns:
            None
        """
        self.name = None
        self.player_class = player_class
        self.level = 1

        stats = CLASS_DATA[player_class]

        self.max_hp = stats.base_hp
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

        self.equipped_weapon = None
        self.gold = 500
        self.exp = 0
        self.items = []
        self.skills = []

    def level_enemy(self, level: int):
        """
        Increase the fighter's level and scale stats deterministically.

        This method is intended for enemies. Instead of using random growth,
        the stats are increased directly according to their growth values
        for each level gained.

        Args:
            level (int): The number of levels to increase.

        Returns:
            None
        """
        level -= 1
        self.level += 1 * level
        self.hp += self.hp_growth * level
        self.strength += self.strength_growth * level
        self.magic += self.magic_growth * level
        self.skill += self.skill_growth * level
        self.speed += self.speed_growth * level
        self.luck += self.luck_growth * level
        self.defense += self.defense_growth * level
        self.res += self.res_growth *level

        self.hp = int(self.hp)
        self.max_hp = self.hp
        self.strength = int(self.strength)
        self.magic = int(self.magic)
        self.skill = int(self.skill)
        self.speed = int(self.speed)
        self.luck = int(self.luck)
        self.defense = int(self.defense)
        self.res = int(self.res)

    def level_up(self):
        """
        Perform a level-up using probabilistic stat growth.

        For each stat, a random roll is compared against the corresponding
        growth rate. If the roll succeeds, the stat increases by 1.

        Returns:
            list[str]: A list containing the names of the stats that increased
            during this level-up.
        """
        increased_stats = []
        stats = [
            ("HP", "hp", "hp_growth"),
            ("Strength", "strength", "strength_growth"),
            ("Magic", "magic", "magic_growth"),
            ("Skill", "skill", "skill_growth"),
            ("Speed", "speed", "speed_growth"),
            ("Luck", "luck", "luck_growth"),
            ("Defense", "defense", "defense_growth"),
            ("Res", "res", "res_growth")
        ]

        for display_name, attr_name, growth_attr in stats:
            growth_chance = getattr(self, growth_attr)

            if random.random() < growth_chance:
                current_value = getattr(self, attr_name)
                setattr(self, attr_name, current_value + 1)
                if attr_name == "hp":
                    setattr(self, "max_hp", current_value + 1)
                increased_stats.append(display_name)

        self.level += 1
        return increased_stats

    def calc_hit(self) -> int:
        """
        Calculate the fighter's hit chance.

        The hit chance is determined by weapon accuracy, skill and luck.

        Returns:
            float: The calculated hit value.
        """
        weapon_hit = self.equipped_weapon.accuracy
        weapon_hit = weapon_hit + self.skill * 2 + self.luck // 2

        return self.check_combat_skills(weapon_hit, "hit")

    def calc_avoid(self) -> int:
        """
        Calculate the fighter's avoid value.

        Avoid is based on corrected speed and luck.

        Returns:
            float: The calculated avoid value.
        """
        avoid = self.calc_corrected_speed() * 2 + self.luck
        return self.check_combat_skills(avoid, "avoid")

    def calc_crit(self) -> int:
        """
        Calculate the fighter's critical hit chance.

        Critical chance is based on weapon crit and the fighter's skill.

        Returns:
            float: The calculated critical hit value.
        """
        weapon_crit = self.equipped_weapon.crit
        weapon_crit += self.skill // 2

        return self.check_combat_skills(weapon_crit, "crt")

    def calc_crit_avoid(self) -> int:
        """
        Calculate the fighter's resistance to critical hits.

        Returns:
            int | float: The critical avoidance value based on luck.
        """
        crt_avoid = self.check_combat_skills(self.luck, "crt_avoid")
        return crt_avoid

    def calc_corrected_speed(self) -> int:
        """
        Calculate the fighter's corrected speed considering weapon weight.

        If the weapon's weight exceeds the fighter's strength, the excess
        weight reduces the effective speed.

        Returns:
            int | float: The corrected speed value used in combat calculations.
        """
        if self.equipped_weapon is None:
            return self.speed
        weapon_weight = self.check_combat_skills(self.equipped_weapon.weight, "weight")
        cor_speed = self.speed - max(0, weapon_weight - self.strength)

        return cor_speed

    def check_combat_skills(self, value_to_modify, value_type):
        for skill in self.skills:
            if isinstance(skill, StatModifierSkill):
                value_to_modify = skill.modify_target(value_to_modify, value_type)

        return value_to_modify