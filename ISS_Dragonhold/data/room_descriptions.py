"""
room_descriptions.py — Dynamic room description functions.

Each function receives (game, first_visit) and prints the room's text.
To add descriptions for a new room, define a function and register it
in DESCRIBERS at the bottom.

NPC-specific descriptions are handled by each NPC's describe() method,
which is called automatically after the room description.
"""

from engine.display import (
    wrap, room_print, dragon_says, alert, danger, success, dim,
)
from data.rooms import ROOMS
from data.items import item_name
from npcs import get_npc, get_room_npcs


def _show_ground_items(game):
    """Print items lying on the ground in the current room."""
    from engine.display import C
    items = ROOMS[game.room]["items"]
    if items:
        print(f"\n  {C.YELLOW}Items here: "
              f"{', '.join(item_name(i) for i in items)}{C.RESET}")


# ─── Room Describers ──────────────────────────────────────────────────────────

def describe_intern_quarters(game, first_visit):
    print(wrap(
        "Tiny bunk room. Ozone smell, bad life choices. Posters: "
        "'SYNERGIZE YOUR MANA!' and 'HUSTLE LIKE A LICH'. "
        "Cot, cluttered desk, shattered dreams."
    ))
    if "usb_wand" in ROOMS[game.room]["items"]:
        dim("Something on the desk blinks a faint, melancholy red.")
    if first_visit:
        get_npc("dracos").say("greeting")
        game.set_flag("dracos_met")
    dim("Exits: NORTH to the corridor.")


def describe_corridor(game, first_visit):
    print(wrap(
        "Mixed-vibe hallway: flickering torches AND fluorescents. "
        "Scorch marks suggest previous interns fared poorly."
    ))
    if "goblin_repellent" in ROOMS[game.room]["items"]:
        dim("It looks like someone dropped something in a hurry and never came back for it.")
    if first_visit:
        get_npc("dracos").say("corridor_intro")
    dim("Exits: NORTH (Bridge), EAST (Cafeteria), WEST (Engineering), SOUTH (Quarters).")


def describe_bridge(game, first_visit):
    print(wrap(
        "Command center meets throne room. Viewscreen shows a cheese "
        "planet — ALARMINGLY close. Warning lights flash everywhere."
    ))
    if first_visit:
        get_npc("dracos").say("bridge_intro")
    if not game.check_flag("looked_out_window"):
        dim("The viewscreen shows something. You could LOOK WINDOW for a closer view.")
    if game.check_flag("hyperdrive_fixed"):
        alert("The hyperdrive status indicator glows GREEN. You could ACTIVATE the jump!")
    dim("Exits: SOUTH (Corridor), EAST (Airlock).")


def describe_cafeteria(game, first_visit):
    if not game.check_flag("cafeteria_cleared"):
        print(wrap(
            "Floating trays. Self-stirring ladles. A translucent chef "
            "glares from behind the counter, spectral rolling pin in hand. "
            "Reeks of ectoplasmic bouillabaisse."
        ))
        if first_visit:
            get_npc("dracos").say("cafeteria_intro")
    else:
        print(wrap(
            "Peaceful now. Trays settled. Faint smell of good cooking."
        ))
    if "space_cheese" in ROOMS[game.room]["items"]:
        dim("One of the drifting trays carries something that gives off a faint, warm glow.")
    dim("Exits: WEST (Corridor), SOUTH (Cargo Hold).")


def describe_engineering(game, first_visit):
    print(wrap(
        "Cauldrons beside server racks. The hyperdrive sparks feebly "
        "in the center. Screen: 'STATUS: Extremely Broken. Need 1x Crystal.'"
    ))
    if "enchanted_duct_tape" in ROOMS[game.room]["items"]:
        dim("A cluttered workbench catches your eye — something among the tools shimmers faintly.")
    if first_visit:
        get_npc("dracos").say("engineering_intro")
    if game.check_flag("hyperdrive_fixed"):
        success("The hyperdrive hums with power! Get to the Bridge to ACTIVATE!")
    dim("Exits: EAST (Corridor), NORTH (Armory).")


def describe_armory(game, first_visit):
    print(wrap(
        "Weapons everywhere: laser staves, blasters, cursed sporks. "
        "All locked — 'Level 5+ only.' One display case has a crack."
    ))
    if "plasma_sword" in ROOMS[game.room]["items"]:
        dim("The cracked case catches the light — something inside is definitely still live.")
    if first_visit:
        get_npc("dracos").say("armory_intro")
    dim("Exits: SOUTH (Engineering).")


def describe_airlock(game, first_visit):
    print(wrap(
        "Reinforced chamber. Big red button: 'DO NOT PRESS'. "
        "Space goblins cling to the hull outside."
    ))
    if first_visit:
        get_npc("dracos").say("airlock_intro")
    dim("Exits: WEST (Bridge), NORTH (Crystal Chamber).")


def describe_cargo_hold(game, first_visit):
    if game.check_flag("goblins_befriended"):
        print(wrap(
            "Cozy goblin village. Circuit-board fire pits, cheerful waving."
        ))
    elif game.check_flag("goblins_defeated"):
        print(wrap(
            "Quiet now. Scattered goblin belongings litter the floor."
        ))
    else:
        print(wrap(
            "GOBLIN NEST. Glowing-eyed goblins chitter from behind barricades. "
            "Their king — circuit-board crown — sits on a packing-peanut throne."
        ))
        if first_visit:
            get_npc("dracos").say("cargo_hold_intro")
    dim("Exits: NORTH (Cafeteria).")


def describe_crystal_chamber(game, first_visit):
    print(wrap(
        "Spherical chamber lined with humming crystals. "
        "In the center, floating in a beam of light..."
    ))
    if not game.check_flag("crystal_obtained"):
        dim("Something in the center of the room pulses slowly — the beam of light is hard to look at directly.")
        dim("A small sign on the wall offers a warning in bureaucratic font.")
    else:
        dim("The containment field is empty. You already took the crystal.")
    dim("Exits: SOUTH (Airlock), NORTH (Escape Pods).")


def describe_escape_pods(game, first_visit):
    print(wrap(
        "Three egg-shaped escape pods sit in launch bays. Two are labeled "
        "'OUT OF ORDER' with sad wizard-face stickers. One glows green: READY."
    ))
    get_npc("dracos").say("escape_pod")
    dim("Exits: SOUTH (Crystal Chamber). Or... LAUNCH the pod.")


# ─── DESCRIBER REGISTRY ──────────────────────────────────────────────────────
#
#   Maps room_id → describe function.
#   If a room has no entry here, a generic description is shown.

DESCRIBERS = {
    "intern_quarters":  describe_intern_quarters,
    "corridor":         describe_corridor,
    "bridge":           describe_bridge,
    "cafeteria":        describe_cafeteria,
    "engineering":      describe_engineering,
    "armory":           describe_armory,
    "airlock":          describe_airlock,
    "cargo_hold":       describe_cargo_hold,
    "crystal_chamber":  describe_crystal_chamber,
    "escape_pods":      describe_escape_pods,
}


# ─── Main Entry Point ────────────────────────────────────────────────────────

def describe_room(game):
    """
    Full room description: header, description text, NPC descriptions,
    ground items, and status bar.
    """
    room_id = game.room
    first_visit = room_id not in game.rooms_visited
    game.rooms_visited.add(room_id)

    room_print(ROOMS[room_id]["name"])

    # Room-specific text
    describer = DESCRIBERS.get(room_id)
    if describer:
        describer(game, first_visit)
    else:
        dim("You are in an unremarkable room.")

    # NPC descriptions (ghost, turret, etc.)
    for npc in get_room_npcs(room_id):
        npc.describe(game, first_visit)

    game.status_bar()
