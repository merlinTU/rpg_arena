import pytest
from unittest.mock import MagicMock, patch

from rpg_arena.service.data import RARE_ITEMS, NORMAL_ITEMS, WEAK_WEAPONS, STRONG_WEAPONS, MEDIUM_WEAPONS
from rpg_arena.service.data.final_boss_data import BOSS_DATA
from rpg_arena.service.roster_service import RosterService
from rpg_arena.entity.fighter import Fighter
from rpg_arena.entity.unit_class import UnitClass


@pytest.fixture
def roster_service_setup():
    """
    Fixture to create a test instance of RosterService with a mocked root service.

    Returns:
        tuple:
            service (RosterService): The service under test.
            root_service_mock (MagicMock): Mocked root service

    """
    root_service_mock = MagicMock()
    root_service_mock.current_game = MagicMock(round=1)

    service = RosterService(root_service_mock)

    return service, root_service_mock

# Tests:
def test_modify_unit_values(roster_service_setup):
    """Test that modify_unit_values increases stats and applies growth."""
    service, _ = roster_service_setup

    fighter = Fighter(UnitClass.MAGE)
    # set stats independent of class data
    fighter.hp = 10
    fighter.strength = 5
    fighter.magic = 5
    fighter.hp_growth = 0.1

    with patch.object(service, "generate_unit_stat_value", return_value=2), \
         patch.object(service, "generate_unit_growth_value", return_value=0.1):

        modified = service.modify_unit_values(fighter, 1)

    assert modified.hp == 27 # because + 15 are always added
    assert modified.strength == 7
    assert modified.magic == 7
    assert modified.hp_growth == 0.5 # because +0.3 is always added

def test_generate_unit_stat_value(roster_service_setup):
    """Test stat generation with mocked random.choices."""
    service, _ = roster_service_setup

    with patch("random.choices", return_value=[5]):
        value = service.generate_unit_stat_value(1)

    assert value == 5
    assert isinstance(value, int)

def test_generate_random_unit(roster_service_setup):
    """Test that a random unit is generated with a weapon."""
    service, _ = roster_service_setup

    with patch.object(service, "random_weapon", return_value="dummy_weapon"):

        unit = service.generate_random_unit(1)

    assert isinstance(unit, Fighter)
    assert "dummy_weapon" in unit.items


def test_random_item_rare(roster_service_setup):
    """Test that a rare item is returned when probability threshold is met."""
    service, _ = roster_service_setup

    with patch("random.random", return_value=0.01):

        item = service.random_item()

    assert item.name in [item.name for item in RARE_ITEMS]

def test_random_item_normal(roster_service_setup):
    """Test that a normal item is returned when rare threshold is not met."""
    service, _ = roster_service_setup

    with patch("random.random", return_value=0.9):

        item = service.random_item()

    assert item.name in [item.name for item in NORMAL_ITEMS]

def test_generate_initial_units(roster_service_setup):
    """Test that initial unit generation returns five fighters."""
    service, _ = roster_service_setup

    units = service.generate_initial_units()

    assert len(units) == 5
    assert all(isinstance(u, Fighter) for u in units)

def test_generate_enemy_units(roster_service_setup):
    """Test enemy unit generation."""
    service, _ = roster_service_setup

    enemies = service.generate_enemy_units()

    assert len(enemies) == 3
    assert all(e.name == "Gladiator" for e in enemies)


@pytest.mark.parametrize(
    "type_, mocked_value, expected_range",
    [
        (1, 5, range(0, 16)),   # player
        (2, 3, range(0, 11)),   # weaker enemy
        (3, 10, range(5, 16)),  # stronger enemy
        (999, 5, range(0, 16)), # default branch
    ],
)
def test_generate_unit_stat_value_cases(roster_service_setup, type_, mocked_value, expected_range):
    """Test stat generation for all type branches with mocked randomness."""
    service, _ = roster_service_setup

    with patch("random.choices", return_value=[mocked_value]):
        value = service.generate_unit_stat_value(type_)

    assert value == mocked_value
    assert value in expected_range
    assert isinstance(value, int)

# to check the range of the units stats
@pytest.mark.parametrize(
    "type_,expected_range,mocked_value",
    [
        (1, range(1, 11), 0.25),
        (2, range(0, 6), 0.10),
        (3, range(1, 8), 0.2),
        (4, range(5, 12), 0.35),
        (999, range(1, 11), 0.25),
    ],
)
def test_generate_unit_growth_value(roster_service_setup, type_, expected_range, mocked_value):
    """Test growth generation for all type branches with mocked randomness."""
    service, _ = roster_service_setup

    with patch("random.choices", return_value=[mocked_value]):
        value = service.generate_unit_growth_value(type_)

    possible = [i * 0.05 for i in expected_range]

    # pytest.approx for float precision problem
    assert value == pytest.approx(mocked_value)

    # compare with tolerance
    assert any(value == pytest.approx(p) for p in possible)

@pytest.mark.parametrize("unit_type,roll,expected_tier", [
    # normal unit
    (1, 0.01, STRONG_WEAPONS),
    (1, 0.2, MEDIUM_WEAPONS),
    (1, 0.7, WEAK_WEAPONS),
    (3, 0.01, STRONG_WEAPONS),
    (3, 0.2, MEDIUM_WEAPONS),
    (3, 0.7, WEAK_WEAPONS),

    # weak unit
    (2, 0.06, MEDIUM_WEAPONS),
    (2, 0.5, WEAK_WEAPONS),

    # strong enemy
    (4, 0.19, STRONG_WEAPONS),
    (4, 0.6, MEDIUM_WEAPONS),
    (4, 0.95, WEAK_WEAPONS),

    # fallback
    (99, 0.01, STRONG_WEAPONS),
    (99, 0.2, MEDIUM_WEAPONS),
    (99, 0.7, WEAK_WEAPONS),
])
def test_random_weapon_modifier_effect(roster_service_setup, unit_type, roll, expected_tier):
    """Test that unit type and random roll correctly selects weapon tier."""
    service, _ = roster_service_setup

    with patch("random.random", return_value=roll):
        weapon = service.random_weapon(UnitClass.MAGE, unit_type)

    assert weapon.name in  [weapon.name for weapon in expected_tier]


def test_level_enemy_unit_all_strengths(roster_service_setup):
    """
    Test that `level_enemy_unit` correctly sets level, gold, and experience
    for all enemy strength types using
    deterministic random values.
    """
    service, root = roster_service_setup

    # easy enemy
    unit_easy = Fighter(UnitClass.MAGE)
    root.current_game.round = 1  # set round for calculation

    with patch("random.normalvariate", return_value=0):
        service.level_enemy_unit(unit_easy, 0)

    assert unit_easy.level == 1
    assert unit_easy.gold == 70
    assert unit_easy.exp == 50

    # medium enemy
    unit_medium = Fighter(UnitClass.MAGE)
    root.current_game.round = 3

    with patch("random.randint", return_value=0), patch("random.normalvariate", return_value=0):
        service.level_enemy_unit(unit_medium, 1)

    assert unit_medium.level == 3
    assert unit_medium.gold == 250
    assert unit_medium.exp == 100

    # strong enemy
    unit_strong = Fighter(UnitClass.MAGE)
    root.current_game.round = 2

    with patch("random.randint", return_value=1), patch("random.normalvariate", return_value=0):
        service.level_enemy_unit(unit_strong, 2)

    assert unit_strong.level == 3
    assert unit_strong.gold == 360
    assert unit_strong.exp == 150


def test_generate_boss_unit(roster_service_setup):
    """
    Test that `generate_boss_unit` correctly selects the boss based on a fixed
    random number.
    """
    service, _ = roster_service_setup

    # Patch random.randint to 0
    with patch("random.randint", return_value=0):
        boss = service.generate_boss_unit()

    # check boss name
    expected_name = BOSS_DATA[0]["name"]
    assert isinstance(boss, Fighter)
    assert boss.name == expected_name