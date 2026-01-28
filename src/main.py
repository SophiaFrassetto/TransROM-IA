from runtime import load_rom
from runtime import resolve_families


if __name__ == "__main__":
    rom = load_rom("C:\\Users\\sophi\\OneDrive\\Documentos\\Projects\\TransROM-IA\\roms\\Legend of Zelda, The - The Minish Cap (USA).gba")

    families = resolve_families(rom)

    for f in families:
        print(f.id, f.name)