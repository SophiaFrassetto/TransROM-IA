# 🟦 Pointers in ROM Hacking and Retrocomputing

> :brazil: [Versão em Português](pointers_PT.md)

## What is a Pointer?
A pointer is a data value that represents a memory address or an offset within a file or memory space. In digital systems, pointers are used to reference the location of data, code, or resources, enabling dynamic access and flexible data structures.

## Technical Importance of Pointers
- **Data referencing:** Pointers allow programs and data structures to reference other locations, enabling tables, linked lists, and dynamic content.
- **ROM and file structure:** Many binary formats use pointers to organize data blocks, text, graphics, and scripts.
- **Reverse engineering:** Understanding pointers is essential for extracting, relocating, or modifying data in ROMs and executables.

## Nomenclature & Notation
- **Absolute pointer:** Stores a full address (e.g., `0x00123456`)
- **Relative pointer:** Stores an offset from a known base (e.g., `0x00002000` from file start)
- **Endianness:** The byte order in which multi-byte pointers are stored (little-endian = least significant byte first; big-endian = most significant byte first)
- **Pointer table:** A contiguous block of pointers, often used to reference lists of data or text blocks.

## Expanded Examples
- **4-byte pointer (little-endian):** `56 34 12 00` → `0x00123456`
- **3-byte pointer:** `34 12 00` → `0x001234`
- **Relative pointer:** Offset `0x200` from base address `0x8000` points to `0x8200`
- **Pointer table:** Sequence of addresses: `00 10 00 08`, `20 20 00 08`, ...

## Techniques
- **Pointer scanning:** Search for values matching known address or offset patterns
- **Pointer table identification:** Detect blocks of consecutive pointers
- **Pointer patching:** Update pointers when moving or expanding data
- **Endianness handling:** Convert between little-endian and big-endian representations as needed.

## Formulas
- **Little-endian to address:** `address = b0 + (b1 << 8) + (b2 << 16) + (b3 << 24)`
- **Relative pointer calculation:** `target = base + offset`
- **Pointer table stride:** Distance in bytes between consecutive pointers (often 2, 3, or 4)

## Usage in ROM Hacking
- **Text extraction:** Locate and follow pointers to text blocks
- **Graphics and assets:** Sprites, tiles, and palettes are often referenced by pointers
- **Script and event systems:** Branching and data-driven logic use pointers for flow control
- **ROM expansion:** Update pointers when adding or moving data

## Console Examples
- **NES:** Uses 2-byte pointers for jump tables and text
- **SNES:** 3-byte pointers for addressing large ROMs
- **PlayStation:** 4-byte pointers for file systems and data blocks
- **Mega Drive:** Pointers for graphics, music, and code

## Further Reading
- [Wikipedia: Pointer (computer programming)](https://en.wikipedia.org/wiki/Pointer_(computer_programming))
- [Romhacking.net - Pointer Tutorials](https://www.romhacking.net/documents/)

---

## Related Topics
- [Hexadecimal](hexadecimal.md)
- [Magic Numbers](magic_numbers.md)
- [Compression](compression.md)
- [Character Tables](character_tables.md)
