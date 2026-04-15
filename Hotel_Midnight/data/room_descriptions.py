"""
room_descriptions.py — Room description functions for Hotel Midnight.
"""

from engine.display import wrap, room_print, virgil_says, alert, danger, success, dim
from data.rooms import ROOMS
from data.items import item_name
from npcs import get_npc, get_room_npcs


def _show_ground_items(game):
    from engine.display import C
    items = ROOMS[game.room]["items"]
    if items:
        print(f"\n  {C.YELLOW}Items here: "
              f"{', '.join(item_name(i) for i in items)}{C.RESET}")


# ─── Room Describers ──────────────────────────────────────────────────────────

def describe_room_314(game, first_visit):
    print(wrap(
        "Rain-soaked carpet. Smashed bathroom mirror. Blood on your "
        "hands — dried, not fresh. The door is locked from outside. "
        "Your phone is dead. A note on the nightstand."
    ))
    if "note" in ROOMS[game.room]["items"]:
        alert("The note is in your handwriting.")
    if first_visit:
        get_npc("virgil").say("greeting")
    dim("Exits: NORTH to the hallway.")


def describe_hallway(game, first_visit):
    print(wrap(
        "A long carpeted corridor. Emergency lighting only — "
        "every third bulb is out. Rain hammers the window at the far end."
    ))
    if first_visit:
        get_npc("virgil").say("hallway_intro")
    dim("Exits: SOUTH (314), WEST (312), EAST (Lounge), NORTH (corridor).")


def describe_room_312(game, first_visit):
    if game.check_flag("chen_helped"):
        print(wrap(
            "Mr. Chen sits by the window with his tea, watching the rain. "
            "He gives you a small nod."
        ))
    else:
        print(wrap(
            "The door is ajar. A slight man in a dressing gown sits "
            "bolt upright in the armchair, reading. He heard you coming."
        ))
    dim("Exits: EAST to the hallway.")


def describe_lounge(game, first_visit):
    print(wrap(
        "A sitting area with leather chairs and a grand piano "
        "against the far wall. A drinks trolley. Framed portraits "
        "of the hotel's founders watch you with painted suspicion."
    ))
    if "whiskey_glass" in ROOMS[game.room]["items"]:
        dim("A crystal glass sits on the piano stool. Fingerprints everywhere.")
    if first_visit:
        get_npc("virgil").say("lounge_intro")
    if not game.check_flag("piano_key_found"):
        dim("The grand piano dominates the far wall. Look PIANO.")
    dim("Exits: WEST (hallway), SOUTH (Manager's Office).")


def describe_managers_office(game, first_visit):
    print(wrap(
        "Papers everywhere. The manager left in a hurry — coat still "
        "on the hook, cold coffee on the desk. Filing cabinet stands open."
    ))
    if "master_keycard" in ROOMS[game.room]["items"]:
        dim("A black keycard sits on the desk blotter.")
    if "guest_ledger" in ROOMS[game.room]["items"]:
        dim("A handwritten guest ledger is splayed open.")
    if first_visit:
        get_npc("virgil").say("office_intro")
    dim("Exits: NORTH (Lounge), EAST (Linen Closet).")


def describe_linen_closet(game, first_visit):
    if not game.check_flag("maid_found"):
        print(wrap(
            "Shelves of folded towels and sheets. Something moves "
            "behind the bottom shelf. Someone is hiding in here."
        ))
    else:
        print(wrap(
            "Shelves of towels and a small folding chair where "
            "Rosa sat until a few minutes ago."
        ))
    dim("Exits: WEST (Manager's Office).")


def describe_north_corridor(game, first_visit):
    print(wrap(
        "The north end of the floor. Darker up here. "
        "Police tape stretches across the door to Room 316 — "
        "or what's left of it after someone cut through."
    ))
    if not game.check_flag("room_316_unlocked"):
        dim("Room 316 is sealed east. You need a keycard or something sharp.")
    if not game.check_flag("piano_key_found"):
        dim("The fire exit north is locked with an old brass mechanism.")
    else:
        alert("The fire exit is unlocked. LEAVE to get out.")
    if first_visit:
        get_npc("virgil").say("north_corridor_intro")
    dim("Exits: SOUTH (hallway), EAST (316, locked), NORTH (exit, locked).")


def describe_room_316(game, first_visit):
    print(wrap(
        "Someone left in a hurry. Overturned lamp, scratches on "
        "the doorframe. A locked metal box sits on the stripped bed. "
        "This room reeks of cigarette smoke and cheap cologne."
    ))
    if not game.check_flag("box_opened"):
        dim("A locked box on the bed. USE MIRROR SHARD to pry it.")
    if first_visit:
        get_npc("virgil").say("room_316_intro")
    dim("Exits: WEST (north corridor).")


def describe_stairwell(game, first_visit):
    print(wrap(
        "Concrete stairs. Rain noise amplified by the shaft. "
        "The street is two floors down. Freedom is right there."
    ))
    if first_visit:
        get_npc("virgil").say("stairwell_intro")
    alert("Type LEAVE to get out of the hotel.")
    dim("Exits: SOUTH (north corridor) or LEAVE.")


# ─── DESCRIBER REGISTRY ───────────────────────────────────────────────────────

DESCRIBERS = {
    "room_314":       describe_room_314,
    "hallway":        describe_hallway,
    "room_312":       describe_room_312,
    "lounge":         describe_lounge,
    "managers_office": describe_managers_office,
    "linen_closet":   describe_linen_closet,
    "north_corridor": describe_north_corridor,
    "room_316":       describe_room_316,
    "stairwell":      describe_stairwell,
}


# ─── Main Entry Point ─────────────────────────────────────────────────────────

def describe_room(game):
    room_id = game.room
    first_visit = room_id not in game.rooms_visited
    game.rooms_visited.add(room_id)

    room_print(ROOMS[room_id]["name"])

    describer = DESCRIBERS.get(room_id)
    if describer:
        describer(game, first_visit)
    else:
        dim("A nondescript hotel room. Nothing stands out.")

    for npc in get_room_npcs(room_id):
        npc.describe(game, first_visit)

    _show_ground_items(game)
    game.status_bar()
