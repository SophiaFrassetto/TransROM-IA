# 🟩 Character Tables in ROM Hacking and Retrocomputing

> :brazil: [Versão em Português](character_tables_PT.md)

## What is a Character Table?
A character table is a mapping between byte values (or sequences of bytes) and characters or strings. In digital systems, especially in retro games and embedded software, character tables define how text is encoded and decoded, often using custom or non-standard schemes.

## Technical Importance of Character Tables
- **Text encoding/decoding:** Character tables are essential for converting between raw byte data and human-readable text.
- **ROM hacking and translation:** Many games use custom tables for text, requiring reverse engineering to extract or insert scripts.
- **Automation:** Tools use table files (simple text files mapping hex values to characters) to automate text extraction, insertion, and translation.

## Nomenclature & Notation
- **Table file (.tbl):** A plain text file mapping hex values to characters (e.g., `80=A`)
- **Single-byte encoding:** 1 byte per character (e.g., ASCII, a standard encoding for English text)
- **Multi-byte encoding:** 2 or more bytes per character (e.g., Shift-JIS, used for Japanese text)
- **Custom encoding:** Game-specific or proprietary mappings.

## Expanded Examples
- **ASCII:** `41` → `A`, `61` → `a`
- **Shift-JIS:** `82 A0` → `あ`
- **Custom table:** `80=A`, `81=B`, `90=É`, `8140=あ`
- **Table file entry:** `80=A` (hex value = character)

## Techniques
- **Table building:** Analyze ROM data to deduce byte-to-character mappings
- **Table editing:** Add or correct mappings for special symbols or diacritics
- **Table-based extraction/insertion:** Use tools (Cartographer, Atlas, WindHex) with table files

## Usage in ROM Hacking
- **Text translation:** Decode and re-encode scripts for localization
- **Font hacking:** Match table to font graphics for custom alphabets
- **Script tools:** Automate insertion/extraction using table files

## Console Examples
- **NES/SNES:** Often use custom single-byte tables
- **Game Boy/Advance:** Mix of ASCII, Shift-JIS, and custom tables
- **PlayStation:** Multi-byte encodings, often Shift-JIS or custom
- **Mega Drive:** Custom tables for Western and Japanese games

## Further Reading
- [Romhacking.net - Table Files](https://www.romhacking.net/utilities/)
- [WindHex Table Tutorial](http://www.loirak.com/gameboy/gbatutor.php)

---

## Related Topics
- [Hexadecimal](hexadecimal.md)
- [Pointers](pointers.md)
- [Magic Numbers](magic_numbers.md)
- [Compression](compression.md)
