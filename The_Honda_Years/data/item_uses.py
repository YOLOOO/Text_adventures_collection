"""
item_uses.py — USE handlers for The Honda Years.

Called by cmd_use() after NPCs get first refusal.
Each item is a piece of emotional context, not a puzzle piece.
Reading them honestly (not just picking them up) affects the ending.
"""

from engine.display import info, dim, success, danger, alert, wrap


def _use_coffee(game):
    if not game.check_flag("coffee_used"):
        game.set_flag("coffee_used", True)
        info(wrap(
            "You drink it. It's bad. You drink it anyway. "
            "Something about having something warm in your hands "
            "makes the next few miles feel possible."
        ))
    else:
        dim("The coffee is long gone. You still have the cup for some reason.")


def _use_therapy_notes(game):
    if not game.check_flag("therapy_notes_read"):
        game.set_flag("therapy_notes_read", True)
        game.honest()
        info(wrap(
            "Three months of weekly sessions, "
            "compressed into two dozen pages. "
            "Homework assignments in Dr. Reyes's handwriting. "
            "Sarah's answers underneath."
        ))
        print()
        info(wrap(
            "Week three: 'Name something your partner does "
            "that makes you feel unseen.' "
            "Her answer is two sentences long and very specific."
        ))
        print()
        info(wrap(
            "Week seven: 'Name one thing you need "
            "that your partner doesn't know about.' "
            "Her answer is one word."
        ))
        print()
        danger("Honesty.")
        print()
        dim(wrap(
            "Not about the almost-affair. Not about February. "
            "About the hundred smaller things you've been "
            "packaging as 'fine' for years."
        ))
    else:
        dim(
            "Week seven. One word. "
            "You already know what you need to do with that."
        )


def _use_gas_receipt(game):
    if not game.check_flag("gas_receipt_read"):
        game.set_flag("gas_receipt_read", True)
        info(wrap(
            "February 14. You were supposed to be in Denver "
            "at a conference that ended at noon."
        ))
        print()
        info(wrap(
            "Instead you drove north. No plan. "
            "Just the highway and the fact that something "
            "had been wrong for months and you didn't know "
            "what to do about it."
        ))
        print()
        dim(wrap(
            "You ended up at a Shell station in Casper. "
            "You sat in the parking lot for forty minutes. "
            "You filled the tank. You drove home. "
            "Nothing happened."
        ))
        print()
        alert(wrap(
            "But Sarah has been carrying the silence since then. "
            "She found the receipt in the console. "
            "She never asked about it. "
            "You need to tell her the whole story."
        ))
    else:
        dim(
            "Casper, WY. Forty minutes in a parking lot. "
            "Nothing happened. "
            "You need to say that out loud."
        )


def _use_emma_drawing(game):
    if not game.check_flag("emma_drawing_read"):
        game.set_flag("emma_drawing_read", True)
        game.honest()
        info(wrap(
            "You look at it properly. "
            "The two figures in front are clearly you and Sarah — "
            "she drew Sarah's sunglasses. "
            "The two in back are waving at something you can't see."
        ))
        print()
        dim(wrap(
            "She drew this during the first day. "
            "She titled it 'We are going on an adventure.' "
            "She's seven. She sees what she sees."
        ))
    else:
        info(wrap(
            "Four stick figures. "
            "The two in front facing away from each other. "
            "'We are going on an adventure.'"
        ))


USE_HANDLERS = {
    "vending_coffee":  _use_coffee,
    "therapy_notes":   _use_therapy_notes,
    "gas_receipt":     _use_gas_receipt,
    "emma_drawing":    _use_emma_drawing,
}
