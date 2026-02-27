from rpg_arena.entity.game import Game
from rpg_arena.service.game_service import GameService

class RootService:
    def __init__(self):
        self.game_service = GameService()
        self.current_game = None
