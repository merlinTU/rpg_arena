from __future__ import annotations
import time
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from rpg_arena.service.root_service import RootService
from rpg_arena.entity.healing_potion import HealingPotion
from rpg_arena.entity.stat_booster import StatBooster
from rpg_arena.entity.weapon_skill import WeaponSkill
from rpg_arena.log.shop_service_printer import ShopServicePrinter
from rpg_arena.service.data.prob_skill_data import SKILLS
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
        self.shop_skills =  SKILLS

    def open_shop(self):
        """
        Open the shop, generate available weapons and items, and print the shop menu.

        Returns:
            None
        """
        self.shop_items = []

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

        for item in player.items:
            item.update_price()

        if not player.items and not convoy:
            print("You have no items to sell.")
            self.open_shop()
            return

        self.printer.print_at_open_sell_items_menu()
        self.action_service.make_sell_items_decision()

    def open_buy_skills_menu(self):
        player_skills = self.root_service.current_game.player.skills
        # filter out skills the player already has
        self.shop_skills = [
            skill for skill in self.shop_skills
            if skill.name not in {ps.name for ps in player_skills}
        ]
        self.filter_weapon_skills_for_player()

        self.printer.print_at_open_buy_skills_menu(self.shop_skills)
        self.action_service.make_buy_skills_decision()

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

        if number > len(player.items) or len(player.items) == 0:
            number -= len(player.items)
            item = game.convoy.pop(number)
        else:
            item = player.items.pop(number)

        player.gold += item.price

        if item == player.equipped_weapon:
            player.equipped_weapon = None

        print(player.name, "sold", item.name, f"and gained {item.price}.")
        print("You have", player.gold, "gold now.")

        self.open_sell_items_menu()

    def buy_skill(self, skill):
        player = self.root_service.current_game.player
        game = self.root_service.current_game
        self.shop_skills.remove(skill)

        # for the skills it should not matter that this not a deep copy
        player.skills.append(skill)

        # if weapon skill, player weapons must be updated
        if isinstance(skill, WeaponSkill):
            game.player_weapons.append(skill.weapon_type)


        player.gold -= skill.price
        print(player.name, "bought", skill.name)
        print("You have", player.gold, "gold left")
        time.sleep(1)

        self.open_buy_skills_menu()

    def filter_weapon_skills_for_player(self):
        """
        Removes WeaponSkills from the shop that the player already owns.

        Only WeaponSkill instances are checked; other skills remain unchanged.
        """
        player_weapon_types = self.root_service.current_game.player_weapons

        # Filter Shop WeaponSkills
        self.shop_skills = [
            skill for skill in self.shop_skills
            if not isinstance(skill, WeaponSkill) or skill.weapon_type not in player_weapon_types
        ]


