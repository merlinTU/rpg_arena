
from rpg_arena.entity.healing_potion import HealingPotion
from rpg_arena.entity.stat_booster import StatBooster
from rpg_arena.log.shop_service_printer import ShopServicePrinter
from rpg_arena.service.shop_action_service import ShopActionService
from rpg_arena.service.data.item_data import ITEMS
from rpg_arena.service.data.weapon_data import WEAPONS

class ShopService:
    """
    Service responsible for managing the shop, buying and selling items and weapons.

    Attributes:
        root_service (RootService): Reference to the central RootService for access to other services.
        printer (ShopServicePrinter): Printer instance for displaying shop menus.
        action_service (ShopActionService): Handles player input/actions in the shop.
        shop_items (list): List of items currently available in the shop.

    Methods:
        open_shop(): Open the shop and initialize available items.
        open_buy_items_menu(): Open the buy items menu and allow purchases.
        open_sell_items_menu(): Open the sell items menu and allow selling.
        generate_shop_weapons(player_weapons): Populate shop with weapons available for the player class.
        generate_shop_items(): Populate shop with healing and stat-boosting items.
        buy_item(item): Buy a given item for the player.
        sell_item(number): Sell an item from inventory or convoy by index.
    """

    def __init__(self, root_service: "RootService"):
        """
        Initialize ShopService with a reference to RootService.

        Args:
            root_service (RootService): Central service managing all sub-services.
        """
        self.root_service = root_service
        self.printer = ShopServicePrinter(root_service)
        self.action_service = ShopActionService(root_service)
        self.shop_items = []

    def open_shop(self):
        """
        Open the shop, generate available weapons and items, and print the shop menu.

        Returns:
            None
        """
        player_weapons = self.root_service.current_game.player_weapons
        self.generate_shop_weapons(player_weapons)
        self.generate_shop_items()
        self.printer.print_at_open_shop()
        self.action_service.choose_shop_action()

    def open_buy_items_menu(self):
        """
        Open the buy items menu and allow the player to choose items to purchase.

        Returns:
            None
        """
        self.printer.print_at_open_buy_items_menu(items=self.shop_items)
        self.action_service.make_buy_items_decision()

    def open_sell_items_menu(self):
        """
        Open the sell items menu and allow the player to sell items from inventory or convoy.

        Returns:
            None
        """
        player = self.root_service.current_game.player
        convoy = self.root_service.current_game.convoy

        if not player.items and not convoy.items:
            print("You have no items to sell.")
            self.open_shop()
            return

        self.printer.print_at_open_sell_items_menu()
        self.action_service.make_sell_items_decision()

    def generate_shop_weapons(self, player_weapons):
        """
        Populate shop with weapons that the player can buy.

        Args:
            player_weapons (list): List of allowed weapon types for the player's class.

        Returns:
            None
        """
        shop_weapons = [w for w in WEAPONS.values() if w.weapon_type in player_weapons]
        for w in shop_weapons:
            self.shop_items.append(w.copy())

    def generate_shop_items(self):
        """
        Populate shop with healing and stat-boosting items.

        Returns:
            None
        """
        for item in ITEMS.values():
            if isinstance(item, HealingPotion):
                self.shop_items.append(item.copy())
        for item in ITEMS.values():
            if isinstance(item, StatBooster):
                self.shop_items.append(item.copy())

    def buy_item(self, item):
        """
        Buy an item for the player, deduct gold, and handle inventory overflow.

        Args:
            item: The item to buy.

        Returns:
            None
        """
        game = self.root_service.current_game
        player = game.player
        player.gold -= item.price

        print(player.name, "bought", item.name)
        print("You have", player.gold, "gold left")

        player.items.append(item.copy())

        if len(player.items) > game.max_items:
            self.printer.print_at_full_inventory()
            self.action_service.make_send_to_convoy_decision()

        self.printer.print_buy_items_decision()

    def sell_item(self, number: int):
        """
        Sell an item from the player's inventory or convoy by index.

        Args:
            number (int): Index of the item to sell.

        Returns:
            None
        """
        game = self.root_service.current_game
        player = game.player

        if number > len(player.items):
            number -= len(player.items)
            item = game.convoy.pop(number)
        else:
            item = player.items.pop(number)

        player.gold += item.price

        print(player.name, "sold", item.name, f"and gained {item.price}.")
        print("You have", player.gold, "gold now.")

        self.open_sell_items_menu()