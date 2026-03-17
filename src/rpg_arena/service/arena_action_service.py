from __future__ import annotations
from typing import TYPE_CHECKING

from rpg_arena.entity.weapon import Weapon
from rpg_arena.entity.healing_potion import HealingPotion
from rpg_arena.log.arena_service_printer import ArneaServicePrinter

if TYPE_CHECKING:
    from rpg_arena.service.root_service import RootService

class ArenaActionService:
    """
    Service class responsible for managing player and enemy decisions during arena battles.

    Attributes:
        root_service (RootService): Reference to the root service managing all sub-services.
        printer (ArneaServicePrinter): Utility to print arena menus and updates.

    """

    def __init__(self, root_service: RootService):
        """
        Initialize ArenaActionService with a reference to the root service.

        Args:
            root_service (RootService): Central service managing all other services.

        Returns:
            None
        """
        self.root_service = root_service
        self.printer = ArneaServicePrinter(root_service)

    def make_player_round_decision(self):
        """
        Handle the player's decision during their turn in the arena.

        Returns:
            None
        """
        self.printer.print_at_make_player_round_decsion()

        while True:
            choice = input(">> Choose an option (1-4): ").strip().lower()

            if self.root_service.information_service.check_information_service_call(choice):
                continue

            if choice not in ("1", "2", "3", "4"):
                print("Invalid choice. Please enter 1, 2, 3 or 4.")
                continue
            choice = int(choice)

            if choice == 1:
                player = self.root_service.current_game.player
                for item in player.items:
                    if isinstance(item, Weapon):
                        self.open_fight_menu()
                        return
                print("You can't attack. You have no Weapons!")

            elif choice == 2:
                self.open_inventory()
                break
            elif choice == 3:
                print(">", self.root_service.current_game.player.name, "waits")
                break
            elif choice == 4:
                confirm = input(">> Are you sure you want to surrender? (y/n): ").lower()
                if confirm == "y":
                    self.root_service.arena_service.continue_fight = "surrender"
                    break
                else:
                    continue

    def open_fight_menu(self):
        """
        Open the fight menu and allow the player to choose a weapon.

        Returns:
            None
        """
        self.printer.print_at_open_fight_menu()
        self.choose_weapon_to_equip()
        self.printer.print_fight_preview()
        self.printer.print_after_print_fight_preview()
        self.make_fight_menu_choice()

    def make_fight_menu_choice(self):
        """
        Handle player's choice in the fight menu.

        Returns:
            None
        """
        while True:
            choice = input(">> Choose an option (1-3): ").strip().lower()

            if self.root_service.information_service.check_information_service_call(choice):
                continue

            if choice not in ("1", "2", "3"):
                print("Invalid choice. Please enter 1, 2, or 3.")
                continue
            choice = int(choice)

            match choice:
                case 1:
                    player = self.root_service.current_game.player
                    enemy = self.root_service.arena_service.enemy
                    self.root_service.arena_service.make_fight_round(player, enemy)
                    break
                case 2:
                    self.open_fight_menu()
                    break
                case 3:
                    self.make_player_round_decision()
                    break

    def choose_weapon_to_equip(self):
        """
        Allow the player to select and equip a weapon from their inventory.

        Returns:
            None
        """
        while True:
            choice = input(">> Choose an option: ").strip().lower()

            if self.root_service.information_service.check_information_service_call(choice):
                continue

            if not choice.isdigit():
                print("Invalid input. Please enter a number.")
                continue
            choice = int(choice)

            if choice < 1 or choice > len(self.root_service.current_game.player.items):
                print(f"Invalid input.")
            else:
                player = self.root_service.current_game.player
                weapons = [item for item in player.items if isinstance(item, Weapon)]
                player.equipped_weapon = weapons[choice - 1]
                break

    def open_inventory(self):
        """
        Open the player's inventory menu and handle item management.

        Returns:
            None
        """
        self.printer.print_inventory()
        self.make_inventory_decision()

    def make_enemy_round_decision(self):
        """
        Handle the enemy's round decision automatically.

        Returns:
            None
        """
        player = self.root_service.current_game.player
        enemy = self.root_service.arena_service.enemy
        if enemy.equipped_weapon is None:
            print("> Gladiator waits.")
        else:
            self.root_service.arena_service.make_fight_round(enemy, player)

    def make_inventory_decision(self):
        """
        Handle inventory commands like 'equip', 'use', and 'exit'.

        Returns:
            None
        """
        game = self.root_service.current_game
        player = game.player

        while True:
            choice = input(">> Command: ").strip().lower()

            if self.root_service.information_service.check_information_service_call(choice):
                continue

            parts = choice.split()

            if choice in ("exit", "e"):
                self.make_player_round_decision()
                return

            if len(parts) != 2:
                print("Invalid command. Use: send <no>, take <no>, use <no>, exit")
                continue

            command, number = parts

            if not number.isdigit():
                print("Invalid item number.")
                continue

            number = int(number)

            if number > len(player.items):
                print("Invalid item number.")
                continue

            match command:
                case "equip":
                    weapon = player.items[number]
                    if not isinstance(weapon, Weapon):
                        print("You can't equip this item.")
                        continue
                    player.equipped_weapon = player.items[number - 1]
                    print(player.name, "equipped,", weapon.name)
                    self.open_inventory()
                    return

                case "use":
                    item = player.items[number]
                    if not item.usable:
                        print("Item not usable.")
                        continue
                    item.use(player, game)
                    if isinstance(item, HealingPotion):
                        print(">", player.name, "used", item.name, "and has", player.hp, "now.")
                    break

                case _:
                    print("Unknown command. Use send, take, use or exit.")