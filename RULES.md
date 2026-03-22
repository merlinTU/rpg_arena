# RPG-Arena Documentation

## Table of Contents
- [1. Starting the Game](#1-starting-the-game)
- [2. Help](#2-help)
- [3. Game Flow](#3-game-flow)
  - [3.1. Choosing Your Fighter](#31-choosing-your-fighter)
  - [3.2. Enter the Camp](#32-enter-the-camp)
  - [3.3. Enter the Arena](#33-enter-the-arena)
  - [3.4. Fight Enemy](#34-fight-enemy)
  - [3.5. End Fight](#35-end-fight)
  - [3.6. Aim of the Game](#36-aim-of-the-game)
- [4. Fighter](#42-status-values)
  - [4.1. Status Values](#42-status-values)
  - [4.2. Growth Values](#43-growth-values)
  - [4.3. Classes](#44-classes)
  - [4.5. Weapons](#45-weapons)
  - [4.6. Items](#46-items)
- [5. Combat](#5-combat)
  - [5.1. Fight Round](#51-fight-round)
  - [5.2. Attack](#52-attack)
  - [5.3. Damage](#53-damage)
  - [5.4. Hit Chance](#54-hit-chance)
  - [5.5. Crit Chance](#55-critical-chance)
  - [5.6. Weapon Advantage](#56-weapon-advantage)
  - [Skills](#57-skills)

## 1. Starting the Game
You can start RPG-arnea via this code:
```python
import rpg_arena

rpg_arena.start_game()
```
After typing this code the Text "Welcome to RPG-Arena" is printed.

## 2. Help

When ever the game asks you to make a decision, you can write "info x" or "check x" to get information
about the [items](#46-items), [weapons](#45-weapons) or mechanics like [battles](#51-fight-round). You can also write
"info player" or "info enemy" to check your own and the enemy fighter.

## 3. Game Flow:

### 3.1. Choosing Your Fighter

At the start of the game, you will be asked to choose one of five randomly generated [fighters](#41-character-generation). 
Each fighter differs in [base stats](#42-status-values), [growth rates](#43-growth-values), [starting inventory](#46-items), 
and [skills](#57-skills).

### 3.2. Enter the Camp
Before each battle, your fighter visits the camp. At the camp, you can:

- **Manage your inventory:** Use [items](#46-items) or equip [weapons](#45-weapons).  
- **Visit the shop:** Buy [weapons](#45-weapons), [items](#46-items), or [skills](#57-skills).  

Once preparations are complete, you can enter the arena.  
⚠️ **Warning:** After entering the arena, you cannot return to the camp until the battle is won,
so choose this step carefully and make sure your fighter is ready for battle.

### 3.3. Enter the Arena
When you enter the arena, you can choose between **three types of gladiators** to fight:

1. **Easy Opponent:**  
   - Gives 50 EXP and a small amount of gold.  
   - Designed to be easily defeated, even without optimal fighter build.  

2. **Normal Opponent:**  
   - Gives 100 EXP and a moderate amount of gold.  
   - Can be easily defeated with the right [class](#44-classes) , [equipment](#45-weapons), and [items](#46-items).

3. **Hard Opponent:**  
   - Gives 150 EXP and a large amount of gold.  
   - Can only be defeated by a well-trained fighter with strong [stats](#42-status-values), the right [class](#44-classes), and proper [equipment](#45-weapons).  

### 3.4. Fight Enemy

Combat in **RPG-Arena** is divided into player and enemy phases.  
During your player phase, you have four options:

1. **Attack:** Initializes a [fight round](#51-fight-round) with the enemy.
2. **Use Item / Equip Weapon:** Use an [item](#46-items) from your inventory or change your [weapon](#45-weapons).
3. **Wait:** Do nothing this turn.
4. **Surrender:** End the fight safely, but you will receive no rewards at the end of the battle.

After your turn, the enemy phase begins. Enemy units will always attack as long as a weapon is equipped. Consider that your fighter can take damage from a counterattack when initiating a [fight round](#51-fight-round) 
, as well as during the enemy phase.

### 3.5. End Fight

When a fighter's **HP drops to 0 or below**, the fight ends.  

- **Victory:** If the enemy is defeated, your fighter earns EXP and gold. If your fighter gets 100 EXP, his level is increased by 1
and his stats are increased according to his [growths](#43-growth-values).
- **Defeat:** If your fighter is defeated, the game is over and you must restart.  


### 3.6. Aim of the Game

After completing **20 arena battles**, your fighter will face a **powerful boss opponent**.  
- One of three preset bosses will appear.  
- To defeat the boss, your fighter must have the **right combination of [equipment](#45-weapons), [items](#46-items), and [skills](#57-skills)**.  

Your goal is to **create the best build** for your fighter, balancing stats, [items](#46-items), and [skills](#57-skills).

## 4. Fighter

### 4.1. Character Generation

The base stats and growth values of each character are **randomly generated**.  
However, adjustments are applied based on the fighter’s [class](#44-classes), so that certain stats and growth values reflect the character’s role.  

This means each character [starts](#42-status-values) with random base stats and [growth values](#43-growth-values), and then the **class modifiers** are added to create a final, balanced fighter suitable for their class.

### 4.2. Status Values
- **HP:** The fighter’s health. If this reaches 0, the fighter is defeated.

- **STR (Strength):** Determines physical [attack](#52-attack) power and damage dealt with non-magical [weapons](#45-weapons).

- **MAG (Magic):** Determines magical [attack](#52-attack) power, used for spells and magical [weapons](#45-weapons).

- **SKL (Skill):** Affects [Hit](#54-hit-chance) and [Crit Chance](#55-critical-chance) during [attacks](#52-attack). 

- **SPD (Speed):** Determines how fast the fighter is in combat. If Speed is 5 points higher than the enemies Speed the fighter can strike
twice in a [fight round](#51-fight-round). This is also true for the enemy.

- **DEF (Defense):** Reduces damage taken from physical [attacks](#52-attack).

- **RES (Resistance):** Reduces damage taken from magical [attacks](#52-attack).

- **LCK (Luck):** Influences [Hit Chance](#54-hit-chance) and [Crit Chance](#55-critical-chance).

### 4.3. Growth Values

Each status value has a corresponding **growth value** ranging between 0 and 1. Whenever your fighter **levels up**, each status has a chance equal to its growth value to **increase by 1 point**.  

### 4.4. Classes

In **RPG-Arena**, each fighter belongs to a **class**, which defines his role, strengths, and weaknesses.  
Classes influence **base stats, growth rates, and available [weapons](#45-weapons)**, shaping how each unit performs in battle.  

Here’s a brief overview of the main classes:

- **Fighter:** Aggressive and rough combatants. They use axes and bows, and have high [Strength](#42-status-values) and [HP](#42-status-values).

- **Mage:** Use magic to attack. High [Magic](#42-status-values) and [Resistance](#42-status-values), but low [Defense](#42-status-values). 

- **Mercenary:** Agile melee fighters with balanced [stats](#42-status-values). Use Swords and Axes.  

- **Knight:** Heavy armored units with high [Defense](#42-status-values) and [HP](#42-status-values), but low [Speed](#42-status-values). Use Lances and Swords. 

- **Sword Master:** Advanced melee units with very high [Skill](#42-status-values) and [Speed](#42-status-values). Use Swords.  

- **Berserker:** Powerful physical attackers with high [Strength](#42-status-values), deals massive damage but may lack [Defense](#42-status-values).
Use Axes.

- **Thief:** Agile combatants with high [Speed](#42-status-values) but low [Strength](#42-status-values). Use Swords and Magic.

- **Soldier:** Basic combat units with high [Skill](#42-status-values) and balanced [Stats](#42-status-values). Uses Lances.

- **Archer:** Weak combat units with high [Crit chance](#55-critical-chance). Uses Bows.

- **Paladin:** Mounted units with high [Stats](#42-status-values),, but lower [growth rates](#43-growth-values). Uses Swords, Lances and Axes.

### 4.5. Weapons

Weapons are used in [combat](#51-fight-round) and each weapon has the following attributes:

1. **Damage:** The base amount of damage the weapon deals on a successful [attack](#52-attack).  
2. **Weapon Type:** Determines the category of the weapon (e.g., Sword, Axe, Lance, Bow, Magic) and affects [weapon advantage](#56-weapon-advantage).  
3. **Accuracy:** Influences the likelihood of hitting the opponent (see [hit chance](#54-hit-chance)).  
4. **Weight:** The fighters speed is reduced by Weight - Player STR  
5. **Critical (Crit):** The chance to deal a **critical hit** (see [critical chance](#55-critical-chance)).
6. **Uses:** The number of times a weapon can be used before it breaks.


### 4.6. Items

RPG-Arena features **two types of items**: **healing items** and **stat boosters**.  

- **Healing Items:** Can be used during [battles](#51-fight-round) to restore a specific status value, such as HP.  
- **Stat Boosters:** Temporarily or permanently increase one of your fighter’s [status values](#42-status-values), helping them perform better in combat.

# 5. Combat

### 5.1. Fight Round

Each battle takes place in **three phases**:

1. **Initiative Phase:** Either the player or the enemy starts the [attack](#52-attack) based on the current turn.  
2. **Counterattack Phase:** The defending unit automatically counterattacks if able.  
3. **Follow-Up Attack Phase:** If either the attacker or the defender has 5 more [Speed](#42-status-values)
 points than the other, they perform a second attack.

Beware: if your fighter initiates an attack, he should be able to withstand the counterattack and the next initiative attack in the enemy phase. Choosing to wait first can sometimes be helpful.

### 5.2. Attack

Each attack has three main attributes: **Damage**, **Hit Chance**, and **Critical Chance**.

### 5.3. Damage

The damage dealt depends on the type of attack:
- **Physical Attack:** 
- Damage = Attacker [STR](#42-status-values) + [Weapon Might](#45-weapons) - Defender [DEF](#42-status-values)

- **Magical Attack:**  
Damage = Attacker [MAG](#42-status-values) + [Weapon Might](#45-weapons) - Defender [RES](#42-status-values)

### 5.4. Hit Chance

The chance for an attack to hit is calculated using this formula:   
Hit = [Weapon Hit ](#45-weapons) + (Attacker [SKL](#42-status-values) * 2) + (Attacker [LCK](#42-status-values) / 2) - (Defender [SPD](#42-status-values) * 2) + Defender [LCK](#42-status-values).  

The hit chance is adjusted by a **[weapon advantage](#56-weapon-advantage)** bonus, which depends on the [weapons](#45-weapons) equipped by 
both the attacker and the defender (for example, swords are strong against axes).

### 5.5. Critical Chance

Critical hits deal triple damage and are calculated as:    
Crit = Attacker [SKL](#42-status-values) / 2  - Defender [LCK](#42-status-values)

### 5.6. Weapon Advantage

Some [weapons](#45-weapons) have advantages over others, following a classic triangle system:
- **Swords > Axes** 
- **Lances > Swords**
- **Axes > Lances** 
- **Magic = Bows** 

When a weapon has an advantage over the opponent, it grants a **+20 bonus to [Hit Chance](#54-hit-chance)**. 
If a weapon is at a **disadvantage**, it receives a **-20 penalty to [Hit Chance](#54-hit-chance)**.

### 5.7. Skills

There are three types of skills in RPG-Arena:

1. **Combat-Boosting Skills:**  
   Increase battle-related stats such as [Hit Chance](#54-hit-chance), [Avoid](#54-hit-chance), or [Crit Chance](#55-critical-chance).  

2. **Triggered Skills:**  
   Activate during [combat](#51-fight-round) with a certain probability, providing effects like extra or reduced damage.  

3. **Weapon Skills:**  
   Grant proficiency of [weapons](#45-weapons), allowing your fighter to use a wider variety of weapons.

Skills can be purchased in the [Skill Shop](#32-enter-the-camp).