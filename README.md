# Pokemon Champions Battle Advisor

A Python command-line tool for pre-match team recommendations and in-battle move analysis. The project combines local JSON data, PokéAPI lookups, type-effectiveness calculations, and a C++ damage-calculation executable.

> **Project status:** Personal learning project / prototype. The application provides estimates and decision support; it is not connected to the game and does not read live battle state automatically.

## Features

### Pre-match team selector

- Loads up to six Pokémon from your saved local box.
- Accepts Pokémon names with fuzzy matching.
- Evaluates your Pokémon against a manually entered opposing team.
- Ranks your Pokémon using a heuristic based on type matchups and a speed bonus.
- Recommends up to four Pokémon from your team.

### In-battle move advisor

- Accepts your active Pokémon and the opponent's active Pokémon.
- Accepts their current HP values as manual input.
- Retrieves move details from local cache files or PokéAPI.
- Estimates damage for damaging moves using a Python wrapper and a C++ executable when available.
- Shows type effectiveness, STAB, a speed comparison, and a highest-estimated-damage recommendation.

### Box manager

- Saves a personal list of up to six Pokémon in `my_box.json`.
- Supports viewing, adding, and removing Pokémon.
- Keeps the personal box out of Git by ignoring `my_box.json`.

## Important limitations

- This is a command-line assistant. It does not connect to Pokémon Champions, inspect the game screen, or obtain live battle state. Pokémon, HP, and moves are entered by the user.
- Pre-match scoring is a project-specific heuristic based on type interactions and speed. It is not a full team simulator and does not evaluate every move, ability, item, or battle condition.
- The damage calculation is a simplified level-50 estimate. It is not a complete implementation of every Pokémon Champions battle mechanic. Accuracy, move priority, critical hits, random damage variation, abilities, items, weather, and other modifiers may not be represented.
- Pokémon and move records are retrieved from PokéAPI. A record being available from PokéAPI does not establish that the Pokémon or move is available in Pokémon Champions.
- The type chart is loaded from `data/type_chart.json`. Verify that this file contains the correct chart for the game and ruleset you intend to model; do not treat the output as authoritative until that data has been validated.
- The C++ backend is currently configured as `engine/damage_calc.exe`, so the instructions below target Windows.

## Requirements

- Windows (the current Python wrapper expects `damage_calc.exe`).
- Python 3.11 or newer.
- A C++ compiler that supports C++17, such as MinGW-w64 `g++`.
- Runtime Python dependency: `requests`.
- Development/test dependency: `pytest`.

## Project setup (Windows PowerShell)

### 1. Clone the repository

```powershell
git clone https://github.com/amlan-sinha07/pokemon_advisor.git
cd pokemon_advisor
```

### 2. Create and activate a virtual environment

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

To run the test suite, also install the development dependencies:

```powershell
python -m pip install -r requirements-dev.txt
```

### 4. Prepare local data

The application expects these files in the project's `data/` directory:

```text
data/
├── pokemon_all.json
├── type_chart.json
└── moves_<pokemon>.json   # optional per-Pokémon move caches
```

`pokemon_all.json` contains Pokémon records and their base stats/move names. `type_chart.json` supplies the type-effectiveness matrix used by the type calculator. Move-cache files are created as move data is fetched.

If the Pokémon database is not present, it can be generated through the scraper's `fetch_and_save()` function. For example, to fetch a small test database containing Bulbasaur, use:

```powershell
python -c "from scraper.fetch_data import fetch_and_save; fetch_and_save(['1'], 'data/pokemon_all.json')"
```

To fetch a larger ID range, pass the required IDs to the same function. The scraper applies a delay between requests, so bulk data collection can take a while. Make sure `data/type_chart.json` is also present; the project does not generate that chart automatically.

### 5. Compile the C++ damage engine

Run this from the project root:

```powershell
g++ -std=c++17 -Wall -Wextra -Wpedantic engine/damage_calc.cpp -o engine/damage_calc.exe
```

The output filename matters: the Python wrapper looks for `engine/damage_calc.exe`. The executable is generated locally and is intentionally excluded from Git.

You can smoke-test the executable with:

```powershell
"50 100 100 1.0 1.0" | .\engine\damage_calc.exe
```

Expected output for this simplified formula and input is:

```text
24
```

### 6. Run the application

```powershell
python main.py
```

## Using the CLI

The main menu provides four options:

1. **Pre-match team selector** — uses your saved box when available, then asks for the opponent's team. If no saved box exists, it asks you to enter your own team.
2. **In-battle move advisor** — asks for both active Pokémon, current HP, and four move names, then ranks the entered moves.
3. **Manage my box** — view, add, or remove Pokémon in your local box.
4. **Exit** — leave the application.

For first-time use, open **Manage my box** and add your Pokémon before using the pre-match selector.

## Running tests

Run the complete automated test suite from the project root:

```powershell
python -m pytest -q
```

For verbose output:

```powershell
python -m pytest -v
```

The tests cover the type calculator, box persistence, data loading, Pokémon and Move models, pre-match and battle advisors, the Python/C++ damage wrapper, and scraper behavior. Tests should use temporary files and mocked network/subprocess calls rather than requiring live API requests.

## Project structure

```text
pokemon_advisor/
├── data/                       # Local Pokémon, type-chart, and move JSON data
├── docs/
│   └── refactoring-baseline.md # Initial state and refactoring outcomes
├── engine/
│   ├── battle_advisor.py       # Move evaluation and recommendation
│   ├── pre_match_advisor.py    # Team matchup scoring and selection
│   ├── type_calc.py            # Type-effectiveness calculations
│   ├── damage_calc.py          # Python wrapper and fallback calculation
│   └── damage_calc.cpp         # C++ damage calculation executable source
├── models/
│   ├── pokemon.py              # Pokémon model and HP/move state
│   └── move.py                 # Move model
├── scraper/
│   └── fetch_data.py           # PokéAPI retrieval and local data generation
├── tests/                      # pytest regression tests
├── box_manager.py              # Personal box persistence and CLI operations
├── data_loader.py              # JSON loading, fuzzy search, model construction
├── main.py                     # CLI entry point and application flow
├── requirements.txt            # Runtime Python dependencies
└── requirements-dev.txt        # Test/development dependencies
```

## Data sources

- [PokéAPI](https://pokeapi.co/) — Pokémon metadata, base stats, and move information.
- `data/type_chart.json` — local type-effectiveness data used by the application. Its source and compatibility with the target game's ruleset should be documented and verified separately.

## Git hygiene

The following files are local/generated and should not normally be committed:

- `engine/damage_calc.exe` — compiled binary; compile it locally using the command above.
- `my_box.json` — personal saved Pokémon box.
- Python cache directories, pytest cache, and virtual environments.

## Author

Amlan Sinha  
GitHub: [amlan-sinha07](https://github.com/amlan-sinha07)
