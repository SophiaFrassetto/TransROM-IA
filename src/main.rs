use std::str::from_utf8;

mod rom;
mod formats;

use rom::Rom;
use rom::RomFamily;
use formats::gba::Gba;

use crate::rom::RomRegion;



fn format_region(raw: &[u8]) -> String {
    match from_utf8(raw) {
        Ok(text) => text.to_string(),
        Err(_) => format!("{:02X?}", raw),
    }
}

fn interpret_region(region: &RomRegion, raw: &[u8]) -> String {
    if let Some(map) = region.value_map {
        if let Some(entry) = map.iter().find(|m| m.raw == raw) {
            return entry.meaning.to_string();
        }
    }

    format!("Unknown")
}


fn main() -> Result<(), Box<dyn std::error::Error>> {
    let rom = Rom::load(
        "Legend of Zelda - Minish Cap",
        "./roms/Legend of Zelda, The - The Minish Cap (USA).gba",
        Gba,
    )?;

    for region in rom.family.spec().regions() {
        let raw = &rom.buffer[region.offset..region.offset+region.size];
        let display = format_region(raw);
        let interpreted = interpret_region(region, raw);
        println!(
            "[{:X}+{}] {}: {:?} - required {} - {} - {}",
            region.offset,
            region.size,
            region.name,
            region.kind,
            region.required,
            display,
            interpreted
        );
    }

    Ok(())
}
