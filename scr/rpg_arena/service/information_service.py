from rpg_arena.log.information_service_printer import InformationServicePrinter
from rpg_arena.service.data.weapon_data import WEAPONS
class InformationService:
    """
    Handles player requests for information about units, stats, combat stats, and weapons.

    Attributes:
        root_service (RootService): Reference to the central RootService for accessing other services.
        printer (InformationServicePrinter): Handles printing information to the player.

    """

    def __init__(self, root_service: "RootService"):
        """
        Initialize the InformationService with a reference to RootService.

        Args:
            root_service (RootService): Central service managing all sub-services.
        """
        self.root_service = root_service
        self.printer = InformationServicePrinter(root_service)

    def check_information_service_call(self, choice: str) -> bool:
        """
        Check if the player input is an information request and handle it.

        Args:
            choice (str): Player input string.

        Returns:
            bool: True if the input was an information command and was handled, False otherwise.
        """
        parts = choice.lower().split()

        if len(parts) < 2:
            return False

        command = parts[0]
        target = " ".join(parts[1:])

        weapons_lower = {name.lower(): obj for name, obj in WEAPONS.items()}

        if command not in ["info", "check"]:
            return False

        match target:
            case "player" | "unit":
                self.printer.print_player()
            case "enemy" | "gladiator":
                self.printer.print_enemy()
            case "stats":
                self.printer.print_all_stats()
            case "str" | "mag" | "spd" | "skl" | "luck" | "def" | "res" | "hp":
                self.printer.print_stat(target)
            case "combat":
                self.printer.print_all_combat_stats()
            case "hit" | "avoid" | "acc" | "crit" | "damage":
                self.printer.print_combat_stat(target)
            case _ if target in weapons_lower:
                weapon = weapons_lower[target]
                self.printer.print_weapon_info(weapon)
            case _:
                print("Unknown information target.")

        return True