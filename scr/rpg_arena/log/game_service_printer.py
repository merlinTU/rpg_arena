
class GameServicePrinter():
    def __init__(self, root_service: "RootService"):
        self.root_service = root_service

    def print_after_start_game(self, initial_units):
        print("=== Welcome to the Arena! ===\n")
        print("=== Choose your Fighter ===\n")
        self.print_initial_units(initial_units)

        player_unit = self.root_service.player_action_service.choose_unit(initial_units)
        print("You chose: ", player_unit.name, "the ", player_unit.player_class.name)
        self.root_service.current_game.player = player_unit
        self.root_service.game_service.start_first_round()

    def print_after_start_frist_round(self, enemy_units):
        print("=== You enter the Arena ===\n")
        print("=== Infront of you stand 3 Gladiors ===\n")

        self.print_enemy_units(enemy_units)
        enemy_unit = self.root_service.player_action_service.choose_enemy(enemy_units)
        self.root_service.arena_service.start_arena(enemy_unit)


    def print_enemy_units(self, enemy_units):
        for unit in enemy_units:
            self.print_unit_stats(unit, is_not_enemy=False)


    def print_initial_units(self, initial_units):
        for unit in initial_units:
            self.print_unit_stats(unit)

    def print_unit_stats(self, unit, is_not_enemy = True):
        if is_not_enemy:
            stats = (
            f"HP: {unit.hp} / "
            f"Str: {unit.strength} / "
            f"Mag: {unit.magic} / "
            f"Skill: {unit.skill} / "
            f"Spd: {unit.speed} / "
            f"Luck: {unit.luck} / "
            f"Def: {unit.defense} / "
            f"Res: {unit.res}"
            )
        else:
            stats = (
                f"Lv: {unit.level} / "
                f"Gold: {unit.gold} / "
            )
        print(f"{unit.name} ({unit.player_class.value}): {stats}")
