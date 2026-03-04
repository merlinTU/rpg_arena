import time

class CampServicePrinter:
    def __init__(self, root_service: "RootService"):
        self.root_service = root_service


    def print_at_open_menu(self):
        print("\n======================================")

        if self.root_service.current_game.round == 1:
            print("You enter the camp to prepare for your first battle")
        else:
            print("You return to the camp after the battle.")

        print("\nWhat will you do?")
        print("1) Enter the arena")
        print("2) Manage equipment")
        print("3) Visit the merchant")
        print("4) Exit game")
        print("======================================\n")

    def print_at_open_item_manager(self):
        player = self.root_service.current_game.player
        convoy = self.root_service.current_game.convoy

        print("\n========================================")
        print("            ITEM MANAGEMENT")
        print("========================================")
        time.sleep(1)

        # --- Player Weapons ---
        print("\n--- Equipped / Inventory ---")
        time.sleep(1)

        if player.items:
            for index, weapon in enumerate(player.items, start=1):
                print(f"{index}) {weapon}")
        else:
            print("No weapons in inventory.")

        # --- Convoy Weapons ---
        print("\n--- Convoy Storage ---")
        time.sleep(1)

        if convoy:
            for index, weapon in enumerate(convoy, start=1):
                print(f"{index}) {weapon}")
        else:
            print("Convoy is empty.")
        time.sleep(1)
        print("----------------------------------------")
        print("Commands:")
        print(" send <no>   - Move item from Inventory to Convoy")
        print(" take <no>   - Move item from Convoy to Inventory")
        print(" use <no>    - Use item from Inventory")
        print(" exit        - Leave menu")
        print("========================================\n")
