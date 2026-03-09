class PlayerActionService:
    """
    Service class responsible for handling player input and unit selection.

    Attributes:
        root_service (RootService): Reference to the root service managing all subservices.

    Methods:
        choose_unit(initial_units): Prompts the player to select a unit from a list.
        choose_enemy(enemy_units): Prompts the player to select an enemy unit.
        search_unit_index(units, choice): Searches for a unit by name in a list and returns its index.
    """

    def __init__(self, root_service: "RootService"):
        """
        Initialize the PlayerActionService with a reference to the root service.

        Args:
            root_service (RootService): The central service managing all other services.

        Returns:
            None
        """
        self.root_service = root_service

    def choose_unit(self, initial_units):
        """
        Prompt the player to select a unit from a list of initial units.

        The player can enter either a number (1-based index) or the unit's name.
        The input is validated. If invalid, the player is prompted again.

        Args:
            initial_units (list[Fighter]): List of available units to choose from.

        Returns:
            Fighter: The selected player unit.
        """
        while True:
            choice = input(">> Write your Fighter's name or number: ")

            if self.root_service.information_service.check_information_service_call(choice):
                continue

            if choice.isdigit():
                index = int(choice) - 1
                if 0 <= index < len(initial_units):
                    player_unit = initial_units[index]
                    return player_unit
                else:
                    print("Invalid number. Try again.")
            else:
                index = self.search_unit_index(initial_units, choice)
                if index != -1:
                    player_unit = initial_units[index]
                    return player_unit
                else:
                    print("Name not found. Try again.")

    def choose_enemy(self, enemy_units):
        """
        Prompt the player to select an enemy unit.

        The player can enter either a number (1-based index) or the enemy's name.
        Input is validated; invalid input prompts the player again.

        Args:
            enemy_units (list[Fighter]): List of enemy units to choose from.

        Returns:
            Fighter: The selected enemy unit.
        """
        while True:
            choice = input("Write the number of the Warrior you want to fight: ")

            if self.root_service.information_service.check_information_service_call(choice):
                continue

            if choice.isdigit():
                index = int(choice)
                if 1 <= index <= len(enemy_units):
                    player_unit = enemy_units[index - 1]
                    return player_unit
                else:
                    print("Invalid number. Try again.")
            else:
                index = self.search_unit_index(enemy_units, choice)
                if index != -1:
                    enemy_unit = enemy_units[index]
                    return enemy_unit
                else:
                    print("Name not found. Try again.")

    def search_unit_index(self, units, choice: str):
        """
        Search for a unit by name in a list.

        Args:
            units (list[Fighter]): List of units to search.
            choice (str): Name of the unit to find.

        Returns:
            int: Index of the unit if found; -1 if not found.
        """
        for i, unit in enumerate(units):
            if unit.name == choice:
                return i
        return -1