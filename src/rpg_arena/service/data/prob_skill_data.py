from rpg_arena.entity.prob_skill import ProbSkill
from rpg_arena.service.data.stat_modifer_data import STAT_MODIFIERS
from rpg_arena.service.data.weapon_skill_data import WEAPON_SKILLS

luna = ProbSkill(
    name="Luna",
    price=2000,
    target="def",
    value=2,
    type_="attacker",
    description="Skill chance to reduce enemy's defense by half."
)

pavise = ProbSkill(
    name="Pavise",
    price=2000,
    target="str",
    value=2,
    type_="defender",
    description="Skill Chance to halve physical damage.."
)

aegis = ProbSkill(
    name="Aegis",
    price=2000,
    target="magic",
    value=2,
    type_="defender",
    description="Skill chance to halve magical damage.."
)

brutal_hit = ProbSkill(
    name="Brutal Hit",
    price=2000,
    target="str",
    value=0.5,
    type_="attacker",
    description="Skill chance for double attack damage."
)

PROB_SKILLS = [
    luna,
    pavise,
    aegis,
    brutal_hit
]

SKILLS = STAT_MODIFIERS + PROB_SKILLS + WEAPON_SKILLS

START_SKILLS = STAT_MODIFIERS + PROB_SKILLS