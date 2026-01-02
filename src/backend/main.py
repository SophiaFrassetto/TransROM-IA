from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from db import get_conn, init_db
from rom import read_rom_to_db

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

ROM_PATH = None
DB_PATH = None

@app.post("/load")
async def load_rom(file: UploadFile = File(...)):
    global ROM_PATH, DB_PATH

    uploads = Path("uploads")
    uploads.mkdir(exist_ok=True)

    ROM_PATH = uploads / file.filename
    DB_PATH = ROM_PATH.with_suffix(".sqlite")

    with open(ROM_PATH, "wb") as f:
        f.write(await file.read())

    conn = get_conn(DB_PATH)
    init_db(conn)
    read_rom_to_db(conn, ROM_PATH)
    conn.close()

    return {"status": "ok"}

@app.get("/page")
def get_page(start: int = 0, count: int = 256):
    conn = get_conn(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "SELECT offset, value, modified FROM rom_bytes WHERE offset BETWEEN ? AND ? ORDER BY offset",
        (start, start + count),
    )
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return rows

@app.post("/edit")
def edit_byte(offset: int, value: int):
    conn = get_conn(DB_PATH)
    conn.execute("UPDATE rom_bytes SET value=?, modified=1 WHERE offset=?", (value, offset))
    conn.commit()
    conn.close()
    return {"status": "ok"}
