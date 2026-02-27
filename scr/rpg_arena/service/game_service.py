from rpg_arena.entity.game import Game
from rpg_arena.log.game_service_printer import GameServicePrinter


class GameService:
    def __init__(self, root_service: "RootService"):
        self.root_service = root_service
        self.printer = GameServicePrinter(root_service)

    def start_game(self):
        self.root_service.current_game = Game()

        initial_units = self.root_service.roster_service.generate_initial_units()
        self.printer.print_after_start_game(initial_units)

    def start_first_round(self):
        enemy_units = self.root_service.roster_service.generate_enemy_units()
        self.printer.print_after_start_frist_round(enemy_units)
