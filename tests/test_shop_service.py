import pytest

from rpg_arena.entity import WeaponType, Item
from rpg_arena.entity.skill import Skill
from rpg_arena.entity.weapon_skill import WeaponSkill
from rpg_arena.service.data import WEAPONS
from unittest.mock import MagicMock
from rpg_arena.service.shop_service import ShopService
from rpg_arena.entity.healing_potion import HealingPotion
from rpg_arena.entity.stat_booster import StatBooster
from rpg_arena.service.data.item_data import ITEMS

@pytest.fixture
def shop_service_setup():
    """
    Fixture for setting up a ShopService instance with mocked dependencies.

    Returns:
        Tuple[ShopService, MagicMock]: The prepared ShopService instance and the mocked RootService object.
    """
    root_service_mock = MagicMock()
    # Setup dummy game, player and convoy
    root_service_mock.current_game = MagicMock()
    root_service_mock.current_game.player = MagicMock(name="Player")
    root_service_mock.current_game.player.items = []
    root_service_mock.current_game.player.gold = 500
    root_service_mock.current_game.player_weapons = [WeaponType.SWORD]
    root_service_mock.current_game.convoy = []
    root_service_mock.current_game.max_items = 2

    service = ShopService(root_service_mock)
    # Mock printer and action_service
    service.printer.print_at_open_shop = MagicMock()
    service.printer.print_at_open_buy_items_menu = MagicMock()
    service.printer.print_at_open_sell_items_menu = MagicMock()
    service.printer.print_at_full_inventory = MagicMock()
    service.printer.print_buy_items_decision = MagicMock()
    service.action_service.choose_shop_action = MagicMock()
    service.action_service.make_buy_items_decision = MagicMock()
    service.action_service.make_sell_items_decision = MagicMock()
    service.action_service.make_send_to_convoy_decision = MagicMock()

    # Override WEAPONS/ITEMS with dummy objects for testing
    service.shop_items = []
    return service, root_service_mock

def test_open_shop(shop_service_setup):
    """
    Test that ShopService.open_shop properly generates shop items and calls the expected methods.

    Args:
        shop_service_setup (Tuple[ShopService, MagicMock]):
        Fixture providing the ShopService instance and RootService mock.
    """
    service, root_mock = shop_service_setup
    service.generate_shop_weapons = MagicMock()
    service.generate_shop_items = MagicMock()

    service.open_shop()

    service.generate_shop_weapons.assert_called_once_with(root_mock.current_game.player_weapons)
    service.generate_shop_items.assert_called_once()
    service.printer.print_at_open_shop.assert_called_once()
    service.action_service.choose_shop_action.assert_called_once()

def test_buy_item(shop_service_setup):
    service, root_mock = shop_service_setup
    player = root_mock.current_game.player
    item = Item("Test Item", True, 100)

    service.buy_item(item)

    assert player.gold == 400
    assert player.items[0].name == "Test Item"


def test_buy_item_full_inventory(shop_service_setup):
    """
    Test that ShopService.buy_item correctly deducts gold and adds the item to the player's inventory.

    Args:
        shop_service_setup (Tuple[ShopService, MagicMock]):
        Fixture providing the ShopService instance and RootService mock.
    """
    service, root_mock = shop_service_setup
    player = root_mock.current_game.player
    # player items capacity full
    player.items = [Item("Test Item", True, 0), Item("Test Item", True, 0)]
    item = Item("Test Item", True, 0)

    service.buy_item(item)

    service.printer.print_at_full_inventory.assert_called_once()
    service.action_service.make_send_to_convoy_decision.assert_called_once()

def test_sell_item_from_inventory(shop_service_setup):
    """
    Test that ShopService.sell_item correctly removes an item from the player's inventory and updates gold.

    Args:
        shop_service_setup (Tuple[ShopService, MagicMock]):
        Fixture providing the ShopService instance and RootService mock.
    """
    service, root_mock = shop_service_setup
    player = root_mock.current_game.player
    item = Item("Test Item", True, 0)
    player.items = [item]

    service.open_sell_items_menu = MagicMock()
    service.sell_item(0)

    assert player.gold == 500
    assert len(player.items) == 0
    service.open_sell_items_menu.assert_called_once()

def test_sell_item_from_convoy(shop_service_setup):
    """
    Test that ShopService.sell_item correctly removes an item from the convoy and updates the player's gold.

    Args:
        shop_service_setup (Tuple[ShopService, MagicMock]):
        Fixture providing the ShopService instance and RootService mock.
    """
    service, root_mock = shop_service_setup
    player = root_mock.current_game.player
    convoy_item = Item("Test Item", True, 0)
    root_mock.current_game.convoy = [convoy_item]

    service.open_sell_items_menu = MagicMock()
    service.sell_item(0)  # Index into convoy

    assert player.gold == 500
    assert len(root_mock.current_game.convoy) == 0
    service.open_sell_items_menu.assert_called_once()

def test_open_buy_items_menu_calls_printer_and_action_service(shop_service_setup):
    """
    Test that ShopService.open_buy_items_menu calls the printer and action_service correctly.

    Args:
        shop_service_setup (Tuple[ShopService, MagicMock]):
        Fixture providing the ShopService instance and RootService mock.
    """
    service, root_mock = shop_service_setup

    # Provide some dummy shop items
    item = Item("Test Item", True, 0)
    service.shop_items = [item]

    # Call the real method
    service.open_buy_items_menu()

    # Assertions
    service.printer.print_at_open_buy_items_menu.assert_called_once_with(items=[item])
    service.action_service.make_buy_items_decision.assert_called_once()

def test_open_sell_items_menu_with_items(shop_service_setup):
    """
    Test that ShopService.open_sell_items_menu calls the printer and action_service correctly when there are items.

    Args:
        shop_service_setup (Tuple[ShopService, MagicMock]):
        Fixture providing the ShopService instance and RootService mock.
    """
    service, root_mock = shop_service_setup
    player = root_mock.current_game.player

    # add items to player inventory:
    # player items capacity full
    player.items = [Item("Test Item", True, 0), Item("Test Item", True, 0)]

    # Call method
    service.open_sell_items_menu()

    # Verify printer and action service were called
    service.printer.print_at_open_sell_items_menu.assert_called_once()
    service.action_service.make_sell_items_decision.assert_called_once()


def test_open_sell_items_menu_no_items_calls_open_shop(shop_service_setup):
    """
    Test that ShopService.open_sell_items_menu calls open_shop when there are no items to sell.

    Args:
        shop_service_setup (Tuple[ShopService, MagicMock]):
        Fixture providing the ShopService instance and RootService mock.
    """
    service, root_mock = shop_service_setup

    service.open_shop = MagicMock()
    service.printer = MagicMock()
    service.action_service = MagicMock()

    service.open_sell_items_menu()

    # Should print "no items" and call open_shop
    service.open_shop.assert_called_once()
    service.printer.print_at_open_sell_items_menu.assert_not_called()
    service.action_service.make_sell_items_decision.assert_not_called()

def test_generate_shop_weapons_filters_and_copies(shop_service_setup):
    """
    Test that ShopService.generate_shop_weapons filters by allowed weapon types and creates copies.

    Args:
        shop_service_setup (Tuple[ShopService, MagicMock]):
        Fixture providing the ShopService instance and RootService mock.
    """
    service, root_mock = shop_service_setup

    # Pick some weapon types from WEAPONS
    allowed_types = [WeaponType.SWORD]

    # Call the method
    service.generate_shop_weapons(allowed_types)

    # Check that shop_items were populated only with allowed types
    assert len(service.shop_items) > 0
    for weapon in service.shop_items:
        assert weapon.weapon_type == WeaponType.SWORD

    # Ensure copies were made
    original_weapon = list(WEAPONS.values())[0]
    assert original_weapon not in service.shop_items


def test_generate_shop_items_adds_healing_and_boosters(shop_service_setup):
    """
    Test that ShopService.generate_shop_items adds healing potions and stat boosters in order.

    Args:
        shop_service_setup (Tuple[ShopService, MagicMock]):
        Fixture providing the ShopService instance and RootService mock.
    """
    service, root_mock = shop_service_setup

    # Call the method
    service.generate_shop_items()

    # Check that shop_items is not empty
    assert len(service.shop_items) > 0

    # Ensure all healing potions come before stat boosters
    first_booster_index = None
    for i, item in enumerate(service.shop_items):
        assert isinstance(item, (HealingPotion, StatBooster))
        if isinstance(item, StatBooster) and first_booster_index is None:
            first_booster_index = i

    # All items before first booster should be healing potions
    if first_booster_index is not None:
        for item in service.shop_items[:first_booster_index]:
            assert isinstance(item, HealingPotion)
        for item in service.shop_items[first_booster_index:]:
            assert isinstance(item, StatBooster)

    # Check that items are copies, not the same objects as ITEMS
    for item in service.shop_items:
        assert item not in ITEMS.values()

# Test Skill shop
def test_open_buy_skills_menu(shop_service_setup):
    """
    Test that open_buy_skills_menu filters already owned skills,
    calls the weapon skill filter, and triggers printer and action service.
    """
    service, root_mock = shop_service_setup
    player = root_mock.current_game.player

    # player should have a skill
    owned_skill = Skill("Owned Skill", 100, "...")
    player.skills = [owned_skill]

    # shop contains own skill and new skill
    new_skill = Skill("New Skill", 100, "...")
    service.shop_skills = [owned_skill, new_skill]

    # mock methods
    service.filter_weapon_skills_for_player = MagicMock()
    service.printer.print_at_open_buy_skills_menu = MagicMock()
    service.action_service.make_buy_skills_decision = MagicMock()

    # call methode
    service.open_buy_skills_menu()

    # check that new skill is in shop, but not the player skill
    assert owned_skill not in service.shop_skills
    assert new_skill in service.shop_skills

    # check other methodes call
    service.filter_weapon_skills_for_player.assert_called_once()
    service.printer.print_at_open_buy_skills_menu.assert_called_once_with(service.shop_skills)
    service.action_service.make_buy_skills_decision.assert_called_once()

def test_buy_skill(shop_service_setup):
    """
    Test that ShopService.buy_skill correctly purchases both normal and weapon skills.

    Args:
        shop_service_setup (Tuple[ShopService, MagicMock]):
        Fixture providing the ShopService instance and RootService mock.
    """
    service, root_mock = shop_service_setup
    player = root_mock.current_game.player
    player.skills = []
    player.gold = 500
    root_mock.current_game.player_weapons = ["Sword"]

    # Test Skills
    test_skill = Skill("TestSkill A", 100, "...")
    test_weapon_skill = WeaponSkill("TestSkill B", 100, WeaponType.AXE ,"...")

    # Test normal Skill
    service.shop_skills = [test_skill]
    service.open_buy_skills_menu = MagicMock()

    service.buy_skill(test_skill)

    # Assertions for normal skill after buying it
    assert test_skill not in service.shop_skills
    assert test_skill in player.skills
    assert player.gold == 400
    assert WeaponType.AXE not in root_mock.current_game.player_weapons
    service.open_buy_skills_menu.assert_called_once()

    # Test Weapon Skill
    player.gold = 500
    player.skills = []
    root_mock.current_game.player_weapons = [WeaponType.SWORD]
    service.shop_skills = [test_weapon_skill]
    service.open_buy_skills_menu.reset_mock()

    service.buy_skill(test_weapon_skill)

    # Assertions für WeaponSkill
    assert test_weapon_skill not in service.shop_skills
    assert test_weapon_skill in player.skills
    assert player.gold == 400
    assert WeaponType.AXE in root_mock.current_game.player_weapons
    service.open_buy_skills_menu.assert_called_once()