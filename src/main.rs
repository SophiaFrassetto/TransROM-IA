mod rom;
mod formats;

use rom::Rom;
use rom::RomFamily;
use formats::gba::Gba;


fn diplay_gba_regions(rom: Rom<Gba>)-> Result<(), Box<dyn std::error::Error>>{
    println!("| offset+size | name | kind | required | ascii | interpreted |");
    for region in rom.family.spec().regions() {
        let formated_region = &rom.format_region(region);
        let interpreted_region = &rom.interpret_region(region);
        println!(
            "| {:04X}+{:02X} | {} | {:?} | {} | {} | {} |",
            region.offset,
            region.size,
            region.name,
            region.kind,
            region.required,
            formated_region,
            interpreted_region
        );
    }
    Ok(())
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let rom = Rom::load(
        "Legend of Zelda - Minish Cap",
        "./roms/Legend of Zelda, The - The Minish Cap (USA).gba",
        Gba,
    )?;
    let jp_rom = Rom::load(
        "Zelda no Densetsu - Fushigi no Boushi",
        "./roms/Zelda no Densetsu - Fushigi no Boushi (Japan).gba",
        Gba,
    )?;
    let tbl_rom = Rom::load(
        "Pokemon - FireRed Version",
        "./roms/Pokemon - FireRed Version (USA).gba",
        Gba,
    )?;

    println!("\n------------------{}------------------", rom.name);
    let _ = diplay_gba_regions(rom);
    println!("\n------------------{}------------------", jp_rom.name);
    let _ = diplay_gba_regions(jp_rom);
    println!("\n------------------{}------------------", tbl_rom.name);
    let _ = diplay_gba_regions(tbl_rom);

    Ok(())
}
