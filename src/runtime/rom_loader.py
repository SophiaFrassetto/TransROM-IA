"""
ROM Loader

This module is responsible for loading a ROM file from disk
and creating a base Rom object.

It performs NO analysis, NO validation and NO interpretation.
It only reads raw bytes and basic file metadata.
"""

from pathlib import Path
from typing import Union

from core.rom import Rom


__all__ = ["load_rom"]


# ------------------------------------------------------------
# Public API
# ------------------------------------------------------------

def load_rom(path: Union[str, Path]) -> Rom:
    """
    Load a ROM file from disk and return a Rom object.

    This function:
    - reads the file as raw bytes
    - determines file extension
    - determines file size

    It does NOT:
    - detect family
    - apply layouts
    - read regions
    - validate data

    Parameters
    ----------
    path : str | Path
        Path to the ROM file.

    Returns
    -------
    Rom
        A Rom instance populated with raw bytes and metadata.
    """
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"ROM file not found: {path}")

    if not path.is_file():
        raise ValueError(f"Path is not a file: {path}")

    raw_bytes = path.read_bytes()

    extension = path.suffix.lower().lstrip(".")

    rom = Rom(
        id=path.stem,
        name=path.stem,
        path=str(path),
        extension=extension,
        size=len(raw_bytes),
        raw_bytes=raw_bytes,

        # These will be filled later by analysis layers
        family_id=None,
        layouts=None,
        regions=None,
        cartridge_hardware_override=None,
        notes=None,
    )

    return rom
