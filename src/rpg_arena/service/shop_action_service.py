from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from rpg_arena.service.root_service import RootService
class ShopActionService:
    """
    Handles all player interactions and decisions inside the shop.

    Attributes:
        root_service (RootService): Reference to the central RootService, allowing access to all services.

    """

    def __init__(self, root_service: "RootService"):
        """
        Initialize ShopActionService with a reference to RootService.

        Args:
            root_service (RootService): Central service managing all sub-services.
        """
        self.root_service = root_service

    def choose_shop_action(self):
        """
        Prompt the player to choose an action in the shop.

        Returns:
            None
        """
        while True:
            choice = input(">> Choose an option (1-3): ")

            if self.root_service.information_service.check_information_service_call(choice):
                continue

            if choice == "exit" or choice == "e":
                self.root_service.camp_service.open_camp()
                break

            if not choice.isdigit():
                print("Invalid input. Please enter a number.")
                continue
            choice = int(choice)

            match choice:
                case 1:
                    self.root_service.shop_service.open_buy_items_menu()
                    break
                case 2:
                    self.root_service.shop_service.open_sell_items_menu()
                    break
                case 3:
                    self.root_service.shop_service.open_buy_skills_menu()
                    break
                case 4:
                    self.root_service.camp_service.open_camp()
                    break
                case _:
                    print("Invalid option. Please choose between 1-3.")

    def make_buy_items_decision(self):
        """
        Handle player input for buying items from the shop.

        Returns:
            None
        """
        game = self.root_service.current_game
        player = game.player
        items = self.root_service.shop_service.shop_items

        while True:
            choice = input(">> Command: ").strip().lower()

            if self.root_service.information_service.check_information_service_call(choice):
                continue

            parts = choice.split()

            if choice == "exit" or choice == "e":
                self.root_service.shop_service.open_shop()
                break

            if len(parts) != 2:
                print("Invalid command. Use: buy <no> or exit")
                continue

            command, number = parts

            if not number.isdigit():
                print("Invalid item number.")
                continue

            number = int(number)

            if number > len(items):
                print("Invalid item number.")
                continue

            match command:
                case "buy":
                    item = items[number - 1]
                    if item.price > player.gold:
                        print("You do not have enough gold!")
                        continue

                    self.root_service.shop_service.buy_item(item)
                    continue

                case _:
                    print("Unknown command. Use: buy or exit.")

    def make_send_to_convoy_decision(self):
        """
        Handle player decision to send an item to the convoy when inventory is full.

        Returns:
            None
        """
        player = self.root_service.current_game.player
        while True:
            choice = input(">> Choose an option: ")

            if self.root_service.information_service.check_information_service_call(choice):
                continue

            if not choice.isdigit():
                print("Invalid input. Please enter a number.")
                continue
            choice = int(choice)

            if choice < 0 or choice > len(player.items):
                print("Invalid input.")
                continue

            # send item to convoy
            game = self.root_service.current_game
            game.convoy.append(player.items.pop(choice - 1))
            break

    def make_sell_items_decision(self):
        """
        Handle player input for selling items.

        Returns:
            None
        """
        items = self.root_service.shop_service.shop_items

        while True:
            choice = input(">> Command: ").strip().lower()

            if self.root_service.information_service.check_information_service_call(choice):
                continue

            parts = choice.split()

            if choice == "exit" or choice == "e":
                self.root_service.shop_service.open_shop()
                break

            if len(parts) != 2:
                print("Invalid command. Use: sell <no> or exit")
                continue

            command, number = parts

            if not number.isdigit():
                print("Invalid item number.")
                continue

            number = int(number)

            if number > len(items):
                print("Invalid item number.")
                continue

            match command:
                case "sell":
                    self.root_service.shop_service.sell_item(number - 1)
                    break

                case _:
                    print("Unknown command. Use sell or exit.")



    def make_buy_skills_decision(self):
        """
        Handle player input for buying skills from the shop.

        Returns:
            None
        """
        game = self.root_service.current_game
        player = game.player
        skills = self.root_service.shop_service.shop_skills

        while True:
            choice = input(">> Command: ").strip().lower()

            if self.root_service.information_service.check_information_service_call(choice):
                continue

            parts = choice.split()

            if choice == "exit" or choice == "e":
                self.root_service.shop_service.open_shop()
                break

            if len(parts) != 2:
                print("Invalid command. Use: buy <no> or exit")
                continue

            command, number = parts

            if not number.isdigit():
                print("Invalid item number.")
                continue

            number = int(number)

            if number > len(skills):
                print("Invalid item number.")
                continue

            match command:
                case "buy":
                    skill = skills[number - 1]
                    if skill.price > player.gold:
                        print("You do not have enough gold!")
                        continue

                    self.root_service.shop_service.buy_skill(skill)
                    return

                case _:
                    print("Unknown command. Use: buy or exit.")
