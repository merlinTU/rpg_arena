import time

from rpg_arena.entity.prob_skill import ProbSkill
from rpg_arena.entity.weapon_type import WeaponType
from rpg_arena.log.arena_service_printer import ArneaServicePrinter
from rpg_arena.service.arena_action_service import ArenaActionService
import random

class ArenaService:
    """
    Service class responsible for managing arena battles between the player and enemy units.

    Attributes:
        root_service (RootService): Reference to the root service managing all sub-services.
        printer (ArneaServicePrinter): Utility to print arena state and updates.
        action_service (ArenaActionService): Service handling player and enemy round decisions.
        enemy (Fighter | None): Reference to the current enemy unit in battle.
        continue_fight (bool | str): Controls whether the fight continues or if a surrender occurred.

    """

    def __init__(self, root_service: "RootService"):
        """
        Initialize ArenaService with references to the root service, printer, and action service.

        Args:
            root_service (RootService): Central service managing all sub-services.

        Returns:
            None
        """
        self.root_service = root_service
        self.printer = ArneaServicePrinter(root_service)
        self.action_service = ArenaActionService(root_service)

        self.enemy: "Fighter" = None
        self.continue_fight = True

    def start_arena(self, enemy: "Fighter"):
        """
        Start an arena battle with the given enemy unit.

        Args:
            enemy (Fighter): The enemy unit to fight against.

        Returns:
            None
        """
        self.enemy = enemy
        self.arena_simulation(self.root_service.current_game.player, enemy)

    def arena_simulation(self, player_unit: "Fighter", enemy_unit: "Fighter"):
        """
        Run the full arena simulation loop until one unit is defeated or player surrenders.

        Handles turn order, round simulation, level-ups, gold and experience rewards.

        Args:
            player_unit (Fighter): The player's unit participating in the arena.
            enemy_unit (Fighter): The enemy unit participating in the arena.

        Returns:
            None
        """
        self.printer.print_at_start_round()
        attacker, defender = player_unit, enemy_unit
        self.printer.print_after_start_round(attacker, defender)

        while self.continue_fight and self.continue_fight != "surrender":
            if attacker == player_unit:
                self.action_service.make_player_round_decision()
            else:
                self.action_service.make_enemy_round_decision()

            # Next fighter's turn
            if self.continue_fight and self.continue_fight != "surrender":
                attacker, defender = defender, attacker
                self.printer.print_after_start_round(attacker, defender)

        if self.continue_fight == "surrender":
            self.printer.print_after_surrender()
            player_unit.hp = player_unit.max_hp
            self.root_service.current_game.round += 1
            self.continue_fight = True
            self.root_service.camp_service.open_camp()
            return

        # Determine winner and loser
        winner = player_unit if player_unit.hp > 0 else enemy_unit
        loser = enemy_unit if player_unit.hp > 0 else player_unit
        self.printer.print_after_arena_simulation(winner, loser)

        if winner == player_unit:
            # Give player gold and experience
            player_unit.gold += enemy_unit.gold
            player_unit.exp += enemy_unit.exp
            player_unit.hp = player_unit.max_hp
            self.continue_fight = True
            self.root_service.current_game.round += 1
            self.printer.print_at_end_fight(enemy_unit.gold, enemy_unit.exp)

            while player_unit.exp >= 100:
                player_unit.exp -= 100
                level_up_stats = player_unit.level_up()
                self.printer.print_level_up(level_up_stats)

            if self.root_service.current_game.round == self.root_service.current_game.end_round:
                self.root_service.game_service.end_game()
            else:
                self.root_service.camp_service.open_camp()
        else:
            return

    def make_fight_round(self, first_unit: "Fighter", second_unit: "Fighter"):
        """
        Execute a single combat round, handling attacks based on speed advantage.

        Args:
            first_unit (Fighter): The first unit in the combat round.
            second_unit (Fighter): The second unit in the combat round.

        Returns:
            int | None: Returns 1 if the round completed, None if the fight ended.
        """
        self.make_attack(first_unit, second_unit, 1)
        first_unit_weapon_broke = self.check_weapon_destroyed(first_unit)


        if second_unit.hp <= 0:
            return self.end_fight()

        elif second_unit.hp > 0 and second_unit.equipped_weapon is not None:
            self.make_attack(second_unit, first_unit, 3)
            second_unit_weapon_broke = self.check_weapon_destroyed(second_unit)

        if second_unit.equipped_weapon is None:
            print(f"> {second_unit.name} can't do anything.")
            second_unit_weapon_broke = False

        if first_unit.hp == 0:
            return self.end_fight()

        if self.check_sec_attack(first_unit, second_unit) and first_unit_weapon_broke:
            self.make_attack(first_unit, second_unit, 2)
            self.check_weapon_destroyed(first_unit)

        elif self.check_sec_attack(second_unit, first_unit) and second_unit_weapon_broke:
            self.make_attack(second_unit, first_unit, 2)
            self.check_weapon_destroyed(second_unit)

        if first_unit.hp == 0 or second_unit.hp == 0:
            return self.end_fight()

        return 1

    def check_sec_attack(self, unit1, unit2):
        """
        Calculates weather unit 1 can strike for a second time.

        Returns:
                second_attack (bool)
        """
        return unit1.calc_corrected_speed() > unit2.calc_corrected_speed() + 5

    def check_weapon_destroyed(self, unit: "Fighter"):
        """
        checks weather a weapon broke during the fight.

        Returns:
            continue_fight (bool): Determines if the fighter can make an attack.
        """
        weapon = unit.equipped_weapon
        continue_fight = True

        if weapon is None:
            print(f"> {unit.name} can't do anything.")
            continue_fight = False
            return continue_fight

        if weapon.uses == 0:
            weapon.break_weapon(unit)
            continue_fight = False
            print(f"> {unit.name}'s", weapon.name, "broke.")
            time.sleep(1)
        return continue_fight

    def end_fight(self):
        """
        End the current fight by setting `continue_fight` to False.

        Returns:
            None
        """
        self.continue_fight = False

    def make_attack(self, attacker: "Fighter", defender: "Fighter", status: int):
        """
        Execute a single attack from attacker to defender, considering hit, crit, and weapon.

        Args:
            attacker (Fighter): Attacking unit.
            defender (Fighter): Defending unit.
            status (int): Indicator of attack order (used for printing).

        Returns:
            None
        """
        hit_chance = self.caluclate_hit_chance(attacker, defender)
        damage = self.calculate_damage_with_skill(attacker, defender)
        rand_no = random.random()
        has_hit = rand_no < hit_chance

        if not has_hit:
            self.printer.print_after_make_attack(attacker, defender, has_hit, False, damage, status)
            return

        crit_chance = self.caluclate_crit_chance(attacker, defender)
        has_crit = random.random() < crit_chance

        if has_crit:
            damage *= 3

        defender.hp -= damage
        defender.hp = max(0, defender.hp)
        attacker.equipped_weapon.uses -= 1

        self.printer.print_after_make_attack(attacker, defender, has_hit, has_crit, damage, status)

    def caluclate_hit_chance(self, attacker: "Fighter", defender: "Fighter"):
        """
        Calculate the hit probability of an attack, considering speed, avoidance, and weapon triangle.

        Args:
            attacker (Fighter): The attacking unit.
            defender (Fighter): The defending unit.

        Returns:
            float: Hit probability as a value between 0.0 and 1.0.
        """
        hit_chance = attacker.calc_hit() - defender.calc_avoid()

        match self.check_weapon_vantage(attacker.equipped_weapon, defender.equipped_weapon):
            case 1:
                hit_chance += 20
            case 2:
                hit_chance -= 20
            case 3:
                pass

        hit_chance = max(0, min(100, hit_chance))
        return hit_chance / 100

    def caluclate_crit_chance(self, attacker: "Fighter", defender: "Fighter"):
        """
        Calculate the critical hit probability of an attack.

        Args:
            attacker (Fighter): The attacking unit.
            defender (Fighter): The defending unit.

        Returns:
            float: Critical hit probability as a value between 0.0 and 1.0.
        """
        crit_chance = max(0, min(100, attacker.calc_crit() - defender.calc_crit_avoid()))
        return crit_chance / 100

    def calculate_damage(self, attacker: "Fighter", defender: "Fighter"):
        """
        Calculate the damage dealt from attacker to defender, considering weapon type. Without skills.
            Args:
                attacker (Fighter): The attacking unit.
                defender (Fighter): The defending unit.
            Returns:
                int: Damage to apply to the defender's HP.
        """
        weapon = attacker.equipped_weapon

        if weapon.weapon_type == WeaponType.MAGIC:
            return max(0, weapon.strength + attacker.magic - defender.res)
        else:
            return max(0, weapon.strength + attacker.strength - defender.defense)

    def calculate_damage_with_skill(self, attacker: "Fighter", defender: "Fighter"):
        """
            Calculate the final damage dealt from the attacker to the defender, taking the skills into account.
            Args:
                attacker (Fighter): The unit performing the attack. Skills of this unit may increase
                                     attack or modify defender stats.
                defender (Fighter): The unit being attacked. Skills of this unit may reduce incoming damage.

            Returns:
                int: The calculated damage to apply to the defender's HP. Ensures damage is at least 0.
            """
        weapon = attacker.equipped_weapon

        # base values, that are modified by the skills
        attacker_attack = weapon.strength + attacker.strength
        attacker_magic = weapon.strength + attacker.magic
        defender_def = defender.defense
        defender_res = defender.res

        # first check attacker skills
        for skill in attacker.skills:
            if not isinstance(skill, ProbSkill):
                continue

            # boost attack values
            if weapon.weapon_type == WeaponType.MAGIC:
                new_attacker_magic = skill.activate(attacker_magic, "magic", "attacker", attacker)
                if new_attacker_magic != attacker_magic:
                    self.printer.print_after_prob_skill(attacker, skill.name)
                attacker_magic = new_attacker_magic

            else:
                new_attacker_attack = skill.activate(attacker_attack, "str", "attacker", attacker)
                if new_attacker_attack != attacker_attack:
                    self.printer.print_after_prob_skill(attacker, skill.name)
                attacker_attack = new_attacker_attack

            # attacker changes enemy defense stats
            if weapon.weapon_type == WeaponType.MAGIC:
                new_defender_res = skill.activate(defender_res, "res", "attacker", attacker)
                if new_defender_res != defender_res:
                    self.printer.print_after_prob_skill(attacker, skill.name)
                defender_res = new_defender_res
            else:
                new_defender_def = skill.activate(defender_def, "def", "attacker", attacker)
                if new_defender_def != defender_def:
                    self.printer.print_after_prob_skill(attacker, skill.name)
                defender_def = new_defender_def

        # skills of the defender
        for skill in defender.skills:
            if not isinstance(skill, ProbSkill):
                continue

            # reduce attack value of the attacker
            if weapon.weapon_type == WeaponType.MAGIC:
                new_attacker_magic = skill.activate(attacker_magic, "magic", "defender", defender)
                if new_attacker_magic != attacker_magic:
                    self.printer.print_after_prob_skill(defender, skill.name)
                attacker_magic = new_attacker_magic
            else:
                new_attacker_attack = skill.activate(attacker_attack, "str", "defender", defender)
                if new_attacker_attack != attacker_attack:
                    self.printer.print_after_prob_skill(defender, skill.name)
                attacker_attack = new_attacker_attack

        # calculate damage
        if weapon.weapon_type == WeaponType.MAGIC:
            damage = attacker_magic - defender_res
        else:
            damage = attacker_attack - defender_def

        return max(0, int(damage))

    def check_weapon_vantage(self, attacker_weapon, defender_weapon):
        """
        Determine weapon triangle advantage.

        Args:
            attacker_weapon (Weapon): Attacker's equipped weapon.
            defender_weapon (Weapon): Defender's equipped weapon.

        Returns:
            int:
                1 if attacker has advantage (+20 hit)
                2 if defender has advantage (-20 hit)
                3 if no advantage
        """
        if defender_weapon is None or attacker_weapon is None:
            return 3
        weapon_triangle = {
            WeaponType.SWORD: WeaponType.AXE,
            WeaponType.AXE: WeaponType.LANCE,
            WeaponType.LANCE: WeaponType.SWORD,
            WeaponType.BOW: None,
            WeaponType.MAGIC: None
        }

        attacker = attacker_weapon.weapon_type
        defender = defender_weapon.weapon_type

        if weapon_triangle.get(attacker) == defender:
            return 1
        elif weapon_triangle.get(defender) == attacker:
            return 2
        else:
            return 3


