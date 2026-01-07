#[derive(Debug, Clone)]
pub enum RegionOrigin {
    Spec,
    Discovered,
    Inferred,
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

pub fn kind_matches(region: &RomRegion, filter: Option<&[RomRegionKind]>) -> bool {
    match filter {
        None => true,
        Some(list) => list.contains(&region.kind),
    }
}
