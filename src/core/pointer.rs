use crate::utils::progress::timed_bar;


#[derive(Debug, Clone)]
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

pub fn detect_pointer_tables(pointers: &[RomPointer]) -> Vec<Vec<(usize, usize)>> {
    let mut sorted = pointers.iter().collect::<Vec<_>>();
    sorted.sort_by_key(|p| p.from);

    let mut tables = Vec::new();
    let mut current = Vec::new();

    for p in sorted {
        if current.is_empty() {
            current.push((p.from, p.to));
        } else {
            let last = current.last().unwrap();
            if p.from == last.0 + 4 {
                current.push((p.from, p.to));
            } else {
                if current.len() >= 4 {
                    tables.push(current.clone());
                }
                current.clear();
                current.push((p.from, p.to));
            }
        }
    }

    if current.len() >= 4 {
        tables.push(current);
    }

    tables
}
