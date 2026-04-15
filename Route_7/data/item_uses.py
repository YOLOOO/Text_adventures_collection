"""
item_uses.py — USE handlers for Route 7.

These fire when the player types USE <item> and no NPC claims it first.
"""

from engine.display import info, dim, success, danger, alert, dispatch_says, wrap
from data.items import item_name


def _use_ticket_stub(game):
    dim(
        "Night Bus Route 7. Destination: END OF LINE. "
        "Issued November 14, 1987. "
        "You did not buy this ticket."
    )


def _use_newspaper(game):
    if not game.check_flag("newspaper_read"):
        game.set_flag("newspaper_read")
        info(wrap(
            "You read it carefully. Route 7 vanished on "
            "November 14, 1987. Six passengers. No wreckage. "
            "No explanation. The service was permanently suspended."
        ))
        dim("The paper feels warm. It shouldn't.")
        dispatch_says("Please keep the aisle clear. Thank you.")
    else:
        dim("You already know what it says. It hasn't changed.")


def _use_folded_map(game):
    if not game.check_flag("map_read"):
        game.set_flag("map_read")
        info(wrap(
            "Route 7 traces a normal city circuit — "
            "eight stops, thirty-two minutes scheduled. "
            "Then a ninth stop with no name. "
            "Just a black square at the end of a road "
            "that isn't on any other map."
        ))
        alert("The black square is close. Keep moving.")
    else:
        dim("Eight stops and a black square. You remember.")


def _use_lighter(game):
    if game.room == "luggage_hatch":
        if not game.check_flag("hatch_lit"):
            game.set_flag("hatch_lit")
            success("Flame catches. The hatch floods with light.")
            info(wrap(
                "Stenciled on the wall: an emergency exit lever mount — "
                "lever already removed. On the floor, half-buried "
                "under a toolbox: a heavy steel key on a TfL ring."
            ))
            dim("TAKE MAINTENANCE KEY while you have the light.")
        else:
            dim("Hatch is already lit. Emergency lever mount is empty. "
                "Maintenance key is on the floor if you haven't taken it.")
    else:
        dim("You flick the lighter. It works. Nothing here needs it.")


def _use_emergency_lever(game):
    if game.room == "rear_seats":
        if not game.check_flag("lever_pulled"):
            game.set_flag("lever_pulled")
            success("You slot the lever into the rear door mount.")
            info(wrap(
                "A mechanical clunk — the emergency door latch disengages. "
                "The door strains against its seal. "
                "Cold air hisses through the gap."
            ))
            alert("Emergency exit ready. Type LEAVE to jump.")
        else:
            dim("The lever is already set. Door is ready.")
    else:
        dim(
            "You need to be at the rear of the bus. "
            "The emergency door mount is back there."
        )


def _use_maintenance_key(game):
    if game.room == "front_seats":
        if not game.check_flag("cab_unlocked"):
            game.set_flag("cab_unlocked")
            success("The key turns. The partition lock disengages.")
            dispatch_says(
                "Unauthorised access to driver's cab detected. "
                "Please return to your seat. "
                "This has been logged."
            )
        else:
            dim("The partition is already unlocked.")
    else:
        dim(
            "The cab partition is at the front of the bus. "
            "You need to be in the front seats to use this."
        )


def _use_drivers_log(game):
    if not game.check_flag("log_read"):
        game.set_flag("log_read")
        info(wrap(
            "You read the last entry: 'Passengers will not disembark. "
            "End of Line confirmed.' "
            "The date is November 14, 1987. "
            "The ink is dry. The handwriting is desperate."
        ))
        danger("This bus has been running since 1987.")
    else:
        dim("Last entry: 'God help us.' You already know.")


def _use_bus_report(game):
    info(wrap(
        "TfL confirmed Route 7 decommissioned after the 1987 incident. "
        "The bus never returned. "
        "The passengers never returned. "
        "'They never stopped riding.'"
    ))


USE_HANDLERS = {
    "ticket_stub":      _use_ticket_stub,
    "newspaper_1987":   _use_newspaper,
    "folded_map":       _use_folded_map,
    "lighter":          _use_lighter,
    "emergency_lever":  _use_emergency_lever,
    "maintenance_key":  _use_maintenance_key,
    "drivers_log":      _use_drivers_log,
    "bus_report":       _use_bus_report,
}
