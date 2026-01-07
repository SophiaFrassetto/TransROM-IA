use encoding_rs::SHIFT_JIS;
use std::{collections::HashMap};

pub type TblMap = HashMap<Vec<u8>, String>;

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum TextEncoding {
    Ascii,
    Utf8,
    Utf16LE,
    ShiftJis,
    Tbl,
}

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

fn is_text_byte(b: u8) -> bool {
    b.is_ascii_graphic() || b == b' ' || b == 0x00 || b == b'\n' || b == b'\r' || b == b'\t'
}

pub fn decode_text(raw: &[u8], tbl: Option<&TblMap>) -> Option<String> {
    let valid = raw
        .iter()
        .filter(|&&b| is_text_byte(b))
        .count();
    let ratio = (valid as f32) / (raw.len().max(1) as f32);

    if ratio >= 0.7 {
        let s = String::from_utf8_lossy(raw).trim_end_matches('\0').to_string();
        if !s.is_empty() {
            return Some(s);
        }
    }

    if let Some(s) = decode_utf16_le(raw) {
        return Some(s);
    }

    let (cow, _, had_errors) = SHIFT_JIS.decode(raw);
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