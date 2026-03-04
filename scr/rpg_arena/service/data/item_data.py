from rpg_arena.entity.healing_potion import HealingPotion
from rpg_arena.entity.stat_booster import StatBooster


vulnerary = HealingPotion(
    name="Vulnerary",
    heal_amount=10,
    uses=3,
    price=200
)

concoction = HealingPotion(
    name="Concoction",
    heal_amount=15,
    uses=5,
    price=350
)

hi_potion = HealingPotion(
    name="Hi-Potion",
    heal_amount=30,
    uses=2,
    price=400
)

seraph_robe = StatBooster(
    name="Seraph Robe",
    status="HP",
    boost=5,
    price=1000
)

secret_book = StatBooster(
    name="Secret Book",
    status="SKL",
    boost=2,
    price=1800
)

luck_charm = StatBooster(
    name="Luck Charm",
    status="LUCK",
    boost=3,
    price=1800
)


elixir = HealingPotion(
    name="Elixir",
    heal_amount=50,
    uses=1,
    price=1500
)

dracoshield = StatBooster(
    name="Dracoshield",
    status="DEF",
    boost=3,
    price=1800
)

spirit_dust = StatBooster(
    name="Spirit Dust",
    status="MAG",
    boost=2,
    price=1800
)

energy_ring = StatBooster(
    name="Energy Ring",
    status="STR",
    boost=2,
    price=1800
)

talisman = StatBooster(
    name="Talisman",
    status="RES",
    boost=3,
    price=1800
)

speedwing = StatBooster(
    name="Speedwing",
    status="SPD",
    boost=2,
    price=1800
)


ITEMS = {
    "Vulnerary": vulnerary,
    "Concoction": concoction,
    "Hi-Potion": hi_potion,
    "Seraph Robe": seraph_robe,
    "Secret Book": secret_book,
    "Luck Charm": luck_charm,
    "Elixir": elixir,
    "Dracoshield": dracoshield,
    "Spirit Dust": spirit_dust,
    "Energy Ring": energy_ring,
    "Talisman": talisman,
    "Speedwing": speedwing
}


NORMAL_ITEMS = [
    vulnerary,
    concoction,
    hi_potion,
    seraph_robe,
    secret_book,
    luck_charm
]

RARE_ITEMS = [
    elixir,
    dracoshield,
    spirit_dust,
    energy_ring,
    talisman,
    speedwing
]