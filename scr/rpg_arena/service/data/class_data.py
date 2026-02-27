from dataclasses import dataclass
from rpg_arena.entity.unit_class import UnitClass

@dataclass
class ClassStats:
    base_hp: int
    base_str: int
    base_magic: int
    base_skill: int
    base_speed: int
    base_luck: int
    base_defense: int
    base_res: int

    growth_hp: float
    growth_str: float
    growth_magic: float
    growth_skill: float
    growth_speed: float
    growth_luck: float
    growth_defense: float
    growth_res: float

CLASS_DATA = {
    UnitClass.MERCENARY: ClassStats(
        base_hp=30, base_str=10, base_magic=0,
        base_skill=8, base_speed=10, base_luck=5,
        base_defense=6, base_res=2,
        growth_hp=0.8, growth_str=0.35, growth_magic=0.1,
        growth_skill=0.25, growth_speed=0.4,
        growth_luck=0.5, growth_defense=0.45, growth_res=0.2
    ),

    UnitClass.MAGE: ClassStats(
        base_hp=25, base_str=4, base_magic=5,
        base_skill=12, base_speed=8, base_luck=7,
        base_defense=3, base_res=10,
        growth_hp=0.5, growth_str=0.2, growth_magic=0.8,
        growth_skill=0.6, growth_speed=0.5,
        growth_luck=0.4, growth_defense=0.1, growth_res=0.7
    ),

    UnitClass.FIGHTER: ClassStats(
        base_hp=35, base_str=12, base_magic=0,
        base_skill=5, base_speed=6, base_luck=4,
        base_defense=5, base_res=3,
        growth_hp=0.8, growth_str=0.6, growth_magic=0.05,
        growth_skill=0.35, growth_speed=0.2,
        growth_luck=0.15, growth_defense=0.35, growth_res=0.15
    )
}