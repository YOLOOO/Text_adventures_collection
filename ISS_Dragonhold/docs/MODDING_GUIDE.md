# ISS Dragonhold — Modding & Architecture Guide

## Project Structure

```
station_quest/
├── main.py                    ← Entry point. Intro + game loop.
│
├── engine/                    ← Core systems (rarely need editing)
│   ├── display.py             ← Colors, formatting, print helpers
│   ├── dice.py                ← Physical dice input system
│   ├── game.py                ← Player state (HP, inventory, flags)
│   └── commands.py            ← Command parser + routing
│
├── data/                      ← Game content (edit freely!)
│   ├── rooms.py               ← Room map, exits, items, NPCs
│   ├── room_descriptions.py   ← What the player sees in each room
│   ├── items.py               ← Item definitions + display names
│   ├── item_uses.py           ← What happens when you USE items
│   └── endings.py             ← All ending sequences
│
├── npcs/                      ← Each NPC is its own file
│   ├── base.py                ← Base NPC class (the framework)
│   ├── __init__.py            ← NPC registry (wiring)
│   ├── dracos.py              ← DRACOS the AI dragon
│   ├── ghost_chef.py          ← Ghost Chef Pierre
│   ├── goblin_king.py         ← Goblin King Zurt
│   └── turret.py              ← Rogue Spell-Turret
│
└── docs/
    └── MODDING_GUIDE.md       ← You are here
```

---

## How Everything Connects

Here's the flow when a player types a command:

```
Player types "talk ghost"
        │
        ▼
  main.py game loop
        │
        ▼
  commands.py  process_command()
        │
        ├── Parses "talk" + "ghost"
        ├── Calls find_npc_by_alias("cafeteria", "ghost")
        │       │
        │       ▼
        │   npcs/__init__.py  NPC_REGISTRY
        │       │
        │       ▼
        │   Finds GhostChef (aliases: ["ghost", "chef", "pierre"])
        │
        ▼
  ghost_chef.py  .talk(game)
        │
        ├── Calls ask_d20() from dice.py
        ├── Reads DIALOG dict for response text
        ├── Modifies game.flags via game.set_flag()
        └── Prints output via display.py helpers
```

### The Key Registries

There are **4 registries** that wire everything together:

| Registry | File | Purpose |
|----------|------|---------|
| `NPC_REGISTRY` | `npcs/__init__.py` | Maps NPC IDs → NPC instances |
| `ROOMS` | `data/rooms.py` | Maps room IDs → room data (includes NPC IDs) |
| `USE_HANDLERS` | `data/item_uses.py` | Maps item IDs → use functions |
| `DESCRIBERS` | `data/room_descriptions.py` | Maps room IDs → describe functions |

---

## How To: Add a New Room

### 1. Define the room in `data/rooms.py`

```python
ROOMS["reactor_core"] = {
    "name": "Reactor Core",
    "items": ["plutonium_wand"],       # Item IDs (define in items.py)
    "exits": {"south": "engineering"},  # Connect to existing rooms
    "npcs": ["reactor_golem"],          # NPC IDs (define in npcs/)
}

# Don't forget to add an exit FROM an existing room:
ROOMS["engineering"]["exits"]["north"] = "reactor_core"
```

### 2. Optionally add a movement DC in `data/rooms.py`

```python
MOVEMENT_DCS["reactor_core"] = {
    "dc": 12,
    "reason": "Navigating through radiation without melting",
}
```

### 3. Add a description in `data/room_descriptions.py`

```python
def describe_reactor_core(game, first_visit):
    print(wrap("A humming chamber of pure energy..."))
    if first_visit:
        get_npc("dracos").say("reactor_intro")  # Add dialog to dracos.py
    dim("Exits: SOUTH (Engineering).")

# Register it:
DESCRIBERS["reactor_core"] = describe_reactor_core
```

---

## How To: Add a New Item

### 1. Define it in `data/items.py`

```python
ITEMS["plutonium_wand"] = {
    "name": "Plutonium Wand (Glowing)",
    "description": "A wand that glows green. Probably fine.",
}
```

### 2. Place it in a room (`data/rooms.py`)

```python
ROOMS["reactor_core"]["items"] = ["plutonium_wand"]
```

### 3. Add USE behavior in `data/item_uses.py`

```python
def use_plutonium_wand(game):
    info("You wave the glowing wand. Your teeth tingle.")
    roll = ask_d20("Radiation resistance check")
    if roll >= 12:
        success("You feel... powerful? And slightly nauseous.")
    else:
        game.take_damage(5)
    return True

# Register it:
USE_HANDLERS["plutonium_wand"] = use_plutonium_wand
```

### 4. Optionally set a pickup DC in `engine/commands.py`

In the `_take_dc()` function:

```python
DCS = {
    "plasma_sword": (10, "Reaching through cracked glass"),
    "plutonium_wand": (12, "Grabbing radioactive material bare-handed"),
}
```

---

## How To: Add a New NPC

This is the most involved addition, but the framework makes it clean.

### 1. Create `npcs/my_npc.py`

```python
"""my_npc.py — Description of this NPC."""

from npcs.base import NPC
from engine.display import info, dim, success, danger, alert, hr, C
from engine.dice import ask_d20, ask_4d6


class ReactorGolem(NPC):
    id = "reactor_golem"           # Must match rooms.py "npcs" list
    name = "Reactor Golem"         # Display name
    aliases = ["golem", "reactor"] # Words player can type to target it

    # ─── Dialog ────────────────────────────────────────────────────
    DIALOG = {
        "talk_success": "The golem hums. 'FUEL... DEPLETED... NEED... CRYSTAL...'",
        "talk_fail": "The golem swats at you like a bug.",
        "defeat": "The golem crumbles into glowing rubble!",
    }

    # ─── Stats ─────────────────────────────────────────────────────
    HP = 18
    ATTACK = 5

    # ─── Framework Methods ─────────────────────────────────────────

    def is_active(self, game):
        return not game.check_flag("golem_defeated")

    def describe(self, game, first_visit):
        if self.is_active(game):
            danger("A REACTOR GOLEM blocks the path, glowing with unstable energy!")

    def look(self, game):
        if self.is_active(game):
            dim("A golem made of reactor parts. TALK, FIGHT, or USE items.")
        else:
            dim("A pile of glowing rubble.")
        return True

    def talk(self, game):
        info("You address the humming golem...")
        roll = ask_d20("Communication — understanding golem language")
        if roll >= 14:
            print(f"  {self.DIALOG['talk_success']}")
            alert("HINT: The golem needs a crystal to calm down!")
        else:
            print(f"  {self.DIALOG['talk_fail']}")
            game.take_damage(3)
        return True

    def use_item(self, game, item_id):
        # Example: feeding it a crystal
        if item_id == "charging_crystal":
            success("The golem absorbs the crystal and powers down peacefully!")
            game.set_flag("golem_defeated")
            game.remove_item("charging_crystal")
            return True
        return False  # Didn't handle this item

    def fight(self, game):
        # Implement combat (see ghost_chef.py or turret.py for patterns)
        info("⚔️  COMBAT: Reactor Golem!")
        # ... combat loop ...
        return True
```

### 2. Register in `npcs/__init__.py`

```python
from npcs.my_npc import ReactorGolem

NPC_REGISTRY["reactor_golem"] = ReactorGolem()
```

### 3. Place in a room (`data/rooms.py`)

```python
ROOMS["reactor_core"]["npcs"] = ["reactor_golem"]
```

**That's it!** The engine automatically:
- Calls `describe()` when the player enters the room
- Routes `TALK golem` to `talk()`
- Routes `FIGHT golem` to `fight()`
- Checks `use_item()` before generic item handlers
- Checks `is_active()` to skip defeated NPCs

---

## How To: Add DRACOS Dialog

DRACOS speaks from anywhere. His dialog is a bank of categorized lines.

### In `npcs/dracos.py`:

```python
DIALOG = {
    # ... existing entries ...

    # Add a new category:
    "reactor_intro": [
        "Ah, the reactor. Don't touch anything. I mean it.",
        "The last intern who came here is now part of the wall.",
    ],
}
```

### Use it from any file:

```python
from npcs import get_npc
get_npc("dracos").say("reactor_intro")        # Says line 0
get_npc("dracos").say("reactor_intro", 1)     # Says line 1
```

---

## How To: Add a New Ending

### In `data/endings.py`:

```python
def ending_self_destruct(game):
    """Triggered by a hypothetical SELF-DESTRUCT command."""
    dragon_says("You pressed the self-destruct? REALLY?!")
    roll = ask_d20("Dramatic countdown escape")
    game.game_over = True
    game.won = (roll >= 10)
    game.ending = "self_destruct"
    # ... print ending text ...
```

### Wire it in `engine/commands.py`:

```python
from data.endings import ending_self_destruct

# In process_command():
elif cmd == "selfdestruct":
    ending_self_destruct(game)
```

---

## How To: Add a New Game Flag

Flags are the glue between systems. They track story progress.

### 1. Initialize in `engine/game.py`

```python
self.flags = {
    # ... existing flags ...
    "golem_defeated": False,
}
```

### 2. Set it anywhere

```python
game.set_flag("golem_defeated")        # Sets to True
game.set_flag("golem_defeated", False) # Sets to False
```

### 3. Check it anywhere

```python
if game.check_flag("golem_defeated"):
    # ...
```

### 4. Optionally use it to block a path (`data/rooms.py`)

```python
BLOCKED_PATHS[("reactor_core", "north")] = {
    "flag": "golem_defeated",
    "message": "The golem blocks the way!",
}
```

---

## Architecture Principles

1. **NPCs own their behavior.** Talk, fight, item reactions — all in the NPC file.
2. **Data is separate from logic.** Rooms, items, and dialog are pure data. Engine code reads them.
3. **Registries are the wiring.** If something isn't registered, it doesn't exist to the engine.
4. **Flags are the glue.** Any system can set/check flags. This keeps systems decoupled.
5. **DRACOS is global.** His dialog bank is accessed from anywhere via `get_npc("dracos").say()`.

---

## Quick Reference: Adding Content

| I want to add... | Files to edit |
|-------------------|---------------|
| New room | `rooms.py` + `room_descriptions.py` |
| New item | `items.py` + `rooms.py` + `item_uses.py` |
| New NPC | `npcs/new_file.py` + `npcs/__init__.py` + `rooms.py` |
| New dialog | NPC's own file (DIALOG dict) or `dracos.py` |
| New ending | `endings.py` + `commands.py` |
| New command | `commands.py` (process_command) |
| New game flag | `game.py` (init) + wherever you set/check it |
| Blocked path | `rooms.py` (BLOCKED_PATHS) |
| Movement check | `rooms.py` (MOVEMENT_DCS) |
| Pickup check | `commands.py` (_take_dc) |
