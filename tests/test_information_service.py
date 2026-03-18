import pytest
from unittest.mock import MagicMock
from rpg_arena.service.information_service import InformationService
from rpg_arena.service.data.weapon_data import WEAPONS


@pytest.fixture
def info_service_setup():
    """
    Provides an InformationService instance with a mocked RootService and
    all printer methods mocked for testing.

    Returns:
        tuple:
            service (InformationService): The service under test.
            printer (MagicMock): The mocked printer with all print methods mocked.
    """
    # RootService-Mock
    root_mock = MagicMock()
    root_mock.current_game = MagicMock()
    root_mock.current_game.player = MagicMock()
    root_mock.current_game.enemy = MagicMock()

    service = InformationService(root_mock)

    printer = service.printer
    printer.print_player = MagicMock()
    printer.print_enemy = MagicMock()
    printer.print_all_stats = MagicMock()
    printer.print_stat = MagicMock()
    printer.print_all_combat_stats = MagicMock()
    printer.print_combat_stat = MagicMock()
    printer.print_weapon_info = MagicMock()

    return service, printer


def test_check_information_service_player(info_service_setup):
    """
    Tests that 'info player' calls the printer's print_player method.

    Args:
        info_service_setup: Fixture providing InformationService and mocked printer.
    """
    service, printer = info_service_setup
    result = service.check_information_service_call("info player")
    assert result is True
    printer.print_player.assert_called_once()


def test_check_information_service_enemy(info_service_setup):
    """
    Tests that 'check <enemy name>' calls the printer's print_enemy method.

    Args:
        info_service_setup: Fixture providing InformationService and mocked printer.
    """
    service, printer = info_service_setup
    result = service.check_information_service_call("check gladiator")
    assert result is True
    printer.print_enemy.assert_called_once()


def test_check_information_service_stat(info_service_setup):
    """
    Tests that 'info <stat>' calls the printer's print_stat method with the correct stat.

    Args:
        info_service_setup: Fixture providing InformationService and mocked printer.
    """
    service, printer = info_service_setup
    result = service.check_information_service_call("info str")
    assert result is True
    printer.print_stat.assert_called_once_with("str")


def test_check_information_service_all_stats(info_service_setup):
    """
    Tests that 'info stats' calls the printer's print_all_stats method.

    Args:
        info_service_setup: Fixture providing InformationService and mocked printer.
    """
    service, printer = info_service_setup
    result = service.check_information_service_call("info stats")
    assert result is True
    printer.print_all_stats.assert_called_once()


def test_check_information_service_combat_stat(info_service_setup):
    """
    Tests that 'info <combat stat>' calls the printer's print_combat_stat method
    with the correct combat stat.

    Args:
        info_service_setup: Fixture providing InformationService and mocked printer.
    """
    service, printer = info_service_setup
    result = service.check_information_service_call("info crit")
    assert result is True
    printer.print_combat_stat.assert_called_once_with("crit")


def test_check_information_service_weapon(info_service_setup):
    """
    Tests that 'info <weapon name>' calls the printer's print_weapon_info method
    with the correct weapon instance.

    Args:
        info_service_setup: Fixture providing InformationService and mocked printer.
    """
    service, printer = info_service_setup
    weapon_name = "Iron Sword"
    result = service.check_information_service_call(f"info {weapon_name}")
    assert result is True
    printer.print_weapon_info.assert_called_once_with(WEAPONS[weapon_name])


def test_check_information_service_unknown(info_service_setup, capsys):
    """
     Tests that an unknown information target prints the correct message
     and still returns True.

     Args:
         info_service_setup: Fixture providing InformationService and mocked printer.
         capsys: Pytest fixture to capture stdout/stderr.
     """
    service, printer = info_service_setup
    result = service.check_information_service_call("info unknown_target")
    captured = capsys.readouterr()
    assert result is True
    assert "Unknown information target" in captured.out

def test_check_information_service_call_is_false(info_service_setup, capsys):
    """
    Tests that invalid or incomplete commands return False.

    Args:
        info_service_setup: Fixture providing InformationService and mocked printer.
        capsys: Pytest fixture to capture stdout/stderr.
    """
    service, printer = info_service_setup
    # fails with command length is smaller than one
    result1 = service.check_information_service_call("info")
    # fails with command ist neither check nor info
    result2 = service.check_information_service_call("test player")
    assert result1 is False
    assert result2 is False

def test_check_information_service_combat(info_service_setup):
    """
     Tests that 'info combat' calls the printer's print_all_combat_stats method.

     Args:
         info_service_setup: Fixture providing InformationService and mocked printer.
     """
    service, printer = info_service_setup

    result = service.check_information_service_call("info combat")
    assert result is True
    printer.print_all_combat_stats.assert_called_once()
