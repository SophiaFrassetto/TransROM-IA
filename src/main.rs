mod core;
pub mod utils;

use core::rom::Rom;



fn main() -> Result<(), Box<dyn std::error::Error>> {
    let rom = Rom::load(
        "Legend of Zelda - Minish Cap",
        "./roms/Legend of Zelda, The - The Minish Cap (USA).gba",
        None,
        None
    )?;

    Ok(())
}
