# 🟪 Hexadecimal in ROM Hacking and Retrocomputing

> :brazil: [Versão em Português](hexadecimal_PT.md)

## What is Hexadecimal?
Hexadecimal (base-16) is a positional numeral system that utilizes sixteen distinct symbols: 0-9 for values zero to nine, and A-F (or a-f) for values ten to fifteen. In computer science and digital systems, hexadecimal provides a human-friendly representation of binary-coded values, as each hex digit corresponds exactly to four binary bits.

## Technical Importance of Hexadecimal
- **Direct mapping to binary:** Each hexadecimal digit represents a nibble (4 bits), so two hex digits represent a full byte (8 bits). This makes it ideal for expressing memory addresses, opcodes, and raw data.
- **Efficient data inspection:** Hexadecimal notation is standard in debuggers, disassemblers, and hex editors for examining and modifying binary files, memory dumps, and ROM images.
- **Universal in low-level computing:** Hexadecimal is the lingua franca for assembly language, firmware analysis, patching, and reverse engineering.

## Nomenclature & Notation
- **Prefix:** `0x` (e.g., `0x1A3F`), or `$` in some assemblers (e.g., `$1A3F`)
- **Suffix:** `h` (e.g., `1A3Fh`)
- **Grouping:** Often grouped in bytes (2 digits), words (4 digits), or longwords (8 digits)
- **Case-insensitive:** `0x1a3f` is equivalent to `0x1A3F`

## Expanded Examples
- **Byte value:** Decimal 255 = Hex `0xFF` = Binary `11111111`
- **16-bit address:** `0x8000` (commonly used as a memory address in many 8/16-bit systems)
- **Instruction encoding:** The opcode for NOP (No Operation) on some CPUs is `0xEA`
- **File signature (magic number):** PNG files start with `89 50 4E 47` (`0x89504E47`)
- **Pointer:** A 24-bit pointer might be stored as `34 12 00` (little-endian for `0x001234`)
- **Palette entry:** A color in RGB565 format: `0x7E0` (pure green; a palette is a table of colors used by graphics)

## Techniques
- **Hex editors:** Tools such as HxD, Hex Workshop, or MadEdit allow direct inspection and modification of binary data.
- **Pattern search:** Search for magic numbers, pointers, or known text encodings in ROMs and executables.
- **Direct patching:** Modify code, graphics (tiles, palettes), or text by editing their hexadecimal representations.

## Formulas
- **Decimal to hex:** `hex(4660)` → `0x1234`
- **Hex to decimal:** `int('1A3F', 16)` → `6719`
- **Bitwise operations:** `0xF0 & 0x0F = 0x00`
- **Extracting nibbles:** High nibble: `(byte & 0xF0) >> 4`, Low nibble: `byte & 0x0F`

## Usage in ROM Hacking
- **Pointers:** Stored as 2, 3, or 4 bytes in hex, referencing locations in memory or files.
- **Text encodings:** ASCII, Shift-JIS, or custom tables, all represented as hex values.
- **Graphics:** Tiles (small blocks of pixels) and palettes (color tables) are stored and manipulated in hex.
- **Compression:** Headers and data blocks are identified by specific hex patterns.
- **Magic numbers:** Unique hex sequences that identify file types or data structures.

## Console Examples
- **NES:** Uses hex addresses for memory mapping (e.g., `0x8000` for PRG ROM).
- **SNES:** Graphics and color palettes are stored in hex, e.g., `0x7FFF` for white in BGR555.
- **Mega Drive/Genesis:** ROM and RAM addresses, tile data, and palette entries are all managed in hex.
- **PlayStation:** File system, pointers, and compressed data blocks are all hex-based.

## Further Reading
- [Wikipedia: Hexadecimal](https://en.wikipedia.org/wiki/Hexadecimal)
- [Hex Editors for ROM Hacking](https://www.romhacking.net/utilities/)

---

## Related Topics
- [Magic Numbers](magic_numbers.md)
- [Pointers](pointers.md)
- [Compression](compression.md)
- [Character Tables](character_tables.md)
