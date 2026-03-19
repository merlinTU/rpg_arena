import pytest
from unittest.mock import MagicMock, patch

from rpg_arena.entity import Game
from rpg_arena.entity.prob_skill import ProbSkill
from rpg_arena.service import CampService, ArenaActionService, GameService
from rpg_arena.service.arena_service import ArenaService
from rpg_arena.entity.weapon import Weapon
from rpg_arena.entity.fighter import Fighter
from rpg_arena.entity.unit_class import UnitClass
from rpg_arena.entity.weapon_type import WeaponType



@pytest.fixture
def arena_service_setup():
    """
    Creates a fully mocked ArenaService environment for testing.
    Returns:
        tuple:
            - service (ArenaService): The configured arena service instance
            - root_service_mock (MagicMock): Mocked root service
            - player (Fighter): Configured player unit
            - enemy (Fighter): Configured enemy unit
    """
    # RootService mock
    root_service_mock = MagicMock()
    root_service_mock.current_game = Game()

    root_service_mock.camp_service = CampService(root_service_mock)
    root_service_mock.camp_service.open_camp = MagicMock()

    root_service_mock.game_service = GameService(root_service_mock)
    root_service_mock.game_service.end_game = MagicMock()

    # Player setup
    player_weapon = Weapon(
        name="Test Magic",
        weapon_type=WeaponType.MAGIC,
        strength=10,
        accuracy=90,
        uses=10,
        crit=5,
        weight=5,
        price=100,
        is_magical=True
    )
    player = Fighter(UnitClass.MAGE)
    player.hp = 25
    player.max_hp = 25
    player.strength = 2
    player.magic = 15
    player.defense = 5
    player.res = 10
    player.equipped_weapon = player_weapon
    player.skill = 10
    player.luck = 10

    root_service_mock.current_game.player = player

    # Enemy setup
    enemy_weapon = Weapon(
        name="Test Axe",
        weapon_type=WeaponType.AXE,
        strength=5,
        accuracy=85,
        uses=10,
        crit=5,
        weight=4,
        price=50
    )
    enemy = Fighter(UnitClass.FIGHTER)
    enemy.hp = 30
    enemy.max_hp = 30
    enemy.strength = 8
    enemy.magic = 0
    enemy.defense = 3
    enemy.res = 0
    enemy.equipped_weapon = enemy_weapon
    enemy.skill = 5
    enemy.luck = 5
    enemy.sped = 5

    # ArenaService setup
    service = ArenaService(root_service_mock)
    service.enemy = enemy

    # Mock printer to suppress output
    service.printer.print_at_start_round = MagicMock()
    service.printer.print_after_start_round = MagicMock()
    service.printer.print_after_make_attack = MagicMock()
    service.printer.print_after_arena_simulation = MagicMock()
    service.printer.print_after_surrender = MagicMock()
    service.printer.print_at_end_fight = MagicMock()
    service.printer.print_level_up = MagicMock()

    # Mock action_service to allow deterministic rounds
    service.action_service.make_player_round_decision = MagicMock()
    service.action_service.make_enemy_round_decision = MagicMock()

    # Ensure continue_fight starts as True
    service.continue_fight = True

    return service, root_service_mock, player, enemy

def test_start_arena(arena_service_setup):
    """
    Tests that `start_arena` sets the enemy and calls `arena_simulation`.

    Args:
        arena_service_setup (tuple): Fixture providing the initialized
            arena service and related test objects.
    """
    service, _, player, enemy = arena_service_setup

    service.arena_simulation = MagicMock() # this function is not tested here

    service.start_arena(enemy)
    assert service.enemy == enemy
    assert service.arena_simulation.call_count == 1


def test_check_weapon_vantage(arena_service_setup):
    """
    Tests the `check_weapon_vantage` method of the arena service.

    Args:
        arena_service_setup (tuple): Fixture providing the initialized
            arena service and related test objects.
    """
    service, _, _, enemy = arena_service_setup
    sword = Weapon("Sword", WeaponType.SWORD, 10, 90, 10, 5, 5, 50)
    axe = Weapon("Axe", WeaponType.AXE, 10, 90, 10, 5, 5, 50)
    lance = Weapon("Lance", WeaponType.LANCE, 10, 90, 10, 5, 5, 50)
    magic = Weapon("Staff", WeaponType.MAGIC, 10, 90, 10, 5, 5, 50)

    # Advantage
    assert service.check_weapon_vantage(sword, axe) == 1
    # Disadvantage
    assert service.check_weapon_vantage(sword, lance) == 2
    # No advantage
    assert service.check_weapon_vantage(magic, sword) == 3


@patch("random.random", side_effect=[0, 1])  # ensures hit always succeeds and no crit takes place
def test_make_attack_hits(mock_random, arena_service_setup):
    """
    Tests that an attack hits and deals damage without a critical hit.

    Args:
        mock_random (MagicMock): Mocked randomness for deterministic behavior.
        arena_service_setup (tuple): Fixture providing the initialized
            arena service and related test objects.
    """
    service, _, player, enemy = arena_service_setup
    service.make_attack(player, enemy, 1)

    assert enemy.hp == 5
    assert enemy.max_hp == 30
    assert player.equipped_weapon.uses == 9

@patch("random.random", side_effect=[1])  # ensures hit always succeeds and no crit takes place
def test_make_attack_hits_not(mock_random, arena_service_setup):
    """
    Tests that an attack hits and deals damage without a critical hit.

    Args:
        mock_random (MagicMock): Mocked randomness for deterministic behavior.
        arena_service_setup (tuple): Fixture providing the initialized
            arena service and related test objects.
    """
    service, _, player, enemy = arena_service_setup
    service.make_attack(player, enemy, 1)

    assert enemy.hp == 30
    assert enemy.max_hp == 30
    assert player.equipped_weapon.uses == 10
    service.printer.print_after_make_attack.assert_called_once()

@patch("random.random", side_effect=[0, 0])  # ensures hit always succeeds and always crits
def test_make_attack_crits(mock_random, arena_service_setup):
    """
    Tests that an attack hits and deals damage without a critical hit.

    Args:
        mock_random (MagicMock): Mocked randomness for deterministic behavior.
        arena_service_setup (tuple): Fixture providing the initialized
            arena service and related test objects.
    """
    service, _, player, enemy = arena_service_setup
    service.make_attack(player, enemy, 1)

    assert enemy.hp == 0
    assert enemy.max_hp == 30
    assert player.equipped_weapon.uses == 9
    service.printer.print_after_make_attack.assert_called_once()


def test_caluclate_hit_chance(arena_service_setup):
    """
    Tests the `calculate_hit_chance` method of the arena service.

    Args:
        arena_service_setup (tuple): Fixture providing the initialized
            arena service and related test objects.
    """
    service, _, player, enemy = arena_service_setup
    hit_chance = service.calculate_hit_chance(player, enemy)
    player_hit = 115
    enemy_avoid = 15
    assert  hit_chance == (player_hit - enemy_avoid) / 100

    # with weapon advantage
    player.equipped_weapon.weapon_type = WeaponType.SWORD
    # so that hit chance is lower than 100
    player.equipped_weapon.accuracy = 70
    hit_chance = service.calculate_hit_chance(player, enemy)
    assert hit_chance == 1.0

    # with weapon disadvantage
    player.equipped_weapon.weapon_type = WeaponType.LANCE
    hit_chance = service.calculate_hit_chance(player, enemy)
    assert hit_chance == 0.7

def test_caluclate_crit_chance(arena_service_setup):
    """
    Tests the `calculate_crit_chance` method of the arena service.

    Args:
        arena_service_setup (tuple): Fixture providing the initialized
            arena service and related test objects.
    """
    service, _, player, enemy = arena_service_setup
    crit_chance = service.calculate_crit_chance(player, enemy)
    player_crit = 10
    enemy_crit_avoid = 5
    assert crit_chance == (player_crit - enemy_crit_avoid) / 100


def test_caluclate_damage(arena_service_setup):
    """
    Tests the `calculate_damage` method of the arena service.

    Args:
        arena_service_setup (tuple): Fixture providing the initialized
            arena service and related test objects.
    """
    service, _, player, enemy = arena_service_setup
    damage = service.calculate_damage(player, enemy)

    # magical attack
    assert  damage == 25
    #physical attack
    damage = service.calculate_damage(enemy, player)
    assert damage == 8


@patch("random.random", return_value=0.0)
def test_make_fight_round(mock_random, arena_service_setup):
    """
    Tests the `make_fight_round` method for various combat scenarios,
    including normal attacks, double attacks, no counterattack, and fight ending.

    Args:
        mock_random (MagicMock): Mocked randomness to ensure deterministic hits.
        arena_service_setup (tuple): Fixture providing the initialized
            arena service and related test objects.
    """
    service, _, player, enemy = arena_service_setup
    service.make_attack = MagicMock()
    service.check_weapon_destroyed = MagicMock()
    service.end_fight = MagicMock()

    service.make_fight_round(player, enemy)

    assert service.make_attack.call_count == 2 # player and enemy attack
    service.make_attack.call_count = 0

    # enemy should not counter if hp is 0
    enemy.hp = 0
    service.make_fight_round(player, enemy)
    assert service.make_attack.call_count == 1
    assert service.end_fight.call_count == 1
    service.make_attack.call_count = 0

    # check for double attack
    enemy.hp = 30
    player.speed = 50
    service.make_fight_round(player, enemy)
    assert service.make_attack.call_count == 3
    service.make_attack.call_count = 0

    # fight should end, if unit player ho is 0
    player.hp = 0
    service.make_fight_round(player, enemy)
    assert service.end_fight.call_count == 2
    player.hp = 25
    service.make_attack.call_count = 0

    # enemy should not counter if weapon is broken
    enemy.equipped_weapon = None
    player.speed = 5
    service.make_fight_round(player, enemy)
    assert service.make_attack.call_count == 1
    service.make_attack.call_count = 0


def test_arena_simulation_surrender(arena_service_setup):
    """
      Tests that surrendering in arena simulation restores player HP and
      triggers the correct print and camp methods.

      Args:
          arena_service_setup (tuple): Fixture providing the initialized
              arena service and related test objects.
      """
    service, root, player, enemy = arena_service_setup
    service.continue_fight = "surrender"
    player.hp = 5

    service.arena_simulation(player, enemy)

    assert player.hp == 25
    assert root.current_game.round == 2
    assert service.printer.print_after_surrender.call_count == 1
    assert root.camp_service.open_camp.call_count == 1


def test_arena_simulation_player_wins(arena_service_setup):
    """
     Tests that the player wins an arena simulation, gaining gold and EXP,
     restoring HP, and triggering camp and print methods.

     Args:
         arena_service_setup (tuple): Fixture providing the initialized
             arena service and related test objects.
     """
    service, root, player, enemy = arena_service_setup

    # Setup player and enemy
    player.hp = 25
    player.gold = 0
    player.exp = 0
    enemy.gold = 50
    enemy.exp = 30
    enemy.hp = 0

    # set up action service mocks
    action_service = ArenaActionService(root)
    action_service.make_enemy_round_decision = MagicMock()
    action_service.make_player_round_decision = MagicMock()

    service.continue_fight = False
    service.arena_simulation(player, enemy)

    # Assertions
    service.printer.print_after_arena_simulation.assert_called_once()
    assert player.gold == 50
    assert player.exp == 30
    assert player.hp == player.max_hp
    assert root.current_game.round == 2
    assert root.camp_service.open_camp.call_count == 1

    # end game call

    root.current_game.round = 20
    service.continue_fight = False
    service.arena_simulation(player, enemy)

    root.game_service.end_game.assert_called_once()

def test_arena_simulation_player_wins_with_level_up(arena_service_setup):
    """
     Tests that the player wins an arena simulation and levels up correctly.

     Args:
         arena_service_setup (tuple): Fixture providing the initialized
             arena service and related test objects.
     """
    service, root, player, enemy = arena_service_setup

    player.exp = 50
    enemy.hp = 0
    enemy.exp = 80

    player.level_up = MagicMock()

    # end fight
    service.continue_fight = False
    service.arena_simulation(player, enemy)

    # Assertions
    player.level_up.assert_called()
    assert player.exp == 30
    root.camp_service.open_camp.assert_called_once()

def test_arena_simulation_enemy_wins(arena_service_setup):
    """
    Tests that the arena simulation handles the enemy winning,
    leaving the player with no gold or EXP and not opening the camp.

    Args:
        arena_service_setup (tuple): Fixture providing the initialized
            arena service and related test objects.
    """
    service, root, player, enemy = arena_service_setup
    # player loses
    player.hp = 0
    player.gold = 0
    player.exp = 0
    enemy.hp = 30

    service.continue_fight = False
    service.arena_simulation(player, enemy)

    root.camp_service.open_camp.assert_not_called()
    assert player.exp == 0
    assert player.gold == 0

def test_arena_simulation_enemy_turn_called(arena_service_setup):
    """
    Tests that the enemy's turn is called during arena simulation and
    can interrupt the fight by setting `continue_fight` to False.

    Args:
        arena_service_setup (tuple): Fixture providing the initialized
            arena service and related test objects.
    """
    service, root, player, enemy = arena_service_setup

    # mock enemy and player turn
    def enemy_decision_side_effect():
        # set continue fight to false so that arena is interrupted
        service.continue_fight = False
        return
    service.action_service.make_enemy_round_decision = MagicMock()
    service.action_service.make_enemy_round_decision = MagicMock(
        side_effect=enemy_decision_side_effect
    )

    service.arena_simulation(player, enemy)

    assert service.action_service.make_player_round_decision.call_count == 1
    assert service.action_service.make_enemy_round_decision.call_count == 1

def test_check_weapon_destroyed(arena_service_setup):
    """
    Tests the `check_weapon_destroyed` method to verify behavior
    when a unit has no weapon, a broken weapon, or a usable weapon.

    Args:
        arena_service_setup (tuple): Fixture providing the initialized
            arena service and related test objects.
    """
    service, _, player, _ = arena_service_setup

    # Case 1: Unit has no weapon
    player.equipped_weapon = None
    can_attack = service.check_weapon_destroyed(player)
    # asserts
    assert can_attack is False

    # Case 2: Weapon with 0 uses (broken)
    weapon = MagicMock()
    weapon.uses = 0
    player.equipped_weapon = weapon
    can_attack = service.check_weapon_destroyed(player)
    # asserts
    weapon.break_weapon.assert_called_once_with(player)
    assert can_attack is False

    # Case 3: Weapon with uses left
    weapon = MagicMock()
    weapon.uses = 5
    player.equipped_weapon = weapon
    can_attack = service.check_weapon_destroyed(player)
    # asserts
    assert can_attack is True
    weapon.break_weapon.assert_not_called()

def test_calucalte_damage_with_skill_reduce_def(arena_service_setup):
    """
    Tests that an attacker skill correctly reduces enemy defense
    depending on the weapon type.

    Args:
        arena_service_setup (tuple): Fixture providing the initialized
            arena service and related test objects.
    """
    service, root, player, enemy = arena_service_setup

    test_skill = ProbSkill("...", 0, "def", 2, "attacker", "...")

    # skills always trigger
    player.skill = 100

    player.skills.append(test_skill)
    enemy.res = 10
    enemy.defense = 10

    damage = service.calculate_damage_with_skill(player, enemy)
    assert damage == 15 # normal damage, since res is target
    player.equipped_weapon.magical = False
    damage = service.calculate_damage_with_skill(player, enemy)
    assert damage == 7


def test_calucalte_damage_with_skill_reduce_res(arena_service_setup):
    """
    Tests that an attacker skill correctly reduces enemy resistance for magical attacks
    and has no effect on physical attacks.

    Args:
        arena_service_setup (tuple): Fixture providing the initialized
            arena service and related test objects.
    """
    service, root, player, enemy = arena_service_setup

    test_skill = ProbSkill("...", 0, "res", 2, "attacker", "...")

    # skills always trigger
    player.skill = 100

    player.skills.append(test_skill)
    enemy.res = 10
    enemy.defense = 10

    damage = service.calculate_damage_with_skill(player, enemy)
    assert damage == 20
    player.equipped_weapon.magical = False
    damage = service.calculate_damage_with_skill(player, enemy)
    assert damage == 2

def test_calucalte_damage_with_skill_boost_attack(arena_service_setup):
    """
    Tests that an attacker skill correctly boosts attack damage for
    physical attacks and has no effect on magical attacks.

    Args:
        arena_service_setup (tuple): Fixture providing the initialized
            arena service and related test objects.
    """
    service, root, player, enemy = arena_service_setup

    test_skill = ProbSkill("...", 0, "str", 0.5, "attacker", "...")

    # skills always trigger
    player.skill = 100

    player.skills.append(test_skill)
    enemy.res = 10
    enemy.defense = 10

    damage = service.calculate_damage_with_skill(player, enemy)
    assert damage == 15 # normal hit
    player.equipped_weapon.magical = False
    damage = service.calculate_damage_with_skill(player, enemy)
    assert damage == 14 # 24 damage - 10 def

def test_calucalte_damage_with_skill_boost_magic(arena_service_setup):
    """
    Tests that an attacker skill correctly boosts magical damage
    and has no effect on physical attacks.

    Args:
        arena_service_setup (tuple): Fixture providing the initialized
            arena service and related test objects.
    """
    service, root, player, enemy = arena_service_setup

    test_skill = ProbSkill("...", 0, "magic", 0.5, "attacker", "...")

    # skills always trigger
    player.skill = 100

    player.skills.append(test_skill)
    enemy.res = 10
    enemy.defense = 10

    damage = service.calculate_damage_with_skill(player, enemy)
    assert damage == 40 # boosted magical damage
    player.equipped_weapon.magical = False
    damage = service.calculate_damage_with_skill(player, enemy)
    assert damage == 2

# test defense skills

def test_calucalte_damage_with_skill_red_attack(arena_service_setup):
    """
    Tests that a defender skill reduces incoming attack damage for both
    physical attacks.

    Args:
        arena_service_setup (tuple): Fixture providing the initialized
            arena service and related test objects.
    """
    service, root, player, enemy = arena_service_setup

    test_skill = ProbSkill("...", 0, "str", 2, "defender", "...")

    # skills always trigger
    player.skill = 100

    player.skills.append(test_skill)
    player.res = 0
    player.defense = 0
    enemy.strength = 11

    damage = service.calculate_damage_with_skill(enemy, player)
    assert damage == 8 # 16 damage halfed
    enemy.equipped_weapon.magical = True
    damage = service.calculate_damage_with_skill(enemy, player)
    assert damage == 5

def test_calucalte_damage_with_skill_red_magical_attack(arena_service_setup):
    """
    Tests that a defender skill reduces incoming magical damage and
    has no effect on physical attacks.

    Args:
        arena_service_setup (tuple): Fixture providing the initialized
            arena service and related test objects.
    """
    service, root, player, enemy = arena_service_setup

    test_skill = ProbSkill("...", 0, "magic", 2, "defender", "...")

    # skills always trigger
    player.skill = 100

    player.skills.append(test_skill)
    player.res = 0
    player.defense = 0
    enemy.magic = 1
    enemy.strength = 11

    damage = service.calculate_damage_with_skill(enemy, player)
    assert damage == 16
    enemy.equipped_weapon.magical = True
    damage = service.calculate_damage_with_skill(enemy, player)
    assert damage == 3

