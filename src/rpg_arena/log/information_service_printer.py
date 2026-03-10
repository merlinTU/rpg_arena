

class InformationServicePrinter:
    """
    Handles all printed messages related to unit stats, combat stats, and weapon information.
    Provides guidance and explanations for the player.
    """

    def __init__(self, root_service: "RootService"):
        """
        Initializes the InformationServicePrinter.

        Args:
            root_service (RootService): Reference to the main root service to access game state.
        """
        self.root_service = root_service

    def print_player(self):
        """
        Prints stats for the player unit by delegating to the GameServicePrinter.
        """
        player = self.root_service.current_game.player
        self.root_service.game_service.printer.print_unit_stats(player, 1)
        print(f"Gold: {player.gold}")

    def print_gold(self):
        """
        Prints the amount of gold the player has
        """
        player = self.root_service.current_game.player
        print(f"You have {player.gold} Gold")

    def print_enemy(self):
        """
        Prints detailed stats for the current enemy unit by delegating to the GameServicePrinter.
        """
        enemy = self.root_service.arena_service.enemy
        self.root_service.game_service.printer.print_unit_stats(enemy, 1)

    def print_weapon_info(self, weapon):
        """
        Prints information about a weapon.

        Args:
            weapon (Weapon): The weapon object to display.
        """
        print(weapon)

    def print_all_stats(self):
        """
        Prints a guide for all basic unit stats (HP, STR, MAG, SKL, SPD, LUCK, DEF, RES).
        """
        print("\n========================================")
        print("              STAT GUIDE")
        print("========================================")

        stats = ["hp", "str", "mag", "skl", "spd", "luck", "def", "res"]

        for stat in stats:
            self.print_stat(stat)

        print("========================================\n")

    def print_stat(self, stat):
        """
        Prints a description for a single stat.

        Args:
            stat (str): The stat name to display. Valid values: "hp", "str", "mag",
                        "skl", "spd", "luck", "def", "res".
        """
        explanations = {
            "hp": "HP (Health Points): Determines how much damage a unit can take before falling.",
            "str": "STR (Strength): Increases physical attack damage with swords, axes, lances and bows.",
            "mag": "MAG (Magic): Increases damage dealt with magic.",
            "skl": "SKL (Skill): Improves hit rate and increases critical hit chance.",
            "spd": "SPD (Speed): Improves hit rate and chance to perform a double attack.",
            "luck": "LUCK: Reduces enemy critical chance and slightly improves hit rate.",
            "def": "DEF (Defense): Reduces incoming physical damage.",
            "res": "RES (Resistance): Reduces incoming magic damage."
        }

        stat = stat.lower()
        if stat in explanations:
            print(explanations[stat])
        else:
            print("Unknown stat.")

    def print_all_combat_stats(self):
        """
        Prints a guide for all combat-related stats (HIT, AVOID, ACC, CRIT, DAMAGE).
        """
        print("\n========================================")
        print("            COMBAT GUIDE")
        print("========================================")

        stats = ["hit", "avoid", "acc", "crit", "damage"]

        for stat in stats:
            self.print_combat_stat(stat)

        print("========================================\n")

    def print_combat_stat(self, stat):
        """
        Prints a description for a single combat stat.

        Args:
            stat (str): The combat stat to display. Valid values: "hit", "avoid",
                        "acc", "crit", "damage".
        """
        explanations = {
            "hit": (
                "HIT (Hit Rate): Chance that an attack will land.\n"
                "Formula: HIT = Weapon Accuracy + (SKL * 2) + LUCK - Enemy Avoid"
            ),
            "avoid": (
                "AVOID: Chance to dodge an enemy attack.\n"
                "Formula: AVOID = (SPD * 2) + LUCK"
            ),
            "acc": (
                "ACC (Accuracy): Weapon-based accuracy used in hit calculation.\n"
            ),
            "crit": (
                "CRIT (Critical Chance): Chance to deal triple damage.\n"
                "Formula: CRIT = Weapon Crit + (SKL * 0.5)"
            ),
            "damage": (
                "DAMAGE: Amount of HP removed when an attack hits.\n"
                "Physical Formula: DAMAGE = STR + Weapon Might - Enemy DEF\n"
                "Magic Formula: DAMAGE = MAG + Book Might - Enemy RES"
            )
        }

        stat = stat.lower()
        if stat in explanations:
            print(f"\n{explanations[stat]}")
        else:
            print("\nUnknown combat stat.")