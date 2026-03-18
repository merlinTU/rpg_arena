import pytest
from unittest.mock import MagicMock

from rpg_arena.entity import Weapon, WeaponType
from rpg_arena.service.root_service import RootService
from rpg_arena.log.information_service_printer import InformationServicePrinter


@pytest.fixture
def info_printer_setup():
    """
    Provides a RootService with mocked current_game, game_service, arena_service,
    and an InformationServicePrinter for testing.

    Returns:
        tuple:
            root_service (RootService): The mocked root service.
            printer (InformationServicePrinter): The printer instance under test.
    """
    root_service = RootService()
    root_service.current_game = MagicMock()
    root_service.game_service = MagicMock()
    root_service.arena_service = MagicMock()
    printer = InformationServicePrinter(root_service)
    return root_service, printer


def test_print_player(info_printer_setup):
    """
    Tests that printing the player calls game_service.printer.print_unit_stats
    with the player and correct argument.
    """
    root_service, printer = info_printer_setup
    player_mock = MagicMock()
    root_service.current_game.player = player_mock

    printer.print_player()

    root_service.game_service.printer.print_unit_stats.assert_called_once_with(player_mock, 1)


def test_print_enemy(info_printer_setup):
    """
    Tests that printing the enemy calls game_service.printer.print_unit_stats
    with the enemy and correct argument.
    """
    root_service, printer = info_printer_setup
    enemy_mock = MagicMock()
    root_service.arena_service.enemy = enemy_mock

    printer.print_enemy()

    root_service.game_service.printer.print_unit_stats.assert_called_once_with(enemy_mock, 1)


def test_print_weapon_info(info_printer_setup, capsys):
    """
    Tests that print_weapon_info prints the weapon's string representation.
    """
    _, printer = info_printer_setup
    weapon = Weapon("TestWeapon", WeaponType.SWORD, 1,2,3,4,5,0)

    printer.print_weapon_info(weapon)
    captured = capsys.readouterr()

    # Split the output into words, remove empty strings
    words = [w for w in captured.out.replace("\n", " ").split(" ") if w]

    assert "TestWeapon" in words
    assert "1" in words
    assert "2" in words
    assert "3" in words
    assert "4" in words
    assert "5" in words
    assert "0" not in words


def test_print_all_stats(info_printer_setup, capsys):
    """
    Tests that print_all_stats prints all expected player stats.
    """
    _, printer = info_printer_setup

    printer.print_all_stats()
    captured = capsys.readouterr()

    for stat in ["HP", "STR", "MAG", "SKL", "SPD", "LUCK", "DEF", "RES"]:
        assert stat in captured.out


def test_print_stat_known(info_printer_setup, capsys):
    """
    Tests that printing a known stat prints its full name.
    """
    _, printer = info_printer_setup

    printer.print_stat("hp")
    captured = capsys.readouterr()

    assert "Health Points" in captured.out

def test_print_stat_unknown(info_printer_setup, capsys):
    """
    Tests that printing an unknown stat outputs the 'Unknown stat' message.
    """
    _, printer = info_printer_setup

    printer.print_stat("foobar")
    captured = capsys.readouterr()

    assert "Unknown stat" in captured.out


def test_print_all_combat_stats(info_printer_setup, capsys):
    """
    Tests that print_all_combat_stats prints all expected combat stats.
    """
    _, printer = info_printer_setup

    printer.print_all_combat_stats()
    captured = capsys.readouterr()

    for stat in ["HIT", "AVOID", "ACC", "CRIT", "DAMAGE"]:
        assert stat in captured.out


def test_print_combat_stat_known(info_printer_setup, capsys):
    """
    Tests that printing a known combat stat outputs its full name.
    """
    _, printer = info_printer_setup

    printer.print_combat_stat("hit")
    captured = capsys.readouterr()

    assert "HIT (Hit Rate)" in captured.out


def test_print_combat_stat_unknown(info_printer_setup, capsys):
    """
    Tests that printing an unknown combat stat outputs the 'Unknown combat stat' message.
    """
    _, printer = info_printer_setup

    printer.print_combat_stat("foobar")
    captured = capsys.readouterr()

    assert "Unknown combat stat" in captured.out