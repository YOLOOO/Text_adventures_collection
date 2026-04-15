"""
dispatch.py — DISPATCH, the Route 7 automated PA system.

Monotone, precise, subtly wrong. It announces stops that don't exist,
thanks passengers for patience they haven't shown, and issues safety
advisories that imply awareness of exactly what is happening.
Analog to VIRGIL.
"""

from npcs.base import NPC
from engine.display import dispatch_says, dim


class Dispatch(NPC):
    id = "dispatch"
    name = "DISPATCH"
    aliases = ["dispatch", "pa", "speaker", "radio", "intercom", "bus", "announcement"]

    DIALOG = {
        "greeting": [
            "Good evening. Welcome to Route 7. "
            "Next stop: End of Line. "
            "Please retain your ticket for inspection.",
        ],
        "front_seats_intro": [
            "Passengers are reminded that the driver's cab "
            "is a restricted area. "
            "Please remain in your allocated seat.",
        ],
        "cab_intro": [
            "Unauthorised personnel in driver's cab. "
            "Please return to your seat. "
            "The driver cannot be disturbed.",
        ],
        # Turn warnings
        "time_warning_35": [
            "Route 7 Express. End of Line in approximately 35 minutes. "
            "Thank you for your patience.",
        ],
        "time_warning_55": [
            "End of Line approaching. Estimated arrival: 15 minutes. "
            "Please ensure you have all personal belongings.",
        ],
        "time_warning_65": [
            "Five minutes to End of Line. "
            "Passengers should prepare to disembark.",
        ],
        "time_warning_69": [
            "One minute. "
            "End of Line. "
            "Please be ready.",
        ],
        # Item reactions (when player uses item near dispatch)
        "ticket_confronted": [
            "Your ticket is valid. "
            "Issued: 11:47 PM, November 14, 1987. "
            "We look forward to serving you.",
        ],
        "newspaper_confronted": [
            "We are unable to comment on historical service incidents. "
            "Thank you for understanding.",
        ],
        "log_confronted": [
            "Operational records are the property of the service operator. "
            "Unauthorised possession may result in prosecution.",
        ],
        # Generic
        "quit": [
            "Thank you for travelling with Route 7. "
            "We hope to see you again.",
        ],
        "generic": [
            "This is a passenger service announcement. "
            "Please remain calm and seated.",
            "Route 7 thanks you for your cooperation.",
            "We are sorry for any inconvenience.",
        ],
    }

    def get_line(self, context, index=0):
        lines = self.DIALOG.get(context, self.DIALOG["generic"])
        return lines[index % len(lines)]

    def say(self, context, index=0):
        line = self.get_line(context, index)
        if line:
            dispatch_says(line)

    # ─── NPC Interface ────────────────────────────────────────────────────

    def talk(self, game):
        if game.has("drivers_log") and not game.check_flag("dispatch_confronted"):
            dispatch_says(self.get_line("log_confronted"))
            game.set_flag("dispatch_confronted")
        elif game.has("newspaper_1987"):
            dispatch_says(self.get_line("newspaper_confronted"))
        elif game.has("ticket_stub"):
            dispatch_says(self.get_line("ticket_confronted"))
        else:
            context_map = {
                "rear_seats":    "greeting",
                "front_seats":   "front_seats_intro",
                "drivers_cab":   "cab_intro",
            }
            context = context_map.get(game.room, "generic")
            dispatch_says(self.get_line(context))
        return True

    def use_item(self, game, item_id):
        if item_id == "ticket_stub":
            dispatch_says(self.get_line("ticket_confronted"))
            return True
        if item_id == "newspaper_1987":
            dispatch_says(self.get_line("newspaper_confronted"))
            return True
        if item_id == "drivers_log":
            dispatch_says(self.get_line("log_confronted"))
            game.set_flag("dispatch_confronted")
            return True
        return False

    def look(self, game):
        dim(
            "DISPATCH is the bus itself — the PA grille, "
            "the route board, the automated doors. "
            "It is aware of you in the way a building is aware "
            "of the people inside it."
        )
        return True

    def describe(self, game, first_visit):
        pass  # DISPATCH speaks contextually, not on room entry
