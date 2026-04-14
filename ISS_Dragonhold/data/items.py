"""
items.py — Item definitions.

To add a new item:
  1. Add an entry to ITEMS with a unique key.
  2. Place it in a room's "items" list (see rooms.py).
  3. If it has special USE behavior, add a handler in item_uses.py.

Fields:
  name        — Display name shown to the player.
  description — Flavor text shown on LOOK/EXAMINE.
  portable    — Can the player pick it up? (default True)
"""

ITEMS = {
    "usb_wand": {
        "name": "USB Wand (dead battery)",
        "description": (
            "A standard-issue wizard wand with a USB-C port. "
            "Battery: DEAD. LED blinks a sad red."
        ),
    },
    "goblin_repellent": {
        "name": "Goblin Repellent (Expired)",
        "aliases": ["can", "spray", "spray can"],
        "description": (
            "A spray can labeled 'GOBLIN-B-GON'. "
            "Expired 300 years ago. Smells like burnt toast and regret."
        ),
    },
    "enchanted_duct_tape": {
        "name": "Enchanted Duct Tape",
        "aliases": ["tape", "duct tape"],
        "description": (
            "Silver duct tape covered in glowing runes. "
            "The label says 'Fixes anything. ANYTHING.' It's not lying."
        ),
    },
    "space_cheese": {
        "name": "Wedge of Space Cheese",
        "aliases": ["wedge", "cheese"],
        "description": (
            "A surprisingly appetizing chunk of cheese from the planet "
            "you're about to crash into. It hums softly."
        ),
    },
    "plasma_sword": {
        "name": "Plasma Sword of Adequate Quality",
        "aliases": ["sword", "plasma sword"],
        "description": (
            "A glowing blade. The hilt reads: "
            "'3.5 / 5 stars — Adequate for most combat situations. — Wizard Weekly'"
        ),
    },
    "hyperdrive_crystal": {
        "name": "Hyperdrive Crystal",
        "description": (
            "A massive enchanted crystal. Thrums with enough energy to power "
            "a jump drive... or a really impressive nightlight."
        ),
    },
    "charging_crystal": {
        "name": "Arcane Charging Crystal",
        "description": (
            "A pulsing blue crystal that radiates magical energy. "
            "Could probably charge something wand-shaped."
        ),
    },
    "ghost_cookbook": {
        "name": "Ghost Chef's Cookbook",
        "description": (
            "Titled 'Cooking for the Deceased and the Mildly Hungry'. "
            "The recipes are translucent."
        ),
    },
    "goblin_crown": {
        "name": "The Goblin Crown",
        "description": (
            "A janky crown made of circuit boards and gemstones. "
            "Wearing it makes you smell like a goblin. Allegedly an honor."
        ),
    },
}


def item_name(item_id):
    """Get display name for an item, with fallback."""
    if item_id in ITEMS:
        return ITEMS[item_id]["name"]
    return item_id
