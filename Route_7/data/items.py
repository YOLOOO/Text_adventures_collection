"""
items.py — Item definitions for Route 7.
"""

ITEMS = {
    "ticket_stub": {
        "name": "Ticket Stub",
        "description": (
            "Night Bus Route 7. Issued: 11:47 PM. "
            "Origin: City Centre. Destination: END OF LINE. "
            "There is no stop called End of Line. "
            "The ticket is dated November 14, 1987."
        ),
        "aliases": ["ticket", "stub", "pass"],
    },
    "newspaper_1987": {
        "name": "Newspaper (1987)",
        "description": (
            "The Evening Standard, November 14, 1987. "
            "Front page: 'NIGHT BUS TRAGEDY — Route 7 vanishes "
            "with 6 passengers. No wreckage found. Service suspended.' "
            "The paper is crisp. Not a day old."
        ),
        "aliases": ["newspaper", "paper", "news", "standard"],
    },
    "lighter": {
        "name": "Disposable Lighter",
        "description": (
            "A yellow plastic lighter wedged under a seat cushion. "
            "Half-full. It works."
        ),
        "aliases": ["lighter", "light", "flame", "fire"],
    },
    "folded_map": {
        "name": "Route 7 Map",
        "description": (
            "A faded bus route map. Route 7 runs a normal city circuit "
            "until the last stop — marked only as a solid black square "
            "with no name, no grid reference, no street."
        ),
        "aliases": ["map", "route map", "folded map", "route"],
    },
    "emergency_lever": {
        "name": "Emergency Door Lever",
        "description": (
            "A red-handled lever stenciled EMERGENCY EXIT. "
            "Pulled from the wall mount in the luggage hatch. "
            "This releases the rear door latch mechanism."
        ),
        "aliases": ["lever", "emergency lever", "red lever", "handle"],
    },
    "maintenance_key": {
        "name": "Maintenance Key",
        "description": (
            "A heavy steel key on a TfL keyring. "
            "Tagged: 'CAB PARTITION — AUTHORISED PERSONNEL ONLY.' "
            "Cold to the touch. Very cold."
        ),
        "aliases": ["maintenance key", "cab key", "key", "steel key"],
    },
    "drivers_log": {
        "name": "Driver's Logbook",
        "description": (
            "Route 7 Operational Log — final entries, Nov 14 1987. "
            "The last line, in a shaking hand: "
            "'Passengers will not disembark. End of Line confirmed. "
            "God help us.' "
            "There are no subsequent entries. The book is current issue."
        ),
        "aliases": ["log", "logbook", "drivers log", "journal"],
    },
    "bus_report": {
        "name": "Incident Report (1987)",
        "description": (
            "An internal TfL incident report. "
            "'Route 7, 14/11/87: Bus failed to return to depot. "
            "Driver and 6 passengers missing, presumed dead. "
            "Cause: unknown. Route 7 permanently decommissioned.' "
            "Handwritten in the margin: 'They never stopped riding.'"
        ),
        "aliases": ["report", "incident report", "file", "tfl report"],
    },
}


def item_name(item_id):
    return ITEMS.get(item_id, {}).get("name", item_id.replace("_", " ").title())
