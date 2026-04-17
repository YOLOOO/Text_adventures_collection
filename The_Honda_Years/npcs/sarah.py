"""
sarah.py — Sarah, Mike's wife.

Eight weeks of couples therapy. An almost-affair that wasn't really
an affair but has reframed the entire marriage. She booked this trip
and called it a reset. She hasn't said what they're resetting to.

Her arc across the trip:
  front_seat  — controlled distance; waiting for you to start
  rest_stop   — first real moment out of the car
  motel       — alone for the first time; the real conversation begins
  breakdown   — no choice but to be present; the affair comes out
  final_miles — aftermath; something has shifted
"""

from npcs.base import NPC
from engine.display import dim, info, success, alert, danger, wrap, ask_choice
import textwrap


class Sarah(NPC):
    id = "sarah"
    name = "Sarah"
    aliases = ["sarah", "wife", "her", "woman", "spouse"]

    def is_active(self, game):
        return True

    def describe(self, game, first_visit):
        if game.room == "front_seat":
            if first_visit:
                return  # Covered in room description
            elif game.check_flag("affair_revealed"):
                dim("Sarah is watching the road. Her hands are still.")
            elif game.check_flag("motel_talk"):
                dim("Sarah is quiet in a different way now.")
            else:
                dim("Sarah has her sunglasses on.")
        elif game.room == "motel_kearney" and first_visit:
            dim("Sarah is sitting on the edge of the bed, shoes off.")
        elif game.room == "rest_stop" and first_visit:
            dim(
                "Sarah is leaning against the car, "
                "coffee in hand, looking at the horizon."
            )
        elif game.room == "breakdown" and first_visit:
            dim(
                "Sarah is standing a few feet from the Honda, "
                "arms crossed, looking at the steam."
            )
        elif game.room == "final_miles" and first_visit:
            dim("Sarah has her window down. Oregon air.")

    def look(self, game):
        dim(
            "She looks like she slept badly — "
            "which she did, which you know "
            "because you were both awake at 3 AM "
            "not talking about it."
        )
        return True

    def fight(self, game):
        _sarah_says("Not in front of the kids.")
        game.deflect()
        return True

    def use_item(self, game, item_id):
        if item_id == "therapy_notes" and game.room == "motel_kearney":
            _sarah_says("You read it.")
            info(wrap("It's not a question."))
            if not game.check_flag("therapy_notes_read"):
                from data.item_uses import _use_therapy_notes
                _use_therapy_notes(game)
            _sarah_says(
                "Week seven. Do you understand now "
                "why I needed you to just be honest? "
                "Not about her. About everything else."
            )
            game.set_flag("therapy_mentioned", True)
            game.honest()
            return True
        if item_id == "gas_receipt":
            _sarah_says("I found that months ago.")
            info(wrap("She's been waiting for you to say something."))
            if not game.check_flag("gas_receipt_read"):
                from data.item_uses import _use_gas_receipt
                _use_gas_receipt(game)
            return True
        if item_id == "emma_drawing":
            _sarah_says("She gave that to you?")
            dim("A small, surprised smile.")
            game.honest()
            return True
        return False

    def talk(self, game):
        room = game.room
        if room == "front_seat":
            return self._talk_front_seat(game)
        elif room == "rest_stop":
            return self._talk_rest_stop(game)
        elif room == "motel_kearney":
            return self._talk_motel(game)
        elif room == "breakdown":
            return self._talk_breakdown(game)
        elif room == "final_miles":
            return self._talk_final_miles(game)
        else:
            _sarah_says("Not here.")
            return True

    # ─── Front Seat ───────────────────────────────────────────────────────

    def _talk_front_seat(self, game):
        if not game.check_flag("sarah_met_properly"):
            game.set_flag("sarah_met_properly", True)
            _sarah_says("Good morning.")
            info(wrap(
                "She says it like it might not be. "
                "You've been driving for forty minutes in silence."
            ))
            choice = ask_choice(
                "How do you respond?",
                [
                    "Good morning. How are you feeling about the trip?",
                    "Did you get the hotel confirmation sorted?",
                    "I've been thinking about what Dr. Reyes said last week.",
                ]
            )
            if choice == 1:
                _sarah_says(
                    "I'm fine. I'm always fine. "
                    "That's sort of the whole problem, isn't it."
                )
                dim("She turns back to the window.")
                game.honest()
            elif choice == 2:
                _sarah_says(
                    "It's in your email. Same as when you asked yesterday."
                )
                dim("Small damage. She looks at her phone.")
                game.deflect()
            else:
                _sarah_says(
                    "You're going to bring up therapy while you're doing "
                    "seventy on the 80. Okay."
                )
                game.set_flag("therapy_mentioned", True)
                game.honest()
            return True

        if game.check_flag("motel_talk") and not game.check_flag("affair_revealed"):
            return self._talk_february_prompt(game)

        if game.check_flag("affair_revealed"):
            _sarah_says(
                "I believe you. I think I believed you "
                "before I heard it. "
                "I just needed to hear it."
            )
            game.honest()
            return True

        _sarah_says("There's a rest stop in about forty miles. STOP to pull over.")
        return True

    def _talk_february_prompt(self, game):
        _sarah_says(
            "February 14. "
            "You're going to tell me what that actually was."
        )
        info(wrap("Somewhere between a question and a statement."))
        choice = ask_choice(
            "What do you say?",
            [
                "I drove to Wyoming. Sat in a parking lot for forty "
                "minutes. That's the whole story.",
                "It wasn't what you think it was.",
                "I don't want to do this while I'm driving.",
            ]
        )
        if choice == 1:
            game.set_flag("affair_revealed", True)
            _sarah_says("You drove to Wyoming and sat in a parking lot.")
            info(wrap("A long pause. The longest since Chicago."))
            _sarah_says(
                "I've been carrying something terrible for six months. "
                "And that's the whole story."
            )
            success("Sarah exhales. The car feels different.")
            game.heal(3)
            game.honest()
        elif choice == 2:
            _sarah_says(
                "I know what I thought it was. "
                "That's why I need to know what it was."
            )
            game.deflect()
        else:
            _sarah_says("We're running out of road, Mike.")
            game.deflect()
        return True

    # ─── Rest Stop ────────────────────────────────────────────────────────

    def _talk_rest_stop(self, game):
        if not game.check_flag("iowa_stop_done"):
            _sarah_says("Finally. Out of the car.")
            info(wrap(
                "She stretches her arms up. "
                "Drew has already disappeared toward the vending machine. "
                "Emma is drawing on a picnic table."
            ))
            choice = ask_choice(
                "What do you say?",
                [
                    "I'm glad we're doing this. The trip. "
                    "All of it.",
                    "We should check the tire pressure.",
                    "I've been thinking about us.",
                ]
            )
            if choice == 1:
                _sarah_says(
                    "It was the only thing I could think of. "
                    "Putting enough miles between us and home. "
                    "Seeing if we still —"
                )
                dim("She doesn't finish the sentence.")
                game.honest()
                game.set_flag("iowa_stop_done", True)
            elif choice == 2:
                _sarah_says("The tires are fine, Mike.")
                dim("She walks to the vending machine without looking back.")
                game.deflect()
                game.set_flag("iowa_stop_done", True)
            else:
                _sarah_says(
                    "I know. I can tell by the way you keep "
                    "starting sentences and stopping."
                )
                game.honest()
                game.set_flag("iowa_stop_done", True)
            return True

        _sarah_says("We should keep moving. WEST to continue.")
        return True

    # ─── Motel ────────────────────────────────────────────────────────────

    def _talk_motel(self, game):
        if not game.check_flag("motel_fight") and not game.check_flag("motel_talk"):
            _sarah_says("Okay. Kids are in their room. Just us.")
            info(wrap(
                "This is what you've been building toward "
                "since Chicago. Or avoiding."
            ))
            choice = ask_choice(
                "How do you start?",
                [
                    "I know I've been avoiding the real conversation. "
                    "I'm done avoiding it.",
                    "How was the drive today? That rest stop was something.",
                    "I want to talk about February.",
                ]
            )
            if choice == 1:
                _sarah_says(
                    "Eight weeks of therapy and that's the first "
                    "actually honest thing you've said to me. "
                    "You know that?"
                )
                dim("Not cruel. Just true.")
                game.honest()
                game.set_flag("motel_talk", True)
                game.heal(2)
                return True
            elif choice == 2:
                _sarah_says(
                    "We're not talking about the rest stop."
                )
                dim("She picks up her phone. The conversation is over.")
                game.deflect()
                game.set_flag("motel_fight", True)
                game.set_flag("motel_night_done", True)
                return True
            else:
                _sarah_says("Finally.")
                game.honest()
                game.set_flag("motel_talk", True)
                game.heal(2)
                return True

        if game.check_flag("motel_talk") and not game.check_flag("affair_revealed"):
            _sarah_says("February. Tell me.")
            choice = ask_choice(
                "The truth is:",
                [
                    "I drove north instead of south. Ended up in Wyoming. "
                    "Sat in a parking lot. Nothing happened.",
                    "I needed space. I handled it badly.",
                    "It's complicated.",
                ]
            )
            if choice == 1:
                game.set_flag("affair_revealed", True)
                game.set_flag("motel_night_done", True)
                _sarah_says(
                    "You drove to Wyoming and sat in a parking lot."
                )
                info(wrap(
                    "She says it like she's testing the weight of it."
                ))
                _sarah_says(
                    "Six months. "
                    "I've been carrying this for six months. "
                    "And it was a parking lot in Casper."
                )
                success("Something releases. The room gets quieter.")
                game.heal(3)
                game.honest()
            elif choice == 2:
                _sarah_says(
                    "I know you handled it badly. "
                    "What happened?"
                )
                game.deflect()
                game.set_flag("motel_night_done", True)
            else:
                danger("That's not good enough and she knows it.")
                _sarah_says("I'm going to sleep.")
                game.deflect()
                game.set_flag("motel_night_done", True)
            return True

        game.set_flag("motel_night_done", True)
        _sarah_says("Let's try to sleep. WEST to continue tomorrow.")
        return True

    # ─── Breakdown ────────────────────────────────────────────────────────

    def _talk_breakdown(self, game):
        if not game.check_flag("sarah_cried"):
            if not game.check_flag("affair_revealed"):
                _sarah_says("Of course. Of course the car breaks down now.")
                info(wrap("She laughs. Genuine. Unexpected."))
                dim(
                    "It breaks something. "
                    "Not bad — just breaks the tension "
                    "that's been in the car since Chicago."
                )
                game.honest()
                game.set_flag("sarah_cried", True)
                game.set_flag("breakdown_done", True)
                return True

            _sarah_says("I keep thinking about the parking lot.")
            choice = ask_choice(
                "You say:",
                [
                    "I didn't know how to come home. "
                    "I was scared of what I was going to find.",
                    "It's strange that this feels like the most "
                    "honest we've talked in a year.",
                    "I don't want to be people who stop trying.",
                ]
            )
            if choice == 1:
                _sarah_says(
                    "I knew something was wrong. "
                    "I just didn't know if you did."
                )
                game.honest()
                game.set_flag("sarah_cried", True)
                game.heal(2)
            elif choice == 2:
                _sarah_says(
                    "Because it is. Isn't that terrible."
                )
                dim("She doesn't sound like she thinks it's terrible.")
                game.honest()
                game.set_flag("sarah_cried", True)
                game.heal(1)
            else:
                _sarah_says("Me neither.")
                dim("Two words. It's enough.")
                game.honest()
                game.set_flag("sarah_cried", True)
                game.heal(2)
            game.set_flag("breakdown_done", True)
            return True

        _sarah_says("Tow truck's twenty minutes out. WEST when you're ready.")
        return True

    # ─── Final Miles ──────────────────────────────────────────────────────

    def _talk_final_miles(self, game):
        if not game.check_flag("final_stretch_done"):
            _sarah_says("We're close.")
            info(wrap(
                "She means Portland. "
                "You both know she means more than Portland."
            ))
            choice = ask_choice(
                "You say:",
                [
                    "I'm glad we did this. The whole thing. Even Wyoming.",
                    "What happens when we actually get there?",
                    "Emma is going to want to move here.",
                ]
            )
            if choice == 1:
                _sarah_says(
                    "Yeah. Even Wyoming. Especially Wyoming."
                )
                game.honest()
                game.heal(1)
            elif choice == 2:
                _sarah_says(
                    "We figure it out. Same as we have been."
                )
                game.honest()
                game.heal(1)
            else:
                _sarah_says("She's going to want to move here.")
                dim("A small smile. The first one that's just a smile.")
                game.honest()
                game.heal(2)
            game.set_flag("final_stretch_done", True)
            return True

        _sarah_says("ARRIVE when you're ready.")
        alert("Type ARRIVE to reach Portland.")
        return True


def _sarah_says(text):
    from engine.display import C, WRAP_WIDTH
    filled = textwrap.fill(
        text, width=WRAP_WIDTH - 2, subsequent_indent="  "
    )
    print(f"\n  {C.MAGENTA}{C.BOLD}Sarah:{C.RESET}")
    print(f"  {C.MAGENTA}\"{filled}\"{C.RESET}")
