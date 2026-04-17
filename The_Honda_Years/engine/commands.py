"""
commands.py — Command parser and handlers for The Honda Years.
Same structure as Route 7 / Hotel Midnight.
"""

from engine.display import info, dim, success, danger, alert, C
from data.rooms import ROOMS, BLOCKED_PATHS, MOVEMENT_DCS
from data.items import ITEMS, item_name
from data.item_uses import USE_HANDLERS
from data.room_descriptions import describe_room
from npcs import find_npc_by_alias, get_active_npcs, get_npc


DIR_MAP = {
    "n": "north", "s": "south", "e": "east", "w": "west",
    "north": "north", "south": "south",
    "east": "east", "west": "west",
    "back":  "back",  "front": "front",
    "stop":  "stop",
}


# ─── Main Dispatcher ──────────────────────────────────────────────────────────

def process_command(game, raw):
    parts = raw.split(maxsplit=1)
    cmd   = parts[0]
    arg   = parts[1] if len(parts) > 1 else ""

    if cmd in ("quit", "exit", "q"):
        get_npc("radio").say("quit")
        return False

    elif cmd in ("help", "?"):
        show_help()

    elif cmd in ("go", "move", "drive", "continue", "keep"):
        direction = DIR_MAP.get(arg, arg) if arg else "west"
        cmd_go(game, direction)

    elif cmd in ("west", "w"):
        cmd_go(game, "west")

    elif cmd in ("east", "e"):
        cmd_go(game, "east")

    elif cmd in ("back", "backseat", "kids"):
        cmd_go(game, "back")

    elif cmd in ("front", "frontseat"):
        cmd_go(game, "front")

    elif cmd in ("stop", "pullover", "pull"):
        cmd_go(game, "stop")

    elif cmd in ("arrive", "portland", "destination", "park"):
        cmd_arrive(game)

    elif cmd in ("look", "examine", "inspect", "l"):
        cmd_look(game, arg)

    elif cmd in ("take", "get", "grab", "pick"):
        cmd_take(game, arg)

    elif cmd in ("use", "read", "open"):
        cmd_use(game, arg)

    elif cmd in ("inventory", "i", "inv"):
        cmd_inventory(game)

    elif cmd in ("talk", "speak", "ask", "say"):
        cmd_talk(game, arg)

    elif cmd in ("fight", "argue", "yell", "shout"):
        cmd_fight(game, arg)

    elif cmd in ("wait", "sleep", "rest", "sit"):
        _cmd_wait(game)

    elif cmd == "status":
        game.status_bar()

    else:
        responses = [
            "The road doesn't respond to that.",
            "Try 'talk', 'go west', or 'help'.",
            "Drew would have something to say. Probably unhelpful.",
        ]
        print(f"  {responses[game.turns % len(responses)]}")

    game.turns += 1
    _check_turn_events(game)
    return not game.game_over


# ─── TURN EVENTS ──────────────────────────────────────────────────────────────

def _check_turn_events(game):
    from data.endings import TURN_LIMIT, ending_ran_out_of_road
    radio = get_npc("radio")

    if game.turns == 20:
        radio.say("time_warning_20")
    elif game.turns == 45:
        radio.say("time_warning_45")
    elif game.turns == 60:
        radio.say("time_warning_60")
    elif game.turns == 70:
        radio.say("time_warning_70")
    elif game.turns >= TURN_LIMIT and not game.game_over:
        ending_ran_out_of_road(game)


# ─── WAIT ─────────────────────────────────────────────────────────────────────

def _cmd_wait(game):
    dim("Miles pass. The road stays the same.")
    if game.room == "front_seat":
        if game.check_flag("motel_talk") and not game.check_flag("affair_revealed"):
            dim("February is still out there. So is Sarah.")
        elif game.check_flag("affair_revealed"):
            dim("The road is different now. Quieter in a good way.")
        else:
            dim("Sarah stares at the passenger window. Emma's pencil scratches.")


# ─── GO ───────────────────────────────────────────────────────────────────────

def cmd_go(game, direction):
    exits = ROOMS[game.room]["exits"]
    if direction not in exits:
        avail = ", ".join(exits.keys())
        print(f"  Can't go {direction} from here. Exits: {avail}.")
        return

    target = exits[direction]

    block = BLOCKED_PATHS.get((game.room, direction))
    if block and not game.check_flag(block["flag"]):
        danger(block["message"])
        return

    game.room = target
    describe_room(game)


# ─── LOOK ─────────────────────────────────────────────────────────────────────

def cmd_look(game, target=""):
    if not target:
        describe_room(game)
        return

    if target in ("road", "outside", "window", "highway", "sky", "landscape"):
        if game.room in ("breakdown",):
            dim(
                "Wyoming shoulder. Sage and gravel and a lot of sky. "
                "No shade. The Honda is leaking something."
            )
        else:
            dim(
                "Flat. Then hills. Then mountains. Then Oregon. "
                "The road keeps going."
            )
        return

    if target in ("car", "honda", "vehicle", "van"):
        dim(
            "2019 Honda Pilot. 47,000 miles. "
            "A crack in the left taillight from when you "
            "backed into the mailbox the morning after February 14. "
            "You told Sarah you hit a parking bollard."
        )
        return

    if target in ("kids", "children", "back", "backseat") \
            and game.room == "front_seat":
        dim(
            "Rearview mirror: Emma drawing, Drew comatose. "
            "They look like they don't have a care in the world. "
            "They probably don't."
        )
        return

    if target in ("mirror", "rearview"):
        dim(
            "Your own face. You look like someone who hasn't slept enough "
            "and is trying not to show it."
        )
        return

    npc = find_npc_by_alias(game.room, target)
    if npc:
        npc.look(game)
        return

    for item in game.inventory:
        aliases = ITEMS.get(item, {}).get("aliases", [])
        if target in item or target in item.replace("_", " ") or target in aliases:
            desc = ITEMS.get(item, {}).get("description", "Nothing notable.")
            print(f"  {desc}")
            return

    print(f"  Nothing notable about '{target}'.")


# ─── TAKE ─────────────────────────────────────────────────────────────────────

def cmd_take(game, arg):
    if not arg:
        print("  Take what?")
        return

    room_items = ROOMS[game.room]["items"]
    matched = None
    for item_id in room_items:
        aliases = ITEMS.get(item_id, {}).get("aliases", [])
        if (arg in item_id
                or arg in item_name(item_id).lower()
                or arg in aliases):
            matched = item_id
            break

    if not matched:
        print(f"  There's no '{arg}' here to pick up.")
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
        # Also search room items (e.g. read therapy_notes in place)
        for item_id in ROOMS[game.room]["items"]:
            aliases = ITEMS.get(item_id, {}).get("aliases", [])
            if (arg in item_id
                    or arg in item_name(item_id).lower()
                    or arg in aliases):
                matched = item_id
                break

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
        print(
            f"  You turn the {item_name(matched)} over in your hands. "
            "It doesn't change anything. Yet."
        )


# ─── ARRIVE ───────────────────────────────────────────────────────────────────

def cmd_arrive(game):
    if game.room != "final_miles":
        dim("Portland is still ahead. Keep driving west.")
        return
    if not game.check_flag("breakdown_done"):
        dim(
            "You're close. But Wyoming isn't finished with you yet. "
            "Talk to Sarah."
        )
        return
    from data.endings import ending_portland
    ending_portland(game)


# ─── INVENTORY ────────────────────────────────────────────────────────────────

def cmd_inventory(game):
    if not game.inventory:
        print("  Pockets empty. Thoughts full.")
    else:
        print(f"\n  {C.BOLD}WHAT YOU'RE CARRYING:{C.RESET}")
        for item in game.inventory:
            print(f"    • {item_name(item)}")
    print(
        f"  {C.DIM}Connection: {game.hp}/{game.max_hp}  |  "
        f"~{game.miles_remaining()} miles left{C.RESET}"
    )


# ─── TALK ─────────────────────────────────────────────────────────────────────

def cmd_talk(game, target=""):
    npc = None
    if target:
        npc = find_npc_by_alias(game.room, target)
        if not npc:
            radio = get_npc("radio")
            if radio and radio.matches(target):
                npc = radio
    else:
        active = get_active_npcs(game.room, game)
        # Priority: Sarah > Emma > Drew
        for preferred_id in ("sarah", "emma", "drew"):
            for n in active:
                if n.id == preferred_id:
                    npc = n
                    break
            if npc:
                break
        if not npc and active:
            npc = active[0]
        if not npc:
            npc = get_npc("radio")

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
            if n.id not in ("radio",):
                npc = n
                break

    if npc:
        npc.fight(game)
    else:
        dim("Nobody to fight. You could argue with the GPS.")


# ─── HELP ─────────────────────────────────────────────────────────────────────

def show_help():
    print(f"""
  {C.BOLD}━━━ COMMANDS ━━━{C.RESET}
  {C.CYAN}go / drive / west{C.RESET}   Continue to next stop
  {C.CYAN}go east{C.RESET}             Backtrack
  {C.CYAN}back / front{C.RESET}        Move between front/back seat
  {C.CYAN}stop{C.RESET}                Pull over at rest stop
  {C.CYAN}look{C.RESET}                Look around current location
  {C.CYAN}look [x]{C.RESET}            Examine something specific
  {C.CYAN}take [x]{C.RESET}            Pick something up
  {C.CYAN}use / read [x]{C.RESET}      Use or read an item
  {C.CYAN}talk{C.RESET}                Talk to whoever is here
  {C.CYAN}talk [name]{C.RESET}         Talk to a specific person
  {C.CYAN}inv / i{C.RESET}             Check what you're carrying
  {C.CYAN}arrive{C.RESET}              Arrive in Portland (final miles)
  {C.CYAN}status{C.RESET}              Connection level and miles
  {C.CYAN}wait{C.RESET}                Let the miles pass
  {C.CYAN}quit{C.RESET}                Give up

  {C.BOLD}━━━ GOAL ━━━{C.RESET}
  {C.DIM}Drive Chicago to Portland. Talk to Sarah. Really talk.{C.RESET}
  {C.DIM}The ending depends on the choices you make, not luck.{C.RESET}
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
