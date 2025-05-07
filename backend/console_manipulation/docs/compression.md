# 🟧 Compression in ROM Hacking and Retrocomputing

> :brazil: [Versão em Português](compression_PT.md)

## What is Compression?
Compression is the process of encoding data to reduce its size, making storage and transmission more efficient. In digital systems, compression algorithms transform data into a more compact representation, often by removing redundancy or encoding patterns more efficiently.

## Technical Importance of Compression
- **Storage optimization:** Allows more data to fit in limited memory or ROM space.
- **Performance:** Reduces loading times and bandwidth requirements.
- **Data management:** Enables efficient packaging, archiving, and distribution of assets.

## Nomenclature & Notation
- **Compression algorithm:** The method used to compress data (e.g., LZ77, Huffman coding, RLE, LZSS; LZ77 and Huffman are common in retro games)
- **Header:** Initial bytes indicating compression type and parameters.
- **Decompression:** The process of restoring original data from compressed form.

## Expanded Examples
- **LZ77:** A dictionary-based algorithm; compressed blocks often start with a specific header (e.g., `0x10`)
- **Huffman coding:** Uses variable-length codes for frequent symbols
- **RLE (Run-Length Encoding):** Encodes repeated bytes as (value, count) pairs
- **Custom formats:** Many games use proprietary or hybrid compression schemes

## Techniques
- **Block detection:** Identify compressed data by magic numbers or headers
- **Decompression tools:** Use or develop scripts to decompress and analyze data
- **Recompression:** Required to repack modified assets into ROMs
- **Reverse engineering:** Analyze unknown formats by studying patterns and headers

## Usage in ROM Hacking
- **Graphics extraction:** Many tilesets, sprites, and backgrounds are compressed
- **Text blocks:** Scripts and dialogue may be stored in compressed form
- **Asset repacking:** Modified data must be recompressed to fit original constraints
- **Format conversion:** Convert between compressed and uncompressed formats for editing

## Console Examples
- **SNES:** Graphics and maps often use RLE or LZ77 variants
- **GBA:** Widespread use of LZ77 and Huffman for graphics and text
- **PlayStation:** Uses a variety of custom and standard algorithms
- **Mega Drive:** Compression for music, graphics, and level data

## Further Reading
- [Wikipedia: Data compression](https://en.wikipedia.org/wiki/Data_compression)
- [GBATEK - BIOS Compression](https://problemkaputt.de/gbatek.htm#biosdecompressionfunctions)
- [Romhacking.net - Compression Tools](https://www.romhacking.net/utilities/)

---

## Related Topics
- [Hexadecimal](hexadecimal.md)
- [Pointers](pointers.md)
- [Magic Numbers](magic_numbers.md)
- [Character Tables](character_tables.md)
