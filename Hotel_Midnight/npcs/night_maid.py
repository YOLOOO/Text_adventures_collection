"""
night_maid.py — Rosa, the night-shift maid hiding in the linen closet.

She witnessed something she shouldn't have. She's terrified —
of VIRGIL more than anything else. Won't talk easily. Can be
calmed with patience or the bandage (showing you need help too).
"""

from npcs.base import NPC
from engine.display import info, dim, success, alert, danger


class NightMaid(NPC):
    id = "night_maid"
    name = "Rosa"
    aliases = ["maid", "rosa", "woman", "housekeeper", "staff"]

    DIALOG = {
        "look": (
            "A young woman in a housekeeping uniform, pressed "
            "against the back shelves. Her eyes are very wide."
        ),
        "first_encounter": (
            "She flinches when she sees you. "
            "'Please — I didn't see anything. Please just go.'"
        ),
        "talk_success": (
            "She takes a breath. 'The man in 316 — he was alive at midnight. "
            "I brought extra towels. He was on the phone, angry. Said "
            "the name Harmon wasn't his.' She grips the shelf. "
            "'At 2:30, I saw Mr. VIRGIL — I mean the man who programs it, "
            "the owner — on the floor. He had a key. He went into 316. "
            "Ten minutes later he was gone and so was... so was the guest.' "
            "She won't meet your eyes. 'I don't know where the guest went.'"
        ),
        "talk_meh": (
            "'I can't. He'll know I talked. The whole system — "
            "it logs everything. He can see the logs.'"
        ),
        "talk_fail": (
            "She shakes her head. She won't say a word."
        ),
        "bandage_response": (
            "'Your hand.' She looks at the blood on your palm. "
            "Something shifts in her expression. "
            "She takes the bandage and wraps it for you. Then she talks."
        ),
        "repeat": (
            "'I've said everything I can. Please — just get out. "
            "Take me with you if you can.'"
        ),
    }

    def is_active(self, game):
        return True

    def describe(self, game, first_visit):
        if not game.check_flag("maid_found"):
            dim("Something shifts behind the bottom shelf.")
            game.set_flag("maid_found")

    def look(self, game):
        dim(self.DIALOG["look"])
        return True

    def talk(self, game):
        if not game.check_flag("maid_found"):
            game.set_flag("maid_found")

        if game.check_flag("maid_talked"):
            print(f"  {self.DIALOG['repeat']}")
            return True

        if not game.check_flag("maid_found"):
            print(f"  {self.DIALOG['first_encounter']}")
            return True

        info("You crouch down and speak quietly...")
        from engine.dice import ask_d20
        roll = ask_d20("Earning trust — she's terrified of VIRGIL")

        if roll >= 14 or roll == 20:
            print(f"  {self.DIALOG['talk_success']}")
            game.set_flag("maid_talked")
            alert("HINT: The owner controls VIRGIL. The ledger has his name.")
            if roll == 20:
                success("She gives you a spare keycard she found!")
                if not game.has("master_keycard"):
                    game.add_item("master_keycard")
        elif roll >= 7:
            print(f"  {self.DIALOG['talk_meh']}")
            alert("HINT: She might open up if you show her you need help too.")
        else:
            print(f"  {self.DIALOG['talk_fail']}")

        return True

    def use_item(self, game, item_id):
        if item_id == "bandage" and not game.check_flag("maid_talked"):
            print(f"  {self.DIALOG['bandage_response']}")
            game.remove_item("bandage")
            game.heal(5)
            # Now she talks — skip straight to the story
            print(f"  {self.DIALOG['talk_success']}")
            game.set_flag("maid_talked")
            alert("HINT: The owner controls VIRGIL. Check the guest ledger.")
            return True
        return False

    def fight(self, game):
        danger("She screams. VIRGIL immediately announces a security alert.")
        game.take_damage(3)
        return True
