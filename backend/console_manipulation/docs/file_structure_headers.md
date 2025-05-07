# 🟫 File Structure & Headers in ROM Hacking

> :brazil: [Versão em Português](file_structure_headers_PT.md)

## What is File Structure & Header?
A file structure is the organization of data within a file, often divided into sections such as headers, data blocks, and footers. The header is a fixed region at the beginning of a file or ROM that contains metadata, magic numbers, and pointers to important data.

## Why is it Important?
- **Navigation:** Understanding the structure allows you to locate and modify specific data (text, graphics, code).
- **Validation:** The header often contains checksums, file size, and other integrity checks.
- **Reverse engineering:** Headers reveal entry points, version info, and data block locations.

## Typical Header Fields
- **Magic number:** Identifies the file type
- **Version:** Indicates file or format version
- **Size:** Total file or data block size
- **Pointers/Offsets:** Addresses to data sections (text, graphics, etc.)
- **Checksums:** For data integrity
- **Game/ROM info:** Title, code, region, etc.

## Examples
- **NES ROM:** Header contains magic number (`4E 45 53 1A`), PRG/CHR sizes, flags
- **SNES ROM:** May have a 512-byte header with game info
- **GBA ROM:** Header includes Nintendo logo, game title, code, checksums
- **General binary:** Custom formats may have a short header with magic, size, and pointers

## Usage in ROM Hacking
- **Patch creation:** Modify header to change game title, region, or checksums
- **Data extraction:** Use pointers/offsets to find and extract assets
- **Format conversion:** Identify and adapt headers for emulators or tools

## Further Reading
- [Wikipedia: File format](https://en.wikipedia.org/wiki/File_format)
- [GBATEK - GBA Cartridge Header](https://problemkaputt.de/gbatek.htm#gbacartridgeheader)

---

## Related Topics
- [Hexadecimal](hexadecimal.md)
- [Magic Numbers](magic_numbers.md)
- [Pointers](pointers.md)
- [Compression](compression.md)
- [Character Tables](character_tables.md)
