# 🟦 Graphics Basics (Tiles & Palettes) in ROM Hacking

> :brazil: [Versão em Português](graphics_basics_PT.md)

## What are Tiles & Palettes?
- **Tiles:** Small, fixed-size blocks of pixel data (e.g., 8x8 or 16x16 pixels) used to build backgrounds, sprites, and maps in retro games. Tiles are reused to save space and create complex images efficiently.
- **Palettes:** Tables of colors. Each pixel in a tile refers to an index in the palette, allowing for compact color representation and easy color swaps.

## Why are They Important?
- **Space efficiency:** Tiles and palettes allow large, colorful graphics with minimal memory usage.
- **Editing:** Understanding tile and palette formats is essential for sprite, font, and background hacks.
- **ROM hacking:** Enables translation of in-game text graphics, custom art, and visual mods.

## Typical Formats
- **Tile size:** 8x8 or 16x16 pixels, 2bpp, 4bpp, or 8bpp (bits per pixel)
- **Palette size:** 16 or 256 colors, often in RGB555 or RGB565 format
- **Tilemaps:** Data structures that define how tiles are arranged on screen

## Examples
- **NES:** 8x8 tiles, 2bpp, 4-color palettes
- **SNES:** 8x8 or 16x16 tiles, 4bpp, 16-color palettes
- **GBA:** 8x8 tiles, 4bpp or 8bpp, 16 or 256-color palettes
- **Mega Drive:** 8x8 tiles, 4bpp, 16-color palettes

## Usage in ROM Hacking
- **Sprite editing:** Change character graphics or animations
- **Font hacking:** Edit in-game fonts for translation
- **Backgrounds:** Redraw or modify backgrounds and UI
- **Palette swaps:** Change color schemes for new effects

## Further Reading
- [Wikipedia: Tile-based video game](https://en.wikipedia.org/wiki/Tile-based_video_game)
- [Romhacking.net - Graphics Tools](https://www.romhacking.net/utilities/)

---

## Related Topics
- [Hexadecimal](hexadecimal.md)
- [Pointers](pointers.md)
- [Magic Numbers](magic_numbers.md)
- [Compression](compression.md)
- [Character Tables](character_tables.md)
