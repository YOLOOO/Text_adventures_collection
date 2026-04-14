"""
commands.py — Command parser and handlers.

Processes raw player input and routes to the appropriate system.
The main game loop calls process_command() each turn.
"""

from engine.display import info, dim, success, danger, C
from engine.dice import ask_d20
from data.rooms import ROOMS, MOVEMENT_DCS, BLOCKED_PATHS
from data.items import ITEMS, item_name
from data.item_uses import USE_HANDLERS
from data.room_descriptions import describe_room
from data.endings import ending_launch_escape_pod, ending_activate_hyperdrive
from npcs import find_npc_by_alias, get_active_npcs, get_npc


# ─── Direction Aliases ────────────────────────────────────────────────────────

DIR_MAP = {"n": "north", "s": "south", "e": "east", "w": "west"}


# ─── Main Dispatcher ─────────────────────────────────────────────────────────

def process_command(game, raw):
    """
    Parse and execute a player command.
    Returns True if the game should continue, False to quit.
    """
    parts = raw.split(maxsplit=1)
    cmd = parts[0]
    arg = parts[1] if len(parts) > 1 else ""

    if cmd in ("quit", "exit", "q"):
        get_npc("dracos").say("quit")
        return False

    elif cmd in ("help", "?"):
        show_help()

    elif cmd in ("go", "move", "walk", "head"):
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

    elif cmd in ("inventory", "i", "inv", "bag"):
        cmd_inventory(game)

    elif cmd in ("talk", "speak", "chat", "ask"):
        cmd_talk(game, arg)

    elif cmd in ("fight", "attack", "hit", "kill", "combat"):
        cmd_fight(game, arg)

    elif cmd == "activate":
        ending_activate_hyperdrive(game)

    elif cmd == "launch":
        ending_launch_escape_pod(game)

    elif cmd == "status":
        game.status_bar()

    else:
        responses = [
            "I don't understand that. Type 'help' for commands.",
            "That's not a thing you can do. Yet. Try 'help'.",
            "The station doesn't recognize that command.",
        ]
        print(f"  {responses[game.turns % len(responses)]}")

    game.turns += 1
    return True


# ─── GO ───────────────────────────────────────────────────────────────────────

def cmd_go(game, direction):
    exits = ROOMS[game.room]["exits"]

    if direction not in exits:
        print(f"  You can't go {direction}. Exits: {', '.join(exits.keys())}.")
        return

    target = exits[direction]

    # Check blocked paths
    block = BLOCKED_PATHS.get((game.room, direction))
    if block and not game.check_flag(block["flag"]):
        danger(block["message"])
        return

    # Movement DC check
    mv = MOVEMENT_DCS.get(target)
    if mv:
        dc = mv["dc"]
        info(f"This passage requires a skill check (DC {dc}).")
        roll = ask_d20(mv["reason"])
        if roll < dc and roll != 20:
            if roll == 1:
                danger("You trip spectacularly and bang your knee on a bulkhead.")
                game.take_damage(2)
                get_npc("dracos").say("crit_fail_move")
            else:
                print(f"  {C.RED}Needed {dc}, rolled {roll}. Stumble — try again.{C.RESET}")
                get_npc("dracos").say("doors_defeat_you")
            return
        elif roll == 20:
            get_npc("dracos").say("crit_success_move")

    game.room = target
    describe_room(game)


# ─── LOOK ─────────────────────────────────────────────────────────────────────

def cmd_look(game, target=""):
    if not target:
        describe_room(game)
        return

    # Special: look desk in intern quarters
    if target == "desk" and game.room == "intern_quarters":
        if "usb_wand" in ROOMS[game.room]["items"]:
            dim("Among the junk on the desk, you make out what looks like a wand — "
                "its tip blinking red. Probably worth grabbing.")
        else:
            dim("Just a desk. Cluttered, sad, yours.")
        return

    # Special: look floor in corridor
    if target == "floor" and game.room == "corridor":
        if "goblin_repellent" in ROOMS[game.room]["items"]:
            dim("You crouch down. A dented spray can — 'GOBLIN-B-GON'. "
                "The best-before date is not reassuring. Still, might be useful.")
        else:
            dim("Just scorch marks and bad memories.")
        return

    # Special: look tray in cafeteria
    if target == "tray" and game.room == "cafeteria":
        if "space_cheese" in ROOMS[game.room]["items"]:
            dim("One of the floating trays drifts close. On it sits a glowing wedge "
                "of cheese — warm, humming faintly. Probably edible.")
        else:
            dim("Just empty trays drifting aimlessly. Tragic.")
        return

    # Special: look workbench in engineering
    if target in ("workbench", "bench") and game.room == "engineering":
        if "enchanted_duct_tape" in ROOMS[game.room]["items"]:
            dim("Among the scattered tools, a roll of silver duct tape glows faintly "
                "with runic script. Definitely enchanted. Definitely useful.")
        else:
            dim("Tools, components, and general chaos. Nothing stands out.")
        return

    # Special: look case in armory
    if target == "case" and game.room == "armory":
        if "plasma_sword" in ROOMS[game.room]["items"]:
            dim("Through the crack in the display case you can clearly make out "
                "a plasma sword. Glowing, functional, and technically reachable.")
        else:
            dim("The cracked case is empty. Someone beat you to it.")
        return

    # Special: look window on bridge
    if target == "window" and game.room == "bridge":
        _look_window(game)
        return

    # Special: look at hyperdrive in engineering
    if target == "hyperdrive" and game.room == "engineering":
        if game.check_flag("hyperdrive_fixed"):
            dim("The hyperdrive hums beautifully. Get to the Bridge to ACTIVATE!")
        else:
            dim("Very broken. Needs a Hyperdrive Crystal and duct tape.")
        return

    # Special: look crystal/center/beam in crystal chamber
    if target in ("crystal", "hyperdrive", "center", "beam", "light") and game.room == "crystal_chamber":
        if not game.check_flag("crystal_obtained"):
            dim("A Hyperdrive Crystal, suspended in a containment beam. "
                "Massive. Pulsing. You could TAKE CRYSTAL to attempt extraction.")
        else:
            dim("The containment field is empty.")
        return

    # Special: look sign/wall in crystal chamber
    if target in ("sign", "wall") and game.room == "crystal_chamber":
        dim("The sign reads: 'CAUTION — Crystal removal requires Arcane Aptitude Check (DC 14). "
            "Unauthorized extraction may result in: mild tingling, severe tingling, or death.'")
        return

    # Check NPC
    npc = find_npc_by_alias(game.room, target)
    if npc:
        npc.look(game)
        return

    # Check inventory
    for item in game.inventory:
        if target in item:
            desc = ITEMS.get(item, {}).get("description", "Nothing special.")
            print(f"  {desc}")
            return

    print(f"  You don't see anything notable about '{target}'.")


def _look_window(game):
    info("You press your face against the viewscreen...")
    roll = ask_d20("Perception check — what do you notice?")
    game.set_flag("looked_out_window")

    if roll >= 15:
        success(
            "You spot a small CHARGING CRYSTAL lodged in hull debris outside! "
            "It clinks against the window and tumbles inside!"
        )
        game.add_item("charging_crystal")
        success("Acquired: Arcane Charging Crystal!")
    elif roll >= 8:
        from engine.display import wrap
        print(wrap(
            "  You see the cheese planet. You notice crystal debris floating "
            "near the hull. Look again for a better roll?"
        ))
        get_npc("dracos").say("perception_meh")
        game.set_flag("looked_out_window", False)  # allow retry
    else:
        from engine.display import wrap
        print(wrap("  All you see is cheese. So much cheese. It haunts you."))
        get_npc("dracos").say("perception_fail")
        game.set_flag("looked_out_window", False)


# ─── TAKE ─────────────────────────────────────────────────────────────────────

def cmd_take(game, arg):
    if not arg:
        print("  Take what?")
        return

    # Special: crystal extraction
    if arg in ("crystal", "hyperdrive crystal"):
        if game.room == "crystal_chamber" and not game.check_flag("crystal_obtained"):
            _take_crystal(game)
            return

    # Fuzzy match items in room
    room_items = ROOMS[game.room]["items"]
    matched = None
    for item_id in room_items:
        aliases = ITEMS.get(item_id, {}).get("aliases", [])
        if arg in item_id or arg in item_name(item_id).lower() or arg in aliases:
            matched = item_id
            break

    if not matched:
        print(f"  There's no '{arg}' here to take.")
        return

    # Some items need a roll
    dc, reason = _take_dc(matched)
    if dc > 0:
        info(f"Requires a skill check (DC {dc}).")
        roll = ask_d20(reason)
        if roll < dc and roll != 20:
            if roll == 1:
                danger("You fumble hilariously!")
                game.take_damage(1)
            else:
                print(f"  {C.RED}Needed {dc}, rolled {roll}. Couldn't grab it.{C.RESET}")
            return
        elif roll == 20:
            from engine.display import dragon_says
            dragon_says("Snatched with supernatural finesse. Show-off.")

    room_items.remove(matched)
    game.add_item(matched)
    success(f"Acquired: {item_name(matched)}!")


def _take_dc(item_id):
    """Return (dc, reason) for picking up an item. (0, '') means automatic."""
    DCS = {
        "plasma_sword": (10, "Reaching through cracked glass without cutting yourself"),
        "space_cheese": (8, "Grabbing the cheese before it floats away"),
    }
    return DCS.get(item_id, (0, ""))


def _take_crystal(game):
    info("You reach for the Hyperdrive Crystal...")
    print(f"  {C.BOLD}Arcane Aptitude Check (DC 14){C.RESET}")
    roll = ask_d20("Extracting a powerful magical crystal without exploding")

    if roll >= 14 or roll == 20:
        if roll == 20:
            success("You pluck the crystal with the grace of an archmage!")
            from engine.display import dragon_says
            dragon_says("...I'm actually speechless. That never happens.")
        else:
            success("The field releases the crystal into your hands!")
        game.add_item("hyperdrive_crystal")
        game.set_flag("crystal_obtained")
        success("Acquired: Hyperdrive Crystal!")
        get_npc("dracos").say("crystal_obtained")
    elif roll == 1:
        danger("The containment field ZAPS you violently!")
        game.take_damage(8)
        from engine.display import dragon_says
        dragon_says("I should have mentioned it's electrified. My mistake. Not really.")
    else:
        print(f"  {C.RED}The field repels you. Needed 14, rolled {roll}. Try again.{C.RESET}")
        game.take_damage(2)


# ─── USE ──────────────────────────────────────────────────────────────────────

def cmd_use(game, arg):
    if not arg:
        print("  Use what? (Check inventory with 'i')")
        return

    # Fuzzy match inventory
    matched = _fuzzy_match_inv(game, arg)
    if not matched:
        print(f"  You don't have anything like '{arg}'.")
        return

    # First, check if an active room NPC wants to handle this item
    for npc in get_active_npcs(game.room, game):
        if npc.use_item(game, matched):
            # NPC handled it — check for DRACOS commentary
            _dracos_use_commentary(game, matched, npc)
            return

    # Fall through to generic item handler
    handler = USE_HANDLERS.get(matched)
    if handler:
        handler(game)
    else:
        print(f"  You fiddle with the {item_name(matched)}. Nothing useful happens.")


def _dracos_use_commentary(game, item_id, npc):
    """DRACOS comments on the result of using an item on an NPC."""
    dracos = get_npc("dracos")
    if npc.id == "ghost_chef" and game.check_flag("cafeteria_cleared"):
        if game.check_flag("ghost_appeased"):
            dracos.say("ghost_appeased")
        else:
            dracos.say("ghost_defeated_fight")
    elif npc.id == "goblin_king":
        if game.check_flag("goblins_befriended"):
            dracos.say("goblins_befriended")
        elif game.check_flag("goblins_defeated"):
            dracos.say("goblins_defeated")
    elif npc.id == "turret" and game.check_flag("turret_disabled"):
        dracos.say("turret_destroyed")


# ─── INVENTORY ────────────────────────────────────────────────────────────────

def cmd_inventory(game):
    if not game.inventory:
        print("  Your pockets are tragically empty.")
    else:
        print(f"\n  {C.BOLD}INVENTORY:{C.RESET}")
        for item in game.inventory:
            flag = ""
            if item == "usb_wand" and game.check_flag("wand_charged"):
                flag = f" {C.GREEN}(CHARGED ⚡){C.RESET}"
            print(f"    • {item_name(item)}{flag}")
    print(f"  {C.DIM}HP: {game.hp}/{game.max_hp}{C.RESET}")


# ─── TALK ─────────────────────────────────────────────────────────────────────

def cmd_talk(game, target=""):
    # Find NPC by alias, or grab the first active one
    npc = None
    if target:
        npc = find_npc_by_alias(game.room, target)
    else:
        active = get_active_npcs(game.room, game)
        if active:
            npc = active[0]
        # Also allow talking to DRACOS from bridge
        if game.room == "bridge" and not npc:
            npc = get_npc("dracos")

    if npc:
        npc.talk(game)
    else:
        print("  Nobody here wants to chat.")


# ─── FIGHT ────────────────────────────────────────────────────────────────────

def cmd_fight(game, target=""):
    npc = None
    if target:
        npc = find_npc_by_alias(game.room, target)
    else:
        active = get_active_npcs(game.room, game)
        # Pick first fightable NPC
        for n in active:
            if n.id != "dracos":  # Can't fight the AI
                npc = n
                break

    if npc and npc.is_active(game):
        npc.fight(game)
        # DRACOS commentary after fight
        dracos = get_npc("dracos")
        if npc.id == "ghost_chef" and game.check_flag("cafeteria_cleared"):
            dracos.say("ghost_defeated_fight")
        elif npc.id == "goblin_king" and game.check_flag("goblins_defeated"):
            dracos.say("goblins_defeated")
        elif npc.id == "turret" and game.check_flag("turret_disabled"):
            dracos.say("turret_destroyed")
    else:
        print("  Nothing here to fight. Thankfully.")


# ─── HELP ─────────────────────────────────────────────────────────────────────

def show_help():
    print(f"""
  {C.BOLD}━━━ COMMANDS ━━━{C.RESET}
  {C.CYAN}go [direction]{C.RESET}     Move (north/south/east/west or n/s/e/w)
  {C.CYAN}look{C.RESET}               Look around the room
  {C.CYAN}look [thing]{C.RESET}       Examine something specific
  {C.CYAN}take [item]{C.RESET}        Pick up an item
  {C.CYAN}use [item]{C.RESET}         Use an item from inventory
  {C.CYAN}talk [someone]{C.RESET}     Talk to a character
  {C.CYAN}fight [enemy]{C.RESET}      Attack an enemy
  {C.CYAN}inventory / i{C.RESET}      Check your stuff
  {C.CYAN}activate{C.RESET}           Fire the hyperdrive (Bridge only)
  {C.CYAN}launch{C.RESET}             Launch escape pod (Escape Pod Bay)
  {C.CYAN}status{C.RESET}             Check your HP
  {C.CYAN}help{C.RESET}               This screen
  {C.CYAN}quit{C.RESET}               Give up

  {C.BOLD}━━━ DICE ━━━{C.RESET}
  {C.YELLOW}d20{C.RESET}   Skill checks, attacks, persuasion, EVERYTHING
  {C.YELLOW}2d6{C.RESET}   Damage, healing, loot quality
  {C.DIM}Nat 20 = Critical Success  |  Nat 1 = Critical Failure{C.RESET}

  {C.BOLD}━━━ GOAL ━━━{C.RESET}
  {C.DIM}Find the Hyperdrive Crystal → Fix the Hyperdrive → Activate from Bridge{C.RESET}
  {C.DIM}Or find Escape Pods for... an alternative ending.{C.RESET}
""")


# ─── Helpers ──────────────────────────────────────────────────────────────────

def _fuzzy_match_inv(game, word):
    """Find an inventory item matching a partial word."""
    for item in game.inventory:
        if word in item:
            return item
    return None
