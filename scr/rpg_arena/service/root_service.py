from rpg_arena.service.game_service import GameService
from rpg_arena.service.roster_service import RosterService


class RootService:
    def __init__(self):
        self.game_service = GameService(self)
        self.roster_service = RosterService(self)
        self.current_game = None
