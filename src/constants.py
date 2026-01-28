from enum import Enum


class Kind(Enum):
    header = "header"
    code = "code"
    data = "data"
    text = "text"

    pointer = "pointer"
    pointer_table = "pointer_table"

    compressed = "compressed"
    asset = "asset"

    bank = "bank"
    mapper = "mapper"

    reserved = "reserved"
    free_space = "free_space"
    mirror = "mirror"

    graphics = "graphics"
    tilemap = "tilemap"
    palette = "palette"

    unknown = "unknown"


class Encoding(Enum):
    ascii = "ascii"
    utf8 = "utf8"
    utf16 = "utf16"
    shift_jis = "shift_jis"
    tbl = "tbl"
    custom = "custom"


class Origin(Enum):
    spec = "spec"
    discovered = "discovered"
    inferred = "inferred"
    tool_generated = "tool_generated"
    observed = "observed"


class ByteOrder(Enum):
    little = "little"
    big = "big"
    mixed = "mixed"


class AddressSpaceKind(Enum):
    rom = "rom"
    wram = "wram"
    vram = "vram"
    sram = "sram"
    io = "io"
    bios = "bios"
    unknown = "unknown"


class CompressionType(Enum):
    # --- Nintendo (padronizados) ---
    lz77 = "lz77"  # GBA BIOS 0x10
    huffman = "huffman"  # GBA BIOS 0x20
    rle = "rle"  # GBA BIOS 0x30

    # --- SNES específicos ---
    sdd1 = "sdd1"  # S-DD1 hardware decompression
    lc_lz2 = "lc_lz2"  # comum em RPGs
    lc_lz3 = "lc_lz3"

    # --- Sega / custom ---
    sega_rle = "sega_rle"
    nemesis = "nemesis"  # famoso no Mega Drive
    kosinski = "kosinski"
    enigma = "enigma"

    # --- Genérico ---
    custom = "custom"
    unknown = "unknown"


class Tag(Enum):
    # --- Semântica funcional ---
    validation = "validation"  # Required for ROM validity / boot
    execution = "execution"  # Affects execution flow (entry points, code paths)
    structural = "structural"  # Defines structure/layout (headers, tables)

    # --- Conteúdo ---
    informational = "informational"  # Metadata / descriptive (titles, names)
    graphics = "graphics"  # Tiles, palettes, sprites, tilemaps
    audio = "audio"  # Sound data, sequences, samples

    # --- Qualidade / status ---
    experimental = "experimental"  # Known but unstable / poorly documented
    deprecated = "deprecated"  # Obsolete but still present
    optional = "optional"  # Valid but not always present
