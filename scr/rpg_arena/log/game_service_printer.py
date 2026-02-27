
class GameServicePrinter:
    def print_after_start_game(self, initial_units):
        print("=== Welcome to the Arena! ===\n")
        print("=== Choose your Fighter ===\n")

        self.print_initial_units(initial_units)


    def print_initial_units(self, initial_units):
        for unit in initial_units:
            self.print_unit_stats(unit)

    def print_unit_stats(self, unit):
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
        print(f"{unit.name} ({unit.player_class.name}): {stats}")
