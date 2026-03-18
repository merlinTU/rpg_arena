import pytest

from rpg_arena.entity import Game, Item, Fighter, UnitClass, HealingPotion, StatBooster
from unittest.mock import MagicMock, patch
from rpg_arena.service.camp_action_service import CampActionService

@pytest.fixture
def camp_action_service_setup():
    """
    Fixture to create a test instance of CampActionService with a partially
    mocked root service.

    Returns:
        tuple:
            service (CampActionService): The service under test.
            root_service_mock (MagicMock): Mocked root service.
    """
    root_service_mock = MagicMock()
    root_service_mock.information_service.check_information_service_call.return_value = False
    root_service_mock.current_game = Game()
    root_service_mock.current_game.player = Fighter(UnitClass.MAGE)
    # mock other services that should not be tested here
    root_service_mock.camp_service = MagicMock()
    root_service_mock.shop_service = MagicMock()
    root_service_mock.game_service = MagicMock()

    service = CampActionService(root_service_mock)
    return service, root_service_mock

# Tests:
def test_choose_camp_action_start_arena(camp_action_service_setup):
    """
    Tests that arena is started correctly.

    Args:
        camp_action_service_setup: Provides CampActionService and mocked root service.
    """
    service, root_mock = camp_action_service_setup
    # User chooses 1 → start_arena called
    with patch("builtins.input", side_effect=["1"]):
        service.choose_camp_action()

    root_mock.game_service.start_arena.assert_called_once()

def test_choose_camp_action_open_item_manager(camp_action_service_setup):
    """
    Tests that item manager is opened correctly.

    Args:
        camp_action_service_setup: Provides CampActionService and mocked root service.
    """
    service, root_mock = camp_action_service_setup

    # User chooses 2 → open_item_manager called
    with patch("builtins.input", side_effect=["2"]):
        service.choose_camp_action()

    root_mock.camp_service.open_item_manager.assert_called_once()

def test_choose_camp_action_open_shop(camp_action_service_setup):
    """
    Tests that shop is opened correctly.

    Args:
        camp_action_service_setup: Provides CampActionService and mocked root service.
    """
    service, root_mock = camp_action_service_setup

    # User chooses 3 → open_shop called
    with patch("builtins.input", side_effect=["3"]):
        service.choose_camp_action()

    root_mock.shop_service.open_shop.assert_called_once()

def test_choose_camp_action_exit(camp_action_service_setup):
    """
    Tests that selecting exit option ends the action without errors.

    Args:
        camp_action_service_setup: Provides CampActionService and mocked root service.
    """
    service, root_mock = camp_action_service_setup

    # User chooses 4 → should exit without error
    with patch("builtins.input", side_effect=["4"]):
        service.choose_camp_action()

# tests for item management
def test_choose_item_manager_send(camp_action_service_setup):
    """
    Tests that sending an item moves it from player inventory to convoy.

    Args:
        camp_action_service_setup: Provides CampActionService and mocked root service.
    """
    service, root_mock = camp_action_service_setup
    game = root_mock.current_game
    player = game.player

    item = Item("Test Item", True, 2)
    player.items.append(item)

    # Send first item to convoy
    with patch("builtins.input", side_effect=["send 1"]):
        service.choose_item_manager_action()

    assert len(player.items) == 0
    assert len(game.convoy) == 1

def test_choose_item_manager_use(camp_action_service_setup):
    """
    Tests using healing items and stat boosters

    Args:
        camp_action_service_setup: Provides CampActionService and mocked root service.
    """
    service, root_mock = camp_action_service_setup
    game = root_mock.current_game
    player = game.player

    player.max_hp = 50
    player.hp = 1

    item1 = HealingPotion("Test Potion", 10, 1, 200)
    item2 = StatBooster("Test Booster", "STR", 50, 200)

    player.items.append(item1)
    player.items.append(item2)
    player.strength = 0

    # Use first item
    with patch("builtins.input", side_effect=["use 1"]):
        service.choose_item_manager_action()

    assert player.hp == 11
    assert item1 not in player.items

    # Use stat booster
    with patch("builtins.input", side_effect=["use 1"]):
        service.choose_item_manager_action()

    assert player.strength == 50
    assert item2 not in player.items


def test_choose_item_manager_exit(camp_action_service_setup):
    """
    Tests that exiting the item manager returns to the camp.

    Args:
        camp_action_service_setup: Provides CampActionService and mocked root service.
    """
    service, root_mock = camp_action_service_setup

    # Exit should call open_camp
    with patch("builtins.input", side_effect=["exit"]):
        service.choose_item_manager_action()

    root_mock.camp_service.open_camp.assert_called_once()


def test_choose_camp_action_info_call(camp_action_service_setup):
    """
     Tests that the information service is called correctly when 'info' is selected.

     Args:
         camp_action_service_setup: Provides CampActionService and mocked root service.
     """
    service, root = camp_action_service_setup

    root.information_service.check_information_service_call.side_effect = [True, False]

    with patch("builtins.input", side_effect=["info", "4"]):
        service.choose_camp_action()

    assert root.information_service.check_information_service_call.call_count == 2

def test_choose_camp_action_invalid_input(camp_action_service_setup):
    """
    Tests that invalid input is handled and the information service is called.

    Args:
        camp_action_service_setup: Provides CampActionService and mocked root service.
    """
    service, root = camp_action_service_setup

    with patch("builtins.input", side_effect=["bad input", "4"]):
        service.choose_camp_action()

    assert root.information_service.check_information_service_call.call_count == 2

def test_choose_item_manager_action_info_call(camp_action_service_setup):
    """
    Tests that the information service is called correctly when 'info' is selected
    in the item manager.

    Args:
        camp_action_service_setup: Provides CampActionService and mocked root service.
    """
    service, root = camp_action_service_setup

    root.information_service.check_information_service_call.side_effect = [True, False]

    with patch("builtins.input", side_effect=["info", "exit"]):
        service.choose_item_manager_action()

    assert root.information_service.check_information_service_call.call_count == 2

def test_choose_item_manager_action_invalid_input(camp_action_service_setup):
    """
     Tests that invalid input in the item manager is handled and the information service is called.

     Args:
         camp_action_service_setup: Provides CampActionService and mocked root service.
     """
    service, root = camp_action_service_setup

    with patch("builtins.input", side_effect=["bad input", "wrong 5", "exit"]):
        service.choose_item_manager_action()

    assert root.information_service.check_information_service_call.call_count == 3


def test_choose_camp_action_leave_camp(camp_action_service_setup):
    """
     Tests that choosing to leave the camp prints the leaving message.

     Args:
         camp_action_service_setup: Provides CampActionService and mocked root service.
     """
    service, root = camp_action_service_setup

    with patch("builtins.input", side_effect=["4"]):
        # Capture the print output
        with patch("builtins.print") as mock_print:
            service.choose_camp_action()

    # Check that the leaving camp message was printed
    mock_print.assert_any_call("Leaving camp...")

def test_choose_item_manager_invalid_length(camp_action_service_setup):
    """
    Tests that item manager commands with invalid length are handled correctly
    and an error message is printed.

    Args:
        camp_action_service_setup: Provides CampActionService and mocked root service.
    """
    service, root = camp_action_service_setup

    # input that is split into more/fewer than 2 parts
    inputs = ["send", "exit"]
    with patch("builtins.input", side_effect=inputs):
        with patch("builtins.print") as mock_print:
            service.choose_item_manager_action()

    mock_print.assert_any_call("Invalid command. Use: send <no>, take <no>, use <no>, exit")

def test_choose_item_manager_take_command(camp_action_service_setup):
    """
    Tests that the 'take' command moves an item from the convoy to the player inventory
    and calls the item manager again.

    Args:
        camp_action_service_setup: Provides CampActionService and mocked root service.
    """
    service, root = camp_action_service_setup

    # Setup items and convoy
    player = root.current_game.player
    player.items = []
    convoy = root.current_game.convoy

    item1 = HealingPotion("Test Potion", 10, 1, 200)
    convoy.append(item1)

    with patch("builtins.input", side_effect=["take 1"]):
        service.choose_item_manager_action()

    # After 'take', player should have the convoy item appended
    assert item1 not in convoy
    assert  item1 in player.items
    # Ensure the camp service method is called
    root.camp_service.open_item_manager.assert_called()

def test_choose_item_manager_use_from_convoy(camp_action_service_setup):
    """
    Tests that using an item with an index greater than the player's inventory
    pulls it from the convoy, applies its effect, and removes it.

    Args:
        camp_action_service_setup: Provides CampActionService and mocked root service.
    """
    service, root = camp_action_service_setup

    # Setup items and convoy
    player = root.current_game.player
    player.hp = 1
    player.max_hp = 50
    player.items = []
    convoy = root.current_game.convoy

    item1 = HealingPotion("Test Potion", 10, 1, 200)
    convoy.append(item1)

    # number > len(player.items) triggers the convoy branch
    with patch("builtins.input", side_effect=["use 1"]):
        service.choose_item_manager_action()

    assert item1 not in convoy
    assert item1 not in player.items
    assert player.hp == 11

def test_choose_camp_action_invalid_option(camp_action_service_setup):
    """
    Tests that selecting an invalid camp action option prints an error
    and that the camp exit message is still displayed.

    Args:
        camp_action_service_setup: Provides CampActionService and mocked root service.
    """
    service, root = camp_action_service_setup

    # Input outside valid options (1-4), then exit with 4
    inputs = ["9", "4"]
    with patch("builtins.input", side_effect=inputs):
        with patch("builtins.print") as mock_print:
            service.choose_camp_action()

    # Check that the invalid option message was printed
    mock_print.assert_any_call("Invalid option. Please choose between 1-4.")
    # Also check that leaving camp is still printed at the end
    mock_print.assert_any_call("Leaving camp...")

def test_choose_item_manager_item_not_usable(camp_action_service_setup):
    """
    Tests that attempting to use a non-usable item prints the correct message.

    Args:
        camp_action_service_setup: Provides CampActionService and mocked root service.
    """
    service, root = camp_action_service_setup

    player = root.current_game.player
    # Player with non-usable item
    player = root.current_game.player
    player.hp = 1
    player.max_hp = 50
    player.items = []

    item1 = Item("Test", False , 999)
    player.items.append(item1)

    # User tries to 'use 1'
    inputs = ["use 1", "exit"]  # exit to end loop
    with patch("builtins.input", side_effect=inputs):
        with patch("builtins.print") as mock_print:
            service.choose_item_manager_action()

    # Check that the correct message is printed
    mock_print.assert_any_call("Item not usable.")

def test_choose_item_manager_unknown_command(camp_action_service_setup):
    """
    Tests that entering an unknown command in the item manager prints the correct message.

    Args:
        camp_action_service_setup: Provides CampActionService and mocked root service.
    """
    service, root = camp_action_service_setup

    player = root.current_game.player
    player.items = ["item1"]
    root.current_game.convoy = []

    # Input an unknown command
    inputs = ["foobar 1", "exit"]
    with patch("builtins.input", side_effect=inputs):
        with patch("builtins.print") as mock_print:
            service.choose_item_manager_action()

    # Check that the unknown command message is printed
    mock_print.assert_any_call("Unknown command. Use send, take, use or exit.")