# 🟧 Magic Numbers in Computing and ROM Hacking

> :brazil: [Versão em Português](magic_numbers_PT.md)

## What is a Magic Number?
A magic number is a unique constant or sequence of bytes embedded in a file, data structure, or memory region to identify its type, format, or special meaning. Magic numbers are widely used as file signatures (unique values at the start of a file), format markers, and validation codes in digital systems.

## Technical Importance of Magic Numbers
- **File identification:** Many file formats begin with a magic number to distinguish them from others.
- **Data validation:** Magic numbers help detect corruption, incorrect file types, or invalid data structures.
- **Reverse engineering:** Recognizing magic numbers is essential for parsing, extracting, or modifying binary files and ROMs.

## Nomenclature & Notation
- **File signature:** The magic number at the start of a file, often used to quickly identify the file type.
- **Header:** The initial data block containing the magic number and metadata.
- **Endianness:** Magic numbers may appear differently depending on byte order (little-endian or big-endian).

## Expanded Examples
- **PNG image:** Starts with `89 50 4E 47 0D 0A 1A 0A` (`0x89504E470D0A1A0A`)
- **ZIP archive:** Starts with `50 4B 03 04` (`0x504B0304`)
- **ELF executable:** Starts with `7F 45 4C 46` (`0x7F454C46`)
- **ROM format:** Many ROMs have unique magic numbers or headers (e.g., NES: `4E 45 53 1A` for iNES)
- **Custom data blocks:** Compression headers, table markers, etc.

## Techniques
- **Hex inspection:** Use hex editors to locate and recognize magic numbers in files.
- **Pattern search:** Scan for known magic numbers to identify file types or data blocks.
- **Signature databases:** Use or build lists of magic numbers for automated detection.

## Usage in ROM Hacking
- **File validation:** Ensure correct ROM or asset type before processing.
- **Data extraction:** Locate and extract blocks by their magic numbers.
- **Format conversion:** Identify and convert between formats using signatures.

## Console Examples
- **NES:** iNES header: `4E 45 53 1A`
- **SNES:** SMC header: `AA BB 04 00` (not always present)
- **PlayStation:** CD-ROMs start with `CD001` in the ISO9660 volume descriptor
- **Game Boy:** Nintendo logo in header acts as a magic number

## Further Reading
- [Wikipedia: Magic number (programming)](https://en.wikipedia.org/wiki/Magic_number_(programming))
- [File Signatures Table](https://www.garykessler.net/library/file_sigs.html)

---

## Related Topics
- [Hexadecimal](hexadecimal.md)
- [Pointers](pointers.md)
- [Compression](compression.md)
- [Character Tables](character_tables.md)
