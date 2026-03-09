from rpg_arena.log.camp_service_printer import CampServicePrinter

class CampService:
    """
    Service class responsible for managing camp interactions in the game.

    Attributes:
        root_service (RootService): Reference to the root service managing all sub-services.
        printer (CampServicePrinter): Utility to print camp menus and updates.

    Methods:
        open_camp(): Opens the camp menu and prompts the player for actions.
        open_item_manager(): Opens the item manager menu and handles player choices.
    """

    def __init__(self, root_service: "RootService"):
        """
        Initialize the CampService with a reference to the root service.

        Args:
            root_service (RootService): The central service managing all other services.

        Returns:
            None
        """
        self.root_service = root_service
        self.printer = CampServicePrinter(root_service)

    def open_camp(self):
        """
        Open the camp menu and prompt the player to choose an action.

        Args:
            None

        Returns:
            None
        """
        self.printer.print_at_open_menu()
        self.root_service.camp_action_service.choose_camp_action()

    def open_item_manager(self):
        """
        Open the item manager menu and prompt the player to manage items.

        Args:
            None

        Returns:
            None
        """
        self.printer.print_at_open_item_manager()
        self.root_service.camp_action_service.choose_item_manager_action()