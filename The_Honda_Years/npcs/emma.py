"""
emma.py — Emma, the younger daughter (~7).

Weirdly wise. Drawing things she shouldn't understand.
Her observation breaks the tension — not by solving it,
but by naming it so plainly that the only response is to laugh
or cry or both.
"""

from npcs.base import NPC
from engine.display import dim, info, success, alert, wrap, ask_choice
import textwrap


class Emma(NPC):
    id = "emma"
    name = "Emma"
    aliases = ["emma", "daughter", "girl", "little one", "em"]

    def is_active(self, game):
        return True

    def describe(self, game, first_visit):
        if game.room == "back_seat" and first_visit:
            dim(
                "Emma is drawing in her notebook. "
                "She has a system — colored pencils sorted by warmth, "
                "coolest on the left. "
                "She got this from nobody in your family."
            )
        elif game.room == "rest_stop" and first_visit:
            dim("Emma is drawing on a picnic table.")
        elif game.room == "breakdown" and first_visit:
            dim(
                "Emma is examining a piece of Wyoming gravel "
                "like it might be a fossil."
            )

    def look(self, game):
        dim(
            "Seven years old. Brown hair. A green backpack containing: "
            "four notebooks, a rock collection, "
            "and an apple she will not eat. "
            "She looks like she's listening even when she isn't."
        )
        return True

    def fight(self, game):
        dim("Emma looks up from her drawing.")
        dim("'You're being loud.'")
        return True

    def use_item(self, game, item_id):
        if item_id == "emma_drawing":
            info(wrap("'You're looking at it.' She doesn't look up."))
            return True
        return False

    def talk(self, game):
        room = game.room

        # First real conversation — Emma's famous question
        if not game.check_flag("emma_observation") and room == "back_seat":
            game.set_flag("emma_observation", True)
            _emma_says("Daddy. Are you and Mommy having a fight?")
            info(wrap(
                "She says it the same way she asks "
                "if the library is open on Sundays. "
                "Entirely matter-of-fact."
            ))
            choice = ask_choice(
                "You say:",
                [
                    "We're having a big conversation.",
                    "No, sweetheart. Everything's fine.",
                    "Why do you ask?",
                ]
            )
            if choice == 1:
                _emma_says("Is a big conversation different from a fight?")
                dim("She goes back to drawing.")
                info(wrap("There's no good answer to that."))
                game.honest()
            elif choice == 2:
                _emma_says("Okay.")
                dim(
                    "She doesn't believe you. "
                    "She draws something and shows it to Drew. "
                    "He shrugs."
                )
                game.deflect()
            else:
                _emma_says("You keep doing the quiet thing.")
                dim(
                    "'The quiet thing.' "
                    "You didn't know you had a thing. "
                    "She's seven."
                )
                game.honest()
            return True

        # Emma gives you her drawing
        if not game.check_flag("emma_drawing_given") and game.turns > 20:
            game.set_flag("emma_drawing_given", True)
            _emma_says("Here.")
            info(wrap(
                "She tears a page from her notebook "
                "and passes it over the seat to you."
            ))
            success("Emma gives you her drawing.")
            game.add_item("emma_drawing")
            return True

        # Breakdown observation — the tension-breaker
        if room == "breakdown" and not game.check_flag("breakdown_emma"):
            game.set_flag("breakdown_emma", True)
            _emma_says("Do you think the car is sad?")
            info(wrap("She's looking at the steaming Honda."))
            _emma_says(
                "It got us all the way here though. "
                "Maybe it just needed a rest."
            )
            dim("She goes back to examining her gravel.")
            info(wrap(
                "You think about how long it took you both "
                "to understand that's what this trip actually was."
            ))
            game.honest()
            return True

        _emma_says("I'm drawing.")
        dim("She is very much drawing.")
        return True


def _emma_says(text):
    from engine.display import C, WRAP_WIDTH
    filled = textwrap.fill(
        text, width=WRAP_WIDTH - 2, subsequent_indent="  "
    )
    print(f"\n  {C.GREEN}{C.BOLD}Emma:{C.RESET}")
    print(f"  {C.GREEN}\"{filled}\"{C.RESET}")
