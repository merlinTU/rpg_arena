import pytest
from unittest.mock import MagicMock, patch

from rpg_arena.entity import WeaponType, Weapon
from rpg_arena.entity.prob_skill import ProbSkill
from rpg_arena.entity.weapon_skill import WeaponSkill
from rpg_arena.entity.healing_potion import HealingPotion
from rpg_arena.entity.stat_booster import StatBooster
from rpg_arena.log.shop_service_printer import ShopServicePrinter
from rpg_arena.entity.stat_modifier_skill import StatModifierSkill


@pytest.fixture
def setup_printer():
    """
    Provides a reusable ShopServicePrinter setup with a mocked
    root service, player, and convoy.
    """
    root_service = MagicMock()
    player_mock = MagicMock()
    player_mock.gold = 100
    player_mock.items = []

    root_service.current_game.player = player_mock
    root_service.current_game.convoy = []

    printer = ShopServicePrinter(root_service)

    return printer, root_service, player_mock

# Tests
def test_print_at_open_shop(setup_printer, capsys):
    """
    Test that the main shop menu is printed correctly.
    """
    printer, _, _ = setup_printer

    printer.print_at_open_shop()
    captured = capsys.readouterr()

    assert "Merchant" in captured.out
    assert "1) Buy Items" in captured.out
    assert "2) Sell Items" in captured.out
    assert "3) Buy Skills" in captured.out
    assert "4) Exit" in captured.out


@patch("time.sleep", return_value=None)
def test_print_at_open_buy_items_menu(mock_sleep, setup_printer, capsys):
    """
    Test that the buy menu correctly prints categorized items
    and includes formatted item stats.
    """
    printer, _, _ = setup_printer

    weapon = Weapon("Test Sword", WeaponType.SWORD, 10, 80, 5, 5, 3, 100)
    potion = HealingPotion("Potion", 20, 3, 10)
    booster = StatBooster("STR Booster", "STR", 2, 15)

    items = [weapon, potion, booster]

    printer.print_at_open_buy_items_menu(items)
    captured = capsys.readouterr()

    assert "Weapons" in captured.out
    assert "Healing Potions" in captured.out
    assert "Stat Boosters" in captured.out

    assert "STR:" in captured.out
    assert "ACC:" in captured.out
    assert "CRIT:" in captured.out

    assert "Heal:" in captured.out
    assert "Uses:" in captured.out

    assert "+2" in captured.out


@patch("time.sleep", return_value=None)
def test_print_at_open_sell_items_menu(mock_sleep, setup_printer, capsys):
    """
    Test that inventory and convoy items are printed with correct formatting.
    """
    printer, root_service, player = setup_printer

    weapon = Weapon("Test Sword", WeaponType.SWORD, 10, 80, 5, 5, 3, 100)

    player.items = [weapon]
    root_service.current_game.convoy = [weapon]

    printer.print_at_open_sell_items_menu()
    captured = capsys.readouterr()

    assert "Inventory" in captured.out
    assert "Convoy Storage" in captured.out

    # check weapon output
    assert "STR:" in captured.out
    assert "ACC:" in captured.out


def test_print_buy_items_decision(setup_printer, capsys):
    """
    Test that the buy decision prompt is printed correctly.
    """
    printer, _, _ = setup_printer

    printer.print_buy_items_decision()
    captured = capsys.readouterr()

    assert "buy <no>" in captured.out
    assert "exit" in captured.out


def test_print_sell_items_decision(setup_printer, capsys):
    """
    Test that the sell decision prompt is printed correctly.
    """
    printer, _, _ = setup_printer

    printer.print_sell_items_decision()
    captured = capsys.readouterr()

    assert "sell <no>" in captured.out
    assert "exit" in captured.out


def test_print_at_full_inventory(setup_printer, capsys):
    """
    Test that the full inventory message and item list are printed correctly.
    """
    printer, _, player = setup_printer

    weapon = Weapon("Test Sword", WeaponType.SWORD, 10, 80, 5, 5, 3, 100)
    player.items = [weapon]

    printer.print_at_full_inventory()
    captured = capsys.readouterr()

    assert "Your inventory is full" in captured.out
    assert "send to the convoy" in captured.out

    # check weapon print
    assert "STR:" in captured.out


@patch("time.sleep", return_value=None)
def test_print_at_open_buy_skills_menu(mock_sleep, setup_printer, capsys):
    """
    Test that skill shop prints categories and formatted skill outputs.
    """
    printer, _, player = setup_printer

    printer.print_buy_skills_decision = MagicMock()

    stat_skill = StatModifierSkill("Stat Skill", 100, "STR", 2, "Boost STR")
    prob_skill = ProbSkill("Crit Skill", 100, "STR", 2, 0.5, "Crit chance")
    weapon_skill = WeaponSkill("Sword Skill", 100, WeaponType.SWORD, "Sword bonus")

    skills = [stat_skill, prob_skill, weapon_skill]

    printer.print_at_open_buy_skills_menu(skills)
    captured = capsys.readouterr()

    assert "You have 100 Gold" in captured.out

    assert "--- Combat Stat Skills ---" in captured.out
    assert "--- Probability Skills ---" in captured.out
    assert "--- Weapon Skills ---" in captured.out

    # echte Skill-Outputs
    assert "Price:" in captured.out
    assert "Boost STR" in captured.out
    assert "Crit chance" in captured.out
    assert "Sword bonus" in captured.out

    printer.print_buy_skills_decision.assert_called_once()