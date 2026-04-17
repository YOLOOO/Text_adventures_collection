"""
items.py — Item definitions for The Honda Years.

Items are tangible objects that carry emotional weight.
No puzzles — each one gives context that affects the ending.
"""

ITEMS = {
    "vending_coffee": {
        "name": "Vending Machine Coffee",
        "description": (
            "Bad coffee in a styrofoam cup. "
            "It tastes like it was brewed in 2003. "
            "Sarah would normally say something about single-use cups. "
            "She doesn't."
        ),
        "aliases": ["coffee", "cup", "vending", "bad coffee"],
    },
    "therapy_notes": {
        "name": "Sarah's Therapy Journal",
        "description": (
            "A small spiral notebook. Blue cover. "
            "Sarah's handwriting — deliberate, like she was "
            "trying to make it legible to herself later. "
            "You weren't supposed to see this. "
            "Or maybe she left it out on purpose."
        ),
        "aliases": [
            "journal", "notebook", "notes",
            "therapy notes", "therapy journal",
            "sarah journal", "blue notebook",
        ],
    },
    "gas_receipt": {
        "name": "Gas Station Receipt",
        "description": (
            "Shell station, Casper, WY. February 14. "
            "Regular unleaded. $48.12. "
            "The date is the thing. "
            "You were supposed to be at a conference in Denver."
        ),
        "aliases": [
            "receipt", "gas receipt", "slip",
            "paper", "shell receipt", "february",
        ],
    },
    "emma_drawing": {
        "name": "Emma's Drawing",
        "description": (
            "Four stick figures in a car. "
            "The two in front face away from each other. "
            "The two in back are waving at something off the page. "
            "Underneath, in careful seven-year-old letters: "
            "'We are going on an adventure.'"
        ),
        "aliases": [
            "drawing", "picture", "sketch",
            "emma drawing", "stick figures",
        ],
    },
}


def item_name(item_id):
    return ITEMS.get(item_id, {}).get(
        "name", item_id.replace("_", " ").title()
    )
