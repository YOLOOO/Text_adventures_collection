"""
drew.py — Drew, the teenage son (~15).

Headphones always on. Total apparent indifference to his parents'
crisis. Comic relief. Occasionally cuts through with accidental
insight — not because he's wise, but because he's fifteen and
hasn't learned to be diplomatic about obvious things.
"""

from npcs.base import NPC
from engine.display import dim, info, success, wrap, ask_choice
import textwrap


class Drew(NPC):
    id = "drew"
    name = "Drew"
    aliases = ["drew", "son", "boy", "teenager", "teen", "kid"]

    def is_active(self, game):
        return True

    def describe(self, game, first_visit):
        if game.room == "back_seat" and first_visit:
            dim(
                "Drew has his headphones on. "
                "He is either asleep or deeply committed "
                "to appearing asleep."
            )
        elif game.room == "rest_stop" and first_visit:
            dim(
                "Drew is buying things from the vending machine. "
                "Everything from the vending machine."
            )
        elif game.room == "breakdown" and first_visit:
            dim(
                "Drew is on his phone. Signal is two bars. "
                "He's making it work."
            )

    def look(self, game):
        dim(
            "Fifteen. Headphones. A hoodie he's been wearing "
            "since Tuesday. He looks exactly like someone who "
            "doesn't want to be looked at."
        )
        return True

    def fight(self, game):
        _drew_says("Dad. I'm literally not doing anything.")
        return True

    def use_item(self, game, item_id):
        return False

    def talk(self, game):
        if not game.check_flag("drew_spoke"):
            game.set_flag("drew_spoke", True)
            _drew_says("What.")
            info(wrap("He pulls one headphone aside. One."))
            choice = ask_choice(
                "You say:",
                [
                    "Just checking in. How are you doing?",
                    "How are you doing with all this — the trip?",
                    "Nothing. Never mind.",
                ]
            )
            if choice == 1:
                _drew_says(
                    "I'm fine. Can I put my headphone back?"
                )
                dim("He puts his headphone back.")
            elif choice == 2:
                _drew_says(
                    "It's a road trip. We're in a car. It's fine."
                )
                info(wrap(
                    "He says it with complete sincerity. "
                    "Drew has no idea anything is wrong. "
                    "Or he has decided, at fifteen, not to engage with it. "
                    "Honestly either seems fine."
                ))
            else:
                _drew_says("Okay.")
                dim("One headphone back on.")
            return True

        if not game.check_flag("drew_noticed") and game.check_flag("affair_revealed"):
            game.set_flag("drew_noticed", True)
            _drew_says("Hey. Are you guys okay?")
            info(wrap(
                "Both headphones off. He's watching you "
                "in the rearview mirror."
            ))
            _drew_says("Like, actually okay. Not road-trip okay.")
            choice = ask_choice(
                "You say:",
                [
                    "We're working on some things. Thanks for asking.",
                    "Yeah, we're fine.",
                ]
            )
            if choice == 1:
                _drew_says("Okay. Cool.")
                dim("He means it. Headphones back on.")
                success("Drew noticed. That counts for something.")
                game.honest()
            else:
                _drew_says("Okay.")
                dim("He knows. He lets it go. Good kid.")
            return True

        _drew_says("Still here.")
        dim("He points at his headphones.")
        return True


def _drew_says(text):
    from engine.display import C, WRAP_WIDTH
    filled = textwrap.fill(
        text, width=WRAP_WIDTH - 2, subsequent_indent="  "
    )
    print(f"\n  {C.BLUE}{C.BOLD}Drew:{C.RESET}")
    print(f"  {C.BLUE}\"{filled}\"{C.RESET}")
