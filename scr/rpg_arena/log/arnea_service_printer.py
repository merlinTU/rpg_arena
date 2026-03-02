import time

from rpg_arena.entity import Weapon


class ArneaServicePrinter():
    def __init__(self, root_service: "RootService"):
        self.root_service = root_service

    def print_after_make_attack(self, attacker, defender, has_hit, has_crit, damage, status):
        attacker_name = attacker.name
        defender_name = defender.name

        # Action Line
        match status:
            case 1:
                print(f"> {attacker_name} attacks!")
            case 2:
                print(f"> {attacker_name} strikes consecutively! (x2)")
            case 3:
                print(f"> {attacker_name} counters!")

        time.sleep(1)

        # Result
        if has_hit:
            if has_crit:
                print(">>> CRITICAL HIT! <<<")
                time.sleep(1)

            print(f"> {defender_name} takes {damage} damage.")
            time.sleep(1)

            print(f"> {defender_name} HP: {defender.hp}")
            time.sleep(3)
        else:
            print(f"> {defender_name} dodged the attack!")
            time.sleep(2)


    def print_at_start_round(self):
        print("\n========================================")
        print("        BATTLE START")
        print("========================================")
        time.sleep(1)


    def print_after_start_round(self, first_unit, second_unit):
        print("\n========================================")

        if first_unit == self.root_service.current_game.player:
            print("        YOUR TURN")
        else:
            print("        ENEMY TURN")

        print("========================================\n")

    def print_after_arena_simulation(self, winner, loser):
        print("Fight over")
        if winner != self.root_service.current_game.player:
            print("You were defeated")
            print("GAME OVER")
            return

        print(loser.name, "falls to the ground")
        time.sleep(1)
        print(loser.name, "is defeated")
        time.sleep(3)
        print("You win!")

    def print_at_open_fight_menu(self):
        """
        Prints all weapons in the player's items in a formatted, numbered box
        so the player can choose which weapon to use.
        """
        items = self.root_service.current_game.player.items
        weapons = [item for item in items if isinstance(item, Weapon)]

        print("\n========================================")
        print("           CHOOSE YOUR WEAPON")
        print("========================================\n")

        if not weapons:
            print("You have no weapons available!")
            print("========================================\n")
            return

        # Print numbered list of weapons
        for index, weapon in enumerate(weapons, start=1):
            print(f"{index}) {weapon}")

        print("========================================\n")

    def print_fight_preview(self):
        player_unit = self.root_service.current_game.player
        enemy_unit = self.root_service.arena_service.enemy
        arena = self.root_service.arena_service

        player_hit = arena.caluclate_hit_chance(player_unit, enemy_unit)
        player_crit = arena.caluclate_crit_chance(player_unit, enemy_unit)
        player_damage = arena.calculate_damage(player_unit, enemy_unit)

        enemy_hit = arena.caluclate_hit_chance(enemy_unit, player_unit)
        enemy_crit = arena.caluclate_crit_chance(enemy_unit, player_unit)
        enemy_damage = arena.calculate_damage(enemy_unit, player_unit)

        player_double = player_unit.speed > enemy_unit.speed + 5
        enemy_double = enemy_unit.speed > player_unit.speed + 5

        print("\n========================================")
        print("           FIGHT PREVIEW")
        print("========================================")

        player_info = f"1) {player_unit.name} | HP: {player_unit.hp} | Hit: {round(player_hit * 100)}% | " \
                      f"Damage: {player_damage} | Crit: {round(player_crit * 100)}%"
        if player_double:
            player_info += " x2"
        print(player_info)

        enemy_info = f"2) {enemy_unit.name} | HP: {player_unit.hp} | Hit: {round(enemy_hit * 100)}% | " \
                     f"Damage: {enemy_damage} | Crit: {round(enemy_crit * 100)}%"
        if enemy_double:
            enemy_info += " x2"
        print(enemy_info)

        print("========================================\n")

    def print_after_print_fight_preview(self):
        print("1) Attack")
        print("2) Choose another weapon")
        print("3) Cancel")
        print("========================================\n")

    def print_at_make_player_round_decsion(self):
        print("What do you want to do?")
        print("1) Attack")
        print("2) Check Inventory")
        print("3) Cancel")
        print("========================================\n")