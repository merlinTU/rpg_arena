import pytest
from unittest.mock import MagicMock, patch

from rpg_arena.entity import Item
from rpg_arena.service.shop_action_service import ShopActionService

@pytest.fixture
def shop_action_service_setup():
    """
    Fixture to create a ShopActionService instance with fully mocked dependencies.

    Returns:
        tuple: (ShopActionService instance, mocked root_service)
    """
    # Create a mock root service
    root_service_mock = MagicMock()
    root_service_mock.current_game = MagicMock()

    # Mock the player
    player_mock = MagicMock(name="Player")
    player_mock.items = []
    player_mock.gold = 500
    root_service_mock.current_game.player = player_mock

    # Mock convoy
    root_service_mock.current_game.convoy = []

    # Mock dependent services
    root_service_mock.shop_service = MagicMock()
    root_service_mock.camp_service = MagicMock()

    # Ensure information_service always returns False unless explicitly changed
    info_service_mock = MagicMock()
    info_service_mock.check_information_service_call.return_value = False
    root_service_mock.information_service = info_service_mock

    # Initialize the ShopActionService with the mocked root_service
    service = ShopActionService(root_service_mock)

    return service, root_service_mock

# test choose shop action:
def test_choose_shop_action_calls_buy_menu():
    """
    Tests that the choose_shop_action() method calls the buy items menu
    when the player selects option '1'.
    """
    root_service = MagicMock()
    root_service.information_service.check_information_service_call.return_value = False

    service = ShopActionService(root_service)

    with patch("builtins.input", side_effect=["1"]):
        service.choose_shop_action()

    root_service.shop_service.open_buy_items_menu.assert_called_once()

def test_choose_shop_action_calls_sell_menu():
    """
    Tests that the choose_shop_action() method calls the sell items menu
    when the player selects option '2'.
    """
    root_service = MagicMock()
    root_service.information_service.check_information_service_call.return_value = False

    service = ShopActionService(root_service)

    with patch("builtins.input", side_effect=["2"]):
        service.choose_shop_action()

    root_service.shop_service.open_sell_items_menu.assert_called_once()

def test_choose_shop_action_calls_open_camp():
    """
    Tests that the choose_shop_action() method opens the camp service
    correctly for different exit-related inputs.
    """
    root_service = MagicMock()
    root_service.information_service.check_information_service_call.return_value = False
    service = ShopActionService(root_service)

    # Test "3"
    with patch("builtins.input", side_effect=["4"]):
        service.choose_shop_action()
    root_service.camp_service.open_camp.assert_called_once()
    root_service.camp_service.open_camp.reset_mock()

    # Test "e"
    with patch("builtins.input", side_effect=["e"]):
        service.choose_shop_action()
    root_service.camp_service.open_camp.assert_called_once()
    root_service.camp_service.open_camp.reset_mock()

    # Test "exit"
    with patch("builtins.input", side_effect=["exit"]):
        service.choose_shop_action()
    root_service.camp_service.open_camp.assert_called_once()

def test_choose_shop_action_invalid_input(capsys):
    """
    Tests that choose_shop_action() handles invalid user input correctly.
    """
    root_service = MagicMock()
    root_service.information_service.check_information_service_call.return_value = False

    service = ShopActionService(root_service)

    with patch("builtins.input", side_effect=["abc", "1"]):
        service.choose_shop_action()

    captured = capsys.readouterr()

    assert "Invalid input. Please enter a number." in captured.out

# Tests for make buy items decision

def test_make_buy_items_decision_exit(shop_action_service_setup):
    """
    Tests that make_buy_items_decision() correctly exits when the user inputs "exit".
    """
    service, root = shop_action_service_setup

    with patch("builtins.input", side_effect=["exit"]):
        service.make_buy_items_decision()

    root.shop_service.open_shop.assert_called_once()

def test_make_buy_items_decision_invalid_command(shop_action_service_setup, capsys):
    """
    Tests that make_buy_items_decision() prints an error message for invalid commands.
    """
    service, root = shop_action_service_setup

    with patch("builtins.input", side_effect=["hello", "exit"]):
        service.make_buy_items_decision()

    captured = capsys.readouterr()

    assert "Invalid command. Use: buy <no> or exit" in captured.out

def test_make_buy_items_decision_invalid_number(shop_action_service_setup, capsys):
    """
    Tests that make_buy_items_decision() prints an error message when the user
    provides a non-numeric item number.
    """
    service, root = shop_action_service_setup

    with patch("builtins.input", side_effect=["buy x", "exit"]):
        service.make_buy_items_decision()

    captured = capsys.readouterr()

    assert "Invalid item number." in captured.out

def test_make_buy_items_decision_number_too_large(shop_action_service_setup, capsys):
    """
    Tests that make_buy_items_decision() prints an error message when the user
    inputs a numeric item number that exceeds the number of items in the shop.
    """
    service, root = shop_action_service_setup

    item = Item("Test Item1", False, 50)
    root.shop_service.shop_items = [item]

    with patch("builtins.input", side_effect=["buy 5", "exit"]):
        service.make_buy_items_decision()

    captured = capsys.readouterr()

    assert "Invalid item number." in captured.out

def test_make_buy_items_decision_not_enough_gold(shop_action_service_setup, capsys):
    """
    Tests that make_buy_items_decision() prints an error message when the player
    tries to buy an item they cannot afford.
    """
    service, root = shop_action_service_setup

    # Create a shop item with price higher than player's gold
    item = Item("Test Item1", False, 5000)
    root.shop_service.shop_items = [item]

    # Set player's gold lower than item price
    root.current_game.player.gold = 100

    # Patch input to first try buying, then exit
    with patch("builtins.input", side_effect=["buy 1", "exit"]):
        service.make_buy_items_decision()

    captured = capsys.readouterr()
    assert "You do not have enough gold!" in captured.out

def test_make_buy_items_decision_buy_item(shop_action_service_setup):
    """
    Tests that make_buy_items_decision() successfully calls buy_item() when the
    player has enough gold.
    """
    service, root = shop_action_service_setup

    item = Item("Test Item1", False, 50)

    root.shop_service.shop_items = [item]

    with patch("builtins.input", side_effect=["buy 1", "exit"]):
        service.make_buy_items_decision()

    root.shop_service.buy_item.assert_called_once_with(item)


def test_make_buy_items_decision_unknown_command(shop_action_service_setup, capsys):
    """
    Tests that make_buy_items_decision() prints an error message when the user
    inputs an unknown command.
    """
    service, root = shop_action_service_setup

    item = Item("Test Item1", False, 10)
    root.shop_service.shop_items = [item]

    with patch("builtins.input", side_effect=["sell 1", "exit"]):
        service.make_buy_items_decision()

    captured = capsys.readouterr()

    assert "Unknown command. Use: buy or exit." in captured.out


def test_make_send_to_convoy_decision(shop_action_service_setup, capsys):
    """
    Tests that make_send_to_convoy_decision() handles invalid input and correctly
    moves a selected item from the player's inventory to the convoy.
    """
    service, root = shop_action_service_setup

    # Set up real items and convoy
    item1 = Item("Test Item1", False, 50)
    item2 = Item("Test Item2", False, 50)
    root.current_game.player.items = [item1, item2]
    root.current_game.convoy = []

    # Scenario: first invalid string, then out-of-range number, then valid choice
    with patch("builtins.input", side_effect=["hello", "5", "1"]):
        service.make_send_to_convoy_decision()

    captured = capsys.readouterr()

    # Validate printed messages for invalid inputs
    assert "Invalid input. Please enter a number." in captured.out
    assert "Invalid input." in captured.out

    # Validate that the correct item was moved to convoy
    assert root.current_game.convoy == [item1]
    assert root.current_game.player.items == [item2]

def test_make_send_to_convoy_decision_valid(shop_action_service_setup, capsys):
    """
    Tests that make_send_to_convoy_decision() moves the selected item to the convoy
    correctly when a valid input number is provided.
    """
    service, root = shop_action_service_setup

    # Single item
    item = Item("Test Item1", False, 50)
    root.current_game.player.items = [item]
    root.current_game.convoy = []

    with patch("builtins.input", side_effect=["1"]):
        service.make_send_to_convoy_decision()

    captured = capsys.readouterr()

    # Nothing invalid should be printed
    assert "Invalid" not in captured.out

    # Validate item moved correctly
    assert root.current_game.convoy == [item]
    assert root.current_game.player.items == []

def test_make_send_to_convoy_decision_invalid_non_digit(shop_action_service_setup, capsys):
    """
    Tests that make_send_to_convoy_decision() handles non-digit input correctly.
    """
    service, root = shop_action_service_setup

    # Single item
    item = Item("Test Item1", False, 50)
    root.current_game.player.items = [item]
    root.current_game.convoy = []

    # Input non-digit, then valid number
    with patch("builtins.input", side_effect=["abc", "1"]):
        service.make_send_to_convoy_decision()

    captured = capsys.readouterr()

    # Check that error message printed for non-digit input
    assert "Invalid input. Please enter a number." in captured.out

    # Validate item moved correctly
    assert root.current_game.convoy == [item]
    assert root.current_game.player.items == []

def test_make_send_to_convoy_decision_out_of_range(shop_action_service_setup, capsys):
    """
    Tests that make_send_to_convoy_decision() handles input numbers out of range.
    """
    service, root = shop_action_service_setup

    # Two items
    item1 = Item("Test Item1", False, 50)
    item2 = Item("Test Item2", False, 50)
    root.current_game.player.items = [item1, item2]
    root.current_game.convoy = []

    # Input number out of range, then valid number
    with patch("builtins.input", side_effect=["3", "2"]):
        service.make_send_to_convoy_decision()

    captured = capsys.readouterr()

    # Check error message printed for out-of-range number
    assert "Invalid input." in captured.out

    # Validate correct item moved to convoy
    assert root.current_game.convoy == [item2]
    assert root.current_game.player.items == [item1]

# test sell items:
def test_make_sell_items_decision_invalid_command(shop_action_service_setup, capsys):
    """
    Tests that make_sell_items_decision() prints an error message for invalid commands.
    """
    service, root = shop_action_service_setup

    # Set up dummy shop items
    item1 = MagicMock(name="Item1")
    item2 = MagicMock(name="Item2")
    root.shop_service.shop_items = [item1, item2]

    # Input invalid command, then exit
    with patch("builtins.input", side_effect=["hello", "exit"]):
        service.make_sell_items_decision()

    captured = capsys.readouterr()
    assert "Invalid command. Use: sell <no> or exit" in captured.out
    root.shop_service.open_shop.assert_called_once()

def test_make_sell_items_decision_non_digit(shop_action_service_setup, capsys):
    """
    Tests that make_sell_items_decision() prints an error message when the user
    inputs a non-digit item number.
    """
    service, root = shop_action_service_setup

    item1 = MagicMock(name="Item1")
    root.shop_service.shop_items = [item1]

    # Input non-digit, then valid sell
    with patch("builtins.input", side_effect=["sell x", "sell 1"]):
        service.make_sell_items_decision()

    captured = capsys.readouterr()
    assert "Invalid item number." in captured.out
    root.shop_service.sell_item.assert_called_once_with(0)

def test_make_sell_items_decision_out_of_range(shop_action_service_setup, capsys):
    """
    Tests that make_sell_items_decision() prints an error message when the user
    inputs an item number that is out of range.
    """
    service, root = shop_action_service_setup

    item1 = Item("Test Item1", False, 50)
    root.shop_service.shop_items = [item1]

    # Input number out of range, then valid sell
    with patch("builtins.input", side_effect=["sell 5", "sell 1"]):
        service.make_sell_items_decision()

    captured = capsys.readouterr()
    assert "Invalid item number." in captured.out
    root.shop_service.sell_item.assert_called_once_with(0)

def test_make_sell_items_decision_unknown_command(shop_action_service_setup, capsys):
    """
    Tests that make_sell_items_decision() prints an error message when the user
    inputs an unknown command (e.g., "buy 1") instead of "sell <no>" or "exit".
    """
    service, root = shop_action_service_setup

    item1 = Item("Test Item1", False, 50)
    root.shop_service.shop_items = [item1]

    # Input unknown command
    with patch("builtins.input", side_effect=["buy 1", "sell 1"]):
        service.make_sell_items_decision()

    captured = capsys.readouterr()
    assert "Unknown command. Use sell or exit." in captured.out
    root.shop_service.sell_item.assert_called_once_with(0)

def test_make_sell_items_decision_exit(shop_action_service_setup, capsys):
    """
    Tests that make_sell_items_decision() correctly exits when the user inputs "exit".
    """
    service, root = shop_action_service_setup

    # No items needed, just exit
    root.shop_service.shop_items = []
    with patch("builtins.input", side_effect=["exit"]):
        service.make_sell_items_decision()

    root.shop_service.open_shop.assert_called_once()

def test_make_sell_items_decision_info_call(shop_action_service_setup, capsys):
    """
    Tests that make_sell_items_decision() correctly interacts with the information service.
    """
    service, root = shop_action_service_setup

    # Add an item to the shop so selling is possible
    item1 = Item("Test Item1", False, 50)
    root.shop_service.shop_items = [item1]

    # Mock the information service call to return True on the first input
    # This simulates the player asking for info, which should skip the loop iteration
    root.information_service.check_information_service_call.side_effect = [True, False]

    # Inputs: first "info" (skipped), then a valid sell command
    with patch("builtins.input", side_effect=["info", "sell 1"]):
        service.make_sell_items_decision()

    # Ensure the information service was called at least once
    assert root.information_service.check_information_service_call.call_count >= 1

    # Ensure the sell_item method was called with the correct index
    root.shop_service.sell_item.assert_called_once_with(0)

def test_choose_shop_action_info_call(shop_action_service_setup, capsys):
    """
    Tests that choose_shop_action() correctly interacts with the information service.
    """
    service, root = shop_action_service_setup

    # Mock the information service call to return True on the first input
    # This simulates the player asking for info, which should skip the loop iteration
    root.information_service.check_information_service_call.side_effect = [True, False]

    # Inputs: first "info" (skipped), then a valid sell command
    with patch("builtins.input", side_effect=["info", "1"]):
        service.choose_shop_action()

    # Ensure the information service was called at least once
    assert root.information_service.check_information_service_call.call_count >= 1

    # Ensure the sell_item method was called with the correct index
    root.shop_service.open_buy_items_menu.assert_called_once()

def test_choose_shop_action_invalid_option(shop_action_service_setup, capsys):
    """Test that entering an invalid number triggers the default case."""
    service, root = shop_action_service_setup

    # Patch input: first an invalid option, then '3' to exit the loop
    with patch("builtins.input", side_effect=["0", "4", "invalid", "3"]):
        service.choose_shop_action()

    captured = capsys.readouterr()
    assert "Invalid option. Please choose between 1-3." in captured.out
    # Also check that eventually open_camp was called for '3'
    root.camp_service.open_camp.assert_called_once()

def test_make_buy_items_decision_info_call(shop_action_service_setup, capsys):
    """Test that info command triggers the information service check and skips the iteration."""
    service, root = shop_action_service_setup

    # Add an item to the shop so buying is possible
    item1 = Item("Test Item1", False, 50)
    item1.price = 100
    root.shop_service.shop_items = [item1]

    # Mock the information service call:
    # First input returns True (info command), second returns False (normal command)
    root.information_service.check_information_service_call.side_effect = [True, False, False]

    # Patch input: first triggers info, second buys item, third exits loop
    with patch("builtins.input", side_effect=["info stats", "buy 1", "exit"]):
        service.make_buy_items_decision()

    # Ensure the information service was called at least once
    assert root.information_service.check_information_service_call.call_count >= 1

    # Ensure buy_item method was called with the correct item
    root.shop_service.buy_item.assert_called_once_with(item1)

def test_make_send_to_convoy_decision_info_call(shop_action_service_setup):
    """Test that info command triggers the information service check and skips the iteration."""
    service, root = shop_action_service_setup

    # Setup player with one item in inventory and empty convoy
    item1 = Item("Test Item1", False, 50)
    root.current_game.player.items = [item1]
    root.current_game.convoy = []

    # Mock information service: first input triggers info (True), second input is valid number (False)
    root.information_service.check_information_service_call.side_effect = [True, False]

    # Patch input: first triggers info, second sends item to convoy
    with patch("builtins.input", side_effect=["info stats", "1"]):
        service.make_send_to_convoy_decision()

    # Ensure information service was called at least once
    assert root.information_service.check_information_service_call.call_count >= 1

    # Ensure the item was moved to the convoy
    assert root.current_game.convoy == [item1]
    assert root.current_game.player.items == []


def test_make_buy_skills_decision_exit(shop_action_service_setup):
    """
    Tests that make_buy_skills_decision() correctly exits when the user inputs "exit".
    """
    service, root = shop_action_service_setup

    with patch("builtins.input", side_effect=["exit"]):
        service.make_buy_skills_decision()

    root.shop_service.open_shop.assert_called_once()

def test_make_buy_skills_decision_e_exit(shop_action_service_setup):
    service, root = shop_action_service_setup

    with patch("builtins.input", side_effect=["e"]):
        service.make_buy_skills_decision()

    root.shop_service.open_shop.assert_called_once()

def test_make_buy_skills_decision_invalid_command(shop_action_service_setup, capsys):
    """
    Tests that make_buy_skills_decision() correctly exits when the user inputs "e".
    """
    service, root = shop_action_service_setup
    root.shop_service.shop_skills = []

    with patch("builtins.input", side_effect=["hello", "exit"]):
        service.make_buy_skills_decision()

    captured = capsys.readouterr()
    assert "Invalid command. Use: buy <no> or exit" in captured.out
    root.shop_service.open_shop.assert_called_once()

def test_make_buy_skills_decision_non_digit_number(shop_action_service_setup, capsys):
    """
    Tests that make_buy_skills_decision() prints an error message when the user
    inputs a non-numeric skill number.
    """
    service, root = shop_action_service_setup

    dummy_skill = MagicMock()
    dummy_skill.price = 50
    root.shop_service.shop_skills = [dummy_skill]

    with patch("builtins.input", side_effect=["buy x", "exit"]):
        service.make_buy_skills_decision()

    captured = capsys.readouterr()
    assert "Invalid item number." in captured.out

def test_make_buy_skills_decision_number_too_large(shop_action_service_setup, capsys):
    """
    Tests that make_buy_skills_decision() prints an error message when the user
    inputs a numeric skill number that exceeds the number of available skills.
    """
    service, root = shop_action_service_setup

    dummy_skill = MagicMock()
    dummy_skill.price = 50
    root.shop_service.shop_skills = [dummy_skill]

    with patch("builtins.input", side_effect=["buy 5", "exit"]):
        service.make_buy_skills_decision()

    captured = capsys.readouterr()
    assert "Invalid item number." in captured.out

def test_make_buy_skills_decision_not_enough_gold(shop_action_service_setup, capsys):
    """
    Tests that make_buy_skills_decision() prints an error message when the player
    tries to buy a skill they cannot afford.
    """
    service, root = shop_action_service_setup

    expensive_skill = MagicMock()
    expensive_skill.price = 200
    root.shop_service.shop_skills = [expensive_skill]
    root.current_game.player.gold = 100

    with patch("builtins.input", side_effect=["buy 1", "exit"]):
        service.make_buy_skills_decision()

    captured = capsys.readouterr()
    assert "You do not have enough gold!" in captured.out

def test_make_buy_skills_decision_successful_purchase(shop_action_service_setup):
    """
    Tests that make_buy_skills_decision() successfully calls buy_skill() when
    the player has enough gold to purchase a skill.
    """
    service, root = shop_action_service_setup

    skill = MagicMock()
    skill.price = 50
    root.shop_service.shop_skills = [skill]
    root.current_game.player.gold = 100

    with patch("builtins.input", side_effect=["buy 1"]):
        service.make_buy_skills_decision()

    root.shop_service.buy_skill.assert_called_once_with(skill)

def test_make_buy_skills_decision_unknown_command(shop_action_service_setup, capsys):
    """
    Tests that make_buy_skills_decision() prints an error message when the user
    inputs an unknown command instead of "buy <no>" or "exit".
    """
    service, root = shop_action_service_setup

    dummy_skill = MagicMock()
    dummy_skill.price = 50
    root.shop_service.shop_skills = [dummy_skill]

    with patch("builtins.input", side_effect=["sell 1", "exit"]):
        service.make_buy_skills_decision()

    captured = capsys.readouterr()
    assert "Unknown command. Use: buy or exit." in captured.out