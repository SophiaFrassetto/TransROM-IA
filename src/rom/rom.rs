use std::{fs, io, path::PathBuf, collections::HashMap, time::Instant};
use indicatif::{ProgressBar, ProgressStyle};
use encoding_rs::SHIFT_JIS;

pub type TblMap = HashMap<Vec<u8>, String>;

// TODO move to Constrains
pub enum TextEncoding {
    Ascii,
    Utf8,
    Utf16LE,
    ShiftJis,
    Tbl,
}

// TODO move to Helpers/utils
fn timed_bar<T>(
    total: u64,
    msg: &'static str,
    f: impl FnOnce(&ProgressBar) -> T,
) -> T {
    let pb = ProgressBar::new(total);
    pb.set_style(
        ProgressStyle::with_template(
            "{msg:20} [{bar:30.magenta/black}] {percent:>3}% {pos:>8}/{len:<8} {prefix:>8}"
        )
        .unwrap()
        .progress_chars("█▉▊▋▌▍▎▏ ")
    );
    pb.set_message(msg);

    let start = Instant::now();
    let out = f(&pb);

    let elapsed = start.elapsed().as_millis();
    pb.set_prefix(format!("{elapsed}ms"));

    pb.finish();
    out
}

// TODO move to Helpers/utils
fn decode_utf16_le(raw: &[u8]) -> Option<String> {
    if raw.len() % 2 != 0 {
        return None;
    }

    let mut out = String::new();

    for chunk in raw.chunks_exact(2) {
        let u = u16::from_le_bytes([chunk[0], chunk[1]]);
        if u == 0 {
            break;
        }
        if let Some(c) = char::from_u32(u as u32) {
            out.push(c);
        } else {
            return None;
        }
    }

    Some(out)
}

// TODO move to Helpers/utils

fn is_text_byte(b: u8) -> bool {
    b.is_ascii_graphic() ||
    b == b' ' ||
    b == 0x00 ||
    b == 0xFF ||
    b == b'\n' ||
    b == b'\r' ||
    b == b'\t'
}

fn decode_text(raw: &[u8], tbl: Option<&TblMap>) -> Option<String> {
    let valid = raw.iter().filter(|&&b| is_text_byte(b)).count();
    let ratio = valid as f32 / raw.len().max(1) as f32;

    if ratio >= 0.7 {
        let s = String::from_utf8_lossy(raw)
            .trim_end_matches(|c| c == '\0' || c == '\u{FFFD}')
            .to_string();

        if !s.is_empty() {
            return Some(s);
        }
    }

    if let Some(s) = decode_utf16_le(raw) {
        return Some(s);
    }

    let (cow, _, had_errors) = encoding_rs::SHIFT_JIS.decode(raw);
    if !had_errors {
        let s = cow.trim_end_matches('\0').to_string();
        if !s.is_empty() {
            return Some(s);
        }
    }

    if let Some(tbl) = tbl {
        let mut out = String::new();
        let mut i = 0;

        while i < raw.len() {
            let mut matched = false;
            for (k, v) in tbl {
                if raw[i..].starts_with(k) {
                    out.push_str(v);
                    i += k.len();
                    matched = true;
                    break;
                }
            }
            if !matched {
                i += 1;
            }
        }

        if !out.is_empty() {
            return Some(out);
        }
    }

    None
}


fn kind_matches(region: &RomRegion, filter: Option<&[RomRegionKind]>) -> bool {
    match filter {
        None => true,
        Some(list) => list.contains(&region.kind),
    }
}




#[derive(Debug, Clone)]
pub enum RegionOrigin {
    Spec,
    Discovered,
    Inferred,
}

#[derive(Debug, Clone)]
pub struct RomPointer {
    pub from: usize,
    pub to: usize,
    pub raw: u32,
}

#[derive(Debug)]
pub struct RomValueMapping {
    pub raw: &'static [u8],
    pub meaning: &'static str,
}

#[derive(Debug)]
pub struct RomRegion {
    pub offset: usize,
    pub size: usize,
    pub name: &'static str,
    pub kind: RomRegionKind,
    pub required: bool,
    pub value_map: Option<&'static [RomValueMapping]>,
    pub origin: RegionOrigin,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum RomRegionKind {
    Header,
    Code,
    Data,
    Text,
    Pointer,
    PointerTable,
    Reserved,
    Unknown,
}

pub trait RomSpec {
    fn regions(&self) -> &'static [RomRegion];
}

pub trait RomFamily {
    fn name(&self) -> &'static str;
    fn spec(&self) -> &'static dyn RomSpec;
}

pub struct Rom<F: RomFamily> {
    pub name: String,
    pub path: PathBuf,
    pub family: F,
    pub buffer: Vec<u8>,
    pub pointers: Vec<RomPointer>,
    pub regions: Vec<RomRegion>,
    pub tbl: Option<&'static TblMap>,
}

impl<F: RomFamily> Rom<F> {
    //---------------------------
    // Loader
    //---------------------------
    pub fn load(name: impl Into<String>, path: impl Into<PathBuf>, family: F, tbl: Option<&'static TblMap>) -> io::Result<Self> {
        let mut rom = Rom {
            name: name.into(),
            path: path.into(),
            family,
            buffer: Vec::new(),
            pointers: Vec::new(),
            regions: Vec::new(),
            tbl: tbl,
        };
        rom.load_buffer()?;
        rom.scan_pointers();
        rom.discover_regions();
        Ok(rom)
    }

    fn load_buffer(&mut self) -> io::Result<()> {
        let size = fs::metadata(&self.path)?.len();

        timed_bar(size, "Reading ROM", |pb| {
            let data = fs::read(&self.path)?;
            pb.inc(size);
            self.buffer = data;
            Ok(())
        })
    }

    //---------------------------
    // Regions
    //---------------------------
    fn all_regions(&self) -> Vec<&RomRegion> {
        let mut all = Vec::new();

        for r in self.family.spec().regions() {
            all.push(r);
        }

        for r in &self.regions {
            all.push(r);
        }

        all
    }

    pub fn add_region(&mut self, region: RomRegion) {
        self.regions.push(region);
    }

    fn discover_regions(&mut self) {
        let tables = self.detect_pointer_tables();
        let pointer_targets: Vec<(usize, usize)> = self.pointers.iter().map(|p| (p.from, p.to)).collect();
        let total = tables.len() + pointer_targets.len();



        timed_bar(total as u64, "Discover regions", |pb|  {
            for (_from, to) in pointer_targets {
                if self.region_exists(to) {
                    continue;
                }

                let size = self.infer_region_size(to);
                let max = self.buffer.len().saturating_sub(to);
                let safe_size = size.min(max);
                let raw = &self.buffer[to..to + safe_size];
                let kind = self.classify_region(raw);

                self.add_region(RomRegion {
                    offset: to,
                    size,
                    name: "Discovered Data",
                    kind,
                    required: false,
                    value_map: None,
                    origin: RegionOrigin::Inferred,
                });

                pb.inc(1);
            }
        });
    }

    fn region_exists(&self, offset: usize) -> bool {
        self.regions.iter().any(|r| r.offset == offset)
    }

    fn infer_region_size(&self, start: usize) -> usize {
        let mut size = 32;
        let max_len = self.buffer.len().saturating_sub(start);

        let mut last_kind = self.classify_region(&self.buffer[start..start + size.min(max_len)]);

        while size < 1024 {
            let next_size = (size + 32).min(max_len);

            if next_size <= size {
                break;
            }

            let next_kind = self.classify_region(&self.buffer[start..start + next_size]);

            if next_kind != last_kind {
                break;
            }

            size = next_size;
            last_kind = next_kind;
        }

        size
    }

    fn classify_region(&self, raw: &[u8]) -> RomRegionKind {
        if raw.len() < 4 {
            return RomRegionKind::Unknown;
        }

        // 1. Texto
        if decode_text(raw, self.tbl.as_deref()).is_some() {
            return RomRegionKind::Text;
        }

        // 2. Possível pointer table (muitos words dentro da faixa de ponteiros)
        let mut ptr_like = 0;
        for chunk in raw.chunks_exact(4).take(8) {
            let v = u32::from_le_bytes(chunk.try_into().unwrap());
            if (0x08000000..0x0A000000).contains(&v) {
                ptr_like += 1;
            }
        }
        if ptr_like >= 4 {
            return RomRegionKind::PointerTable;
        }

        // 3. Possível código ARM/Thumb
        if raw[0] & 0b1 == 1 || raw[1] & 0b1110 == 0b1110 {
            return RomRegionKind::Code;
        }

        // 4. Possível dados / assets
        if raw.iter().any(|&b| b == 0x10 || b == 0x28 || b == 0x78) {
            return RomRegionKind::Data;
        }

        RomRegionKind::Unknown
    }

    //---------------------------
    // Pointers
    //---------------------------
    fn scan_pointers(&mut self) {
        let total = self.buffer.len().saturating_sub(4) / 4;

        timed_bar(total as u64, "Scanning pointers", |pb| {
            let mut found = Vec::new();
            let buf = &self.buffer;

            for i in (0..buf.len().saturating_sub(4)).step_by(4) {
                let raw = u32::from_le_bytes(buf[i..i+4].try_into().unwrap());

                if (0x08000000..0x0A000000).contains(&raw) {
                    let target = (raw - 0x08000000) as usize;
                    if target < buf.len() {
                        found.push(RomPointer { from: i, to: target, raw });
                    }
                }
                pb.inc(1);
            }

            self.pointers = found;
        });
    }

    fn detect_pointer_tables(&self) -> Vec<Vec<(usize, usize)>> {
        let mut sorted = self.pointers.iter().collect::<Vec<_>>();
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

    //---------------------------
    // Display
    //---------------------------

    fn display_region(&self, region:&RomRegion){
        let raw = self.bytes_region(region);
        let decoded = decode_text(raw, self.tbl.as_deref()).unwrap_or_else(|| "Not decoded".to_string());
        let interpreted_region = &self.interpret_region(region);
        println!(
            "| {:04X}+{:02X} | {} | {:?} | {} | {} | {} |",
            region.offset,
            region.size,
            region.name,
            region.kind,
            region.required,
            decoded,
            interpreted_region
        );
    }

    pub fn display_family_regions(
        &self,
        kind_filter: Option<&[RomRegionKind]>,
    ) -> Result<(), Box<dyn std::error::Error>> {
        let regions = self.family.spec().regions();

        println!("| offset+size | name | kind | required | text | interpreted |");

        for region in regions {
            if !kind_matches(region, kind_filter) {
                continue;
            }
            self.display_region(region)
        }
        Ok(())
    }


    pub fn display_regions(
        &self,
        kind_filter: Option<&[RomRegionKind]>,
    ) {
        println!("| offset+size | name | kind | required | text | interpreted |");

        for region in self.all_regions() {
            if !kind_matches(region, kind_filter) {
                continue;
            }

            self.display_region(region)
        }
    }

    pub fn bytes_region(&self, region: &RomRegion) -> &[u8]{
        let raw = &self.buffer[region.offset..region.offset+region.size];
        return raw;
    }

    pub fn interpret_region(&self, region: &RomRegion) -> String {
        let raw = self.bytes_region(region);
        if region.value_map.is_none() {
            return "-".to_string();
        }
        if let Some(map) = region.value_map {
            if let Some(entry) = map.iter().find(|m: &&RomValueMapping| m.raw == raw) {
                return entry.meaning.to_string();
            }
        }

        format!("Unknown")
    }

    pub fn pointer_graph(&self) -> HashMap<usize, Vec<usize>> {
        let mut graph = HashMap::new();

        for p in &self.pointers {
            graph.entry(p.from).or_insert_with(Vec::new).push(p.to);
        }

        graph
    }
}
