use std::time::SystemTime;

use crate::core::region::*;

pub struct HeuristicModel {
    pub name: String,
}

#[derive(Debug)]
pub struct HeuristicScores {
    pub text_ratio: f32, // % bytes plausíveis texto
    pub utf8_score: f32,
    pub utf16_score: f32,
    pub shift_jis_score: f32,
    pub tbl_score: f32,

    pub pointer_density: f32, // proporção de words que parecem ponteiro
    pub entropy: f32,         // Shannon entropy
    pub zero_ratio: f32,      // proporção de 0x00
    pub ascii_ratio: f32,

    pub alignment_score: f32,  // se offset está alinhado (4 bytes etc)
    pub repetition_score: f32, // padrões repetitivos
}

#[derive(Debug)]
pub struct Classification {
    pub predicted_kind: RomRegionKind,
    pub confidence: f32, // 0.0 – 1.0
    pub model: String,   // "heuristic_v1", "ml_v3", etc
}

#[derive(Debug)]
pub struct HumanAnnotation {
    pub approved: bool,
    pub corrected_kind: Option<RomRegionKind>,
    pub notes: Option<String>,
}

// pub fn region_exists(regions: Vec<&RomRegion>, offset: usize) -> bool {
//     regions.iter().any(|r| r.offset == offset)
// }

// pub fn infer_region_size(buffer: &[u8], start: usize, tbl: Option<&TblMap>) -> usize {
//     let mut size = 32;
//     let max_len = buffer.len().saturating_sub(start);

//     let mut last = classify_region(&buffer[start..start + size.min(max_len)], tbl);

//     while size < 1024 && start + size < buffer.len() {
//         let next_size = (size + 32).min(max_len);

//         if next_size <= size {
//             break;
//         }

//         let next = classify_region(&buffer[start..start + next_size], tbl);

//         if next != last {
//             break;
//         }

//         size += 32;
//         last = next;
//     }

//     size
// }

// pub fn classify_region(raw: &[u8], tbl: Option<&TblMap>) -> RomRegionKind {
//     if raw.len() < 4 {
//         return RomRegionKind::Unknown;
//     }

//     // if decode_text(raw, tbl).is_some() {
//     //     return RomRegionKind::Text;
//     // }

//     let mut ptr_like = 0;
//     for chunk in raw.chunks_exact(4).take(8) {
//         let v = u32::from_le_bytes(chunk.try_into().unwrap());
//         if (0x08000000..0x0A000000).contains(&v) {
//             ptr_like += 1;
//         }
//     }

//     if ptr_like >= 4 {
//         return RomRegionKind::PointerTable;
//     }

//     // 3. Possível código ARM/Thumb
//     if raw[0] & 0b1 == 1 || raw[1] & 0b1110 == 0b1110 {
//         return RomRegionKind::Code;
//     }

//     // 4. Possível dados / assets
//     if raw.iter().any(|&b| b == 0x10 || b == 0x28 || b == 0x78) {
//         return RomRegionKind::Data;
//     }

//     RomRegionKind::Unknown
// }
