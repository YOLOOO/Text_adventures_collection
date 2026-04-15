"""
mr_chen.py — Mr. Chen, insomniac guest in Room 312.

A retired archivist who doesn't sleep much and notices everything.
He saw someone in the corridor earlier. Can be an ally if approached
with patience. Can be offended if rushed.
"""

from npcs.base import NPC
from engine.display import info, dim, success, alert


class MrChen(NPC):
    id = "mr_chen"
    name = "Mr. Chen"
    aliases = ["chen", "man", "guest", "old man", "archivist"]

    DIALOG = {
        "look": (
            "A slight man in his seventies. Dressing gown, reading glasses, "
            "cup of tea. He doesn't look afraid — he looks like someone "
            "who has been waiting for something interesting to happen."
        ),
        "talk_success": (
            "'I heard you earlier. Quite a crash.' He sets down his book. "
            "'At 2:40, a man in a grey coat came from the north corridor "
            "and took the stairs down. He was carrying something flat. "
            "A case, or an envelope.' He pauses. 'The concierge passed him "
            "in the hallway and said nothing. Not even a good evening.'"
        ),
        "talk_meh": (
            "'You look terrible.' He sips his tea. "
            "'I mind my own business, normally. "
            "But I will say — Room 316 has had unusual traffic tonight.'"
        ),
        "talk_fail": (
            "'I don't know you. I don't know what happened. "
            "I suggest you speak to the concierge.' "
            "He returns to his book with finality."
        ),
        "talk_repeat": (
            "'I've told you what I saw. The rest is your problem.'"
        ),
    }

    def is_active(self, game):
        return True  # Always present

    def describe(self, game, first_visit):
        if first_visit and not game.check_flag("chen_helped"):
            alert("Mr. Chen looks up from his book as you enter.")

    def look(self, game):
        dim(self.DIALOG["look"])
        return True

    def talk(self, game):
        if game.check_flag("chen_helped"):
            dim(self.DIALOG["talk_repeat"])
            return True

        info("You approach Mr. Chen...")
        from engine.dice import ask_d20
        roll = ask_d20("Reading the room — will he talk to you?")

        if roll >= 12 or roll == 20:
            print(f"  {self.DIALOG['talk_success']}")
            game.set_flag("chen_helped")
            alert("HINT: Check the north corridor and manager's office.")
        elif roll >= 6:
            print(f"  {self.DIALOG['talk_meh']}")
            alert("HINT: Room 316 is worth investigating.")
        else:
            print(f"  {self.DIALOG['talk_fail']}")

        return True

    def fight(self, game):
        dim("He's a seventy-year-old man reading a book. Absolutely not.")
        return False
