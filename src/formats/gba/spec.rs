use crate::rom::{RomFamily, RomRegion, RomRegionKind, RomSpec, RomValueMapping, RegionOrigin};

pub struct GbaRomSpec;

impl RomSpec for GbaRomSpec {
    fn regions(&self) -> &'static [RomRegion] {
        &[
            // DOCUMENTATION: https://problemkaputt.de/gbatek.htm#gbacartridgeheader
            // The first 192 bytes at 8000000h-80000BFh in ROM are used as cartridge header
            // Note: With all entry points, the CPU is initially set into system mode.
            // Address | Bytes | Expl.
            RomRegion {
                offset: 0x00,
                size: 192,
                name: "GBA Complete Header",
                kind: RomRegionKind::Header,
                required: false,
                value_map: None,
                origin: RegionOrigin::Spec,
            },

            // 000h | 4 | ROM Entry Point | (32bit ARM branch opcode, eg. "B rom_start")
            RomRegion {
                offset: 0x00,
                size: 4,
                name: "Entry Point",
                kind: RomRegionKind::Reserved,
                required: false,
                value_map: None,
                origin: RegionOrigin::Spec,
            },

            // 004h | 156 | Nintendo Logo | (compressed bitmap, required!)
            RomRegion {
                offset: 0x04,
                size: 156,
                name: "Entry Point",
                kind: RomRegionKind::Reserved,
                required: true,
                value_map: None,
                origin: RegionOrigin::Spec,
            },

            // 0A0h | 12 | Game Title | (uppercase ascii, max 12 characters, padded with 00h (if less than 12 chars))
            RomRegion {
                offset: 0xA0,
                size: 12,
                name: "Game Title",
                kind: RomRegionKind::Text,
                required: false,
                value_map: None,
                origin: RegionOrigin::Spec,
            },

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
            RomRegion {
                offset: 0xAC,
                size: 4,
                name: "Game Code",
                kind: RomRegionKind::Text,
                required: false,
                value_map: None,
                origin: RegionOrigin::Spec,
            },
            // U  Unique Code          (usually "A" or "B" or special meaning)
            RomRegion {
                offset: 0xAC,
                size: 1,
                name: "Unique Code (U)",
                kind: RomRegionKind::Text,
                required: false,
                value_map: Some(&[
                    RomValueMapping { raw: b"A", meaning: "Normal game; Older titles (mainly 2001..2003)" },
                    RomValueMapping { raw: b"B", meaning: "Normal game; Newer titles (2003..)" },
                    RomValueMapping { raw: b"C", meaning: "Normal game; Not used yet, but might be used for even newer titles" },
                    RomValueMapping { raw: b"F", meaning: "Famicom/Classic NES Series (software emulated NES games)" },
                    RomValueMapping { raw: b"P", meaning: "e-Reader (dot-code scanner) (or NDS PassMe image when gamecode='PASS')" },
                    RomValueMapping { raw: b"R", meaning: "Warioware Twisted (cartridge with rumble and z-axis gyro sensor)" },
                    RomValueMapping { raw: b"U", meaning: "Boktai 1 and 2 (cartridge with RTC and solar sensor)" },
                    RomValueMapping { raw: b"V", meaning: "Drill Dozer (cartridge with rumble)" },
                ]),
                origin: RegionOrigin::Spec,
            },
            // TT Short Title          (eg. "PM" for Pac Man)
            RomRegion {
                offset: 0xAD,
                size: 2,
                name: "Short Title (TT)",
                kind: RomRegionKind::Text,
                required: false,
                value_map: None,
                origin: RegionOrigin::Spec,
            },
            // D  Destination/Language (usually "J" or "E" or "P" or specific language)
            RomRegion {
                offset: 0xAF,
                size: 1,
                name: "Destination/Language (D)",
                kind: RomRegionKind::Text,
                required: false,
                value_map: Some(&[
                    RomValueMapping { raw: b"J", meaning: "Japan" },
                    RomValueMapping { raw: b"P", meaning: "Europe/Elsewhere" },
                    RomValueMapping { raw: b"F", meaning: "French" },
                    RomValueMapping { raw: b"S", meaning: "Spanish" },
                    RomValueMapping { raw: b"E", meaning: "USA/English" },
                    RomValueMapping { raw: b"D", meaning: "German" },
                    RomValueMapping { raw: b"I", meaning: "Italian" },
                ]),
                origin: RegionOrigin::Spec,
            },

            // 0B0h | 2 | Maker Code | (uppercase ascii, 2 characters, Identifies the (commercial) developer. For example, "01"=Nintendo)
            RomRegion {
                offset: 0xB0,
                size: 2,
                name: "Maker Code",
                kind: RomRegionKind::Text,
                required: false,
                value_map: Some(&[
                    RomValueMapping { raw: b"01", meaning: "Nintendo" },
                ]),
                origin: RegionOrigin::Spec,
            },

            // 0B2h | 1 | Fixed value | (must be 96h, required!)
            RomRegion {
                offset: 0xB2,
                size: 1,
                name: "Fixed value",
                kind: RomRegionKind::Reserved,
                required: true,
                value_map: None,
                origin: RegionOrigin::Spec,
            },

            // 0B3h | 1 | Main unit code | (00h for current GBA models, Identifies the required hardware. Should be 00h for current GBA models.)
            RomRegion {
                offset: 0xB3,
                size: 1,
                name: "Main unit code",
                kind: RomRegionKind::Reserved,
                required: false,
                value_map: None,
                origin: RegionOrigin::Spec,
            },

            // 0B4h | 1 | Device type | (usually 00h) (bit7=DACS/debug related)
            // Normally, this entry should be zero. With Nintendo's hardware debugger Bit 7 identifies
            // the debugging handlers entry point and size of DACS (Debugging And Communication System)
            // memory: Bit7=0: 9FFC000h/8MBIT DACS, Bit7=1: 9FE2000h/1MBIT DACS. The debugging handler can be enabled in 800009Ch (see above),
            // normal cartridges do not have any memory (nor any mirrors) at these addresses though.
            RomRegion {
                offset: 0xB4,
                size: 1,
                name: "Device type",
                kind: RomRegionKind::Reserved,
                required: false,
                value_map: None,
                origin: RegionOrigin::Spec,
            },

            // 0B5h | 7 | Reserved Area | (should be zero filled)
            RomRegion {
                offset: 0xB5,
                size: 7,
                name: "Reserved Area",
                kind: RomRegionKind::Reserved,
                required: false,
                value_map: None,
                origin: RegionOrigin::Spec,
            },

            // 0BCh | 1 | Software version | (usually 00h)
            RomRegion {
                offset: 0xBC,
                size: 1,
                name: "Software version",
                kind: RomRegionKind::Reserved,
                required: false,
                value_map: None,
                origin: RegionOrigin::Spec,
            },

            // 0BDh | 1 | Complement check | (header checksum, required!)
            // Header checksum, cartridge won't work if incorrect. Calculate as such:
            // chk=0:for i=0A0h to 0BCh:chk=chk-[i]:next:chk=(chk-19h) and 0FFh
            RomRegion {
                offset: 0xBD,
                size: 1,
                name: "Complement check",
                kind: RomRegionKind::Reserved,
                required: true,
                value_map: None,
                origin: RegionOrigin::Spec,
            },

            // 0BEh | 2 | Reserved Area | (should be zero filled)
            // Below required for Multiboot/slave programs only. For Multiboot,
            // the above 192 bytes are required to be transferred as header-block (loaded to 2000000h-20000BFh),
            // and some additional header-information must be located at the beginning of the actual program/data-block (loaded to 20000C0h and up).
            // This extended header consists of Multiboot Entry point(s) which must be set up correctly,
            // and of two reserved bytes which are overwritten by the boot procedure:
            RomRegion {
                offset: 0xBE,
                size: 2,
                name: "Reserved Area",
                kind: RomRegionKind::Reserved,
                required: false,
                value_map: None,
                origin: RegionOrigin::Spec,
            },

            // --- Additional Multiboot Header Entries ---

            // 0C0h | 4 | RAM Entry Point | (32bit ARM branch opcode, eg. "B ram_start")
            // This entry is used only if the GBA has been booted by using Normal or Multiplay transfer mode (but not by Joybus mode).
            // Typically deposit a ARM-32bit "B <start>" branch opcode at this location, which is pointing to your actual initialization procedure.
            RomRegion {
                offset: 0xC0,
                size: 4,
                name: "RAM Entry Point",
                kind: RomRegionKind::Reserved,
                required: false,
                value_map: None,
                origin: RegionOrigin::Spec,
            },

            // 0C4h | 1 | Boot mode (BYTE) | (init as 00h - BIOS overwrites this value!)
            // The slave GBA download procedure overwrites this byte by a value which is indicating the used multiboot transfer mode.
            //   Value  Expl.
            //   01h    Joybus mode
            //   02h    Normal mode
            //   03h    Multiplay mode
            // Typically set this byte to zero by inserting DCB 00h in your source.
            // Be sure that your uploaded program does not contain important program code or data at this location, or at the ID-byte location below.
            RomRegion {
                offset: 0xC4,
                size: 1,
                name: "Boot mode",
                kind: RomRegionKind::Reserved,
                required: false,
                value_map: None,
                origin: RegionOrigin::Spec,
            },

            // 0C5h | 1 | Slave ID Number (BYTE) | (init as 00h - BIOS overwrites this value!)
            // If the GBA has been booted in Normal or Multiplay mode, this byte becomes overwritten by the slave ID number of the local GBA (that'd be always 01h for normal mode).
            //   Value  Expl.
            //   01h    Slave #1
            //   02h    Slave #2
            //   03h    Slave #3
            // Typically set this byte to zero by inserting DCB 00h in your source.
            // When booted in Joybus mode, the value is NOT changed and remains the same as uploaded from the master GBA.
            RomRegion {
                offset: 0xC5,
                size: 1,
                name: "Slave ID Number",
                kind: RomRegionKind::Reserved,
                required: false,
                value_map: None,
                origin: RegionOrigin::Spec,
            },

            // 0C6h | 26 | Not used | (seems to be unused)
            RomRegion {
                offset: 0xC6,
                size: 26,
                name: "Not used",
                kind: RomRegionKind::Reserved,
                required: false,
                value_map: None,
                origin: RegionOrigin::Spec,
            },

            // 0E0h | 4 | JOYBUS Entry Pt. | (32bit ARM branch opcode, eg. "B joy_start")
            // If the GBA has been booted by using Joybus transfer mode, then the entry point is located at this address rather than at 20000C0h.
            // Either put your initialization procedure directly at this address, or redirect to the actual boot procedure by depositing a "B <start>"
            // opcode here (either one using 32bit ARM code). Or, if you are not intending to support joybus mode (which is probably rarely used), ignore this entry.
            RomRegion {
                offset: 0xE0,
                size: 4,
                name: "JOYBUS Entry Pt.",
                kind: RomRegionKind::Reserved,
                required: false,
                value_map: None,
                origin: RegionOrigin::Spec,
            },

        ]
    }
}

pub struct Gba;

impl RomFamily for Gba {
    fn name(&self) -> &'static str {
        "Game Boy Advance"
    }

    fn spec(&self) -> &'static dyn RomSpec {
        &GbaRomSpec
    }
}