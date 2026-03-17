from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from rpg_arena.service.root_service import RootService

class CampActionService:
    """
    Service class responsible for handling player actions within the camp.

    Attributes:
        root_service (RootService): Reference to the root service managing all sub-services.

    """

    def __init__(self, root_service: RootService):
        """
        Initialize the CampActionService with a reference to the root service.

        Args:
            root_service (RootService): Central service managing all other services.

        Returns:
            None
        """
        self.root_service = root_service

    def choose_camp_action(self):
        """
        Prompt the player to choose an action from the camp menu.

        Returns:
            None
        """
        while True:
            choice = input(">> Choose an option: ")

            if self.root_service.information_service.check_information_service_call(choice):
                continue

            if not choice.isdigit():
                print("Invalid input. Please enter a number.")
                continue
            choice = int(choice)

            match choice:
                case 1:
                    self.root_service.game_service.start_arena()
                    break
                case 2:
                    self.root_service.camp_service.open_item_manager()
                    break
                case 3:
                    self.root_service.shop_service.open_shop()
                    break
                case 4:
                    print("Leaving camp...")
                    return
                case _:
                    print("Invalid option. Please choose between 1-4.")

    def choose_item_manager_action(self):
        """
        Handle player commands for managing items in inventory and convoy.

        Returns:
            None
        """
        game = self.root_service.current_game
        player = game.player

        while True:
            choice = input(">> Command: ").strip().lower()

            if self.root_service.information_service.check_information_service_call(choice):
                continue

            if choice in ("exit", "e"):
                self.root_service.camp_service.open_camp()
                return

            parts = choice.split()

            if len(parts) != 2:
                print("Invalid command. Use: send <no>, take <no>, use <no>, exit")
                continue

            command, number = parts

            if not number.isdigit():
                print("Invalid item number.")
                continue

            number = int(number)

            if number > len(player.items) + len(game.convoy):
                print("Invalid item number.")
                continue

            match command:
                case "send":
                    game.convoy.append(player.items.pop(number - 1))
                    self.root_service.camp_service.open_item_manager()
                    break

                case "take":
                    number = len(player.items)
                    player.items.append(game.convoy.pop(number - 1))
                    self.root_service.camp_service.open_item_manager()
                    break

                case "use":
                    if number > len(player.items):
                        number = number - len(player.items)
                        item = game.convoy[number - 1]
                        in_convoy = True
                    else:
                        item = player.items[number - 1]
                        in_convoy = False

                    if not item.usable:
                        print("Item not usable.")
                        continue

                    item.use(player, game, in_convoy)
                    self.root_service.camp_service.open_item_manager()
                    break

                case _:
                    print("Unknown command. Use send, take, use or exit.")