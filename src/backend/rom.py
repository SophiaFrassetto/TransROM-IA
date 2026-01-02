from pathlib import Path

def read_rom_to_db(conn, rom_path: Path):
    cur = conn.cursor()
    with open(rom_path, "rb") as f:
        offset = 0
        while True:
            chunk = f.read(1024 * 1024)
            if not chunk:
                break
            for b in chunk:
                cur.execute(
                    "INSERT OR REPLACE INTO rom_bytes (offset, value) VALUES (?, ?)",
                    (offset, b),
                )
                offset += 1
    conn.commit()
