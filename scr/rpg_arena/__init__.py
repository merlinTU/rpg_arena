"""
RPG Arena main package.

Contains the following subpackages:
- entity: All game entities like units, weapons, and items.
- service: All service classes handling game logic.
- log: All printer/logging classes for displaying game info.
"""
from rpg_arena.service.root_service import RootService

def start_game():
    root_service = RootService()
    root_service.game_service.start_game()