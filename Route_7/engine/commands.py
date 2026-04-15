"""
commands.py — Command parser and handlers for Route 7.
Same structure as Hotel Midnight / ISS Dragonhold.
"""

from engine.display import info, dim, success, danger, alert, C
from engine.dice import ask_d20
from data.rooms import ROOMS, BLOCKED_PATHS, MOVEMENT_DCS
from data.items import ITEMS, item_name
from data.item_uses import USE_HANDLERS
from data.room_descriptions import describe_room
from npcs import find_npc_by_alias, get_active_npcs, get_npc


DIR_MAP = {
    "n": "north", "s": "south", "e": "east", "w": "west",
    "u": "up", "d": "down",
    "up": "up", "down": "down",
    "front": "north", "back": "south",
    "forward": "north", "backward": "south",
}


# ─── Main Dispatcher ──────────────────────────────────────────────────────────

def process_command(game, raw):
    parts = raw.split(maxsplit=1)
    cmd = parts[0]
    arg = parts[1] if len(parts) > 1 else ""

    if cmd in ("quit", "exit", "q"):
        get_npc("dispatch").say("quit")
        return False

    elif cmd in ("help", "?"):
        show_help()

    elif cmd in ("go", "move", "walk"):
        if not arg:
            arg = input("  Direction? (north/south/up/down/front/back): ").strip().lower()
        cmd_go(game, DIR_MAP.get(arg, arg))

    elif cmd in ("north", "south", "east", "west", "n", "s", "e", "w",
                 "up", "down", "u", "d", "front", "back", "forward"):
        cmd_go(game, DIR_MAP.get(cmd, cmd))

    elif cmd in ("look", "examine", "inspect", "l"):
        cmd_look(game, arg)

    elif cmd in ("take", "get", "grab", "pick"):
        cmd_take(game, arg)

    elif cmd == "use":
        cmd_use(game, arg)

    elif cmd in ("pull",):
        # Alias: PULL LEVER → USE LEVER
        target = arg if arg else "lever"
        cmd_use(game, target)

    elif cmd in ("inventory", "i", "inv"):
        cmd_inventory(game)

    elif cmd in ("talk", "speak", "ask"):
        cmd_talk(game, arg)

    elif cmd in ("fight", "attack", "hit", "grab"):
        cmd_fight(game, arg)

    elif cmd in ("leave", "escape", "jump"):
        cmd_leave(game)

    elif cmd == "status":
        game.status_bar()

    else:
        responses = [
            "That's not something you can do right now.",
            "Focus. Type 'help' if you're stuck.",
            "The bus doesn't respond to that.",
        ]
        print(f"  {responses[game.turns % len(responses)]}")

    game.turns += 1
    _check_turn_events(game)
    return True


# ─── TURN EVENTS ──────────────────────────────────────────────────────────────

def _check_turn_events(game):
    from data.endings import TURN_LIMIT, ending_end_of_line
    dispatch = get_npc("dispatch")

    if game.turns == 35:
        dispatch.say("time_warning_35")
    elif game.turns == 55:
        dispatch.say("time_warning_55")
    elif game.turns == 65:
        dispatch.say("time_warning_65")
    elif game.turns == 69:
        dispatch.say("time_warning_69")
    elif game.turns >= TURN_LIMIT and not game.game_over:
        ending_end_of_line(game)


# ─── GO ───────────────────────────────────────────────────────────────────────

def cmd_go(game, direction):
    exits = ROOMS[game.room]["exits"]
    if direction not in exits:
        print(f"  Can't go {direction}. Exits: {', '.join(exits.keys())}.")
        return

    # Open luggage hatch on first descent
    if direction == "down" and game.room == "middle_aisle":
        if not game.check_flag("hatch_open"):
            game.set_flag("hatch_open")
            success("You lift the floor hatch. A dark space below.")

    target = exits[direction]

    block = BLOCKED_PATHS.get((game.room, direction))
    if block and not game.check_flag(block["flag"]):
        danger(block["message"])
        return

    mv = MOVEMENT_DCS.get(target)
    if mv and target not in game.rooms_visited:
        dc = mv["dc"]
        info(f"Requires a check (DC {dc}).")
        roll = ask_d20(mv["reason"])
        if roll < dc and roll != 20:
            if roll == 1:
                danger("You slip. Hard knock to the head.")
                game.take_damage(2)
            else:
                print(f"  {C.RED}Needed {dc}, rolled {roll}. Try again.{C.RESET}")
            return

    game.room = target
    describe_room(game)


# ─── LOOK ─────────────────────────────────────────────────────────────────────

def cmd_look(game, target=""):
    if not target:
        describe_room(game)
        return

    # Special: look at passengers in rear_seats
    if target in ("passengers", "passenger", "people", "them", "figures") \
            and game.room == "rear_seats":
        from engine.display import danger
        danger(
            "You look directly at the two rear passengers. "
            "They are wearing coats from another decade. "
            "One is holding a handbag. One has a briefcase. "
            "Neither is breathing."
        )
        return

    # Special: look at emergency door
    if target in ("door", "emergency door", "exit", "rear door") \
            and game.room == "rear_seats":
        if game.check_flag("lever_pulled"):
            alert("Emergency door is unsealed. LEAVE to jump.")
        else:
            dim(
                "A double-leaf emergency door. A red lever mount "
                "is set into the side wall — the lever is missing. "
                "You need to find it and slot it back in."
            )
        return

    # Special: look at hatch in middle_aisle
    if target in ("hatch", "floor", "panel", "trapdoor") \
            and game.room == "middle_aisle":
        if not game.check_flag("hatch_open"):
            dim("A hinged floor panel. Latched but not locked. Go DOWN.")
        else:
            dim("Open hatch. Dark below. Go DOWN.")
        return

    # Special: look at partition / driver's cab
    if target in ("partition", "cab", "window", "door", "glass") \
            and game.room == "front_seats":
        if game.check_flag("cab_unlocked"):
            alert("The partition is unlocked. Go NORTH.")
        else:
            dim(
                "Reinforced steel partition. Small wired-glass porthole, "
                "too grimy to see through clearly. "
                "One industrial keyhole."
            )
        return

    # Special: look at window anywhere
    if target in ("window", "outside", "road", "dark"):
        dim(
            "Motorway. No lights, no signs, no other vehicles. "
            "The road narrows ahead until it disappears."
        )
        return

    # Special: look at map on partition
    if target in ("map", "route map") and game.room == "front_seats":
        if "folded_map" in ROOMS[game.room]["items"]:
            dim("A faded Route 7 map. TAKE MAP for a closer look.")
        else:
            dim("You already took the map.")
        return

    # Check NPC
    npc = find_npc_by_alias(game.room, target)
    if npc:
        npc.look(game)
        return

    # Check inventory
    for item in game.inventory:
        if target in item or target in item.replace("_", " "):
            desc = ITEMS.get(item, {}).get("description", "Nothing notable.")
            print(f"  {desc}")
            return

    print(f"  Nothing notable about '{target}'.")


# ─── TAKE ─────────────────────────────────────────────────────────────────────

def cmd_take(game, arg):
    if not arg:
        print("  Take what?")
        return

    # Special: maintenance_key requires lighter
    if (arg in ("maintenance key", "maintenance_key", "key", "steel key", "cab key")
            and game.room == "luggage_hatch"):
        if "maintenance_key" in ROOMS[game.room]["items"]:
            if not game.has("lighter"):
                danger("Too dark. You can feel the lever mount "
                       "but can't find the key. USE LIGHTER first.")
                return
            ROOMS[game.room]["items"].remove("maintenance_key")
            game.add_item("maintenance_key")
            success("Taken: Maintenance Key.")
            return
        else:
            print("  The key is already in your pocket.")
            return

    room_items = ROOMS[game.room]["items"]
    matched = None
    for item_id in room_items:
        aliases = ITEMS.get(item_id, {}).get("aliases", [])
        if (arg in item_id or arg in item_name(item_id).lower()
                or arg in aliases):
            matched = item_id
            break

    if not matched:
        print(f"  There's no '{arg}' here.")
        return

    room_items.remove(matched)
    game.add_item(matched)
    success(f"Taken: {item_name(matched)}.")


# ─── USE ──────────────────────────────────────────────────────────────────────

def cmd_use(game, arg):
    if not arg:
        print("  Use what? (Check inventory with 'i')")
        return

    matched = _fuzzy_match_inv(game, arg)
    if not matched:
        print(f"  You don't have anything like '{arg}'.")
        return

    for npc in get_active_npcs(game.room, game):
        if npc.use_item(game, matched):
            return

    handler = USE_HANDLERS.get(matched)
    if handler:
        handler(game)
    else:
        print(f"  You fiddle with the {item_name(matched)}. Nothing happens.")


# ─── LEAVE / ESCAPE ───────────────────────────────────────────────────────────

def cmd_leave(game):
    if game.room == "rear_seats":
        from data.endings import ending_escape_rear
        ending_escape_rear(game)
    elif game.room == "drivers_cab":
        from data.endings import ending_escape_cab
        ending_escape_cab(game)
    else:
        dim(
            "There's no exit here. "
            "Rear door is in the rear seats. "
            "Or reach the driver's cab."
        )


# ─── INVENTORY ────────────────────────────────────────────────────────────────

def cmd_inventory(game):
    if not game.inventory:
        print("  Your pockets are empty.")
    else:
        print(f"\n  {C.BOLD}INVENTORY:{C.RESET}")
        for item in game.inventory:
            print(f"    • {item_name(item)}")
    print(f"  {C.DIM}HP: {game.hp}/{game.max_hp}  |  {game.bus_time()}{C.RESET}")


# ─── TALK ─────────────────────────────────────────────────────────────────────

def cmd_talk(game, target=""):
    npc = None
    if target:
        npc = find_npc_by_alias(game.room, target)
        if not npc:
            dispatch = get_npc("dispatch")
            if dispatch and dispatch.matches(target):
                npc = dispatch
    else:
        active = get_active_npcs(game.room, game)
        if active:
            npc = active[0]
        if not npc:
            npc = get_npc("dispatch")

    if npc:
        npc.talk(game)
    else:
        print("  Nobody here to talk to.")


# ─── FIGHT ────────────────────────────────────────────────────────────────────

def cmd_fight(game, target=""):
    npc = None
    if target:
        npc = find_npc_by_alias(game.room, target)
    else:
        active = get_active_npcs(game.room, game)
        for n in active:
            if n.id != "dispatch":
                npc = n
                break

    if npc and npc.is_active(game):
        npc.fight(game)
    else:
        print("  There's nobody here to fight. Probably for the best.")


# ─── HELP ─────────────────────────────────────────────────────────────────────

def show_help():
    print(f"""
  {C.BOLD}━━━ COMMANDS ━━━{C.RESET}
  {C.CYAN}go [dir]{C.RESET}     Move N/S/UP/DOWN/FRONT/BACK
  {C.CYAN}look{C.RESET}         Look around
  {C.CYAN}look [x]{C.RESET}     Examine something
  {C.CYAN}take [x]{C.RESET}     Pick up an item
  {C.CYAN}use [x]{C.RESET}      Use from inventory
  {C.CYAN}pull [x]{C.RESET}     Pull a lever or handle
  {C.CYAN}talk [x]{C.RESET}     Talk to someone
  {C.CYAN}fight [x]{C.RESET}    Physical confrontation
  {C.CYAN}inv / i{C.RESET}      Check your items
  {C.CYAN}leave{C.RESET}        Escape (rear or cab)
  {C.CYAN}status{C.RESET}       HP and bus time
  {C.CYAN}quit{C.RESET}         Give up

  {C.BOLD}━━━ DICE ━━━{C.RESET}
  {C.YELLOW}d20{C.RESET}  Checks, escapes, confrontations
  {C.DIM}Nat 20 = Crit  |  Nat 1 = Fail{C.RESET}

  {C.BOLD}━━━ GOAL ━━━{C.RESET}
  {C.DIM}Get off Route 7 before End of Line.{C.RESET}
  {C.DIM}Collect evidence for a better ending.{C.RESET}
  {C.DIM}Talk to Rosa. Search the luggage hatch.{C.RESET}
""")


# ─── Helpers ──────────────────────────────────────────────────────────────────

def _fuzzy_match_inv(game, word):
    for item in game.inventory:
        if word in item or word in item.replace("_", " "):
            return item
        aliases = ITEMS.get(item, {}).get("aliases", [])
        if word in aliases:
            return item
    return None
