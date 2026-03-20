import pytest
from unittest.mock import MagicMock, patch

from rpg_arena.entity import UnitClass, Fighter
from rpg_arena.service.arena_action_service import ArenaActionService
from rpg_arena.entity.weapon import Weapon, WeaponType
from rpg_arena.entity.healing_potion import HealingPotion

@pytest.fixture
def arena_action_service_setup():
    """
    Provides a fully mocked setup for testing the ArenaActionService.

    Initializes a mock RootService with a player and enemy, and configures
    all dependent services and printer methods to avoid side effects during tests.

    Returns:
        tuple: Contains the initialized ArenaActionService, the mocked root service,
        the player instance, and the enemy instance.
    """
    root_service_mock = MagicMock()
    root_service_mock.current_game = MagicMock()
    player = Fighter(UnitClass.MAGE)
    player.hp = 20
    player.name = "Test"
    player.max_hp = 20
    enemy = Fighter(UnitClass.FIGHTER)
    enemy.hp = 30
    enemy.name = "Gladiator"
    player.equipped_weapon = None
    root_service_mock.current_game.player = player

    # mock arnea service functions
    root_service_mock.arena_service = MagicMock()
    root_service_mock.arena_service.enemy = enemy
    root_service_mock.arena_service.make_fight_round = MagicMock()
    root_service_mock.information_service = MagicMock()
    root_service_mock.information_service.check_information_service_call = MagicMock(return_value=False)

    # mock printer functions
    service = ArenaActionService(root_service_mock)
    service.printer.print_at_make_player_round_decsion = MagicMock()
    service.printer.print_at_open_fight_menu = MagicMock()
    service.printer.print_fight_preview = MagicMock()
    service.printer.print_after_print_fight_preview = MagicMock()
    service.printer.print_inventory = MagicMock()
    return service, root_service_mock, player, enemy

def test_make_enemy_round_decision(arena_action_service_setup, capsys):
    """
    Tests enemy behavior: waits without weapon and attacks with a weapon.

    Args:
        arena_action_service_setup (tuple): Fixture providing the initialized
            arena action service and related test objects.
    """
    service, root, player, enemy = arena_action_service_setup

    service.make_enemy_round_decision()
    captured = capsys.readouterr()
    assert "> Gladiator waits." in captured.out

    enemy.equipped_weapon = MagicMock() # exact weapon not relevant here
    service.make_enemy_round_decision()
    assert root.arena_service.make_fight_round.call_count == 1


def test_make_player_round_decision_fight_menu(arena_action_service_setup):
    """
    Tests that selecting option '1' opens the fight menu when the player has a weapon.

    Args:
        arena_action_service_setup (tuple): Fixture providing the initialized
            arena action service and related test objects.
    """
    service, root_mock, player, enemy = arena_action_service_setup
    service.open_fight_menu = MagicMock()
    # information service call should be false
    root_mock.information_service.check_information_service_call = MagicMock(return_value=False)
    test_weapon = Weapon("Test", WeaponType.SWORD,0,0,0,0,0,0)
    player.items = [test_weapon]

    with patch("builtins.input", side_effect=["1"]):
        service.make_player_round_decision()
        assert service.open_fight_menu.call_count == 1


def test_make_player_round_decision_inventory(arena_action_service_setup):
    """
    Tests that selecting option '2' opens the player's inventory.

    Args:
        arena_action_service_setup (tuple): Fixture providing the initialized
            arena action service and related test objects.
    """
    service, root_mock, _, _ = arena_action_service_setup
    root_mock.information_service.check_information_service_call = MagicMock(return_value=False)

    with patch("builtins.input", side_effect=["2"]):
        service.open_inventory = MagicMock()
        service.make_player_round_decision()
        service.open_inventory.assert_called_once()


def test_make_player_round_decision_wait(arena_action_service_setup, capsys):
    """
    Tests that selecting option '3' causes the player to wait.

    Args:
        arena_action_service_setup (tuple): Fixture providing the initialized
            arena action service and related test objects.
        capsys: Pytest fixture to capture stdout/stderr output.
    """
    service, root_mock, _, _ = arena_action_service_setup
    root_mock.information_service.check_information_service_call = MagicMock(return_value=False)

    with patch("builtins.input", side_effect=["3"]):
        service.make_player_round_decision()
        captured = capsys.readouterr()
        assert "> Test waits\n" in captured.out


def test_make_player_round_decision_surrender_yes(arena_action_service_setup):
    """
    Tests that selecting option '4' and confirming with 'y' sets continue_fight to 'surrender'.

    Args:
        arena_action_service_setup (tuple): Fixture providing the initialized
            arena action service and related test objects.
    """
    service, root_mock, _, _ = arena_action_service_setup
    root_mock.information_service.check_information_service_call = MagicMock(return_value=False)

    with patch("builtins.input", side_effect=["4", "y"]):
        service.make_player_round_decision()
        assert root_mock.arena_service.continue_fight == "surrender"

def test_make_player_round_decision_surrender_no(arena_action_service_setup, capsys):
    """
    Tests that selecting option '4' and answering 'n' does not surrender the fight,
    and the player can then choose to wait (option '3').

    Args:
        arena_action_service_setup (tuple): Fixture providing the initialized
            arena action service and related test objects.
        capsys: Pytest fixture to capture stdout/stderr output.
    """
    service, root_mock, _, _ = arena_action_service_setup
    root_mock.information_service.check_information_service_call = MagicMock(return_value=False)

    # to correctly end the loop
    with patch("builtins.input", side_effect=["4", "n", "3"]):
        service.make_player_round_decision()
        captured = capsys.readouterr()
        assert "> Test waits\n" in captured.out

def test_make_player_round_decision_invalid_input(arena_action_service_setup, capsys):
    """
    Tests that invalid input prompts an error message and allows the player to re-enter a choice.

    Args:
        arena_action_service_setup (tuple): Fixture providing the initialized
            arena action service and related test objects.
        capsys: Pytest fixture to capture stdout/stderr output.
    """
    service, root_mock, _, _ = arena_action_service_setup

    with patch("builtins.input", side_effect=["x", "3"]):
        service.make_player_round_decision()
    captured = capsys.readouterr()
    assert "Invalid choice. Please enter 1, 2, 3 or 4." in captured.out

def test_make_player_round_decision_information_service_call(arena_action_service_setup):
    """
    Tests that the information service correctly intercepts player input and
    causes the input loop to continue until a valid choice is made.

    Args:
        arena_action_service_setup (tuple): Fixture providing the initialized
            arena action service and related test objects.
    """
    service, root_mock, _, _ = arena_action_service_setup
    root_mock.information_service.check_information_service_call = MagicMock(side_effect=[True, False])

    with patch("builtins.input", side_effect=["info enemy", "3"]): # to end the loop
        service.make_player_round_decision()

    # check information service call
    assert root_mock.information_service.check_information_service_call.call_count == 2


def test_open_fight_menu(arena_action_service_setup):
    """
    Tests that `open_fight_menu` correctly calls all expected sub-methods and printers.

    The method is tested in isolation by mocking all recursive or interactive calls
    to prevent loops or user input requirements.

    Args:
        arena_action_service_setup (tuple): Fixture providing the initialized
            arena action service and related test objects.
    """
    service, root_mock, _, _ = arena_action_service_setup

    # mock all recursive methods to make to function stop
    service.choose_weapon_to_equip = MagicMock()
    service.make_fight_menu_choice = MagicMock()
    service.printer.print_at_open_fight_menu = MagicMock()
    service.printer.print_fight_preview = MagicMock()
    service.printer.print_after_print_fight_preview = MagicMock()

    # call methode
    service.open_fight_menu()

    # assert printer calls
    service.printer.print_at_open_fight_menu.assert_called_once()
    service.choose_weapon_to_equip.assert_called_once()
    service.printer.print_fight_preview.assert_called_once()
    service.printer.print_after_print_fight_preview.assert_called_once()
    service.make_fight_menu_choice.assert_called_once()

def test_make_fight_menu_choice_fight(arena_action_service_setup):
    """
    Tests that selecting '1' in the fight menu triggers a fight round with the enemy.

    Args:
        arena_action_service_setup (tuple): Fixture providing the initialized
            arena action service and related test objects.
    """
    service, root_mock, _, _ = arena_action_service_setup

    with patch("builtins.input", side_effect=["1"]):
        service.make_fight_menu_choice()
        root_mock.arena_service.make_fight_round.assert_called_once_with(
            root_mock.current_game.player, root_mock.arena_service.enemy
        )

def test_make_fight_menu_choice_open_menu(arena_action_service_setup):
    """
    Tests that selecting '2' in the fight menu re-opens the fight menu.

    Args:
        arena_action_service_setup (tuple): Fixture providing the initialized
            arena action service and related test objects.
    """
    service, root_mock, _, _ = arena_action_service_setup

    with patch("builtins.input", side_effect=["2"]):
        service.open_fight_menu = MagicMock()
        service.make_fight_menu_choice()
        service.open_fight_menu.assert_called_once()

def test_make_fight_menu_choice_player_round(arena_action_service_setup):
    """
     Tests that selecting '3' in the fight menu triggers the player's round decision.

     Args:
         arena_action_service_setup (tuple): Fixture providing the initialized
             arena action service and related test objects.
     """
    service, root_mock, _, _ = arena_action_service_setup

    with patch("builtins.input", side_effect=["3"]):
        service.make_player_round_decision = MagicMock()
        service.make_fight_menu_choice()
        service.make_player_round_decision.assert_called_once()

def test_make_fight_menu_choice_invalid_input(arena_action_service_setup):
    """
    Tests that invalid input in the fight menu is handled by looping until a valid choice.

    Args:
        arena_action_service_setup (tuple): Fixture providing the initialized
            arena action service and related test objects.
    """
    service, root_mock, _, _ = arena_action_service_setup

    with patch("builtins.input", side_effect=["x", "3"]): # to end the loop
        service.make_player_round_decision = MagicMock()
        service.make_fight_menu_choice()
        service.make_player_round_decision.assert_called_once()

def test_make_fight_menu_choice_information_service(arena_action_service_setup):
    """
    Tests that the fight menu correctly defers to the information service when input is intercepted.

    Args:
        arena_action_service_setup (tuple): Fixture providing the initialized
            arena action service and related test objects.
    """
    service, root_mock, _, _ = arena_action_service_setup
    root_mock.information_service.check_information_service_call.side_effect = [True, False]

    with patch("builtins.input", side_effect=["info", "3"]):
        service.make_player_round_decision = MagicMock()
        service.make_fight_menu_choice()
        service.make_player_round_decision.assert_called_once()
    assert root_mock.information_service.check_information_service_call.call_count == 2

def test_choose_weapon_to_equip_valid(arena_action_service_setup):
    """
    Tests that `choose_weapon_to_equip` correctly equips a valid weapon selected by the player.

    Args:
        arena_action_service_setup (tuple): Fixture providing the initialized
            arena action service and related test objects.
    """
    service, root_mock, _, _ = arena_action_service_setup
    root_mock.arena_service.continue_fight = None
    root_mock.information_service.check_information_service_call.return_value = False

    weapon1 = Weapon("Sword", WeaponType.SWORD, 0, 0, 0, 0, 0, 0)
    weapon2 = Weapon("Axe", WeaponType.AXE, 0, 0, 0, 0, 0, 0)
    root_mock.current_game.player.items = [weapon1, weapon2]

    with patch("builtins.input", side_effect=["1"]):
        service.choose_weapon_to_equip()
        assert root_mock.current_game.player.equipped_weapon == weapon1

def test_choose_weapon_to_equip_invalid_non_number(arena_action_service_setup):
    """
    Tests that `choose_weapon_to_equip` correctly handles non-numeric input by
    looping until a valid weapon selection is made.

    Args:
        arena_action_service_setup (tuple): Fixture providing the initialized
            arena action service and related test objects.
    """
    service, root_mock, _, _ = arena_action_service_setup
    # player need weapon to call that methode
    weapon = Weapon("Sword", WeaponType.SWORD, 10, 80, 10, 5, 5, 100)
    root_mock.current_game.player.items = [weapon]

    with patch("builtins.input", side_effect=["x", "1"]):
        service.choose_weapon_to_equip()
        assert root_mock.current_game.player.equipped_weapon == weapon

def test_choose_weapon_to_equip_invalid_out_of_range(arena_action_service_setup):
    """
    Tests that `choose_weapon_to_equip` correctly handles numeric input that is
    out of the valid inventory range by looping until a valid selection is made.

    Args:
        arena_action_service_setup (tuple): Fixture providing the initialized
            arena action service and related test objects.
    """
    service, root_mock, player, _ = arena_action_service_setup
    # player needs a weapon to call that methode
    weapon = Weapon("Sword", WeaponType.SWORD, 10, 80, 10, 5, 5, 100)
    player.items = [weapon]

    with patch("builtins.input", side_effect=["5", "1"]):
        service.choose_weapon_to_equip()
        assert root_mock.current_game.player.equipped_weapon == weapon


def test_make_inventory_decision_use_healing_potion(arena_action_service_setup):
    """
    Tests that `make_inventory_decision` correctly uses a healing potion
    and removes it from the player's inventory.

    Args:
        arena_action_service_setup (tuple): Fixture providing the initialized
            arena action service and related test objects.
    """
    service, root_mock, player, _ = arena_action_service_setup
    player.hp = 10
    player.max_hp = 15

    potion = HealingPotion("Potion", 5, 1, 90)
    player.items = [potion]

    initial_hp = player.hp
    with patch.object(service, "open_inventory", return_value=None), \
         patch("builtins.input", side_effect=["use 1"]):
        service.make_inventory_decision()

    assert player.hp == 15
    assert player.items == []

def test_make_inventory_decision_exit_command(arena_action_service_setup):
    """
    Tests that `make_inventory_decision` correctly exits the inventory menu
    when the player enters the 'exit' command.

    Args:
        arena_action_service_setup (tuple): Fixture providing the initialized
            arena action service and related test objects.
    """
    service, root_mock, _, _ = arena_action_service_setup
    service.make_player_round_decision = MagicMock()

    with patch.object(service, "open_inventory", return_value=None), \
         patch("builtins.input", side_effect=["exit"]):
        service.make_inventory_decision()

    service.make_player_round_decision.assert_called_once()




