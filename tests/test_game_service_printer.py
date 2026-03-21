"""
Test module for the GameServicePrinter class.

This module contains unit tests for the GameServicePrinter which is responsible
for displaying game related information to the console.

The tests verify that the printer correctly formats and outputs
information such as fighter selection, fighter statistics and
enemy information at the start of arena rounds.

External dependencies such as RootService and related services
are mocked to isolate the behavior of the GameServicePrinter.

Tested functionality:
- Printing the fighter selection screen
- Printing confirmation after choosing the first fighter
- Printing fighter statistics
- Printing arena round information
"""
import re
from unittest.mock import MagicMock

from rpg_arena.service.root_service import RootService
from rpg_arena.log.game_service_printer import GameServicePrinter
from rpg_arena.entity.fighter import Fighter
from rpg_arena.entity.unit_class import UnitClass


def create_fighter(name, player_class=UnitClass.FIGHTER):
    """Create a fighter with default test stats."""
    fighter = Fighter(player_class)
    fighter.name = name
    fighter.gold = 10
    fighter.level = 1
    fighter.items = []
    return fighter


def test_print_after_start_game(capsys):
    """
    Verify that the fighter selection screen is printed correctly.

    Args:
        capsys : pytest fixture
            Captures printed console output.
    """

    root_service = RootService()
    root_service.current_game = MagicMock()

    fighter = create_fighter("Hero", UnitClass.MAGE)

    printer = GameServicePrinter(root_service)

    printer.print_after_start_game([fighter])

    captured = capsys.readouterr()

    assert "  Welcome to RPG-Arena!" in captured.out
    assert "Choose Your Fighter" in captured.out
    assert "Hero" in captured.out


def test_print_after_choose_first_unit(capsys):
    """
    Verify that a confirmation message is printed after choosing the first fighter.

    Args:
        capsys : pytest fixture
            Captures printed console output.
    """

    root_service = RootService()
    root_service.current_game = MagicMock()

    fighter = create_fighter("Hero", UnitClass.MAGE)

    printer = GameServicePrinter(root_service)

    printer.print_after_choose_first_unit(fighter)

    captured = capsys.readouterr()

    assert "You chose" in captured.out
    assert "Hero" in captured.out
    assert "MAGE" in captured.out


def test_print_unit_stats_with_items(capsys):
    """
    Verify that fighter statistics are printed correctly when items exist.

    Args:
        capsys : pytest fixture
            Captures printed console output.
    """

    root_service = MagicMock()

    fighter = create_fighter("Hero", UnitClass.MAGE)

    item = MagicMock()
    item.name = "Fire"
    fighter.items = [item]

    printer = GameServicePrinter(root_service)

    printer.print_unit_stats(fighter, 1)

    captured = capsys.readouterr()
    output = captured.out

    assert "Hero" in output
    assert "Mage" in output

    # Regex allows flexible spacing in formatted numbers
    assert re.search(r"HP:\s*\d+", output)
    assert re.search(r"STR:\s*\d+", output)

    assert "Items:   Fire" in output


def test_print_unit_stats_no_items(capsys):
    """
    Verify that the printer displays 'Items: None' when the unit has no items.

    Args:
        capsys : pytest fixture
            Captures printed console output.
    """

    root_service = RootService()
    root_service.current_game = MagicMock()

    fighter = create_fighter("Hero", UnitClass.MAGE)

    printer = GameServicePrinter(root_service)

    printer.print_unit_stats(fighter, 1)

    captured = capsys.readouterr()

    assert "Items: None" in captured.out


def test_print_after_start_first_round_with_enemy_units(capsys):
    """
    Verify that the arena start screen prints enemy information
    and triggers the enemy selection process.

    Args:
        capsys : pytest fixture
            Captures printed console output.
    """

    root_service = MagicMock()

    root_service.player_action_service.choose_enemy = MagicMock(return_value="enemy_mock")
    root_service.arena_service.start_arena = MagicMock()

    printer = GameServicePrinter(root_service)

    # Create enemy fighters
    enemy1 = create_fighter("Enemy1")
    enemy1.gold = 10
    enemy1.level = 1

    enemy2 = create_fighter("Enemy2")
    enemy2.gold = 20
    enemy2.level = 2

    enemy_units = [enemy1, enemy2]

    printer.print_after_start_frist_round(enemy_units)

    captured = capsys.readouterr()
    output = captured.out

    assert "THE ARENA AWAITS" in output
    assert "Three gladiators stand before you" in output

    assert "1) Enemy1" in output
    assert "2) Enemy2" in output

    assert "LVL:" in output
    assert "GOLD:" in output

    root_service.player_action_service.choose_enemy.assert_called_once_with(enemy_units)
    root_service.arena_service.start_arena.assert_called_once_with("enemy_mock")