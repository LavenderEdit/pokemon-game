# 🎮 Pokémon Battle Simulator Roguelike

> Endless roguelike battle simulator inspired by Pokémon FireRed/LeafGreen Link Rooms, developed with Python + Pygame using authentic GBA-style rendering.

---

# 📜 Overview

**Pokémon Battle Simulator Roguelike** is an endless combat-focused Pokémon fangame where the player survives increasingly difficult trainer encounters inside a recreated GBA Link Room environment.

The game combines:

* ⚔️ Endless Pokémon battles
* 🎲 Procedural enemy generation
* 📈 Progressive roguelike scaling
* 🧬 Evolution and leveling systems
* 🎨 Authentic Game Boy Advance visuals
* 🕹️ Grid-based overworld movement
* ✨ Animated battle transitions and effects

Inspired primarily by:

* Pokémon FireRed / LeafGreen
* Battle Tower systems
* Roguelike progression loops
* Endless survival game design

---

# 🧠 Core Gameplay Loop

```text
Spawn in Link Room
      ↓
Explore Overworld
      ↓
Cross Battle Trigger Line
      ↓
Random Trainer Appears
      ↓
Battle Starts
      ↓
Win?
 ├── Yes → Gain EXP, Level Up, Continue
 └── No  → Game Over
```

The difficulty scales infinitely as the player accumulates victories.

---

# 🏗️ Project Architecture

```text
pokemon-game/

├── assets/                    # All visual/audio resources
│
├── data/                      # Game databases and static JSON files
│
├── docs/                      # Technical documentation and diagrams
│
├── saves/                     # Save files and temporary session data
│
├── src/
│   ├── core/                  # Engine-level systems
│   ├── game/                  # Main gameplay logic
│   ├── systems/               # Reusable gameplay systems
│   ├── ui/                    # Menus and interfaces
│   ├── battle/                # Battle engine
│   ├── overworld/             # Map and movement logic
│   ├── pokemon/               # Pokémon data structures
│   ├── managers/              # High-level managers
│   ├── utils/                 # Utility helpers
│   └── main.py                # Entry point
│
├── tests/                     # Unit and integration tests
│
├── requirements.txt
├── .gitignore
├── LICENSE
└── README.md
```

---

# 📁 Detailed Folder Structure

## 🎨 assets/

Contains every game resource.

```text
assets/

├── audio/
│   ├── music/
│   └── sfx/
│
├── fonts/
│   └── pokemon_fire_red.ttf
│
├── backgrounds/
│   ├── overworld/
│   └── battle/
│
├── sprites/
│   ├── player/
│   ├── pokemon/
│   ├── trainers/
│   ├── effects/
│   ├── ui/
│   └── items/
│
├── animations/
│
└── shaders/
```

---

# ⚙️ Engine Design

## 📺 Rendering System

The game renders internally using authentic GBA resolution:

```python
BASE_WIDTH = 240
BASE_HEIGHT = 160
SCALE_FACTOR = 4
```

Final window size:

```python
WINDOW_WIDTH = 960
WINDOW_HEIGHT = 640
```

Advantages:

* Crisp pixel-perfect scaling
* Retro authenticity
* Stable sprite proportions
* Consistent animation timing

---

# 🧱 Core Engine Modules

## 🔧 core/

Low-level engine architecture.

```text
core/

├── constants.py
├── game.py
├── renderer.py
├── state_machine.py
├── sprite_loader.py
├── animation.py
├── camera.py
├── input_handler.py
└── event_bus.py
```

### Responsibilities

| Module           | Responsibility               |
| ---------------- | ---------------------------- |
| renderer.py      | Screen rendering and scaling |
| sprite_loader.py | Automatic sprite slicing     |
| state_machine.py | State transitions            |
| animation.py     | Frame animation handling     |
| input_handler.py | Keyboard/controller input    |
| event_bus.py     | Internal event communication |

---

# 🗺️ Overworld System

## 📍 overworld/

```text
overworld/

├── link_room.py
├── player.py
├── npc.py
├── movement.py
├── collision.py
├── triggers.py
└── pathfinding.py
```

---

## 🚶 Grid Movement

Movement uses fixed tile coordinates:

```python
TILE_SIZE = 16
```

Features:

* Smooth interpolation
* Locked directional movement
* Walking animations
* Collision detection
* Trigger zones

---

# ⚔️ Battle Engine

## 📂 battle/

```text
battle/

├── battle_manager.py
├── battle_state.py
├── damage_calculator.py
├── move_executor.py
├── status_effects.py
├── battle_animator.py
├── ai/
│   ├── enemy_ai.py
│   └── decision_tree.py
└── ui/
```

---

# 🧬 Pokémon System

## 📂 pokemon/

```text
pokemon/

├── pokemon.py
├── species.py
├── evolution.py
├── stats.py
├── experience.py
├── move_pool.py
├── type_chart.py
└── generation.py
```

---

# 📚 Pokémon Database

The game uses internal JSON databases.

Example:

```json
{
  "id": 25,
  "name": "Pikachu",
  "types": ["Electric"],
  "base_stats": {
    "hp": 35,
    "attack": 55,
    "defense": 40,
    "speed": 90,
    "special_attack": 50,
    "special_defense": 50
  }
}
```

---

# 🎲 Roguelike Scaling System

Enemy level formula:

```python
enemy_level = 5 + (wins * 2)
```

Possible future scaling:

```python
enemy_level = floor(5 + wins^1.15)
```

Additional scaling:

* Smarter AI
* Better move pools
* Evolution thresholds
* Held items
* Status strategies

---

# 🎨 Battle Presentation

## Battle Flow

```text
Trainer Appears
      ↓
Slide Animation
      ↓
Pokéball Throw
      ↓
Pokémon Entry
      ↓
Command Selection
      ↓
Attack Animation
      ↓
Damage Interpolation
```

---

# 💥 Animation Systems

Separate animation layers:

| Layer          | Purpose             |
| -------------- | ------------------- |
| attack_effects | Physical impacts    |
| move_effects   | Elemental attacks   |
| stat_effects   | Buff/debuff visuals |
| particles      | Dynamic effects     |
| transitions    | Scene transitions   |

---

# 🎒 Secondary Menus

## Party Menu

Features:

* Pokémon switching
* HP preview
* Status conditions
* Team order

## Bag System

Initial items:

* Potion
* Antidote
* Paralyze Heal

Future expansions:

* Revives
* Held items
* Rare Candies

---

# 💀 Game Over System

The run ends when:

```text
All party Pokémon faint
```

The player receives:

* Total victories
* Highest level reached
* Total damage dealt
* Longest win streak

---

# 🧪 Testing Structure

```text
tests/

├── battle/
├── pokemon/
├── overworld/
├── ui/
└── integration/
```

Recommended testing tools:

* pytest
* coverage
* unittest.mock

---

# 🚀 Future Features

## Planned

* Save system
* Shiny Pokémon
* Procedural trainer names
* Battle modifiers
* Online leaderboard
* Boss trainers
* Dynamic music transitions
* Weather system
* Nuzlocke mode
* Seed-based runs

---

# 🛠️ Tech Stack

| Technology  | Purpose               |
| ----------- | --------------------- |
| Python      | Main language         |
| Pygame      | Rendering/game engine |
| JSON        | Static databases      |
| NumPy       | Future optimization   |
| PyInstaller | Packaging executable  |

---

# 📦 Installation

```bash
git clone https://github.com/LavenderEdit/pokemon-game.git
cd pokemon-game
pip install -r requirements.txt
```

Run:

```bash
python src/main.py
```

---

# 📄 License

MIT License

Nintendo, Game Freak and The Pokémon Company own all Pokémon-related assets and intellectual property.

This project is a non-commercial fan game created for educational purposes only.
