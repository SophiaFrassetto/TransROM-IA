use uuid::Uuid;

use crate::core::{family::RomFamily, heuristics::heuristics::{Classification, HeuristicScores, HumanAnnotation, RegionHistoryEntry}};

#[derive(Debug)]
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
    Compressed,
    Asset,
    Unknown,
}

#[derive(Debug)]
pub struct RomRegion {
    pub id: Uuid,

    // Identidade
    pub offset: usize,
    pub size: usize,
    pub name: String,
    pub origin: RegionOrigin,
    pub family: Option<RomFamily>,

    // Classificação
    pub classification: Classification,

    // Heurísticas
    pub heuristics: HeuristicScores,

    // Humano
    pub human: Option<HumanAnnotation>,

    // Histórico
    pub history: Vec<RegionHistoryEntry>,
}

pub fn kind_matches(region: &RomRegion, filter: Option<&[RomRegionKind]>) -> bool {
    match filter {
        None => true,
        Some(list) => list.contains(&region.classification.predicted_kind),
    }
}
