"""
endings.py — Endings for The Honda Years.

Endings branch on:
  - honest_choices count (0-N)
  - affair_revealed flag
  - motel_talk flag
  - items read (therapy_notes, gas_receipt, emma_drawing)

No dice. The ending you get is the one you earned.
"""

from engine.display import (
    wrap, hr, title_print, slow_print, success, danger,
    radio_says, info, dim, alert, C
)
import textwrap

TURN_LIMIT = 80


# ─── Time-out ending ──────────────────────────────────────────────────────────

def ending_ran_out_of_road(game):
    """Too many turns without arriving — you kept driving."""
    game.game_over = True
    game.won = False
    game.ending = "ran_out_of_road"
    print()
    hr()
    title_print("ENDING: Miles and Miles")
    slow_print(wrap(
        "Portland was right there. "
        "Three days, 2,100 miles, and you kept driving."
    ), 0.02)
    print()
    slow_print(wrap(
        "Sarah eventually says: "
        "'Are you going to drive us into the ocean?' "
        "She's half-joking. You're not sure about the other half."
    ), 0.02)
    print()
    dim(wrap(
        "The kids are asleep. The radio is on. "
        "The road goes on in both directions."
    ))
    radio_says(
        "This is WKND. We'll be here when you're ready to stop."
    )
    print(f"\n  {C.DIM}THE END (Still Driving — {game.turns} turns){C.RESET}")
    hr()


# ─── Portland ending (main branch) ───────────────────────────────────────────

def ending_portland(game):
    """Player arrives in Portland. Branches on what they did."""
    game.game_over = True
    game.won = True

    honest      = game.flags.get("honest_choices", 0)
    revealed    = game.check_flag("affair_revealed")
    motel_talk  = game.check_flag("motel_talk")
    items_read  = sum([
        game.check_flag("therapy_notes_read"),
        game.check_flag("gas_receipt_read"),
        game.check_flag("emma_drawing_read"),
    ])

    print()
    hr()

    if revealed and motel_talk and honest >= 4:
        _ending_fresh_start(game, items_read)
    elif revealed and honest >= 2:
        _ending_still_figuring(game, items_read)
    elif motel_talk and honest >= 2:
        _ending_holding_pattern(game, items_read)
    elif honest <= 1:
        _ending_two_rooms(game)
    else:
        _ending_open_question(game, items_read)

    hr()


# ─── Ending subbranches ───────────────────────────────────────────────────────

def _ending_fresh_start(game, items_read):
    game.ending = "fresh_start"
    title_print("⭐  ENDING: Portland  ⭐")
    slow_print(wrap(
        "The Honda pulls into the rental driveway at 4 PM. "
        "Drew is already asking about wifi. "
        "Emma names the house before anyone else can."
    ), 0.02)
    print()
    slow_print(wrap(
        "Sarah sits for a moment after you park. "
        "Hands in her lap. Not the waiting-for-something quiet. "
        "A different kind."
    ), 0.02)
    print()
    _sarah_line(
        "I don't know what we are right now. "
        "But I know we talked. "
        "That's more than last month."
    )
    print()
    if items_read >= 2:
        slow_print(wrap(
            "You have Emma's drawing in your jacket pocket. "
            "Four stick figures going on an adventure. "
            "She wasn't wrong."
        ), 0.02)
        print()
    slow_print(wrap(
        "You don't know what comes next. "
        "You know you're here. "
        "You know she's still in the car."
    ), 0.02)
    radio_says("WKND. End of the road. You made it.")
    print(f"\n  {C.BOLD}{C.GREEN}THE END (Fresh Start — {game.turns} turns){C.RESET}")


def _ending_still_figuring(game, items_read):
    game.ending = "still_figuring"
    title_print("ENDING: Work in Progress")
    slow_print(wrap(
        "Portland. Three days, 2,100 miles. "
        "February is out now — the parking lot, the receipt, "
        "the forty minutes of nothing that felt like everything."
    ), 0.02)
    print()
    slow_print(wrap(
        "Sarah heard it. Let it sit. Hasn't decided yet "
        "what it means for the two of you."
    ), 0.02)
    print()
    slow_print(wrap(
        "You unpack the car in near-silence. "
        "But it's a different silence. Lighter. "
        "Or maybe you're just tired."
    ), 0.02)
    if items_read >= 1:
        print()
        dim(wrap(
            "You know what she wrote in week seven. "
            "You're working on it."
        ))
    print(
        f"\n  {C.GREEN}THE END (Still Figuring It Out — {game.turns} turns){C.RESET}"
    )


def _ending_holding_pattern(game, items_read):
    game.ending = "holding_pattern"
    title_print("ENDING: To Be Continued")
    slow_print(wrap(
        "Portland. You had the motel conversation. "
        "It wasn't everything, but it was something real. "
        "February is still unfinished. "
        "It will need another night."
    ), 0.02)
    print()
    slow_print(wrap(
        "The kids run into the rental house. "
        "Sarah follows. "
        "You stand by the car a moment longer."
    ), 0.02)
    if items_read >= 1:
        print()
        slow_print(wrap(
            "Emma's drawing is in your bag. "
            "You know she was watching the whole time."
        ), 0.02)
    print(
        f"\n  {C.YELLOW}THE END (To Be Continued — {game.turns} turns){C.RESET}"
    )


def _ending_two_rooms(game):
    game.ending = "two_rooms"
    title_print("ENDING: Two Rooms")
    slow_print(wrap(
        "Portland. You made it. "
        "2,100 miles and you didn't say anything that mattered."
    ), 0.02)
    print()
    slow_print(wrap(
        "Over dinner the first night, Sarah checks her phone "
        "and mentions that Dr. Reyes has a Thursday slot open. "
        "'If we want to keep going,' she says. "
        "She says it very carefully."
    ), 0.02)
    print()
    danger(
        "You are, more or less, back where you started."
    )
    radio_says(
        "WKND. The road goes on in both directions. "
        "You know where you parked."
    )
    print(f"\n  {C.RED}THE END (Two Rooms — {game.turns} turns){C.RESET}")


def _ending_open_question(game, items_read):
    game.ending = "open_question"
    title_print("ENDING: Open Road")
    slow_print(wrap(
        "Portland. You both tried, in your way. "
        "It's not resolved. It was never going to be resolved "
        "in 2,100 miles."
    ), 0.02)
    print()
    slow_print(wrap(
        "But you're standing in the same driveway, "
        "looking at the same rental house, "
        "and you both still want to walk through the door."
    ), 0.02)
    print()
    if items_read >= 2:
        slow_print(wrap(
            "You have Emma's drawing. "
            "That counts for something."
        ), 0.02)
    print(
        f"\n  {C.YELLOW}THE END (Open Question — {game.turns} turns){C.RESET}"
    )


# ─── Shared helper ────────────────────────────────────────────────────────────

def _sarah_line(text):
    filled = textwrap.fill(
        text, width=58 - 2, subsequent_indent="  "
    )
    print(f"\n  {C.MAGENTA}{C.BOLD}Sarah:{C.RESET}")
    print(f"  {C.MAGENTA}\"{filled}\"{C.RESET}")
