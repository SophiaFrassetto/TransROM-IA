use crate::utils::progress::timed_bar;


#[derive(Debug)]
pub struct RomPointer {
    pub from: usize,
    pub to: usize,
    pub raw: u32,
}

pub fn scan_pointers(buffer: &[u8]) -> Vec<RomPointer> {
    let total = buffer.len().saturating_sub(4) / 4;
    let mut found = Vec::new();


    timed_bar(total as u64, "Scanning pointers", |pb| {
        let mut ifound = Vec::new();
        let buf = buffer;

        for i in (0..buf.len().saturating_sub(4)).step_by(4) {
            let raw = u32::from_le_bytes(buf[i..i+4].try_into().unwrap());

            if (0x08000000..0x0A000000).contains(&raw) {
                let target = (raw - 0x08000000) as usize;
                if target < buf.len() {
                    ifound.push(RomPointer { from: i, to: target, raw });
                }
            }
            pb.inc(1);
        }
        found = ifound;
    });

    found
}