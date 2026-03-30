from rpg_arena.service.root_service import RootService

def main():
    root_service = RootService()
    root_service.game_service.start_game()


if __name__ == "__main__":
    main()