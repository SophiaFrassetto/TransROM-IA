"""
Family Resolver

This module determines which console families a ROM *may* belong to,
based on static information such as file extension.

No ROM content is inspected here.
"""

from typing import List

from core.rom import Rom
from core.family import Family

# ------------------------------------------------------------
# Family registry
#
# For now, this is a simple static list.
# In the future, this may be replaced by:
# - plugin discovery
# - dynamic registry
# - database-backed registry
# ------------------------------------------------------------

from families.gba.gba import GBA
from families.snes.snes import SNES
from families.sg.sg import SEGA_GENESIS


ALL_FAMILIES: List[Family] = [
    GBA,
    SNES,
    SEGA_GENESIS,
]


# ------------------------------------------------------------
# Public API
# ------------------------------------------------------------

def resolve_families(rom: Rom) -> List[Family]:
    """
    Determine possible families for a ROM based on file extension.

    Parameters
    ----------
    rom : Rom
        Loaded ROM object.

    Returns
    -------
    list[Family]
        List of possible matching families.
    """
    if not rom.extension:
        return []

    ext = rom.extension.lower()

    candidates: List[Family] = []

    for family in ALL_FAMILIES:
        if family.extensions and ext in family.extensions:
            candidates.append(family)

    return candidates
