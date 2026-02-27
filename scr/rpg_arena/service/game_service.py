from rpg_arena.entity.game import Game
from rpg_arena.log.game_service_printer import GameServicePrinter
from rpg_arena.service.root_service import RootService

class GameService:
    def __init__(self, root_service: RootService):
        self.root_service = root_service
        self.printer = GameServicePrinter()

    def start_game(self):
        self.root_service.current_game = Game()
        self.printer.print_after_start_game()
