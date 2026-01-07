use std::{fs, io, path::PathBuf};
// use crate::core::encoding::decode_text;
use crate::core::pointer::*;
use crate::core::region::*;
// use crate::core::heuristics::*;
use crate::core::encoding::TblMap;
use crate::utils::progress::timed_bar;


pub trait RomSpec {
    fn regions(&self) -> &'static [RomRegion];
}

pub trait RomFamily {
    fn name(&self) -> &'static str;
    fn spec(&self) -> &'static dyn RomSpec;
}

// pub struct Rom<F: RomFamily> {
pub struct Rom{
    pub name: String,
    pub path: PathBuf,
    // pub family: F,
    pub buffer: Vec<u8>,
    pub pointers: Vec<RomPointer>,
    pub regions: Vec<RomRegion>,
    pub tbl: Option<&'static TblMap>,
}

// impl<F: RomFamily> Rom<F> {
impl Rom<> {
    // pub fn load(name: impl Into<String>, path: impl Into<PathBuf>, family: F, tbl: Option<&'static TblMap>) -> io::Result<Self> {
    pub fn load(name: impl Into<String>, path: impl Into<PathBuf>, tbl: Option<&'static TblMap>) -> io::Result<Self> {
        let mut rom = Rom {
            name: name.into(),
            path: path.into(),
            // family,
            buffer: Vec::new(),
            pointers: Vec::new(),
            regions: Vec::new(),
            tbl,
        };
        rom.load_buffer()?;
        rom.pointers = scan_pointers(&rom.buffer);
        // rom.discover_regions();
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

    fn all_regions(&self) -> Vec<&RomRegion> {
        let mut all = Vec::new();

        // for r in self.family.spec().regions() {
        //     all.push(r);
        // }

        for r in &self.regions {
            all.push(r);
        }

        all
    }

    pub fn add_region(&mut self, region: RomRegion) {
        self.regions.push(region);
    }

    // fn discover_regions(&mut self) {
    //     let tables = detect_pointer_tables(&self.pointers);
    //     let targets: Vec<(usize, usize)> = self.pointers.iter().map(|p| (p.from, p.to)).collect();
    //     let total = tables.len() + targets.len();

    //     timed_bar(total as u64, "Discover regions", |pb|  {
    //         for (_from, to) in targets {
    //             if region_exists(self.all_regions(), to) {
    //                 continue;
    //             }

    //             let size = infer_region_size(&self.buffer, to, None);
    //             let max = self.buffer.len().saturating_sub(to);
    //             let safe_size = size.min(max);
    //             let raw = &self.buffer[to..to + safe_size];
    //             let kind = classify_region(raw, None);

    //             self.add_region(RomRegion {
    //                 offset: to,
    //                 size,
    //                 name: "Discovered Data",
    //                 kind,
    //                 required: false,
    //                 value_map: None,
    //                 origin: RegionOrigin::Inferred,
    //             });

    //             pb.inc(1);
    //         }
    //     });
    // }
}
