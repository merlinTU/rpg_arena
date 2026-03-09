from rpg_arena.service.camp_action_service import CampActionService
from rpg_arena.service.camp_service import CampService
from rpg_arena.service.arena_service import ArenaService
from rpg_arena.service.game_service import GameService
from rpg_arena.service.information_service import InformationService
from rpg_arena.service.player_action_service import PlayerActionService
from rpg_arena.service.roster_service import RosterService
from rpg_arena.service.shop_service import ShopService

class RootService:
    """
    Root service that initializes and contains all sub-services of the game.

    Attributes:
        game_service (GameService): Service to manage game flow and state.
        roster_service (RosterService): Service to generate and manage units.
        player_action_service (PlayerActionService): Service handling player input and selections.
        arena_service (ArenaService): Service managing arena battles.
        camp_service (CampService): Service handling camp-related actions.
        camp_action_service (CampActionService): Service for player actions in camp.
        shop_service (ShopService): Service managing shop interactions.
        information_service (InformationService): Service handling informational commands.
        current_game (Game | None): Reference to the current Game instance, None if no game started.
    """

    def __init__(self):
        """
        Initialize the RootService and all sub-services.

        Returns:
            None
        """
        self.game_service = GameService(self)
        self.roster_service = RosterService(self)
        self.player_action_service = PlayerActionService(self)
        self.arena_service = ArenaService(self)
        self.camp_service = CampService(self)
        self.camp_action_service = CampActionService(self)
        self.shop_service = ShopService(self)
        self.information_service = InformationService(self)
        self.current_game = None