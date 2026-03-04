

class CampActionService:
    def __init__(self, root_service: "RootService"):
        self.root_service = root_service

    def choose_camp_action(self):
        while True:
            choice = input(">> Choose an option: ")

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
                    self.root_service.camp_service.open_shop()
                    break
                case 4:
                    print("Leaving camp...")
                    return
                case _:
                    print("Invalid option. Please choose between 1-4.")

    def choose_item_manager_action(self):
        game = self.root_service.current_game
        player = game.player

        while True:
            choice = input(">> Command: ").strip().lower()

            if choice == "exit":
                self.root_service.camp_service.open_camp()
                return

            parts = choice.split()

            # Erwartet: Befehl + Nummer
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
                        item = game.convoy[number - 1]
                    else:
                        item = player.items[number - 1]

                    if not item.usable:
                        print("Item not usable.")
                        continue

                    item.use(player, game)
                    self.root_service.camp_service.open_item_manager()
                    break

                case _:
                    print("Unknown command. Use send, take, use or exit.")