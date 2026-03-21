import time

class CampServicePrinter:
    """
    Handles all printed messages for the camp-related actions in the game.

    This includes:
        - Opening the camp menu
        - Displaying the item management interface
        - Showing player inventory and convoy
    """

    def __init__(self, root_service: "RootService"):
        """
        Initializes the CampServicePrinter.

        Args:
            root_service (RootService): Reference to the main root service for accessing game state.
        """
        self.root_service = root_service


    def print_at_open_menu(self):
        """
        Prints the main camp menu when the player enters the camp.

        - Displays different messages depending on whether it is the first round.
        - Shows available options such as entering the arena, managing equipment, visiting the merchant, or exiting the game.
        """
        print("\n======================================")
        print(f"Round {self.root_service.current_game.round} / {self.root_service.current_game.end_round}")

        if self.root_service.current_game.round == 1:
            print("You enter the camp to prepare for your first battle")
        elif self.root_service.current_game.round == self.root_service.current_game.end_round:
            print("The final round has arrived!")
            print("A mighty foe awaits you in the next battle… Brace yourself!")
        else:
            print("You return to the camp after the battle.")


        print("\nWhat will you do?")
        print("1) Enter the arena")
        print("2) Manage equipment")
        print("3) Visit the merchant")
        print("4) Exit game")
        print("======================================\n")



    def print_at_open_item_manager(self):
        """
        Prints the item management menu for the player.

        - Shows all items in the player's inventory (equipped weapons first).
        - Shows items stored in the convoy.
        - Displays the available commands for managing items:
            - send <no>: Move item from Inventory to Convoy
            - take <no>: Move item from Convoy to Inventory
            - use <no>: Use an item from Inventory
            - exit: Leave the item management menu
        """
        player = self.root_service.current_game.player
        convoy = self.root_service.current_game.convoy

        print("\n========================================")
        print("            ITEM MANAGEMENT")
        print("========================================")
        time.sleep(1)

        # --- Player Weapons ---
        print("\n--- Equipped / Inventory ---")
        time.sleep(1)

        index = 1
        if player.items:
            for weapon in player.items:
                print(f"{index}) {weapon}")
                index += 1
        else:
            print("No weapons in inventory.")

        # --- Convoy Weapons ---
        print("\n--- Convoy Storage ---")
        time.sleep(1)

        if convoy:
            for weapon in convoy:
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