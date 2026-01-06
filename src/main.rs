mod rom;
mod formats;

use rom::Rom;
use rom::RomRegionKind;
use formats::gba::Gba;



fn main() -> Result<(), Box<dyn std::error::Error>> {
    let rom = Rom::load(
        "Legend of Zelda - Minish Cap",
        "./roms/Legend of Zelda, The - The Minish Cap (USA).gba",
        Gba,
        None,
    )?;
    // let mut jp_rom = Rom::load(
        //     "Zelda no Densetsu - Fushigi no Boushi",
        //     "./roms/Zelda no Densetsu - Fushigi no Boushi (Japan).gba",
        //     Gba,
        // )?;
        // let mut tbl_rom = Rom::load(
            //     "Pokemon - FireRed Version",
            //     "./roms/Pokemon - FireRed Version (USA).gba",
            //     Gba,
            // )?;

    println!("\n------------------{}------------------", rom.name);
    println!("------------------ Family Regions");
    let _ = rom.display_family_regions(None);
    // println!("------------------ All Regions [Text, Pointer]");
    // let _ = rom.display_regions(Some(&[RomRegionKind::Text, RomRegionKind::Pointer]));


    Ok(())
}
