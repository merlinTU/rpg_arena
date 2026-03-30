from rpg_arena.entity.weapon_skill import WeaponSkill
from rpg_arena.entity.weapon import WeaponType

# --- Weapon Skills (Proficiencies) ---

# Sword Skills
sword_proficiency = WeaponSkill(
    name="Sword Prof.",
    price=1000,
    weapon_type=WeaponType.SWORD,
    description="Allows the unit to wield swords."
)

# Lance Skills
lance_proficiency = WeaponSkill(
    name="Lance Prof.",
    price=1000,
    weapon_type=WeaponType.LANCE,
    description="Allows the unit to wield lances."
)

# Axe Skills
axe_proficiency = WeaponSkill(
    name="Axe Prof.",
    price=1000,
    weapon_type=WeaponType.AXE,
    description="Allows the unit to wield axes."
)

# Bow Skills
bow_proficiency = WeaponSkill(
    name="Bow Prof.",
    price=1000,
    weapon_type=WeaponType.BOW,
    description="Allows the unit to wield bows."
)

# Magic Skills
magic_proficiency = WeaponSkill(
    name="Magic Prof.",
    price=1000,
    weapon_type=WeaponType.MAGIC,
    description="Allows the unit to cast offensive magic spells."
)

WEAPON_SKILLS = [
    sword_proficiency,
    lance_proficiency,
    axe_proficiency,
    bow_proficiency,
    magic_proficiency
]