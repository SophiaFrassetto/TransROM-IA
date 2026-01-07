mod consoles;
mod core;
pub mod utils;

// use consoles::gba::spec::Gba;

// use core::{rom::Rom, region::RomRegionKind};
use core::rom::Rom;



fn main() -> Result<(), Box<dyn std::error::Error>> {
    let rom = Rom::load(
        "Legend of Zelda - Minish Cap",
        "./roms/Legend of Zelda, The - The Minish Cap (USA).gba",
        // Gba,
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


    Ok(())
}
