from rpg_arena.log.camp_service_printer import CampServicePrinter


class CampService:
    def __init__(self, root_service: "RootService"):
        self.root_service = root_service
        self.printer = CampServicePrinter(root_service)

    def open_camp(self):
        self.printer.print_at_open_menu()
        self.root_service.camp_action_service.choose_camp_action()

    def open_item_manager(self ):
        self.printer.print_at_open_item_manager()
        pass

    def open_shop(self):
        pass