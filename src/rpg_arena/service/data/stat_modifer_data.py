from rpg_arena.entity.stat_modifier_skill import StatModifierSkill

# --- Stat Modifier Skills ---

hit_plus_15 = StatModifierSkill(
    name="Hit +15",
    price=1000,
    target="hit",
    value=15,
    description = "Increases unit's hit rate by 15 points.")

avoid_plus_15 = StatModifierSkill(
    name="Avoid +15",
    price=1000,
    target="avoid",
    value=15,
    description = "Increases unit's avoid (evasion) by 15 points.")

crit_plus_15 = StatModifierSkill(
    name="Crit +15",
    price=1000,
    target="crt",
    value=15,
    description = "Increases unit's critical hit rate by 15 points.")

crit_avoid_plus_15 = StatModifierSkill(
    name="Crit Avoid +15",
    price=250,
    target="crt_avoid",
    value=15,
    description = "Increases unit's critical avoidance by 15 points.")

weapon_master = StatModifierSkill(
    name="Weapon Master",
    price=2500,
    target="weight",
    value=0,
    description = "Removes weapon weight penalties for the unit.")

hit_plus_30 = StatModifierSkill(
    name="Hit +30",
    price=1500,
    target="hit",
    value=30,
    description = "Increases unit's hit rate by 30 points.")

avoid_plus_30 = StatModifierSkill(
    name="Avoid +30",
    price=2000,
    target="avoid",
    value=30,
    description = "Increases unit's avoid (evasion) by 30 points.")

crit_plus_30 = StatModifierSkill(
    name="Crit +30",
    price=2000,
    target="crt",
    value=30,
    description = "Increases unit's critical hit rate by 30 points.")

crit_avoid_plus_30 = StatModifierSkill(
    name="Crit Avoid +30",
    price=500,
    target="crt_avoid",
    value=30,
    description = "Increases unit's critical avoidance by 30 points.")

STAT_MODIFIERS = [
    hit_plus_15,
    avoid_plus_15,
    crit_plus_15,
    crit_avoid_plus_15,
    hit_plus_30,
    avoid_plus_30,
    crit_plus_30,
    crit_avoid_plus_30,
    weapon_master,
]