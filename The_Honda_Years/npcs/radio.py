"""
radio.py — RADIO, The Honda's car stereo.

Plays songs that are accidentally on-point, gives traffic updates
that have nothing to do with traffic. The omnipresent ambient voice
of the trip. Analog to DISPATCH in Route 7.
"""

from npcs.base import NPC
from engine.display import radio_says, dim


class Radio(NPC):
    id = "radio"
    name = "RADIO"
    aliases = [
        "radio", "stereo", "music", "car radio",
        "speaker", "station", "wknd",
    ]

    DIALOG = {
        "front_seat_first": [
            "Traffic on the 294 Expressway. Long delays. "
            "Consider an alternate route. "
            "There is no alternate route.",
        ],
        "time_warning_20": [
            "This is WKND. A reminder that the things "
            "you haven't said yet are still unsaid.",
        ],
        "time_warning_45": [
            "Weather ahead: cloudy with intermittent honesty. "
            "Expect clearing by late afternoon.",
        ],
        "time_warning_60": [
            "Station identification: WKND. You are more than halfway "
            "to where you're going. "
            "Are you more than halfway to where you need to be?",
        ],
        "time_warning_70": [
            "Portland in approximately three hundred miles. "
            "Some things cannot be resolved by arrival.",
        ],
        "rest_stop_song": [
            "Now playing: something slow you both know the words to. "
            "Neither of you sings along.",
        ],
        "breakdown_song": [
            "Static. Then a clear signal. "
            "'Here Comes the Sun.' Wrong moment, but here it is.",
        ],
        "generic": [
            "Road noise. A song half-remembered. "
            "The click of the turn signal in the quiet.",
            "WKND. Playing the songs you mean something to.",
            "Miles and miles.",
        ],
        "quit": [
            "This is WKND. Drive safe. "
            "Talk to the people in your car.",
        ],
    }

    def get_line(self, context, index=0):
        lines = self.DIALOG.get(context, self.DIALOG["generic"])
        return lines[index % len(lines)]

    def say(self, context, index=0):
        line = self.get_line(context, index)
        if line:
            radio_says(line)

    # ─── NPC Interface ────────────────────────────────────────────────────

    def talk(self, game):
        context_map = {
            "rest_stop":  "rest_stop_song",
            "breakdown":  "breakdown_song",
        }
        context = context_map.get(game.room, "generic")
        radio_says(self.get_line(context, game.turns % 3))
        return True

    def look(self, game):
        dim(
            "A 2019 Honda factory radio. AM/FM, Bluetooth. "
            "It's been on WKND since Chicago. "
            "Nobody has changed the station."
        )
        return True

    def describe(self, game, first_visit):
        pass  # Radio speaks contextually, not on room entry

    def use_item(self, game, item_id):
        return False
