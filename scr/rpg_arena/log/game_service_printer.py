import time

class GameServicePrinter():
    """
    Handles all printed messages related to the game flow, including:
        - Starting the game
        - Choosing a fighter
        - Displaying initial and enemy units
        - Showing unit stats
    """

    def __init__(self, root_service: "RootService"):
        """
        Initializes the GameServicePrinter.

        Args:
            root_service (RootService): Reference to the main root service to access game state.
        """
        self.root_service = root_service

    def print_after_start_game(self, initial_units):
        """
        Prints introductory messages when the game starts.

        Displays the arena introduction, story flavor text, and
        prompts the player to choose their first fighter.

        Args:
            initial_units (list[Fighter]): List of player's initial units to choose from.
        """
        print("\n======================================")
        print("🔥  Welcome to the Arena!  🔥")
        print("======================================\n")
        time.sleep(1)

        print("The crowd roars as warriors from across the lands gather.")
        print("Only the strongest will survive the trials of the arena.")
        print("Choose your champion wisely!\n")
        time.sleep(2)

        print("\n========================================")
        print("           Choose Your Fighter")
        print("========================================")
        time.sleep(2)
        self.print_initial_units(initial_units)

    def print_after_choose_first_unit(self, player_unit):
        """
        Prints confirmation of the player's chosen unit.

        Args:
            player_unit (Fighter): The player's selected unit.
        """
        print("You chose: ", player_unit.name, "the ", player_unit.player_class.name)

    def print_after_start_frist_round(self, enemy_units):
        """
        Prints the start of the first round in the arena.

        Displays the enemy units, prompts the player to choose
        an enemy to fight, and starts the arena simulation.

        Args:
            enemy_units (list[Fighter]): List of enemy units for the first round.
        """
        print("========================================")
        print("           THE ARENA AWAITS")
        print("========================================")

        print("Three gladiators stand before you.\n")
        time.sleep(0.5)
        self.print_enemy_units(enemy_units)
        enemy_unit = self.root_service.player_action_service.choose_enemy(enemy_units)
        self.root_service.arena_service.start_arena(enemy_unit)

    def print_enemy_units(self, enemy_units):
        """
        Prints all enemy units in a numbered list.

        Args:
            enemy_units (list[Fighter]): List of enemy units to display.
        """
        for i, unit in enumerate(enemy_units, start=1):
            self.print_enemy_stats(unit, i)

    def print_initial_units(self, initial_units):
        """
        Prints all initial player units for selection.

        Args:
            initial_units (list[Fighter]): List of player's starting units.
        """
        for i, unit in enumerate(initial_units, start=1):
            self.print_unit_stats(unit, i)

    def print_unit_stats(self, unit, number: int):
        """
        Prints detailed stats for a player unit, including base stats, growth rates, and items.

        Args:
            unit (Fighter): The unit whose stats to print.
            number (int): The numbered index to display before the unit.
        """
        name_width = 15
        print(f"{number}) {unit.name:<{name_width}} ({unit.player_class.value})")

        # Stats
        stat_width = 6
        stats_line = (
            "Stats:   "
            f"HP: {unit.hp:>{stat_width}} | "
            f"STR: {unit.strength:>{stat_width}} | "
            f"MAG: {unit.magic:>{stat_width}} | "
            f"SKL: {unit.skill:>{stat_width}} | "
            f"SPD: {unit.speed:>{stat_width}} | "
            f"LUCK: {unit.luck:>{stat_width}} | "
            f"DEF: {unit.defense:>{stat_width}} | "
            f"RES: {unit.res:>{stat_width}}"
        )
        print(stats_line)

        # Growths
        growth_line = (
            "Growths: "
            f"HP: {unit.hp_growth:>{stat_width}.2f} | "
            f"STR: {unit.strength_growth:>{stat_width}.2f} | "
            f"MAG: {unit.magic_growth:>{stat_width}.2f} | "
            f"SKL: {unit.skill_growth:>{stat_width}.2f} | "
            f"SPD: {unit.speed_growth:>{stat_width}.2f} | "
            f"LUCK: {unit.luck_growth:>{stat_width}.2f} | "
            f"DEF: {unit.defense_growth:>{stat_width}.2f} | "
            f"RES: {unit.res_growth:>{stat_width}.2f}"
        )
        print(growth_line)

        # Items
        item_names = [item.name for item in unit.items] if unit.items else []
        items_line = "Items:   " + ", ".join(item_names) if item_names else "Items: None"
        print(items_line)

        time.sleep(1)
        print("========================================")

    def print_enemy_stats(self, unit, number: int):
        """
        Prints basic stats for an enemy unit, including level, gold, and items.

        Args:
            unit (Fighter): The enemy unit to display.
            number (int): The numbered index to display before the unit.
        """
        name_width = 15
        print(f"{number}) {unit.name:<{name_width}} ({unit.player_class.value})")

        stat_width = 6
        stats_line = (
            f"LVL: {unit.level:>{stat_width}} | "
            f"GOLD: {unit.gold:>{stat_width}}"
        )
        print(stats_line)

        item_names = [item.name for item in unit.items] if unit.items else []
        items_line = "Items:   " + ", ".join(item_names) if item_names else "Items: None"
        print(items_line)

        time.sleep(1)
        print("========================================")