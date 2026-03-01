
class CampServicePrinter:
    def __init__(self, root_service: "RootService"):
        self.root_service = root_service


    def print_at_open_menu(self):
        print("\n======================================")
        print("You return to the camp after the battle.")
        print("\nWhat will you do?")
        print("1) Enter the arena")
        print("2) Manage equipment")
        print("3) Visit the merchant")
        print("4) Exit game")
        print("======================================\n")

    def print_at_open_item_manager(self):
        player = self.root_service.current_game.player

        print("\n====== Your Weapons ======")

        if not player.weapons:
            print("You do not own any weapons.")
            return

        for index, weapon in enumerate(player.weapons, start=1):
            print(f"{index}) {weapon}")

        print("==========================\n")
