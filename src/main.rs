use std::{fs::{File, Metadata}, io::{Read,Error}, path::Path, ops::Range};

pub struct RomBinaryField {
    pub offset: usize,
    pub size: usize,
    pub name: &'static str,
    pub required: &'static bool,
}

pub struct Rom {
    pub name: &'static str,
    pub path: &Path,
    pub size: u64,
    pub buffer: Vec<u8>,
}

struct GbaRomHeader;

impl GbaRomHeader {
    // DOCUMENTATION: https://problemkaputt.de/gbatek.htm#gbacartridgeheader
    // The first 192 bytes at 8000000h-80000BFh in ROM are used as cartridge header
    // Note: With all entry points, the CPU is initially set into system mode.
    // Address | Bytes | Expl.
    pub const HEADER: RomBinaryField = RomBinaryField {
        offset: 0x00,
        size: 192,
        name: "GBA Complete Header",
        required: false
    }

    // 000h | 4 | ROM Entry Point | (32bit ARM branch opcode, eg. "B rom_start")
    pub const ENTRY_POINT:  RomBinaryField = RomBinaryField {
        offset: 0x00,
        size: 4,
        name: "Entry Point",
        required: false
    }

    // 004h | 156 | Nintendo Logo | (compressed bitmap, required!)
    pub const NINTENDO_LOGO:  RomBinaryField = RomBinaryField {
        offset: 0x04,
        size: 156,
        name: "Entry Point",
        required: true
    }

    // 0A0h | 12 | Game Title | (uppercase ascii, max 12 characters, padded with 00h (if less than 12 chars))
    pub const GAME_TITLE: RomBinaryField = RomBinaryField {
        offset: 0xA0,
        size: 12,
        name: "Game Title",
        required: false
    }

    // 0ACh | 4 | Game Code | (uppercase ascii, 4 characters)
    // cartridges (excluding the leading "AGB-" part).
    //   U  Unique Code          (usually "A" or "B" or special meaning)
    //   TT Short Title          (eg. "PM" for Pac Man)
    //   D  Destination/Language (usually "J" or "E" or "P" or specific language)
    // The first character (U) is usually "A" or "B", in detail:
    //   A  Normal game; Older titles (mainly 2001..2003)
    //   B  Normal game; Newer titles (2003..)
    //   C  Normal game; Not used yet, but might be used for even newer titles
    //   F  Famicom/Classic NES Series (software emulated NES games)
    //   K  Yoshi and Koro Koro Puzzle (acceleration sensor)
    //   P  e-Reader (dot-code scanner) (or NDS PassMe image when gamecode="PASS")
    //   R  Warioware Twisted (cartridge with rumble and z-axis gyro sensor)
    //   U  Boktai 1 and 2 (cartridge with RTC and solar sensor)
    //   V  Drill Dozer (cartridge with rumble)
    // The second/third characters (TT) are:
    //   Usually an abbreviation of the game title (eg. "PM" for "Pac Man") (unless
    //   that gamecode was already used for another game, then TT is just random)
    // The fourth character (D) indicates Destination/Language:
    //   J  Japan             P  Europe/Elsewhere   F  French          S  Spanish
    //   E  USA/English       D  German             I  Italian
    pub const GAME_CODE: RomBinaryField = RomBinaryField {
        offset: 0xAC,
        size: 4,
        name: "Game Code",
        required: false
    }
    // U  Unique Code          (usually "A" or "B" or special meaning)
    pub const GAME_CODE_U: RomBinaryField = RomBinaryField {
        offset: 0xAC,
        size: 1,
        name: "Unique Code (U)",
        required: false
    }
    // TT Short Title          (eg. "PM" for Pac Man)
    pub const GAME_CODE_TT: RomBinaryField = RomBinaryField {
        offset: 0xAD,
        size: 2,
        name: "Short Title (TT)",
        required: false
    }
    // D  Destination/Language (usually "J" or "E" or "P" or specific language)
    pub const GAME_CODE_D: RomBinaryField = RomBinaryField {
        offset: 0xAF,
        size: 1,
        name: "Destination/Language (D)",
        required: false
    }

    // 0B0h | 2 | Maker Code | (uppercase ascii, 2 characters, Identifies the (commercial) developer. For example, "01"=Nintendo)
    pub const MAKER_CODE: RomBinaryField = RomBinaryField {
        offset: 0xB0,
        size: 2,
        name: "Maker Code",
        required: false
    }

    // 0B2h | 1 | Fixed value | (must be 96h, required!)
    pub const FIXED_VALUE: RomBinaryField = RomBinaryField {
        offset: 0xB2,
        size: 1,
        name: "Fixed value",
        required: true
    }

    // 0B3h | 1 | Main unit code | (00h for current GBA models, Identifies the required hardware. Should be 00h for current GBA models.)
    pub const MAIN_UNIT_CODE: RomBinaryField = RomBinaryField {
        offset: 0xB3,
        size: 1,
        name: "Main unit code",
        required: false
    }

    // 0B4h | 1 | Device type | (usually 00h) (bit7=DACS/debug related)
    // Normally, this entry should be zero. With Nintendo's hardware debugger Bit 7 identifies
    // the debugging handlers entry point and size of DACS (Debugging And Communication System)
    // memory: Bit7=0: 9FFC000h/8MBIT DACS, Bit7=1: 9FE2000h/1MBIT DACS. The debugging handler can be enabled in 800009Ch (see above),
    // normal cartridges do not have any memory (nor any mirrors) at these addresses though.
    pub const DEVICE_TYPE: RomBinaryField = RomBinaryField {
        offset: 0xB4,
        size: 1,
        name: "Device type",
        required: false
    }

    // 0B5h | 7 | Reserved Area | (should be zero filled)
    pub const FIRST_RESERVED_AREA: RomBinaryField = RomBinaryField {
        offset: 0xB5,
        size: 7,
        name: "Reserved Area",
        required: false
    }

    // 0BCh | 1 | Software version | (usually 00h)
    pub const SOFTWARE_VERSION: RomBinaryField = RomBinaryField {
        offset: 0xBC,
        size: 1,
        name: "Software version",
        required: false
    }

    // 0BDh | 1 | Complement check | (header checksum, required!)
    // Header checksum, cartridge won't work if incorrect. Calculate as such:
    // chk=0:for i=0A0h to 0BCh:chk=chk-[i]:next:chk=(chk-19h) and 0FFh
    pub const COMPLEMENT_CHECK: RomBinaryField = RomBinaryField {
        offset: 0xBD,
        size: 1,
        name: "Complement check",
        required: true
    }

    // 0BEh | 2 | Reserved Area | (should be zero filled)
    // Below required for Multiboot/slave programs only. For Multiboot,
    // the above 192 bytes are required to be transferred as header-block (loaded to 2000000h-20000BFh),
    // and some additional header-information must be located at the beginning of the actual program/data-block (loaded to 20000C0h and up).
    // This extended header consists of Multiboot Entry point(s) which must be set up correctly,
    // and of two reserved bytes which are overwritten by the boot procedure:
    pub const SECOND_RESERVED_AREA: RomBinaryField = RomBinaryField {
        offset: 0xBE,
        size: 2,
        name: "Reserved Area",
        required: false
    }

    // --- Additional Multiboot Header Entries ---

    // 0C0h | 4 | RAM Entry Point | (32bit ARM branch opcode, eg. "B ram_start")
    // This entry is used only if the GBA has been booted by using Normal or Multiplay transfer mode (but not by Joybus mode).
    // Typically deposit a ARM-32bit "B <start>" branch opcode at this location, which is pointing to your actual initialization procedure.
    pub const RAM_ENTRY_POINT: RomBinaryField = RomBinaryField {
        offset: 0xC0,
        size: 4,
        name: "RAM Entry Point",
        required: false
    }

    // 0C4h | 1 | Boot mode (BYTE) | (init as 00h - BIOS overwrites this value!)
    // The slave GBA download procedure overwrites this byte by a value which is indicating the used multiboot transfer mode.
    //   Value  Expl.
    //   01h    Joybus mode
    //   02h    Normal mode
    //   03h    Multiplay mode
    // Typically set this byte to zero by inserting DCB 00h in your source.
    // Be sure that your uploaded program does not contain important program code or data at this location, or at the ID-byte location below.
    pub const BOOT_MODE: RomBinaryField = RomBinaryField {
        offset: 0xC4,
        size: 1,
        name: "Boot mode",
        required: false
    }

    // 0C5h | 1 | Slave ID Number (BYTE) | (init as 00h - BIOS overwrites this value!)
    // If the GBA has been booted in Normal or Multiplay mode, this byte becomes overwritten by the slave ID number of the local GBA (that'd be always 01h for normal mode).
    //   Value  Expl.
    //   01h    Slave #1
    //   02h    Slave #2
    //   03h    Slave #3
    // Typically set this byte to zero by inserting DCB 00h in your source.
    // When booted in Joybus mode, the value is NOT changed and remains the same as uploaded from the master GBA.
    pub const SLAVE_ID_NUMBER: RomBinaryField = RomBinaryField {
        offset: 0xC5,
        size: 1,
        name: "Slave ID Number",
        required: false
    }

    // 0C6h | 26 | Not used | (seems to be unused)
    pub const NOT_USED: RomBinaryField = RomBinaryField {
        offset: 0xC6,
        size: 26,
        name: "Not used",
        required: false
    }

    // 0E0h | 4 | JOYBUS Entry Pt. | (32bit ARM branch opcode, eg. "B joy_start")
    // If the GBA has been booted by using Joybus transfer mode, then the entry point is located at this address rather than at 20000C0h.
    // Either put your initialization procedure directly at this address, or redirect to the actual boot procedure by depositing a "B <start>"
    // opcode here (either one using 32bit ARM code). Or, if you are not intending to support joybus mode (which is probably rarely used), ignore this entry.
    pub const JOYBUS_ENTRY_POINT: RomBinaryField = RomBinaryField {
        offset: 0xE0,
        size: 4,
        name: "JOYBUS Entry Pt.",
        required: false
    }
}


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
