"""
rooms.py — Room definitions.

To add a new room:
  1. Add an entry to ROOMS with a unique key.
  2. Connect it by adding exits to/from neighboring rooms.
  3. Optionally add a describe() function to ROOM_DESCRIPTIONS.
  4. Optionally set a movement DC in MOVEMENT_DCS.

Fields:
  name   — Display name.
  items  — List of item IDs that start in this room.
  exits  — Dict mapping direction → room_id.
  npcs   — List of NPC IDs present here (see npcs/).
"""

ROOMS = {
    "intern_quarters": {
        "name": "Intern Quarters",
        "items": ["usb_wand"],
        "exits": {"north": "corridor"},
        "npcs": [],
    },
    "corridor": {
        "name": "Corridor of Questionable Decisions",
        "items": ["goblin_repellent"],
        "exits": {
            "north": "bridge",
            "east": "cafeteria",
            "west": "engineering",
            "south": "intern_quarters",
        },
        "npcs": [],
    },
    "bridge": {
        "name": "The Bridge (But Also a Throne Room)",
        "items": [],
        "exits": {"south": "corridor", "east": "airlock"},
        "npcs": ["dracos"],
    },
    "cafeteria": {
        "name": "Cafeteria of the Damned",
        "items": ["space_cheese"],
        "exits": {"west": "corridor", "south": "cargo_hold"},
        "npcs": ["ghost_chef"],
    },
    "engineering": {
        "name": "Engineering Bay / Wizard Workshop",
        "items": ["enchanted_duct_tape"],
        "exits": {"east": "corridor", "north": "armory"},
        "npcs": ["turret"],
    },
    "armory": {
        "name": "Armory of Mild Convenience",
        "items": ["plasma_sword"],
        "exits": {"south": "engineering"},
        "npcs": [],
    },
    "airlock": {
        "name": "Airlock of Mild Peril",
        "items": [],
        "exits": {"west": "bridge", "north": "crystal_chamber"},
        "npcs": [],
    },
    "cargo_hold": {
        "name": "Cargo Hold / Goblin Nest",
        "items": [],
        "exits": {"north": "cafeteria"},
        "npcs": ["goblin_king"],
    },
    "crystal_chamber": {
        "name": "Crystal Chamber",
        "items": [],
        "exits": {"south": "airlock", "north": "escape_pods"},
        "npcs": [],
    },
    "escape_pods": {
        "name": "Escape Pod Bay",
        "items": [],
        "exits": {"south": "crystal_chamber"},
        "npcs": [],
    },
}


# Movement DCs — if a room isn't listed here, movement is automatic (DC 0).
# Keys are DESTINATION room IDs.
MOVEMENT_DCS = {
    "crystal_chamber": {"dc": 10, "reason": "Climbing through a precarious airlock hatch"},
    "cargo_hold":      {"dc": 8,  "reason": "Sneaking through the hatch quietly"},
    "escape_pods":     {"dc": 7,  "reason": "Squeezing through a narrow passage"},
}


# Blocked paths — conditions that must be true before movement is allowed.
# Format: (from_room, direction) → (required_flag, block_message)
BLOCKED_PATHS = {
    ("engineering", "north"): {
        "flag": "turret_disabled",
        "message": "The spell-turret blocks the armory door! Deal with it first.",
    },
    ("cafeteria", "south"): {
        "flag": "cafeteria_cleared",
        "message": "Ghost Chef Pierre floats in front of the hatch! Deal with him first.",
    },
}
