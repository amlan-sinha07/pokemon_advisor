# Pokemon Champions Battle Advisor

A real time battle decision tool for Pokemon Champions (2026) built in Python with a C++ damage calculation engine.

## What It Does

**Pre-Match (1 minute window):**

- Input opponent's 6 Pokemon
- Loads your saved box automatically
- Scores each of your pokemon against opponent team 
- Recommends best 4 to bring with type coverage reasoning

**In-Battle (40 seconds window):**

- Input your active Pokemon + current HP
- Input opponent's active Pokemon + current HP
- Enter your 4 moves
- Recommends best move with damage estimate, effectiveness, speed check

## Sample Output

### Pre-match Team Selector
![Pre-Match team selector](<Screenshot 2026-06-27 185749.png>)
![Team Suggestion](<Screenshot 2026-06-27 185804.png>)

### In-Battle Move Advisor
![In-Battle Move Advisor](<Screenshot 2026-06-27 190707.png>)
![Move Selector](<Screenshot 2026-06-27 190721.png>)

### Viewing full box
![Viewing full box](<Screenshot 2026-06-27 190731.png>)

### Pre Match Analysis

Opponent's team:
 Charizard [Fire/Flying]
 Venusaur [Grass/Poison]
 Blaziken [Fire/Fighting]
 Abomasnow [Grass/Ice]
 Pikachu [Electric]
 Lucario [Fighting/Steel]

Your team score:
 Infernape    [Fire/Fighting  ] score:19.75
 Ceruledge    [Fire/Ghost     ] score:18.25
 Froslass     [Ice/Ghost      ] score:14.0
 Pelipper     [Water/Flying   ] score:13.0
 Scizor       [Bug/Steel      ] score:8.75
 Raichu       [Electric       ] score:8.75

>>> BRING THESE 4 POKEMON <<<
 Infernape (score: 19.75)
 Ceruledge (score: 18.25)
 Froslass (score: 14.0)
 Pelipper (score: 13.0)

### In battle 

=== BATTLE ADVISOR ===
Your : Infernape HP: 76/76
Opponent: Abomasnow HP: 90/90
⚡ You go FIRST (spd 108 > 60)

Move analysis:
    flare-blitz      dmg:451    effectiveness: 4.0x (double super effective)
    heat-wave        dmg:319    effectiveness: 4.0x (double super effective)
    flamethrower     dmg:303    effectiveness: 4.0x (double super effective)
    solar-beam       dmg:33     effectiveness: 0.5x (not very effective)

>>> USE: flare-blitz (double super effective, ~ 451 damage) <<<

## Installation

### Requirements
- Python 3.11+
- g++ compiler (for C++ damage engine)

### Setup

1. Clone the repository
```bash
git clone https://github.com/amlan-sinha07/pokemon_advisor.git
cd pokemon_advisor
```

2. Install Python dependencies
```bash
pip install requests
```

3. Compile C++ damage calculator
```bash
g++ engine/damage_calc.cpp -o engine/damage_calc
```

4. Data is already cached — 1025 Pokemon ready to use.

## Usage

Run as normal user (no admin required):
```bash
python main.py
```

### Menu

1. Pre-match team selector = use before match starts 
2. In-battle move advisor = use during battle
3. Manage my box = save your pokemon's once 
4. Exit

### First time setup
Go to option 3 first — add your 6 Pokemon to your box.
After that, option 1 loads your team automatically.

## How it works

User input

↓

Python (data layer)

1025 Pokemon cached from PokeAPI
Move data fetched on demand + cached locally
Fuzzy name matching (partial names work)

↓

Python (calculation layer)
Type effectiveness (18×18 chart)
Team scoring algorithm

↓

C++ (damage engine)
Standard Pokemon damage formula
Called via subprocess for speed

↓

Recommendation output

## Tech Stack

- **Python 3.11** — core logic, CLI, data pipeline
- **C++** — damage calculation engine
- **PokeAPI** — Pokemon and move data source
- **JSON** — local data caching
- **difflib** — fuzzy name matching
- **subprocess** — Python-C++ bridge

## Data Sources

- [PokeAPI](https://pokeapi.co) — base Pokemon stats and moves
- Type effectiveness chart — hardcoded from official Pokemon Champions data

## Project Structure

pokemon_advisor/

├── data/               ← cached JSON data

├── engine/             ← type calc, damage calc (Python + C++)

├── models/             ← Pokemon, Move classes

├── scraper/            ← PokeAPI data fetcher

├── box_manager.py      ← personal box save/load

├── data_loader.py      ← loads data into objects

├── main.py             ← CLI entry point

└── my_box.json         ← your saved Pokemon box

## Author

Amlan Sinha  
GitHub: [amlan-sinha07](https://github.com/amlan-sinha07)

---
*Built in 32 days as part of a self-directed Python + C++ learning journey.*