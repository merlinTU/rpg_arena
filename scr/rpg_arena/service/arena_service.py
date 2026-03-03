from rpg_arena.entity.weapon_type import WeaponType
from rpg_arena.log.arnea_service_printer import ArneaServicePrinter
from rpg_arena.service.arena_action_service import ArenaActionService
import random


class ArenaService:
    def __init__(self, root_service: "RootService"):
        self.root_service = root_service
        self.printer = ArneaServicePrinter(root_service)
        self.action_service = ArenaActionService(root_service)

        self.enemy: "Fighter" = None
        self.continue_fight = True

    def start_arena(self, enemy: "Fighter"):
        self.enemy = enemy
        self.arena_simulation(self.root_service.current_game.player, enemy)

    def arena_simulation(self, player_unit: "Fighter", enemy_unit: "Fighter"):
        self.printer.print_at_start_round()

        attacker, defender = player_unit, enemy_unit

        self.printer.print_after_start_round(attacker, defender)

        while self.continue_fight:
            if attacker == player_unit:
                self.action_service.make_player_round_decision()
            else:
                self.action_service.make_enemy_round_decision()

            # next fighters turn
            if self.continue_fight:
                attacker, defender = defender, attacker
                self.printer.print_after_start_round(attacker, defender)

        winner = player_unit if player_unit.hp > 0 else enemy_unit
        loser = enemy_unit if player_unit.hp > 0 else player_unit
        self.printer.print_after_arena_simulation(winner, loser)

        if winner == player_unit:
            self.root_service.camp_service.open_camp()
        else:
            return

    def make_fight_round(self, first_unit: "Fighter", second_unit: "Fighter"):

        self.make_attack(first_unit, second_unit, 1)
        if second_unit.hp > 0:
            self.make_attack(second_unit, first_unit, 3)
        else:
            return self.end_fight()

        if first_unit.hp == 0:
            return self.end_fight()

        if first_unit.speed > second_unit.speed + 5:
            self.make_attack(first_unit, second_unit, 2)
        elif second_unit.speed > first_unit.speed + 5:
            self.make_attack(second_unit, first_unit, 2)

        if first_unit.hp == 0 or second_unit.hp == 0:
            return self.end_fight()

        return 1

    def end_fight(self):
        self.continue_fight = False

    def make_attack(self, attacker: "Fighter", defender: "Fighter", status: int):
        hit_chance = self.caluclate_hit_chance(attacker, defender)
        damage = self.calculate_damage(attacker, defender)
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
        attacker.items[0].uses -= 1

        self.printer.print_after_make_attack(attacker, defender, has_hit, has_crit, damage, status)


    def caluclate_hit_chance(self, attacker: "Fighter", defender: "Fighter"):
        hit_chance = max(0, min(100, attacker.calc_hit() - defender.calc_avoid()))
        return hit_chance / 100

    def caluclate_crit_chance(self, attacker: "Fighter", defender: "Fighter"):
        crit_chance = max(0, min(100, attacker.calc_crit() - defender.calc_crit_avoid()))
        return crit_chance / 100

    def calculate_damage(self, attacker: "Fighter", defender: "Fighter"):
        weapon = attacker.items[0]
        if weapon.weapon_type == WeaponType.MAGIC:
            return max(0, weapon.strength + attacker.magic - defender.res)
        else:
            return max(0, weapon.strength + attacker.strength - defender.defense)

