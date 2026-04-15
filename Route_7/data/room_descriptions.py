"""
room_descriptions.py — Room descriptions for Route 7.
"""

from engine.display import wrap, room_print, dispatch_says, alert, danger, dim, info
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

def describe_rear_seats(game, first_visit):
    print(wrap(
        "Back of the bus. Six rows of seats, mostly empty. "
        "Two passengers sit rigid in the rearmost row — "
        "coats too heavy for the weather, faces turned away. "
        "Neither has moved since you woke up."
    ))
    if first_visit:
        dim(
            "A newspaper is wedged between the seats. "
            "The emergency door is sealed at the rear."
        )
        dispatch_says(
            "Good evening. Welcome to Route 7. "
            "Next stop: End of Line. "
            "Please retain your ticket for inspection."
        )
    if game.check_flag("lever_pulled"):
        alert("Emergency door ready. LEAVE to jump from the bus.")
    else:
        dim("Emergency door is sealed. You need to release the latch.")
    dim("Exits: NORTH (middle aisle).")


def describe_middle_aisle(game, first_visit):
    print(wrap(
        "The centre of the bus. Fluorescent tubes flicker "
        "in the ceiling. Outside: a motorway you don't recognise, "
        "no lights, no other cars. The city ended some time ago."
    ))
    if first_visit:
        dim("A floor hatch near the rear wheel arch. Maintenance access.")
    if not game.check_flag("hatch_open"):
        dim("The hatch is secured but not locked. DOWN to open it.")
    dim("Exits: NORTH (front seats), SOUTH (rear), DOWN (hatch).")


def describe_front_seats(game, first_visit):
    print(wrap(
        "The front section. Driver's partition ahead — "
        "reinforced steel, a small wired-glass window "
        "too dirty to see through. A route map is tacked "
        "above the window. Bench seats face inward here."
    ))
    if first_visit:
        get_npc("dispatch").say("front_seats_intro")
    if "lighter" in ROOMS[game.room]["items"]:
        dim("Something yellow is wedged under the left bench seat.")
    if "folded_map" in ROOMS[game.room]["items"]:
        dim("A folded bus map is tacked to the partition.")
    if game.check_flag("cab_unlocked"):
        alert("Cab partition is unlocked. NORTH to enter.")
        dim("Exits: SOUTH (middle aisle), NORTH (cab).")
    else:
        dim("Cab partition is locked. You need a maintenance key.")
        dim("Exits: SOUTH (middle aisle), NORTH (cab — locked).")


def describe_luggage_hatch(game, first_visit):
    if not game.check_flag("hatch_lit"):
        print(wrap(
            "Near-total darkness. The hatch lets in a thin shaft "
            "of aisle light. You can hear road noise, very close. "
            "The chassis vibrates. Something is mounted on the wall "
            "to your left — a lever mechanism. You feel it by touch."
        ))
        dim(
            "Too dark to see clearly. "
            "USE LIGHTER to illuminate the space."
        )
    else:
        print(wrap(
            "Low ceiling, cramped. Spare tyre, toolbox, road grime. "
            "The emergency exit lever mount is on the left wall — "
            "the lever itself is already removed. "
            "A steel key lies on the floor by the toolbox."
        ))
    dim("Exits: UP (back to middle aisle).")


def describe_drivers_cab(game, first_visit):
    print(wrap(
        "A cramped driver's compartment. The windscreen shows "
        "a road that narrows to nothing in the headlights. "
        "No signage. No other vehicles. "
        "The driver is seated, hands on the wheel, unmoving."
    ))
    if first_visit:
        game.set_flag("driver_looked", False)   # reset so LOOK driver works fresh
        get_npc("dispatch").say("cab_intro")
        danger(
            "The driver has not turned around. "
            "The route board above the windscreen reads: "
            "END OF LINE — 0 MIN."
        )
    if "drivers_log" in ROOMS[game.room]["items"]:
        dim("A logbook sits on the dashboard shelf.")
    alert("LEAVE to seize control and force a stop.")
    dim("Exits: SOUTH (back to front seats).")


# ─── DESCRIBER REGISTRY ───────────────────────────────────────────────────────

DESCRIBERS = {
    "rear_seats":    describe_rear_seats,
    "middle_aisle":  describe_middle_aisle,
    "front_seats":   describe_front_seats,
    "luggage_hatch": describe_luggage_hatch,
    "drivers_cab":   describe_drivers_cab,
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
        dim("An unremarkable part of the bus.")

    for npc in get_room_npcs(room_id):
        npc.describe(game, first_visit)

    _show_ground_items(game)
    game.status_bar()
