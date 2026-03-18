import pytest
from unittest.mock import MagicMock

from rpg_arena.entity import Weapon, HealingPotion, StatBooster, WeaponType
from rpg_arena.service.root_service import RootService
from rpg_arena.log.camp_service_printer import CampServicePrinter

@pytest.fixture
def camp_printer_setup():
    """
    Fixture that provides a RootService with a mocked current_game and a CampServicePrinter.

    Returns:
        tuple: (printer, root_service)
    """
    root_service = RootService()
    root_service.current_game = MagicMock()
    printer = CampServicePrinter(root_service)
    return printer, root_service


def test_print_at_open_menu_first_round(camp_printer_setup, capsys):
    """
    Tests that the menu text for the first round is printed correctly.
    """
    printer, root = camp_printer_setup
    root.current_game.round = 1

    printer.print_at_open_menu()
    captured = capsys.readouterr()

    assert "first battle" in captured.out
    assert "Enter the arena" in captured.out


def test_print_at_open_menu_later_round(camp_printer_setup, capsys):
    """
    Tests that the menu text for later rounds is printed correctly.
    """
    printer, root = camp_printer_setup
    root.current_game.round = 3

    printer.print_at_open_menu()
    captured = capsys.readouterr()

    assert "return to the camp" in captured.out
    assert "Visit the merchant" in captured.out


def test_print_at_open_item_manager_empty_inventory(camp_printer_setup, capsys):
    """
    Tests the item manager display when both player inventory and convoy are empty.
    """
    printer, root = camp_printer_setup
    root.current_game.player.items = []
    root.current_game.convoy = []

    printer.print_at_open_item_manager()
    captured = capsys.readouterr()

    assert "No weapons in inventory" in captured.out
    assert "Convoy is empty" in captured.out
    assert "send <no>" in captured.out
    assert "exit" in captured.out


def test_print_at_open_item_manager_with_items(camp_printer_setup, capsys):
    """
    Tests the item manager display when player inventory and convoy contain items.
    Uses actual item classes.
    """
    printer, root = camp_printer_setup

    weapon = Weapon("Sword", WeaponType.SWORD, 10, 80, 20, 5, 5, 100)
    potion = HealingPotion("Small Potion", 10, 1, 50)
    booster = StatBooster("STR Booster", "STR", 5, 75)

    root.current_game.player.items = [weapon, potion, booster]
    root.current_game.convoy = [weapon, potion, booster]

    printer.print_at_open_item_manager()
    captured = capsys.readouterr()

    # Check that string representations appear
    assert "Sword" in captured.out
    assert "Small Potion" in captured.out
    assert "STR Booster" in captured.out

    # Check command hints are printed
    assert "send <no>" in captured.out
    assert "take <no>" in captured.out