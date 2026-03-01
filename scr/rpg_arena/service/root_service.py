from rpg_arena.service.camp_action_service import CampActionService
from rpg_arena.service.camp_service import CampService
from rpg_arena.service.arena_service import ArenaService
from rpg_arena.service.game_service import GameService
from rpg_arena.service.player_action_service import PlayerActionService
from rpg_arena.service.roster_service import RosterService


class RootService:
    def __init__(self):
        self.game_service = GameService(self)
        self.roster_service = RosterService(self)
        self.player_action_service = PlayerActionService(self)
        self.arena_service = ArenaService(self)
        self.camp_service = CampService(self)
        self.camp_action_service = CampActionService(self)
        self.current_game = None
