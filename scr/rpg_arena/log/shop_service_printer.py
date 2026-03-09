import time
from rpg_arena.entity.healing_potion import HealingPotion
from rpg_arena.entity.stat_booster import StatBooster

class ShopServicePrinter:
    """
    Handles all printed messages related to the Shop/Merchant.
    Displays shop menus, item lists, and guides the player through buying and selling.
    """

    def __init__(self, root_service: "RootService"):
        """
        Initializes the ShopServicePrinter.

        Args:
            root_service (RootService): Reference to the main root service to access game state.
        """
        self.root_service = root_service

    def print_at_open_shop(self):
        """
        Prints the main shop menu with options to buy, sell, or exit.
        """
        print("========================================")
        print("           Merchant")
        print("========================================")
        print("What do you want to do?")
        print("1) Buy Items")
        print("2) Sell Items")
        print("3) Exit")
        print("========================================\n")

    def print_at_open_buy_items_menu(self, items):
        """
        Prints a list of all items available to buy, categorized by type.

        Args:
            items (list): List of item objects available in the shop.
        """
        first_heal = True
        first_booster = True

        print("\n--- Weapons ---")
        time.sleep(1)
        for i, item in enumerate(items, start=1):
            if first_heal and isinstance(item, HealingPotion):
                print("\n--- Healing Potions ---")
                first_heal = False
                time.sleep(1)

            if first_booster and isinstance(item, StatBooster):
                print("\n--- Stat Boosters ---")
                first_booster = False
                time.sleep(1)

            print(item.__str__(i), f"Price: {item.price:>{6}}")

        self.print_buy_items_decision()

    def print_at_open_sell_items_menu(self):
        """
        Prints the player's inventory and convoy for selling items.
        """
        player = self.root_service.current_game.player
        convoy = self.root_service.current_game.convoy

        print("--- Inventory ---")
        index = 1
        if player.items:
            for item in player.items:
                print(item.__str__(index), f"Price: {item.price:>{6}}")
                index += 1
        else:
            print("No weapons in inventory.")

        print("\n--- Convoy Storage ---")
        time.sleep(1)
        if convoy:
            for item in convoy:
                print(item.__str__(index), f"Price: {item.price:>{6}}")
        else:
            print("Convoy is empty.")

        self.print_sell_items_decision()

    def print_buy_items_decision(self):
        """
        Prints guidance for player actions in the buy items menu.
        """
        print("========================================")
        print("What do you want to do?")
        print("buy <no>    - Buy item")
        print("exit        - Leave shop")
        print("========================================\n")

    def print_sell_items_decision(self):
        """
        Prints guidance for player actions in the sell items menu.
        """
        print("========================================")
        print("What do you want to do?")
        print("sell <no>   - Sell item")
        print("exit        - Leave shop")
        print("========================================\n")

    def print_at_full_inventory(self):
        """
        Prints a warning when the player's inventory is full and
        instructs which item can be sent to the convoy.
        """
        player = self.root_service.current_game.player
        print("Your inventory is full!")
        time.sleep(1)
        print("--- Inventory ---")

        for index, weapon in enumerate(player.items, start=1):
            print(f"{index}) {weapon}")

        print("========================================")
        print("Write the number of the item you want to send to the convoy")
        print("========================================\n")