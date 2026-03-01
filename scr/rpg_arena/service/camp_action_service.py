

class CampActionService:
    def __init__(self, root_service: "RootService"):
        self.root_service = root_service

    def choose_camp_action(self):
        while True:
            choice = input(">> Choose an option: ")

            # Prüfen ob Zahl
            if not choice.isdigit():
                print("Invalid input. Please enter a number.")
                continue
            choice = int(choice)

            match choice:
                case 1:
                    self.root_service.game_service.start_first_round()
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