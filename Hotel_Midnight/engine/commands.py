"""
commands.py — Command parser and handlers for Hotel Midnight.
Same structure as ISS Dragonhold.
"""

from engine.display import info, dim, success, danger, C
from engine.dice import ask_d20
from data.rooms import ROOMS, BLOCKED_PATHS, MOVEMENT_DCS
from data.items import ITEMS, item_name
from data.item_uses import USE_HANDLERS
from data.room_descriptions import describe_room
from npcs import find_npc_by_alias, get_active_npcs, get_npc


DIR_MAP = {"n": "north", "s": "south", "e": "east", "w": "west"}


# ─── Main Dispatcher ──────────────────────────────────────────────────────────

def process_command(game, raw):
    parts = raw.split(maxsplit=1)
    cmd = parts[0]
    arg = parts[1] if len(parts) > 1 else ""

    if cmd in ("quit", "exit", "q"):
        get_npc("virgil").say("quit")
        return False

    elif cmd in ("help", "?"):
        show_help()

    elif cmd in ("go", "move", "walk"):
        if not arg:
            arg = input("  Direction? (north/south/east/west): ").strip().lower()
        cmd_go(game, DIR_MAP.get(arg, arg))

    elif cmd in ("north", "south", "east", "west", "n", "s", "e", "w"):
        cmd_go(game, DIR_MAP.get(cmd, cmd))

    elif cmd in ("look", "examine", "inspect", "l"):
        cmd_look(game, arg)

    elif cmd in ("take", "get", "grab", "pick"):
        cmd_take(game, arg)

    elif cmd == "use":
        cmd_use(game, arg)

    elif cmd in ("inventory", "i", "inv"):
        cmd_inventory(game)

    elif cmd in ("talk", "speak", "ask"):
        cmd_talk(game, arg)

    elif cmd in ("fight", "attack", "hit"):
        cmd_fight(game, arg)

    elif cmd in ("leave", "escape", "exit") and game.room == "stairwell":
        from data.endings import ending_leave
        ending_leave(game)

    elif cmd == "status":
        game.status_bar()

    else:
        responses = [
            "That's not something you can do right now.",
            "Focus. Type 'help' if you're lost.",
            "The hotel doesn't respond to that.",
        ]
        print(f"  {responses[game.turns % len(responses)]}")

    game.turns += 1
    _check_turn_events(game)
    return True


# ─── TURN EVENTS ──────────────────────────────────────────────────────────────

def _check_turn_events(game):
    from data.endings import TURN_LIMIT, ending_dawn_lockdown
    virgil = get_npc("virgil")

    if game.turns == 48:
        virgil.say("time_warning_48")
    elif game.turns == 64:
        virgil.say("time_warning_64")
    elif game.turns == 79:
        virgil.say("time_warning_79")
    elif game.turns >= TURN_LIMIT and not game.game_over:
        ending_dawn_lockdown(game)


# ─── GO ───────────────────────────────────────────────────────────────────────

def cmd_go(game, direction):
    exits = ROOMS[game.room]["exits"]
    if direction not in exits:
        print(f"  Can't go {direction}. Exits: {', '.join(exits.keys())}.")
        return

    target = exits[direction]

    block = BLOCKED_PATHS.get((game.room, direction))
    if block and not game.check_flag(block["flag"]):
        danger(block["message"])
        return

    mv = MOVEMENT_DCS.get(target)
    if mv:
        dc = mv["dc"]
        info(f"Requires a check (DC {dc}).")
        roll = ask_d20(mv["reason"])
        if roll < dc and roll != 20:
            if roll == 1:
                danger("You stumble hard.")
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

    # Special: look at note in room 314
    if target == "note" and game.room == "room_314":
        dim(
            "In your own handwriting: 'Don't trust the concierge. "
            "The key is in the piano. Get out before 4 AM!'"
        )
        return

    # Special: look at mirror in room 314
    if target in ("mirror", "bathroom") and game.room == "room_314":
        if "mirror_shard" in ROOMS[game.room]["items"]:
            dim(
                "Smashed. A shard large enough to be useful "
                "sits on the edge of the sink."
            )
        else:
            dim("Just the frame. You already took the shard.")
        return

    # Special: look at piano in lounge
    if target == "piano" and game.room == "lounge":
        if not game.check_flag("piano_key_found"):
            dim(
                "A grand piano, lid slightly raised. Something glints "
                "inside the case — small, metallic. TAKE PIANO KEY."
            )
        else:
            dim("The piano. Beautiful. You already took what was inside.")
        return

    # Special: look at box in room 316
    if target in ("box", "case", "locked box") and game.room == "room_316":
        if not game.check_flag("box_opened"):
            dim("A metal document box. Locked. USE MIRROR SHARD to pry it.")
        else:
            dim("Empty box, sprung latch.")
        return

    # Special: look at window (any hallway)
    if target == "window" and game.room in ("hallway", "north_corridor"):
        dim("Rain. Street lamps. No one on the street at this hour.")
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

    # Special: take piano key from piano
    if arg in ("piano key", "key", "piano_key") and game.room == "lounge":
        if not game.check_flag("piano_key_found"):
            info("You reach inside the piano case...")
            roll = ask_d20("Retrieving something from inside a grand piano")
            if roll >= 6 or roll == 20:
                success("Your fingers close around a heavy brass key!")
                game.add_item("piano_key")
                game.set_flag("piano_key_found")
                ROOMS["lounge"]["items"].append("piano_key") # show in room until taken
                ROOMS["lounge"]["items"].remove("piano_key")
                get_npc("virgil").say("piano_key_taken")
            else:
                danger("Your hand slips on the strings. Cuts your palm.")
                game.take_damage(2)
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


# ─── INVENTORY ────────────────────────────────────────────────────────────────

def cmd_inventory(game):
    if not game.inventory:
        print("  Your pockets are empty.")
    else:
        print(f"\n  {C.BOLD}INVENTORY:{C.RESET}")
        for item in game.inventory:
            print(f"    • {item_name(item)}")
    print(f"  {C.DIM}HP: {game.hp}/{game.max_hp}{C.RESET}")


# ─── TALK ─────────────────────────────────────────────────────────────────────

def cmd_talk(game, target=""):
    npc = None
    if target:
        npc = find_npc_by_alias(game.room, target)
        if not npc:
            # VIRGIL responds from anywhere
            virgil = get_npc("virgil")
            if virgil and virgil.matches(target):
                npc = virgil
    else:
        active = get_active_npcs(game.room, game)
        if active:
            npc = active[0]
        if not npc:
            npc = get_npc("virgil")

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
            if n.id != "virgil":
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
  {C.CYAN}go [dir]{C.RESET}     Move N/S/E/W
  {C.CYAN}look{C.RESET}         Look around
  {C.CYAN}look [x]{C.RESET}     Examine something
  {C.CYAN}take [x]{C.RESET}     Pick up an item
  {C.CYAN}use [x]{C.RESET}      Use from inventory
  {C.CYAN}talk [x]{C.RESET}     Talk to someone
  {C.CYAN}fight [x]{C.RESET}    Attack (last resort)
  {C.CYAN}inv / i{C.RESET}      Check your stuff
  {C.CYAN}leave{C.RESET}        Escape (Stairwell only)
  {C.CYAN}status{C.RESET}       Check your HP
  {C.CYAN}quit{C.RESET}         Give up

  {C.BOLD}━━━ DICE ━━━{C.RESET}
  {C.YELLOW}d20{C.RESET}  Checks, rolls, everything
  {C.YELLOW}2d6{C.RESET}  Damage and healing
  {C.DIM}Nat 20 = Crit  |  Nat 1 = Fail{C.RESET}

  {C.BOLD}━━━ GOAL ━━━{C.RESET}
  {C.DIM}Find the piano key. Get out before 4 AM.{C.RESET}
  {C.DIM}Collect evidence for a better ending.{C.RESET}
""")


# ─── Helpers ──────────────────────────────────────────────────────────────────

def _fuzzy_match_inv(game, word):
    for item in game.inventory:
        if word in item or word in item.replace("_", " "):
            return item
    return None
