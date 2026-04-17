"""
rooms.py — Locations for The Honda Years.

Road layout (west = progress toward Portland):

  [Front Seat] ↔ back ↔ [Back Seat]
  [Front Seat] → stop → [Rest Stop — Iowa]
  [Rest Stop] → west → [Motel — Kearney, NE]
  [Motel] → west → [Roadside — Wyoming]
  [Roadside] → west → [Final Miles — Oregon]
  [Final Miles] → ARRIVE → Portland (ending)

Progress gates (BLOCKED_PATHS) require completing
each stop's conversation beat before moving on.
"""

ROOMS = {
    "front_seat": {
        "name": "Front Seat — The Honda",
        "exits": {
            "back":  "back_seat",
            "west":  "rest_stop",
            "stop":  "rest_stop",
        },
        "items": [],
        "npcs": ["sarah", "radio"],
    },
    "back_seat": {
        "name": "Back Seat",
        "exits": {
            "front": "front_seat",
            "south": "front_seat",
        },
        "items": [],
        "npcs": ["drew", "emma"],
    },
    "rest_stop": {
        "name": "Rest Stop — Iowa",
        "exits": {
            "east":  "front_seat",
            "west":  "motel_kearney",
        },
        "items": ["vending_coffee"],
        "npcs": ["sarah", "drew", "emma", "radio"],
    },
    "motel_kearney": {
        "name": "Motel — Kearney, NE",
        "exits": {
            "east":  "rest_stop",
            "west":  "breakdown",
        },
        "items": ["therapy_notes"],
        "npcs": ["sarah", "radio"],
    },
    "breakdown": {
        "name": "Roadside — Wyoming",
        "exits": {
            "east":  "motel_kearney",
            "west":  "final_miles",
        },
        "items": ["gas_receipt"],
        "npcs": ["sarah", "drew", "emma", "radio"],
    },
    "final_miles": {
        "name": "Final Miles — Oregon",
        "exits": {
            "east": "breakdown",
        },
        "items": [],
        "npcs": ["sarah", "radio"],
    },
}


# ─── Blocked Paths ────────────────────────────────────────────────────────────

BLOCKED_PATHS = {
    ("rest_stop", "west"): {
        "flag":    "iowa_stop_done",
        "message": (
            "You haven't finished here. "
            "Talk to Sarah before you get back in the car."
        ),
    },
    ("motel_kearney", "west"): {
        "flag":    "motel_night_done",
        "message": (
            "It's too late to drive. "
            "You need to get through tonight first. Talk to Sarah."
        ),
    },
    ("breakdown", "west"): {
        "flag":    "breakdown_done",
        "message": (
            "The Honda isn't going anywhere. "
            "You're stuck here until you work through it."
        ),
    },
}


# ─── Movement DCs ─────────────────────────────────────────────────────────────

MOVEMENT_DCS = {}  # No dice checks in this game
