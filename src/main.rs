use std::{fs::{File, Metadata}, io::Read, io::Error, path::Path, ops::Range};

fn file_size(path: &Path) -> Result<u64, Error> {
    let f = File::open(path)?;
    let metadata:Metadata = f.metadata()?;
    Ok(metadata.len())

}

fn read_header(path: &Path) -> Result<Vec<u8>, Error> {
    let mut f: File = File::open(path)?;
    let mut buffer = [0u8; 192];

    f.read_exact(&mut buffer)?;
    Ok(buffer.to_vec())
}

fn parse_header(header: &Vec<u8>, offset: Range<usize>) -> Result<String, Error> {
    let title_bytes: &[u8] = &header[offset];
    let parsed = match String::from_utf8(title_bytes.to_vec()) {
        Ok(str) => format!("{:?}: {}", &title_bytes, str),
        Err(_) => format!("{:?}", &title_bytes),
    };
    Ok(parsed)
}

fn validate_checksum(header: &Vec<u8>) -> Result<String, Error> {
    let mut chk: u8 = 0;

    for i in 0xA0..0xBC {
        chk = chk.wrapping_sub(header[i]);
    }

    chk = chk.wrapping_sub(0x19);
    Ok(chk.to_string())

}

fn main() {
    // GBA HARDWARE MANUAL https://problemkaputt.de/gbatek.htm#gbacartridgeheader
    let game_title_offset: Range<usize> = 0xA0..0xA0 + 12;  // GBA GAME TITLE - 0xA0 - 12 bytes
    let game_code_offset: Range<usize>= 0xAC..0xAC + 4; // GBA GAME CODE - 0xAC - 4 bytes
    let maker_code_offset: Range<usize> = 0xB0..0xB0 + 2; // GBA MAKER CODE - 0xB2 - 2 bytes
    let version_offset: Range<usize> = 0xBC..0xBC + 1; // GBA VERSION - 0xBC - 1 bytes
    let checksum_offset: Range<usize> = 0xBD..0xBD + 1; // GBA CHECKSUM - 0xBD - 1 bytes

    let rom_path = Path::new("./roms/Legend of Zelda, The - The Minish Cap (USA).gba");

    match file_size(rom_path) {
        Ok(size) => println!("ROM size: {} bytes\n", size),
        Err(e) => println!("Erro ao ler ROM: {}", e),
    }

    let header = match read_header(rom_path) {
        Ok(buf )  => buf,
        Err(e) => {println!("Erro ao ler ROM: {}", e); return;},
    };

    println!("Header Bytes {:?}\n", &header);

    match parse_header(&header, game_title_offset) {
        Ok(parsed) => println!("Game Title: {parsed}", ),
        Err(e) => println!("Erro ao ler ROM: {}", e),
    };

    match parse_header(&header, game_code_offset) {
        Ok(parsed) => println!("Game Code: {parsed}", ),
        Err(e) => println!("Erro ao ler ROM: {}", e),
    };

    match parse_header(&header, maker_code_offset) {
        Ok(parsed) => println!("Maker Code: {parsed}", ),
        Err(e) => println!("Erro ao ler ROM: {}", e),
    };

    match parse_header(&header, version_offset) {
        Ok(parsed) => println!("Version: {parsed}", ),
        Err(e) => println!("Erro ao ler ROM: {}", e),
    };

    match parse_header(&header, checksum_offset) {
        Ok(parsed) => println!("Header Checksum: {parsed}", ),
        Err(e) => println!("Erro ao ler ROM: {}", e),
    };

    match validate_checksum(&header) {
        Ok(valid) => println!("Calculated Checksum: {valid}", ),
        Err(e) => println!("Erro ao ler ROM: {}", e),
    };

}
