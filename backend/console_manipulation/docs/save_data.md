# 🟨 Save Data (SRAM/EEPROM/Flash) in ROM Hacking

> :brazil: [Versão em Português](save_data_PT.md)

## What is Save Data?
Save data refers to persistent storage used by games to keep progress, settings, or unlocks. In retro consoles, this is usually implemented as SRAM, EEPROM, or Flash memory on the cartridge or device.

## Why is it Important?
- **Progress:** Stores player progress, high scores, unlocked content, and settings.
- **ROM hacking:** Allows translation of menus, unlocking features, or creating custom saves.
- **Debugging:** Useful for testing, cheats, and rapid development.

## Types of Save Data
- **SRAM:** Static RAM, usually battery-backed, up to 64 KB.
- **EEPROM:** Electrically erasable, small (512B–8KB), often used for save files.
- **Flash:** Larger, rewritable memory, used in some later cartridges.

## Examples
- **GBA/GB:** SRAM at 0x0E000000, EEPROM/Flash mapped to special addresses.
- **SNES:** SRAM mapped to a specific address range in the ROM.
- **PlayStation:** Memory cards use flash memory for saves.

## Usage in ROM Hacking
- **Save editing:** Modify values (money, items, progress) directly in save files.
- **Translation:** Patch in-game text or menus stored in save data.
- **Unlocks:** Set flags for items, levels, or features.
- **Debug:** Create test saves for development or speedrunning.

## Further Reading
- [Wikipedia: Save game](https://en.wikipedia.org/wiki/Save_game)
- [GBATEK - Save Types](https://problemkaputt.de/gbatek.htm#gbacartbackupflashsramandeeprom)

---

## Related Topics
- [Hexadecimal](hexadecimal.md)
- [Pointers](pointers.md)
- [Magic Numbers](magic_numbers.md)
- [Compression](compression.md)
- [Character Tables](character_tables.md)
