"""
TransROM Legacy Exporter

Exports the full legacy (pre-DB) TransROM model to JSON,
preserving all semantic information exactly as defined
in the Python source code.

- Offsets are exported as hex strings
- Sizes are exported as decimal integers
- No inference or reconstruction is performed
"""

import json
from pathlib import Path
from enum import Enum
from typing import Any

# ------------------------------------------------------------
# Imports from the legacy project
# ------------------------------------------------------------

from families.gba import GBA_Family
from families.snes import SNES_Family
from families.sg import SG_Family


# ------------------------------------------------------------
# Helpers
# ------------------------------------------------------------


def serialize_enum(value):
    if isinstance(value, Enum):
        return value.value
    return value


def serialize_value(value):
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, (bytes, bytearray)):
        return value.hex()
    return value


def make_json_safe(obj):
    # None
    if obj is None:
        return None

    # Primitivos
    if isinstance(obj, (str, int, float, bool)):
        return obj

    # Enum
    if isinstance(obj, Enum):
        return obj.value

    # Bytes → hex string (CRÍTICO)
    if isinstance(obj, (bytes, bytearray)):
        return "0x" + obj.hex()

    # List / Tuple
    if isinstance(obj, (list, tuple)):
        return [make_json_safe(x) for x in obj]

    # Dict (chaves também!)
    if isinstance(obj, dict):
        return {
            make_json_safe(k): make_json_safe(v)
            for k, v in obj.items()
        }

    # Objeto com to_dict
    if hasattr(obj, "to_dict") and callable(obj.to_dict):
        return make_json_safe(obj.to_dict())

    # Objeto genérico
    if hasattr(obj, "__dict__"):
        return make_json_safe(obj.__dict__)

    # Fallback final (nunca deveria acontecer)
    return str(obj)


# ------------------------------------------------------------
# MappedDefaultValue
# ------------------------------------------------------------


def export_mapped_default(md):
    return {
        "id": make_json_safe(md.id),
        "raw": make_json_safe(md.raw),
        "meaning": make_json_safe(md.meaning),
        "origin": make_json_safe(md.origin),
        "confidence": md.confidence,
    }


# ------------------------------------------------------------
# BytesRegion
# ------------------------------------------------------------


def export_region(region):
    return {
        "id": region.id,
        "name": region.name,
        "address_space": region.address_space,
        "kind": serialize_enum(region.kind),
        "origin": serialize_enum(region.origin),
        "confidence": region.confidence,
        "offset": hex(region.offset),
        "size": region.size,
        "required": region.required,
        "tags": [serialize_enum(t) for t in (region.tags or [])],
        "encoding": serialize_enum(region.encoding) if region.encoding else None,
        "byte_order": serialize_enum(region.byte_order)
        if hasattr(region, "byte_order")
        else None,
        "bank": serialize_value(region.bank) if hasattr(region, "bank") else None,
        "default_value_mapped": [
            export_mapped_default(md) for md in (region.default_value_mapped or [])
        ],
        "notes": region.notes,
    }


# ------------------------------------------------------------
# BytesLayout
# ------------------------------------------------------------


def export_layout(layout):
    return {
        "id": layout.id,
        "name": layout.name,
        "address_space": layout.address_space,
        "origin": serialize_enum(layout.origin),
        "confidence": layout.confidence,
        "canonical_offset": (
            hex(layout.canonical_offset)
            if layout.canonical_offset is not None
            else None
        ),
        "tags": [serialize_enum(t) for t in (layout.tags or [])],
        "notes": layout.notes,
        "regions": [export_region(r) for r in layout.regions],
    }


# ------------------------------------------------------------
# Hardware
# ------------------------------------------------------------


def export_hardware(hardware):
    return make_json_safe(hardware)


# ------------------------------------------------------------
# Family
# ------------------------------------------------------------


def export_family(family):
    return {
        "id": family.id,
        "name": family.name,
        "extensions": list(family.extensions) if family.extensions else [],
        "notes": family.notes,
        "hardware": make_json_safe(family.hardware),
        "default_cartridge_hardware": make_json_safe(
            family.default_cartridge_hardware
        ),
        "layouts": {layout.id: export_layout(layout) for layout in family.layouts},
    }


# ------------------------------------------------------------
# Entry point
# ------------------------------------------------------------


def export_all(output_path: Path):
    families = [GBA_Family, SNES_Family, SG_Family]

    data = {
        "meta": {
            "schema": "transrom_legacy_v1",
            "offset_format": "hex",
            "size_format": "int",
            "notes": "Full legacy export from Python source (pre-DB).",
        },
        "families": {family.id: export_family(family) for family in families},
    }

    with output_path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"[OK] Export completed: {output_path}")


# ------------------------------------------------------------
# Run
# ------------------------------------------------------------

if __name__ == "__main__":
    output = Path("transrom_legacy_full_export.json")
    export_all(output)
