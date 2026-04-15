"""
items.py — Item definitions for Hotel Midnight.
"""

ITEMS = {
    "note": {
        "name": "Handwritten Note",
        "description": (
            "In your own handwriting: 'Don't trust the concierge. "
            "The key is in the piano. Get out before 4 AM!'"
        ),
        "aliases": ["note", "handwriting", "message"],
    },
    "mirror_shard": {
        "name": "Mirror Shard",
        "description": (
            "A jagged piece of mirror from the smashed bathroom mirror. "
            "Sharp. Could pry things open or cut something."
        ),
        "aliases": ["shard", "mirror", "glass"],
    },
    "piano_key": {
        "name": "Antique Piano Key",
        "description": (
            "A long brass key, tarnished with age. "
            "An old-fashioned fire exit key — heavy, solid."
        ),
        "aliases": ["piano_key", "key", "brass key", "antique"],
    },
    "whiskey_glass": {
        "name": "Whiskey Glass",
        "description": (
            "A crystal whiskey glass. Someone else's fingerprints are all over it. "
            "The kind of print that doesn't belong to any guest."
        ),
        "aliases": ["glass", "whiskey", "crystal", "drink"],
    },
    "hotel_stationery": {
        "name": "Hotel Stationery",
        "description": "Embossed notepad. 'Hotel Midnight — Where Every Night Is Memorable.'",
        "aliases": ["stationery", "notepad", "paper"],
    },
    "master_keycard": {
        "name": "Master Keycard",
        "description": (
            "A black keycard marked 'MASTER — STAFF ONLY'. "
            "Opens every guest room and restricted area on the floor."
        ),
        "aliases": ["keycard", "card", "master", "master card"],
    },
    "guest_ledger": {
        "name": "Guest Registration Ledger",
        "description": (
            "The paper check-in log. Room 316 was booked under a false name — "
            "but the handwriting in the notes column matches the concierge's."
        ),
        "aliases": ["ledger", "register", "log", "book"],
    },
    "bandage": {
        "name": "First Aid Bandage",
        "description": "A sterile bandage from the linen closet first-aid kit.",
        "aliases": ["bandage", "first aid", "aid", "wrap"],
    },
    "investigators_badge": {
        "name": "Investigator's Badge",
        "description": (
            "Your PI license and badge. Someone took it from you — "
            "and left it here. They wanted to identify you."
        ),
        "aliases": ["badge", "license", "id", "pi badge"],
    },
}


def item_name(item_id):
    """Return the display name for an item ID."""
    return ITEMS.get(item_id, {}).get("name", item_id.replace("_", " ").title())
