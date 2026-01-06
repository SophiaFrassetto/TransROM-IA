use std::fs;
use std::io;
use std::path::PathBuf;

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
}

#[derive(Debug)]
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
}

impl<F: RomFamily> Rom<F> {
    pub fn load(name: impl Into<String>, path: impl Into<PathBuf>, family: F) -> io::Result<Self> {
        let mut rom = Rom {
            name: name.into(),
            path: path.into(),
            family,
            buffer: Vec::new(),
        };
        rom.load_buffer()?;
        Ok(rom)
    }

    pub fn load_buffer(&mut self) -> io::Result<()> {
        self.buffer = fs::read(&self.path)?;
        Ok(())
    }
}
