import time

from rpg_arena.entity import Weapon


class ArneaServicePrinter:
    """
    Printer class for the Arena Service.
    Handles all combat-related console outputs such as attack results,
    battle start/end notifications, weapon selection, and inventory display.
    """

    def __init__(self, root_service: "RootService"):
        """
        Initialize the printer with a reference to the root service.

        Args:
            root_service: Reference to RootService for accessing current game state.
        """
        self.root_service = root_service

    def print_after_make_attack(self, attacker, defender, has_hit, has_crit, damage, status):
        """
        Prints the result of a single attack in the arena.

        Args:
            attacker: The attacking fighter.
            defender: The defending fighter.
            has_hit: Boolean, True if the attack hits.
            has_crit: Boolean, True if the attack is a critical hit.
            damage: Damage dealt by the attack.
            status: Attack type/status (1 = normal, 2 = double, 3 = counter).
        """
        attacker_name = attacker.name
        defender_name = defender.name

        match status:
            case 1:
                print(f"> {attacker_name} attacks!")
            case 2:
                print(f"> {attacker_name} strikes consecutively! (x2)")
            case 3:
                print(f"> {attacker_name} counters!")

        time.sleep(1)

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
        """Prints the header for the start of a battle round."""
        print("\n========================================")
        print("        BATTLE START")
        print("========================================")
        time.sleep(1)

    def print_after_start_round(self, first_unit, second_unit):
        """
        Prints whose turn it is at the start of a round.

        Args:
            first_unit: Fighter whose turn it is.
            second_unit: Opponent fighter.
        """
        print("\n========================================")
        if first_unit == self.root_service.current_game.player:
            print("        YOUR TURN")
        else:
            print("        ENEMY TURN")
        print("========================================")

    def print_after_arena_simulation(self, winner, loser):
        """
        Prints the result of the battle after a fight ends.

        Args:
            winner: Fighter who won.
            loser: Fighter who lost.
        """
        print("\n================ FIGHT OVER ================\n")
        time.sleep(1)

        if winner != self.root_service.current_game.player:
            print("You have been defeated!")
            time.sleep(1)
            print("GAME OVER")
            return

        print(f"{loser.name} falls to the ground...")
        time.sleep(1)
        print(f"{loser.name} is defeated!")
        time.sleep(2)
        print("\n================ YOU WIN! =================\n")
        time.sleep(2)

    def print_at_open_fight_menu(self):
        """
        Prints the player's available weapons for selection in a formatted, numbered list.
        """
        items = self.root_service.current_game.player.items
        weapons = [item for item in items if isinstance(item, Weapon)]

        print("\n========================================")
        print("           CHOOSE YOUR WEAPON")
        print("========================================")

        if not weapons:
            print("You have no weapons available!")
            print("========================================")
            return

        for index, weapon in enumerate(weapons, start=1):
            print(f"{index}) {weapon}")

        print("========================================")

    def print_fight_preview(self):
        """
        Prints a detailed fight preview between the player and the enemy.

        This method calculates and displays:
            - Hit chance, critical chance, and damage for both units
            - Whether a unit attacks twice (based on speed difference)
            - Weapon advantage indicators (↑ or ↓)
            - Formatted display of stats including HP, Hit, Damage, Crit, and weapon

        The preview helps the player make tactical decisions before committing to an attack.

        No parameters; uses current game state from root_service.
        """
        player_unit = self.root_service.current_game.player
        enemy_unit = self.root_service.arena_service.enemy
        arena = self.root_service.arena_service

        # Calculate combat stats for preview
        player_hit = arena.calculate_hit_chance(player_unit, enemy_unit)
        player_crit = arena.calculate_crit_chance(player_unit, enemy_unit)
        player_damage = arena.calculate_damage(player_unit, enemy_unit)

        enemy_hit = arena.calculate_hit_chance(enemy_unit, player_unit)
        enemy_crit = arena.calculate_crit_chance(enemy_unit, player_unit)
        enemy_damage = arena.calculate_damage(enemy_unit, player_unit)

        # Determine double attack eligibility
        player_double = player_unit.calc_corrected_speed() > enemy_unit.calc_corrected_speed() + 5
        enemy_double = enemy_unit.calc_corrected_speed() > player_unit.calc_corrected_speed() + 5

        # Determine weapon advantage arrows
        player_weapon_arrow = ""
        enemy_weapon_arrow = ""
        vantage_player = arena.check_weapon_vantage(player_unit.equipped_weapon, enemy_unit.equipped_weapon)
        if vantage_player == 1:
            player_weapon_arrow = " ↑"
        elif vantage_player == 2:
            player_weapon_arrow = " ↓"

        vantage_enemy = arena.check_weapon_vantage(enemy_unit.equipped_weapon, player_unit.equipped_weapon)
        if vantage_enemy == 1:
            enemy_weapon_arrow = " ↑"
        elif vantage_enemy == 2:
            enemy_weapon_arrow = " ↓"

        # Print formatted fight preview
        print("\n========================================")
        print("           FIGHT PREVIEW")
        print("========================================")

        name_width = 15
        hp_width = 5
        stat_width = 6
        weapon_width = 15

        # Player info
        player_weapon_str = f"{player_unit.equipped_weapon.name:<{weapon_width - 1}}{player_weapon_arrow:>1}"
        player_info = (
            f"1) {player_unit.name:<{name_width}} | "
            f"{player_weapon_str} | "
            f"HP: {player_unit.hp:>{hp_width}} | "
            f"Hit: {round(player_hit * 100):>{stat_width}}% | "
            f"Dmg: {player_damage:>{stat_width}} | "
            f"Crit: {round(player_crit * 100):>{stat_width}}%"
        )
        if player_double:
            player_info += "  x2"
        print(player_info)

        # Enemy info
        enemy_weapon_str = f"{enemy_unit.equipped_weapon.name:<{weapon_width - 1}}{enemy_weapon_arrow:>1}"
        enemy_info = (
            f"2) {enemy_unit.name:<{name_width}} | "
            f"{enemy_weapon_str} | "
            f"HP: {enemy_unit.hp:>{hp_width}} | "
            f"Hit: {round(enemy_hit * 100):>{stat_width}}% | "
            f"Dmg: {enemy_damage:>{stat_width}} | "
            f"Crit: {round(enemy_crit * 100):>{stat_width}}%"
        )
        if enemy_double:
            enemy_info += "  x2"
        print(enemy_info)

        print("========================================")

    def print_after_print_fight_preview(self):
        """
        Prints the menu options for the player after viewing the fight preview.

        Options presented:
            1) Attack
            2) Choose another weapon
            3) Cancel

        No parameters; intended to guide the player's next action.
        """
        print("What do you want to do?")
        print("1) Attack")
        print("2) Choose another weapon")
        print("3) Cancel")
        print("========================================\n")

    def print_at_make_player_round_decsion(self):
        """
        Prints the main menu for the player at the start of their round.

        Options presented:
            1) Attack
            2) Check Inventory
            3) Wait
            4) Surrender

        No parameters; intended to guide the player's choice for the round.
        """
        print("What do you want to do?")
        print("1) Attack")
        print("2) Check Inventory")
        print("3) Wait")
        print("4) Surrender")
        print("========================================\n")

    def print_inventory(self):
        """
        Prints the player's current inventory in a formatted view.

        - Shows the equipped weapon at the top.
        - Lists all other items in the inventory.
        - Calls `print_inventar_choice` at the end to show available commands.

        Uses the current game state from `root_service`.
        """
        player_unit = self.root_service.current_game.player

        print("\n====== Your Inventory ======\n")

        # mark equipped weapon
        if player_unit.equipped_weapon:
            print("Equipped Weapon:")
            print(f"{player_unit.equipped_weapon}")
            print("--------------------------------")

        # other items in inventory
        other_items = [item for item in player_unit.items if item != player_unit.equipped_weapon]

        if not other_items:
            print("No other items in inventory.")
            print("\n============================\n")
            self.print_inventar_choice()
            return

        for index, item in enumerate(other_items, start=1):
            print(f"{index}) {item}")

        print("============================")

        self.print_inventar_choice()

    def print_inventar_choice(self):
        """
        Prints available commands for interacting with the inventory.

        Options:
            - equip <no>: Equip a weapon
            - use <no>: Use an item
            - exit: Exit inventory
        """
        time.sleep(1)
        print("What do you want to do?")
        print("equip <no>   - Equip weapon")
        print("use <no>     - Use item")
        print("exit")
        print("========================================\n")

    def print_after_use_item(self, unit: "Fighter"):
        """
        Prints a confirmation message that a unit has used an item.

        Args:
            unit (Fighter): The unit that used the item.
        """
        print(">", unit.name, "used item")

    def print_at_end_fight(self, gold: int, exp: int):
        """
        Prints the battle results at the end of a fight.

        Displays the amount of gold earned and experience gained.

        Args:
            gold (int): Amount of gold earned by the player.
            exp (int): Amount of experience gained by the player.
        """
        print("========================================")
        print("           BATTLE RESULTS")
        print("========================================")
        time.sleep(1)
        print(f"You earned {gold} Gold.")
        time.sleep(1)
        print(f"You gained {exp} EXP.")
        time.sleep(1)

    def print_level_up(self, level_up_stats: list):
        """
        Prints a level-up message for the player and lists which stats increased.

        If no stats increased, prints a message indicating no level-up occurred.

        Args:
            level_up_stats (list): List of stat names that increased.
        """
        if level_up_stats:
            print("LEVEL UP! The following stats increased:")
            for stat in level_up_stats:
                print(f" - {stat} +1")
        else:
            print("No level up this time.")

        time.sleep(1)

    def print_after_surrender(self):
        """
        Prints a message and battle results when the player surrenders.

        - Displays that the player surrendered.
        - Shows 0 Gold and 0 EXP earned.
        """
        player_unit = self.root_service.current_game.player
        print(">", player_unit.name, "surrendered.")

        print("========================================")
        print("           BATTLE RESULTS")
        print("========================================")
        time.sleep(1)
        print(f"You earned 0 Gold.")
        time.sleep(1)
        print(f"You gained 0 EXP.")
        time.sleep(1)

    def print_after_prob_skill(self, unit, skill_name):
        """
        Prints that a unit has activated a ProbSkill.

        :param unit: The unit/player activating the skill
        :param skill_name: Name of the skill being activated
        """
        # Assuming the unit has a 'name' attribute
        print(f"> {unit.name} activates {skill_name}!")
        time.sleep(1)
