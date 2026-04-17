"""
room_descriptions.py — Room descriptions for The Honda Years.
"""

from engine.display import wrap, room_print, radio_says, alert, danger, dim, info
from data.rooms import ROOMS
from data.items import item_name
from npcs import get_npc, get_room_npcs


def _show_ground_items(game):
    from engine.display import C
    items = ROOMS[game.room]["items"]
    if items:
        print(
            f"\n  {C.YELLOW}Items here: "
            f"{', '.join(item_name(i) for i in items)}{C.RESET}"
        )


# ─── Room Describers ──────────────────────────────────────────────────────────

def describe_front_seat(game, first_visit):
    if first_visit:
        print(wrap(
            "You're driving. Sarah is in the passenger seat, "
            "sunglasses on, coffee from home going cold in the cupholder. "
            "The Chicago suburbs thin out behind you. "
            "The GPS says 2,094 miles."
        ))
        get_npc("radio").say("front_seat_first")
    else:
        if game.check_flag("affair_revealed"):
            print(wrap(
                "Front seat. You and Sarah. "
                "The road ahead. Something lighter than before."
            ))
        elif game.check_flag("motel_talk"):
            print(wrap(
                "Front seat. The Honda. "
                "The miles pass. There's still something left to say."
            ))
        else:
            print(wrap(
                "Front seat. Sarah is quiet. "
                "The radio fills the space."
            ))
    dim("Exits: BACK (back seat), DRIVE west (next stop).")


def describe_back_seat(game, first_visit):
    if first_visit:
        print(wrap(
            "You twist around. "
            "Drew is in the left back seat, headphones on, "
            "either asleep or deeply committed to appearing asleep. "
            "Emma is in the right back seat. "
            "She is drawing. She is always drawing."
        ))
        dim("Two kids who have no idea anything is wrong.")
    else:
        print(wrap(
            "The back seat. Drew and Emma. "
            "Same positions as before."
        ))
    dim("Exits: FRONT (front seat).")


def describe_rest_stop(game, first_visit):
    print(wrap(
        "I-80 Rest Area, Iowa. "
        "Concrete picnic tables. A vending machine humming in the heat. "
        "The horizon is flat enough to see the curve of the earth."
    ))
    if first_visit:
        dim(
            "Everyone is out of the car. First time since Chicago. "
            "The sky is enormous."
        )
        get_npc("radio").say("rest_stop_song")
    dim("Exits: EAST (back to car), WEST (continue to Nebraska).")


def describe_motel(game, first_visit):
    print(wrap(
        "Motel 6, Kearney, Nebraska. Room 114. "
        "Two queen beds and a TV bolted to the dresser. "
        "Drew and Emma are in 116. "
        "The walls are thin."
    ))
    if first_visit:
        info(
            "Drew took the good bed the second he walked in. "
            "Emma has arranged a small rock collection on the windowsill."
        )
        dim("Talk to Sarah. You're alone for the first time since Chicago.")
    if "therapy_notes" in ROOMS[game.room]["items"]:
        dim("A blue spiral notebook is on the nightstand.")
    dim("Exits: EAST (back to Iowa), WEST (continue tomorrow).")


def describe_breakdown(game, first_visit):
    print(wrap(
        "I-80 westbound shoulder. Wyoming. "
        "The Honda is making a sound it shouldn't. "
        "Steam from the hood. "
        "You're on gravel with an hour until the tow truck."
    ))
    if first_visit:
        get_npc("radio").say("breakdown_song")
        danger(
            "The car broke down in Wyoming. "
            "You have nowhere to be and no way to get there. "
            "Everyone is here. There's nowhere to go."
        )
        dim("Talk to Sarah. Or Drew. Or Emma.")
    dim("Exits: EAST (back toward Nebraska), WEST (continue to Oregon).")


def describe_final_miles(game, first_visit):
    print(wrap(
        "Oregon. "
        "The road has changed — hills, trees, the smell "
        "of something different through the vents. "
        "Portland is two hours away. "
        "You've been driving for three days."
    ))
    if first_visit:
        info(
            "The Honda sounds different on Oregon pavement. "
            "Or maybe you're just listening differently now."
        )
        dim("Talk to Sarah. Then ARRIVE when you're ready.")
    else:
        dim("Almost there. ARRIVE when you're ready.")
    dim("Exits: EAST (back toward Wyoming), ARRIVE (Portland).")


# ─── DESCRIBER REGISTRY ───────────────────────────────────────────────────────

DESCRIBERS = {
    "front_seat":    describe_front_seat,
    "back_seat":     describe_back_seat,
    "rest_stop":     describe_rest_stop,
    "motel_kearney": describe_motel,
    "breakdown":     describe_breakdown,
    "final_miles":   describe_final_miles,
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
        dim("Miles of highway.")

    for npc in get_room_npcs(room_id):
        npc.describe(game, first_visit)

    _show_ground_items(game)
    game.status_bar()
