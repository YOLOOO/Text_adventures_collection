"""
driver.py — The Driver of Route 7.

Has been driving Route 7 since November 14, 1987.
Never speaks. Never turns around. Something about the face,
if you can call it that.
"""

from npcs.base import NPC
from engine.display import dim, danger, dispatch_says


class Driver(NPC):
    id = "driver"
    name = "The Driver"
    aliases = ["driver", "man", "person", "figure", "wheel"]

    def describe(self, game, first_visit):
        if first_visit and not game.check_flag("driver_looked"):
            dim(
                "The driver is in the seat, hands on the wheel. "
                "Uniform correct, posture correct. "
                "They have not turned around."
            )

    def talk(self, game):
        dispatch_says(
            "The driver is unable to assist passengers at this time. "
            "For assistance, please use the emergency contact panel."
        )
        return True

    def fight(self, game):
        from engine.dice import ask_d20
        danger(
            "You grab the driver's shoulder and pull. "
            "They resist — or rather, the seat resists, "
            "as if something is holding him in place."
        )
        roll = ask_d20("Pulling a ghost off a steering wheel")
        if roll >= 14 or roll == 20:
            danger(
                "The driver's form flickers. For a moment "
                "the seat is empty — just long enough for you "
                "to lunge for the wheel."
            )
            from data.endings import ending_escape_cab
            ending_escape_cab(game)
        elif roll >= 7:
            danger("You stagger back. Take 3 damage.")
            game.take_damage(3)
            dim("The driver hasn't moved. Try LEAVE instead.")
        else:
            danger("You fall hard into the dashboard. Take 5 damage.")
            game.take_damage(5)
            dispatch_says(
                "Passenger disturbance in driver's cab. "
                "Please be seated."
            )
        return True

    def look(self, game):
        if not game.check_flag("driver_looked"):
            game.set_flag("driver_looked")
            danger(
                "You look through the wired-glass partition. "
                "The driver's hands are correct. "
                "The driver's uniform is correct. "
                "The reflection in the windscreen is not."
            )
            dim(
                "There is no face. Not hidden, not obscured. "
                "Just the back of a head and, in the glass reflection, "
                "where a face should be: nothing."
            )
        else:
            dim(
                "You already looked. "
                "It hasn't improved."
            )
        return True

    def use_item(self, game, item_id):
        return False
