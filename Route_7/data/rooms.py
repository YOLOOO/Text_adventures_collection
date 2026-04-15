"""
rooms.py — Room definitions for Route 7.

Bus layout (front of bus = north):

  [Driver's Cab]    ← maintenance_key required
       |N/S
  [Front Seats]     ← Rosa is here; lighter + folded_map
       |N/S
  [Middle Aisle]    ← D: Luggage Hatch
       |N/S
  [Rear Seats]      ← start; newspaper; emergency door (needs lever)
       |D
  [Luggage Hatch]   ← dark; emergency_lever + maintenance_key (need lighter)
"""

ROOMS = {
    "rear_seats": {
        "name": "Rear of Bus",
        "exits": {"north": "middle_aisle"},
        "items": ["newspaper_1987"],
        "npcs": [],
    },
    "middle_aisle": {
        "name": "Middle Aisle",
        "exits": {
            "south": "rear_seats",
            "north": "front_seats",
            "down":  "luggage_hatch",
        },
        "items": [],
        "npcs": [],
    },
    "front_seats": {
        "name": "Front Seats",
        "exits": {
            "south": "middle_aisle",
            "north": "drivers_cab",
        },
        "items": ["lighter", "folded_map"],
        "npcs": ["rosa"],
    },
    "luggage_hatch": {
        "name": "Luggage Hatch",
        "exits": {"up": "middle_aisle"},
        "items": ["emergency_lever", "maintenance_key"],
        "npcs": [],
    },
    "drivers_cab": {
        "name": "Driver's Cab",
        "exits": {"south": "front_seats"},
        "items": ["drivers_log"],
        "npcs": ["driver"],
    },
}


# ─── Blocked Paths ────────────────────────────────────────────────────────────

BLOCKED_PATHS = {
    ("front_seats", "north"): {
        "flag":    "cab_unlocked",
        "message": (
            "A locked steel partition divides the cab from the passenger area. "
            "The keyhole is industrial — you need a maintenance key."
        ),
    },
}


# ─── Movement DCs ─────────────────────────────────────────────────────────────

MOVEMENT_DCS = {
    "luggage_hatch": {
        "dc":     6,
        "reason": "Squeezing through the floor access hatch",
    },
}
