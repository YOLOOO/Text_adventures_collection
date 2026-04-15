"""
rooms.py — Room definitions and connections for Hotel Midnight.

Floor layout (third floor, Hotel Midnight):

  [Stairwell/Exit]  ← piano_key required
        |N
  [North Corridor]  ← W:307, E:316
        |S
    [Hallway]       ← W:312, E:Lounge, S:314(your room)
        |S
   [Room 314]       ← start
   [Lounge]         ← south from hallway east; S:Manager's
   [Manager's]      ← E:Linen Closet
   [Linen Closet]
"""

ROOMS = {
    "room_314": {
        "name": "Room 314",
        "exits": {"north": "hallway"},
        "items": ["note", "mirror_shard"],
        "npcs": [],
    },
    "hallway": {
        "name": "Third Floor Hallway",
        "exits": {
            "south": "room_314",
            "west":  "room_312",
            "east":  "lounge",
            "north": "north_corridor",
        },
        "items": [],
        "npcs": [],
    },
    "room_312": {
        "name": "Room 312",
        "exits": {"east": "hallway"},
        "items": [],
        "npcs": ["mr_chen"],
    },
    "lounge": {
        "name": "Third Floor Lounge",
        "exits": {"west": "hallway", "south": "managers_office"},
        "items": ["whiskey_glass", "hotel_stationery"],
        "npcs": [],
    },
    "managers_office": {
        "name": "Manager's Office",
        "exits": {"north": "lounge", "east": "linen_closet"},
        "items": ["master_keycard", "guest_ledger"],
        "npcs": [],
    },
    "linen_closet": {
        "name": "Linen Closet",
        "exits": {"west": "managers_office"},
        "items": ["bandage"],
        "npcs": ["night_maid"],
    },
    "north_corridor": {
        "name": "North Corridor",
        "exits": {
            "south": "hallway",
            "east":  "room_316",
            "north": "stairwell",
        },
        "items": [],
        "npcs": [],
    },
    "room_316": {
        "name": "Room 316",
        "exits": {"west": "north_corridor"},
        "items": ["investigators_badge"],
        "npcs": [],
    },
    "stairwell": {
        "name": "Stairwell — Third Floor",
        "exits": {"south": "north_corridor"},
        "items": [],
        "npcs": [],
    },
}


# ─── Blocked Paths ────────────────────────────────────────────────────────────
#
#   Paths that require a flag before the player can pass.

BLOCKED_PATHS = {
    ("north_corridor", "east"): {
        "flag": "room_316_unlocked",
        "message": (
            "Room 316 is sealed with police tape and a keycard lock. "
            "You need a master keycard."
        ),
    },
    ("north_corridor", "north"): {
        "flag": "piano_key_found",
        "message": (
            "The fire exit is locked with an old mechanism. "
            "Your note said something about a piano key."
        ),
    },
}


# ─── Movement DCs ─────────────────────────────────────────────────────────────
#
#   Rooms that require a skill check to enter.
#   Format: room_id → {"dc": int, "reason": str}

MOVEMENT_DCS = {}
