"""
item_uses.py — Handlers for generic item use (no active NPC target).

If an NPC is present and wants to handle the item, it gets first
chance via npc.use_item(). These handlers are the fallback.
"""

from engine.display import info, dim, success, danger, alert


def _use_note(game):
    dim(
        "Your own handwriting stares back at you: "
        "'Don't trust the concierge. The key is in the piano. "
        "Get out before 4 AM!'"
    )
    dim("You wrote this. You just can't remember when.")


def _use_mirror_shard(game):
    if game.room == "north_corridor" and not game.check_flag("room_316_unlocked"):
        info("You jam the shard into the keycard reader...")
        from engine.dice import ask_d20
        roll = ask_d20("Bypassing a keycard lock with a mirror shard")
        if roll >= 13 or roll == 20:
            success("The reader sparks and the door clicks open!")
            game.set_flag("room_316_unlocked")
            if roll == 20:
                from npcs import get_npc
                get_npc("virgil").say("shard_crit")
        else:
            print(f"  The reader beeps angrily. Not quite.")
    elif game.room == "room_316" and not game.check_flag("box_opened"):
        info("You use the shard to pry open the locked box...")
        from engine.dice import ask_d20
        roll = ask_d20("Prying open a locked box")
        if roll >= 8 or roll == 20:
            success("The latch pops. Your badge is inside!")
            game.set_flag("box_opened")
            from data.rooms import ROOMS
            ROOMS["room_316"]["items"].append("investigators_badge")
        else:
            danger("The shard snaps! You cut your hand.")
            game.take_damage(2)
    else:
        dim("Sharp but no obvious use here right now.")


def _use_master_keycard(game):
    if game.room == "north_corridor" and not game.check_flag("room_316_unlocked"):
        success("The keycard reader beeps green. Room 316 is unlocked.")
        game.set_flag("room_316_unlocked")
        from npcs import get_npc
        get_npc("virgil").say("keycard_used")
    else:
        dim("No keycard reader to use here.")


def _use_bandage(game):
    healed = min(8, game.max_hp - game.hp)
    if healed > 0:
        game.heal(8)
        game.remove_item("bandage")
    else:
        dim("You're already at full health. Save it.")


def _use_guest_ledger(game):
    info("You flip through the guest register...")
    dim(
        "Room 316: checked in under 'G. Harmon' — but the notes column "
        "reads: 'Package delivery confirmed. No record required.' "
        "The handwriting is VIRGIL's nightly print-out. "
        "Someone used the hotel's system to hide a meeting."
    )
    game.set_flag("ledger_read")


def _use_investigators_badge(game):
    dim(
        "Your PI license. Photo, name, number — all yours. "
        "Someone stole it, identified you, and put it back. "
        "That means they know exactly who you are."
    )


def _use_whiskey_glass(game):
    dim(
        "A nice glass but you'd need an actual lab to lift prints. "
        "Take it with you — it could be evidence if the right person sees it."
    )
    if game.check_flag("maid_talked"):
        alert("HINT: The night maid might recognize those prints.")


USE_HANDLERS = {
    "note":                _use_note,
    "mirror_shard":        _use_mirror_shard,
    "master_keycard":      _use_master_keycard,
    "bandage":             _use_bandage,
    "guest_ledger":        _use_guest_ledger,
    "investigators_badge": _use_investigators_badge,
    "whiskey_glass":       _use_whiskey_glass,
}
