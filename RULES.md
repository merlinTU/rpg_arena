## Starting the Game
You can start RPG-arnea via this code:
```python
import rpg_arena

rpg_arena.start_game()
```
After typing this code the Text "Welcome to the Arena" is printed.

## Help
When ever the game asks you to make a decision, you can write "info x" or "check x" to get information
about the [items](#items), [weapons](#weapons) or mechanics like [battles](#fight-round). You can also write
"info player" or "info enemy" to check our own fighter and the enemy fighter.
---
# Game Flow:

## 1. Choosing Your Fighter

At the start of the game, you will be asked to choose one of five randomly generated [fighters](#character-generation). 
Each fighter differs in [base stats](#status-values), [growth rates](#growth-values), [starting inventory](#items), 
and [skills](#skills).

## 2. Enter the Camp
Before each battle, your fighter visits the camp. At the camp, you can:

- **Manage your inventory:** Use [items](#items) or equip [weapons](#weapons).  
- **Visit the shop:** Buy [weapons](#weapons), [items](#items), or [skills](#skills).  

Once preparations are complete, you can enter the arena.  
⚠️ **Warning:** After entering the arena, you cannot return to the camp until the battle is won,
so choose this step carefully and make sure your fighter is ready for battle.

## 3. Enter the Arena
When you enter the arena, you can choose between **three types of gladiators** to fight:

1. **Easy Opponent:**  
   - Gives 50 EXP and a small amount of gold.  
   - Designed to be easily defeated, even without optimal fighter build.  

2. **Normal Opponent:**  
   - Gives 100 EXP and a moderate amount of gold.  
   - Can be easily defeated with the right [class](#classes) , [equipment](#weapons), and [items](#items).

3. **Hard Opponent:**  
   - Gives 150 EXP and a large amount of gold.  
   - Can only be defeated by a well-trained fighter with strong [stats](#status-values), the right [class](#classes), and proper [equipment](#weapons).  

## 4. Fight Enemy

Combat in **RPG-Arena** is divided into player and enemy phases.  
During your player phase, you have four options:

1. **Attack:** Initializes a [fight round](#fight-round) with the enemy.
2. **Use Item / Equip Weapon:** Use an [item](#items) from your inventory or change your [weapon](#weapons).
3. **Wait:** Do nothing this turn.
4. **Surrender:** End the fight safely, but you will receive no rewards at the end of the battle.

## 5. End Fight

When a fighter's **HP drops to 0 or below**, the fight ends.  

- **Victory:** If the enemy is defeated, your fighter earns EXP and gold. If your fighter gets 100 EXP, his level is increased by 1
and his stats are increased according to his [growths](#growth-values).
- **Defeat:** If your fighter is defeated, the game is over and you must restart.  


## 6. Aim of the Game

After completing **20 arena battles**, your fighter will face a **powerful boss opponent**.  
- One of three preset bosses will appear.  
- To defeat the boss, your fighter must have the **right combination of [equipment](#weapons), [items](#items), and [skills](#skills)**.  

Your goal is to **create the best build** for your fighter, balancing stats, [items](#items), and [skills](#skills).

---
## Status Values
- **HP:** The fighter’s health. If this reaches 0, the fighter is defeated.

- **STR (Strength):** Determines physical [attack](#attack) power and damage dealt with non-magical [weapons](#weapons).

- **MAG (Magic):** Determines magical [attack](#attack) power, used for spells and magical [weapons](#weapons).

- **SKL (Skill):** Affects [Hit](#2-hit-chance) and [Crit Chance](#3-critical-chance) during [attacks](#attack). 

- **SPD (Speed):** Determines how fast the fighter is in combat. If Speed is 5 points higher than the enemies Speed the fighter can strike
twice in a [fight round](#fight-round). This is also true for the enemy.

- **DEF (Defense):** Reduces damage taken from physical [attacks](#attack).

- **RES (Resistance):** Reduces damage taken from magical [attacks](#attack).

- **LCK (Luck):** Influences [Hit Chance](#2-hit-chance) and [Crit Chance](#3-critical-chance).

## Growth Values

Each status value has a corresponding **growth value** ranging between 0 and 1. Whenever your fighter **levels up**, each status has a chance equal to its growth value to **increase by 1 point**.  

---

## Character Generation

The base stats and growth values of each character are **randomly generated**.  
However, adjustments are applied based on the fighter’s [class](#classes), so that certain stats and growth values reflect the character’s role.  

This means each character [starts](#status-values) with random base stats and [growth values](#growth-values), and then the **class modifiers** are added to create a final, balanced fighter suitable for their class.

## Classes

In **RPG-Arena**, each fighter belongs to a **class**, which defines their role, strengths, and weaknesses.  
Classes influence **base stats, growth rates, and available [weapons](#weapons)**, shaping how each unit performs in battle.  

Here’s a brief overview of the main classes:

- **Fighter:** Aggressive and rough combatants. They use axes and bows, and have high [Strength](#status-values) and [HP](#status-values).

- **Mage:** Use magic to attack. High [Magic](#status-values) and [Resistance](#status-values), but low [Defense](#status-values). 

- **Mercenary:** Agile melee fighters with balanced [stats](#status-values). Use Swords and Axes.  

- **Knight:** Heavy armored units with high [Defense](#status-values) and [HP](#status-values), but low [Speed](#status-values). Use Lances and Swords. 

- **Sword Master:** Advanced melee units with very high [Skill](#status-values) and [Speed](#status-values). Use Swords.  

- **Berserker:** Powerful physical attackers with high [Strength](#status-values), deals massive damage but may lack [Defense](#status-values).
Use Axes.

- **Thief:** Agile combatants with high [Speed](#status-values) but low [Strength](#status-values). Use Swords and Magic.

- **Soldier:** Basic combat units with high [Skill](#status-values) and balanced [Stats](#status-values). Uses Lances.

- **Archer:** Weak combat units with high [Crit chance](#3-critical-chance). Uses Bows.

- **Paladin:** Mounted units with high [Stats](#status-values),, but lower [growth rates](#growth-values). Uses Swords, Lances and Axes.
---

## Weapons

Weapons are used in [combat](#fight-round) and each weapon has the following attributes:

1. **Damage:** The base amount of damage the weapon deals on a successful [attack](#attack).  
2. **Weapon Type:** Determines the category of the weapon (e.g., Sword, Axe, Lance, Bow, Magic) and affects [weapon advantage](#weapon-advantage).  
3. **Accuracy:** Influences the likelihood of hitting the opponent (see [hit chance](#2-hit-chance)).  
4. **Weight:** The fighters speed is reduced by Weight - Player STR  
5. **Critical (Crit):** The chance to deal a **critical hit** (see [critical chance](#3-critical-chance)).
6. **Uses:** The number of times a weapon can be used before it breaks.


## Items

RPG-Arena features **two types of items**: **healing items** and **stat boosters**.  

- **Healing Items:** Can be used during [battles](#fight-round) to restore a specific status value, such as HP.  
- **Stat Boosters:** Temporarily or permanently increase one of your fighter’s [status values](#status-values), helping them perform better in combat.

---
## Fight Round

Each battle takes place in **three phases**:

1. **Initiative Phase:** Either the player or the enemy starts the [attack](#attack) based on speed or pre-determined initiative.  
2. **Counterattack Phase:** The defending unit automatically counterattacks if able.  
3. **Follow-Up Attack Phase:** If the attacker’s **Speed** is at least **5 points higher** than the defender’s, they perform a **follow-up attack**, hitting a second time.

---

## Attack

Each attack has three main attributes: **Damage**, **Hit Chance**, and **Critical Chance**.

### 1. Damage

The damage dealt depends on the type of attack:
- **Physical Attack:** 
- Damage = Attacker [STR](#status-values) + [Weapon Might](#weapons) - Defender [DEF](#status-values)

- **Magical Attack:**  
Damage = Attacker [MAG](#status-values) + [Weapon Might](#weapons) - Defender [RES](#status-values)

### 2. Hit Chance

The chance for an attack to hit is calculated using this formula:   
Hit = [Weapon Hit ](#weapons) + (Attacker [SKL](#status-values) * 2) + (Attacker [LCK](#status-values) / 2) - (Defender [SPD](#status-values) * 2) + Defender [LCK](#status-values).  

The hit chance is adjusted by a **[weapon advantage](#weapon-advantage)** bonus, which depends on the [weapons](#weapons) equipped by 
both the attacker and the defender (for example, swords are strong against axes).

### 3. Critical Chance

Critical hits deal triple damage and are calculated as:    
Crit = Attacker [SKL](#status-values) / 2  - Defender [LCK](#status-values)

## Weapon Advantage

Some [weapons](#weapons) have advantages over others, following a classic triangle system:
- **Swords > Axes** 
- **Lances > Swords**
- **Axes > Lances** 
- **Magic = Bows** 

When a weapon has an advantage over the opponent, it grants a **+20 bonus to [Hit Chance](#2-hit-chance)**. 
If a weapon is at a **disadvantage**, it receives a **-20 penalty to [Hit Chance](#2-hit-chance)**.

## Skills

There are three types of skills in RPG-Arena:

1. **Combat-Boosting Skills:**  
   Increase battle-related stats such as [Hit Chance](#2-hit-chance), [Avoid](#2-hit-chance), or [Crit Chance](#3-critical-chance).  

2. **Triggered Skills:**  
   Activate during [combat](#fight-round) with a certain probability, providing effects like extra damage, healing, or stat boosts.  

3. **Weapon Skills:**  
   Grant proficiency or special effects with specific types of [weapons](#weapons), allowing your fighter to use them more effectively.

Skills can be purchased in the [Skill Shop](#2-enter-the-camp).