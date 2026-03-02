from rpg_arena.entity import Weapon
from rpg_arena.log.arnea_service_printer import ArneaServicePrinter

class ArenaActionService:
    def __init__(self, root_service: "RootService"):
        self.root_service = root_service
        self.printer = ArneaServicePrinter(root_service)

    def make_player_round_decision(self):
        self.printer.print_at_make_player_round_decsion()

        while True:

            choice = input(">> Choose an option (1-3): ")

            if choice not in ("1", "2", "3"):
                print("Invalid choice. Please enter 1, 2, or 3.")
            choice = int(choice)

            if choice == 1:
                self.open_fight_menu()
                break

            elif choice == 2:
                self.open_inventory()
                break

            elif choice == 3:
                confirm = input("Are you sure you want to surrender? (y/n): ").lower()
                if confirm == "y":
                    return "surrender"
                else:
                    continue


    def open_fight_menu(self):
        self.printer.print_at_open_fight_menu()
        self.choose_weapon_to_equip()

        self.printer.print_fight_preview()
        self.printer.print_after_print_fight_preview()
        self.make_fight_menu_choice()

    def make_fight_menu_choice(self):
        while True:

            choice = input(">> Choose an option (1-3): ")

            if choice not in ("1", "2", "3"):
                print("Invalid choice. Please enter 1, 2, or 3.")
            choice = int(choice)

            if choice == 1:
                player = self.root_service.current_game.player
                enemy = self.root_service.arena_service.enemy
                self.root_service.arena_service.make_fight_round(player, enemy)
                break

            elif choice == 2:
                self.open_inventory()
                break

            elif choice == 3:
                confirm = input("Are you sure you want to surrender? (y/n): ").lower()
                if confirm == "y":
                    return "surrender"
                else:
                    continue


    def choose_weapon_to_equip(self):
        while True:
            choice = input(">> Choose an option: ")

            if not choice.isdigit():
                print("Invalid input. Please enter a number.")
            choice = int(choice)

            if choice < 1 or choice > len(self.root_service.current_game.player.items):
                print(f"Invalid input.")

            else:
                player = self.root_service.current_game.player
                weapons = [item for item in player.items if isinstance(item, Weapon)]
                player.equipped_weapon = weapons[choice - 1]

                break


    def open_inventory(self):
        pass

    def make_enemy_round_decision(self):
        player = self.root_service.current_game.player
        enemy = self.root_service.arena_service.enemy
        self.root_service.arena_service.make_fight_round(enemy, player)