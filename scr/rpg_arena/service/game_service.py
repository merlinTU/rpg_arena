from rpg_arena.entity.game import Game
from rpg_arena.log.game_service_printer import GameServicePrinter
from rpg_arena.service.data.weapon_data import CLASS_WEAPON_MAP

class GameService:
    """
    Service class responsible for managing game flow, including starting the game,
    selecting initial units, initializing player weapons, and handling the arena.

    Attributes:
        root_service (RootService): Reference to the root service managing all subservices.
        printer (GameServicePrinter): Utility to print game state updates for the user.
    """

    def __init__(self, root_service: "RootService"):
        """
        Initialize the GameService with a reference to the root service.

        Args:
            root_service (RootService): The central service that manages all other services.

        Returns:
            None
        """
        self.root_service = root_service
        self.printer = GameServicePrinter(root_service)

    def start_game(self):
        """
        Start a new game session.

        This method:
        - Creates a new Game instance
        - Generates the initial units
        - Prints the state after game start
        - Prompts the player to choose their first unit
        - Assigns the player's weapons based on unit class
        - Opens the camp for further actions

        Args:
            None

        Returns:
            None
        """
        self.root_service.current_game = Game()

        initial_units = self.root_service.roster_service.generate_initial_units()
        self.printer.print_after_start_game(initial_units)

        player_unit = self.root_service.player_action_service.choose_unit(initial_units)
        self.printer.print_after_choose_first_unit(player_unit)

        self.root_service.current_game.player = player_unit

        # Set the initial weapons the player can buy in the shop
        self.root_service.current_game.player_weapons = CLASS_WEAPON_MAP[player_unit.player_class]
        self.root_service.camp_service.open_camp()

    def start_arena(self):
        """
        Initialize the arena by generating enemy units and printing the initial state.

        Args:
            None

        Returns:
            None
        """
        enemy_units = self.root_service.roster_service.generate_enemy_units()
        self.printer.print_after_start_frist_round(enemy_units)