import pytest
from unittest.mock import MagicMock, patch
from rpg_arena.entity import Weapon, WeaponType, UnitClass, Fighter
from rpg_arena.log.arena_service_printer import ArneaServicePrinter

@pytest.fixture
def root_service_fixture():
    """Provides a MagicMock root_service with player and enemy mocks."""
    root_service = MagicMock()
    # Player setup
    player = Fighter(UnitClass.MAGE)
    player.name = "Hero"
    player.hp = 30
    player.max_hp = 30
    player.calc_corrected_speed = MagicMock(return_value=20)
    player.equipped_weapon = None
    player.items = []
    root_service.current_game.player = player

    # Enemy setup
    enemy = Fighter(UnitClass.FIGHTER)
    enemy.name = "Enemy"
    enemy.hp = 25
    enemy.calc_corrected_speed = MagicMock(return_value=10)
    enemy.equipped_weapon = None

    # Arena service mock
    arena = MagicMock()
    arena.enemy = enemy
    arena.calculate_hit_chance.return_value = 0.8
    arena.calculate_crit_chance.return_value = 0.1
    arena.calculate_damage.return_value = 12
    arena.check_weapon_vantage.return_value = 0
    root_service.arena_service = arena

    return root_service, player, enemy


@pytest.fixture
def printer_fixture(root_service_fixture):
    """Provides a printer instance and unpacks root_service, player, enemy."""
    root_service, player, enemy = root_service_fixture
    printer = ArneaServicePrinter(root_service)
    return printer, root_service, player, enemy

# Tests:
@patch("time.sleep", return_value=None)
def test_print_after_make_attack_hit_and_crit(mock_sleep, printer_fixture, capsys):
    """
    Tests `print_after_make_attack` when the attack hits and is critical.

    Args:
        mock_sleep (MagicMock): patched `time.sleep` to skip delays.
        printer_fixture (tuple): fixture providing (printer, root_service, attacker, defender).
        capsys (CaptureFixture): pytest fixture to capture stdout.
    """
    printer, _, attacker, defender = printer_fixture

    attacker.name = "Attacker"
    defender.name = "Defender"
    defender.hp = 50

    printer.print_after_make_attack(
        attacker, defender, has_hit=True, has_crit=True, damage=10, status=1
    )
    captured = capsys.readouterr()
    assert "Attacker attacks" in captured.out
    assert "CRITICAL HIT" in captured.out
    assert "Defender takes 10 damage" in captured.out
    assert "Defender HP: 50" in captured.out

@patch("time.sleep", return_value=None)
def test_print_after_make_attack_miss(mock_sleep, printer_fixture, capsys):
    """
    Tests `print_after_make_attack` when the attack misses.

    Args:
        mock_sleep (MagicMock): patched `time.sleep` to skip delays.
        printer_fixture (tuple): fixture providing (printer, root_service, attacker, defender).
        capsys (CaptureFixture): pytest fixture to capture stdout.
    """
    printer, _, attacker, defender = printer_fixture
    attacker.name = "Attacker"
    defender.name = "Defender"
    defender.hp = 50

    printer.print_after_make_attack(
        attacker, defender, has_hit=False, has_crit=False, damage=0, status=1
    )
    captured = capsys.readouterr()
    assert "dodged the attack" in captured.out

@patch("time.sleep", return_value=None)
def test_print_at_start_round(mock_sleep, printer_fixture, capsys):
    """
    Tests `print_at_start_round` prints the battle start message.

    Args:
        mock_sleep (MagicMock): patched `time.sleep` to skip delays.
        printer_fixture (tuple): fixture providing (printer, root_service, attacker, defender).
        capsys (CaptureFixture): pytest fixture to capture stdout.
    """
    printer, _, _, _ = printer_fixture
    printer.print_at_start_round()
    captured = capsys.readouterr()
    assert "BATTLE START" in captured.out

@patch("time.sleep", return_value=None)
def test_print_after_start_round_player_turn(mock_sleep, printer_fixture, capsys):
    """
    Tests that the printer correctly indicates the player's turn after the start of a round.

    Args:
        printer_fixture (tuple): Fixture providing printer instance, root service, player, and enemy mocks.
        capsys: Pytest fixture to capture stdout/stderr output.
    """
    printer, root_service, player, _ = printer_fixture
    printer.print_after_start_round(player, MagicMock())
    captured = capsys.readouterr()
    assert "YOUR TURN" in captured.out

@patch("time.sleep", return_value=None)
def test_print_after_start_round_enemy_turn(mock_sleep, printer_fixture, capsys):
    """
    Tests that the printer correctly indicates the enemy's turn after the start of a round.

    Args:
        printer_fixture (tuple): Fixture providing printer instance, root service, player, and enemy mocks.
        capsys: Pytest fixture to capture stdout/stderr output.
    """
    printer, root_service, player, enemy = printer_fixture
    printer.print_after_start_round(enemy, player)
    captured = capsys.readouterr()
    assert "ENEMY TURN" in captured.out

@patch("time.sleep", return_value=None)
def test_print_at_open_fight_menu_with_weapons(mock_sleep, printer_fixture, capsys):
    """
    Test that the printer correctly lists available weapons when opening the fight menu.

    Args:
        mock_sleep: Patched time.sleep to prevent delays.
        printer_fixture (tuple): Fixture providing printer instance, root service, player, and enemy mocks.
        capsys: Pytest fixture to capture stdout/stderr output.
    """
    printer, root_service, player, _ = printer_fixture

    weapon_mock = MagicMock(spec=Weapon)
    weapon_mock.__str__ = MagicMock(return_value="Test print") # to test independent of real print methode
    player.items = [weapon_mock]

    printer.print_at_open_fight_menu()
    captured = capsys.readouterr()
    assert "CHOOSE YOUR WEAPON" in captured.out
    assert "Test print" in captured.out

@patch("time.sleep", return_value=None)
def test_print_at_open_fight_menu_no_weapons(mock_sleep, printer_fixture, capsys):
    """
    Test that the printer displays a message when the player has no weapons in their inventory.

    Args:
        mock_sleep: Patched time.sleep to prevent delays.
        printer_fixture (tuple): Fixture providing printer instance, root service, player, and enemy mocks.
        capsys: Pytest fixture to capture stdout/stderr output.
    """
    printer, _, player, _ = printer_fixture

    # Ensure player has no weapons
    player.items = []

    # Call the printer method
    printer.print_at_open_fight_menu()
    captured = capsys.readouterr()

    # Assert that the proper message is printed
    assert "You have no weapons available" in captured.out

@patch("time.sleep", return_value=None)
def test_print_after_print_fight_preview(mock_sleep, printer_fixture, capsys):
    """
    Test that the fight preview options are printed correctly after showing fight preview.

    Args:
        mock_sleep: Patched time.sleep to prevent delays during printing.
        printer_fixture (tuple): Fixture providing printer instance, root service, player, and enemy mocks.
        capsys: Pytest fixture to capture stdout/stderr output.
    """
    printer, _, _, _ = printer_fixture

    # Call the method to print fight preview options
    printer.print_after_print_fight_preview()
    captured = capsys.readouterr()

    # Assert expected output
    assert "What do you want to do?" in captured.out
    assert "1) Attack" in captured.out

@patch("time.sleep", return_value=None)
def test_print_at_make_player_round_decsion(mock_sleep, printer_fixture, capsys):
    """
    Test that the player round decision menu is printed correctly.

    Args:
        mock_sleep: Patched time.sleep to prevent delays (standard for printer tests).
        printer_fixture (tuple): Fixture providing printer instance, root service, player, and enemy mocks.
        capsys: Pytest fixture to capture stdout/stderr output.
    """
    printer, _, _, _ = printer_fixture

    # Call the method to print the player round decision menu
    printer.print_at_make_player_round_decsion()
    captured = capsys.readouterr()

    # Assert that attack and surrender options are displayed
    assert "1) Attack" in captured.out
    assert "4) Surrender" in captured.out

@patch("time.sleep", return_value=None)
def test_print_inventory_with_equipped_and_items(mock_sleep, printer_fixture, capsys):
    """
    Test that the inventory prints correctly, showing equipped weapon and other items.

    Args:
        mock_sleep: Patched time.sleep to prevent delays (standard for printer tests).
        printer_fixture (tuple): Fixture providing printer instance, root service, player, and enemy mocks.
        capsys: Pytest fixture to capture stdout/stderr output.
    """
    printer, _, player, _ = printer_fixture

    # Setup player inventory
    weapon1 = MagicMock()
    weapon1.__str__ = MagicMock(return_value="Test Sword")
    weapon2 = MagicMock()
    weapon2.__str__ = MagicMock(return_value="Test Axe")
    player.items = [weapon1, weapon2]
    player.equipped_weapon = weapon1

    # Call the method to print the inventory
    printer.print_inventory()
    captured = capsys.readouterr()

    # Assertions: equipped weapon and other items are displayed
    assert "Equipped Weapon" in captured.out
    assert "Test Sword" in captured.out
    assert "Test Axe" in captured.out


@patch("time.sleep", return_value=None)
def test_print_after_use_item(mock_sleep, printer_fixture, capsys):
    """
    Test that using an item prints the correct message.

    Args:
        mock_sleep: Patched time.sleep to prevent delays.
        printer_fixture (tuple): Fixture providing printer instance, root service, player, and enemy mocks.
        capsys: Pytest fixture to capture stdout/stderr output.
    """
    printer, _, player, _ = printer_fixture

    printer.print_after_use_item(player)
    captured = capsys.readouterr()
    assert "Hero used item" in captured.out

@patch("time.sleep", return_value=None)
def test_print_at_end_fight(mock_sleep, printer_fixture, capsys):
    """
    Test that the end of fight prints gold and experience gained.

    Args:
        mock_sleep: Patched time.sleep to prevent delays.
        printer_fixture (tuple): Fixture providing printer instance, root service, player, and enemy mocks.
        capsys: Pytest fixture to capture stdout/stderr output.
    """
    printer, _, _, _ = printer_fixture

    printer.print_at_end_fight(100, 50)
    captured = capsys.readouterr()
    assert "You earned 100 Gold" in captured.out
    assert "You gained 50 EXP" in captured.out

@patch("time.sleep", return_value=None)
def test_print_level_up(mock_sleep, printer_fixture, capsys):
    """
    Test that printing level up displays the correct stats and header.

    Args:
        printer_fixture (tuple): Fixture providing printer instance, root service, player, and enemy mocks.
        capsys: Pytest fixture to capture stdout/stderr output.
    """
    printer, _, _, _ = printer_fixture
    printer.print_level_up(["STR", "SPD"])
    captured = capsys.readouterr()
    assert "LEVEL UP" in captured.out
    assert "STR +1" in captured.out
    assert "SPD +1" in captured.out

@patch("time.sleep", return_value=None)
def test_print_level_up_no_stats(mock_sleep, printer_fixture, capsys):
    """
    Test that printing level up with no stat increases shows the correct message.

    Args:
        printer_fixture (tuple): Fixture providing printer instance, root service, player, and enemy mocks.
        capsys: Pytest fixture to capture stdout/stderr output.
    """
    printer, _, _, _ = printer_fixture
    printer.print_level_up([])
    captured = capsys.readouterr()
    assert "No level up this time" in captured.out

@patch("time.sleep", return_value=None)
def test_print_after_surrender(mock_sleep, printer_fixture, capsys):
    """
    Test that the printer correctly outputs surrender messages for the player.

    Args:
        mock_sleep: Patched time.sleep to avoid delays during tests.
        printer_fixture (tuple): Fixture providing printer instance, root service, player, and enemy mocks.
        capsys: Pytest fixture to capture stdout/stderr output.
    """
    printer, _, player, _ = printer_fixture
    printer.print_after_surrender()
    captured = capsys.readouterr()

    assert "Hero surrendered" in captured.out
    assert "You earned 0 Gold" in captured.out
    assert "You gained 0 EXP" in captured.out

@patch("time.sleep", return_value=None)
def test_print_after_make_attack_double_attack(mock_sleep, printer_fixture, capsys):
    """
    Test that the printer correctly outputs a double attack message.

    Args:
        mock_sleep: Patched time.sleep to avoid delays during tests.
        printer_fixture (tuple): Fixture providing printer instance, root service, attacker, and defender mocks.
        capsys: Pytest fixture to capture stdout/stderr output.
    """
    printer, _, attacker, defender = printer_fixture

    printer.print_after_make_attack(
        attacker, defender, has_hit=True, has_crit=False, damage=15, status=2
    )

    captured = capsys.readouterr()
    assert "Hero strikes consecutively! (x2)" in captured.out
    assert "Enemy takes 15 damage" in captured.out
    assert "Enemy HP: 25" in captured.out

@patch("time.sleep", return_value=None)
def test_print_after_make_attack_counter(mock_sleep, printer_fixture, capsys):
    """
    Test that the printer correctly outputs a counterattack message.

    Args:
        mock_sleep: Patched time.sleep to avoid delays during tests.
        printer_fixture (tuple): Fixture providing printer instance, root service, attacker, and defender mocks.
        capsys: Pytest fixture to capture stdout/stderr output.
    """
    printer, _, attacker, defender = printer_fixture

    printer.print_after_make_attack(attacker, defender, has_hit=True, has_crit=False, damage=8, status=3)
    captured = capsys.readouterr()
    assert "Hero counters!" in captured.out
    assert "Enemy takes 8 damage" in captured.out
    assert "Enemy HP: 25" in captured.out

@patch("time.sleep", return_value=None)
def test_print_after_arena_simulation_player_loses(mock_sleep, printer_fixture, capsys):
    """
    Test that the printer correctly outputs the arena simulation result when the player loses.

    Args:
        mock_sleep: Patched time.sleep to avoid delays in the test.
        printer_fixture (tuple): Fixture providing printer instance, root service, player, and enemy mocks.
        capsys: Pytest fixture to capture stdout/stderr output.
    """
    printer, _, player, enemy = printer_fixture

    printer.print_after_arena_simulation(winner=enemy, loser=player)
    captured = capsys.readouterr()
    assert "FIGHT OVER" in captured.out
    assert "You have been defeated!" in captured.out
    assert "GAME OVER" in captured.out

@patch("time.sleep", return_value=None)
def test_print_after_arena_simulation_player_wins(mock_sleep, printer_fixture, capsys):
    """
    Test that the printer correctly outputs the arena simulation result when the player wins.

    Args:
        mock_sleep: Patched time.sleep to avoid delays in the test.
        printer_fixture (tuple): Fixture providing printer instance, root service, player, and enemy mocks.
        capsys: Pytest fixture to capture stdout/stderr output.
    """
    printer, _, player, enemy = printer_fixture
    printer.print_after_arena_simulation(winner=player, loser=enemy)
    captured = capsys.readouterr()

    assert "FIGHT OVER" in captured.out
    assert "Enemy falls to the ground..." in captured.out
    assert "Enemy is defeated!" in captured.out
    assert "YOU WIN!" in captured.out


def test_print_fight_preview(printer_fixture, capsys):
    """
    Test the print_fight_preview method of ArneaServicePrinter.

    Args:
        printer_fixture (tuple): Pytest fixture providing (printer, root_service, player, enemy)
        capsys (pytest fixture): Captures stdout/stderr output during the test
    """
    printer, root_service, player, enemy = printer_fixture

    # Setup weapons
    player.equipped_weapon = Weapon("Test A", WeaponType.SWORD, 0,0,0,0,0,0)

    enemy.equipped_weapon =  Weapon("Test B", WeaponType.SWORD, 0,0,0,0,0,0)

    printer.print_fight_preview()
    captured = capsys.readouterr()
    assert "FIGHT PREVIEW" in captured.out
    assert "Hero" in captured.out
    assert "Enemy" in captured.out
    assert "Test A" in captured.out
    assert "Test B" in captured.out
    assert "HP:" in captured.out
    assert "Hit:" in captured.out
    assert "Dmg:" in captured.out
    assert "Crit:" in captured.out