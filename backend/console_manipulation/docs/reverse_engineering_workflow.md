# 🟫 Reverse Engineering Workflow in ROM Hacking

> :brazil: [Versão em Português](reverse_engineering_workflow_PT.md)

## What is a Reverse Engineering Workflow?
A reverse engineering workflow is a step-by-step process for analyzing, understanding, and modifying ROMs or binary files. It helps organize the approach to extracting, editing, and testing data in retro games.

## Why is it Important?
- **Systematic approach:** Ensures nothing is missed and increases efficiency.
- **Repeatability:** Useful for multiple games or projects.
- **Documentation:** Helps share knowledge and onboard new contributors.

## Typical Steps
1. **ROM Acquisition:** Obtain a clean ROM dump.
2. **Header Analysis:** Read and interpret the ROM header for metadata and entry points.
3. **Pointer Table Detection:** Find tables of addresses to data blocks.
4. **Text & Asset Identification:** Locate and extract text, graphics, and other assets.
5. **Compression Analysis:** Identify and decompress compressed data blocks.
6. **Editing:** Modify extracted data (text, graphics, code).
7. **Repacking:** Recompress and reinsert modified data into the ROM.
8. **Testing:** Run the modified ROM in an emulator or on real hardware.

## Usage in ROM Hacking
- **Translation:** Extract and reinsert text for localization.
- **Restoration:** Recover unused or hidden content.
- **Mods:** Add new features, graphics, or levels.
- **Debug:** Test changes and automate repetitive tasks.

## Further Reading
- [Wikipedia: Reverse engineering](https://en.wikipedia.org/wiki/Reverse_engineering)
- [Romhacking.net - Documents](https://www.romhacking.net/documents/)

---

## Related Topics
- [Hexadecimal](hexadecimal.md)
- [Pointers](pointers.md)
- [Magic Numbers](magic_numbers.md)
- [Compression](compression.md)
- [Character Tables](character_tables.md)
