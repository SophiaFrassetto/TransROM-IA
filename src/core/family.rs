use crate::core::region::RomRegion;

#[derive(Debug)]
pub struct RomFamily {
    pub name: &'static str,
    pub extensions: Vec<String>,
    pub regions: Vec<RomRegion>,
}