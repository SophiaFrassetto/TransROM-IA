import sqlite3
from pathlib import Path
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import time
import hashlib

CHUNK_SIZE = 1024 * 1024
PAGE_LINES = 5000  # linhas visuais (cada linha = 16 bytes)


# =============================================================================
# BANCO
# =============================================================================

def init_db(conn):
    conn.executescript("""
    PRAGMA synchronous = OFF;
    PRAGMA journal_mode = MEMORY;
    PRAGMA temp_store = MEMORY;

    CREATE TABLE IF NOT EXISTS rom_bytes (
        offset INTEGER PRIMARY KEY,
        value INTEGER NOT NULL,
        ascii TEXT,
        is_text BOOLEAN DEFAULT 0
    );

    CREATE TABLE IF NOT EXISTS cache_meta (
        key TEXT PRIMARY KEY,
        value TEXT
    );
    """)


def sha1_of_file(path: Path) -> str:
    h = hashlib.sha1()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def populate_db(conn, rom_path, progress_cb=None):
    total = rom_path.stat().st_size
    processed = 0
    cur = conn.cursor()
    offset = 0
    batch = []

    with open(rom_path, "rb") as f:
        while True:
            chunk = f.read(CHUNK_SIZE)
            if not chunk:
                break

            for b in chunk:
                is_text = 32 <= b <= 126
                ch = chr(b) if is_text else "."
                batch.append((offset, b, ch, is_text))
                offset += 1

            processed += len(chunk)
            if progress_cb:
                progress_cb(processed, total)

            if len(batch) >= 50000:
                cur.executemany("INSERT OR REPLACE INTO rom_bytes VALUES (?, ?, ?, ?)", batch)
                conn.commit()
                batch.clear()

        if batch:
            cur.executemany("INSERT OR REPLACE INTO rom_bytes VALUES (?, ?, ?, ?)", batch)
            conn.commit()

    # salvar metadados do cache
    cur.execute("DELETE FROM cache_meta")
    cur.execute("INSERT INTO cache_meta VALUES ('rom_size', ?)", (str(total),))
    cur.execute("INSERT INTO cache_meta VALUES ('rom_sha1', ?)", (sha1_of_file(rom_path),))
    conn.commit()


def is_cache_valid(conn, rom_path: Path) -> bool:
    cur = conn.cursor()
    cur.execute("SELECT key, value FROM cache_meta")
    meta = dict(cur.fetchall())

    if not meta:
        return False

    if meta.get("rom_size") != str(rom_path.stat().st_size):
        return False

    if meta.get("rom_sha1") != sha1_of_file(rom_path):
        return False

    return True


# =============================================================================
# UI
# =============================================================================

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ROM Translation Platform")
        self.geometry("1000x700")
        self.center_window(self, 1000, 700)

        self.conn = None
        self.current_rom = None
        self.current_page = 0
        self.rendered_lines = set()

        self.active_cell = {"tree": None, "row": None, "col": None}
        self.cell_editor = None

        self.build_menu()
        self.build_tabs()
        self.build_status_bar()

        self.hex_tree.bind("<Button-1>", lambda e: self.activate_cell(self.hex_tree, e))
        self.ascii_tree.bind("<Button-1>", lambda e: self.activate_cell(self.ascii_tree, e))

    # ---------------------------------------------------------------------

    def build_menu(self):
        top = ttk.Frame(self)
        top.pack(fill="x")

        self.import_btn = ttk.Button(top, text="Importar ROM", command=self.import_rom)
        self.import_btn.pack(side="left", padx=5)

        self.regen_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(top, text="Regerar cache", variable=self.regen_var).pack(side="left", padx=5)

    # ---------------------------------------------------------------------

    def build_tabs(self):
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True)

        self.hex_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.hex_tab, text="Hex Viewer")

        self.build_hex_tab()

    # ---------------------------------------------------------------------

    def build_status_bar(self):
        status = ttk.Frame(self)
        status.pack(fill="x", side="bottom")

        self.status_var = tk.StringVar(value="Pronto.")
        self.progress_var = tk.DoubleVar(value=0)

        ttk.Label(status, textvariable=self.status_var).pack(side="left", padx=5)
        self.progress = ttk.Progressbar(status, variable=self.progress_var, maximum=100)
        self.progress.pack(side="right", fill="x", expand=True, padx=5)

    # ---------------------------------------------------------------------

    def activate_cell(self, tree, event):
        row_id, col_index = self.get_clicked_cell(tree, event)
        if row_id is None:
            return

        self.active_cell = {"tree": tree, "row": row_id, "col": col_index}

        for t in (self.offset_tree, self.hex_tree, self.ascii_tree):
            t.selection_set(row_id)
            t.focus(row_id)
            t.see(row_id)

        self.show_cell_editor(tree, row_id, col_index)

    def show_cell_editor(self, tree, row_id, col_index):
        if self.cell_editor:
            self.cell_editor.destroy()

        col_id = f"#{col_index+1}"
        bbox = tree.bbox(row_id, col_id)
        if not bbox:
            return

        x, y, w, h = bbox
        value = tree.set(row_id, col_id)

        self.cell_editor = ttk.Entry(tree)
        self.cell_editor.place(x=x, y=y, width=w, height=h)
        self.cell_editor.insert(0, value)
        self.cell_editor.focus_set()

        self.cell_editor.bind("<Return>", self.commit_cell_edit)
        self.cell_editor.bind("<Escape>", lambda e: self.cell_editor.destroy())

    def commit_cell_edit(self, event):
        value = self.cell_editor.get()
        tree = self.active_cell["tree"]
        row = self.active_cell["row"]
        col = self.active_cell["col"]
        col_id = f"#{col+1}"

        if tree == self.hex_tree:
            if len(value) != 2 or not all(c in "0123456789ABCDEFabcdef" for c in value):
                return
            tree.set(row, col_id, value.upper())
        else:
            if len(value) != 1:
                return
            tree.set(row, col_id, value)

        self.cell_editor.destroy()
        self.cell_editor = None

    # ---------------------------------------------------------------------

    def get_clicked_cell(self, tree, event):
        if tree.identify("region", event.x, event.y) != "cell":
            return None, None
        row = tree.identify_row(event.y)
        col = tree.identify_column(event.x)
        if not row or not col:
            return None, None
        return row, int(col[1:]) - 1

    # ---------------------------------------------------------------------

    def set_busy(self, text):
        self.status_var.set(text)
        self.progress_var.set(0)
        self.notebook.state(["disabled"])
        self.import_btn.state(["disabled"])
        self.update()

    def set_idle(self):
        self.status_var.set("Pronto.")
        self.progress_var.set(0)
        self.notebook.state(["!disabled"])
        self.import_btn.state(["!disabled"])
        self.update()

    # ---------------------------------------------------------------------

    def import_rom(self):
        path = filedialog.askopenfilename(title="Selecione a ROM")
        if not path:
            return

        rom_path = Path(path)
        db_path = rom_path.with_suffix("").with_name(rom_path.stem + "_temp.sqlite")

        if self.regen_var.get() and db_path.exists():
            db_path.unlink()

        self.current_rom = rom_path

        if not db_path.exists():
            self.set_busy("Gerando cache...")
            threading.Thread(target=self.build_cache_async, args=(db_path, rom_path), daemon=True).start()
        else:
            conn = sqlite3.connect(db_path)
            valid = is_cache_valid(conn, rom_path)
            conn.close()

            if not valid:
                if not messagebox.askyesno("Cache inválido", "Cache desatualizado. Regerar?"):
                    return
                db_path.unlink()
                self.set_busy("Gerando cache...")
                threading.Thread(target=self.build_cache_async, args=(db_path, rom_path), daemon=True).start()
            else:
                self.set_busy("Carregando cache...")
                threading.Thread(target=self.load_cache_async, args=(db_path,), daemon=True).start()

    # ---------------------------------------------------------------------

    def build_cache_async(self, db_path, rom_path):
        conn = sqlite3.connect(db_path)
        init_db(conn)

        def progress(processed, total):
            percent = processed / total * 100
            self.after(0, lambda: self.progress_var.set(percent))
            self.after(0, lambda: self.status_var.set(f"Gerando cache... {percent:.1f}%"))

        populate_db(conn, rom_path, progress_cb=progress)
        conn.close()

        self.after(0, lambda: self.finish_load(db_path))

    def load_cache_async(self, db_path):
        for i in range(0, 101, 20):
            self.after(0, lambda v=i: self.progress_var.set(v))
            self.after(0, lambda v=i: self.status_var.set(f"Carregando cache... {v}%"))
            time.sleep(0.05)

        self.after(0, lambda: self.finish_load(db_path))

    def finish_load(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.current_page = 0

        for tree in (self.offset_tree, self.hex_tree, self.ascii_tree):
            for item in tree.get_children():
                tree.delete(item)

        self.rendered_lines.clear()
        self.load_hex_page(0)
        self.set_idle()

    # ---------------------------------------------------------------------

    def build_hex_tab(self):
        container = ttk.Frame(self.hex_tab)
        container.pack(fill="both", expand=True)

        style = ttk.Style()
        style.configure("Offset.Treeview", background="#f0f0f0", fieldbackground="#f0f0f0")
        style.configure("Hex.Treeview", background="#ffffff", fieldbackground="#ffffff")
        style.configure("Ascii.Treeview", background="#fdf5e6", fieldbackground="#fdf5e6")

        self.offset_tree = ttk.Treeview(container, columns=("offset",), show="headings", style="Offset.Treeview")
        self.offset_tree.heading("offset", text="Offset")
        self.offset_tree.column("offset", width=90, anchor="center")

        hex_cols = [f"{i:02X}" for i in range(16)]
        self.hex_tree = ttk.Treeview(container, columns=hex_cols, show="headings", style="Hex.Treeview")
        for col in hex_cols:
            self.hex_tree.heading(col, text=col)
            self.hex_tree.column(col, width=25, anchor="center")

        ascii_cols = [f"A{i:X}" for i in range(16)]
        self.ascii_tree = ttk.Treeview(container, columns=ascii_cols, show="headings", style="Ascii.Treeview")
        for col in ascii_cols:
            self.ascii_tree.heading(col, text=col)
            self.ascii_tree.column(col, width=25, anchor="center")

        self.offset_tree.pack(side="left", fill="y")
        self.hex_tree.pack(side="left", fill="both", expand=True)
        self.ascii_tree.pack(side="left", fill="y", padx=(5, 0))

        scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.sync_scroll)
        scrollbar.pack(side="right", fill="y")

        for t in (self.offset_tree, self.hex_tree, self.ascii_tree):
            t.configure(yscrollcommand=scrollbar.set)
            t.bind("<MouseWheel>", self.on_mousewheel)
            t.bind("<Button-4>", self.on_mousewheel)
            t.bind("<Button-5>", self.on_mousewheel)

    # ---------------------------------------------------------------------

    def sync_scroll(self, *args):
        for t in (self.offset_tree, self.hex_tree, self.ascii_tree):
            t.yview(*args)

    def on_mousewheel(self, event):
        if event.num == 5 or event.delta < 0:
            self.sync_scroll("scroll", 1, "units")
        elif event.num == 4 or event.delta > 0:
            self.sync_scroll("scroll", -1, "units")

        # se chegou no fim, carrega mais
        if self.hex_tree.yview()[1] >= 0.999:
            self.load_more()

        return "break"

    def get_clicked_cell(self, tree, event):
        region = tree.identify("region", event.x, event.y)
        if region != "cell":
            return None, None

        row_id = tree.identify_row(event.y)
        col = tree.identify_column(event.x)  # "#1", "#2", ...

        if not row_id or not col:
            return None, None

        col_index = int(col.replace("#", "")) - 1
        return row_id, col_index

    def sync_selection(self, source_tree, target_tree, event):
        row_id, col_index = self.get_clicked_cell(source_tree, event)
        if row_id is None:
            return

        target_tree.selection_set(row_id)
        target_tree.focus(row_id)
        target_tree.see(row_id)
        target_tree.focus_set()

        self.active_row = row_id
        self.active_col = col_index
    # ---------------------------------------------------------------------

    def load_more(self):
        self.current_page += 1
        loaded = self.load_hex_page(self.current_page)
        if not loaded:
            self.status_var.set("Fim do arquivo.")

    def load_hex_page(self, page):
        start = (page * PAGE_LINES * 16) // 16 * 16
        end = start + PAGE_LINES * 16 + 15

        cur = self.conn.cursor()
        cur.execute("""
            SELECT offset, value, ascii FROM rom_bytes
            WHERE offset BETWEEN ? AND ?
            ORDER BY offset
        """, (start, end))

        rows = cur.fetchall()
        if not rows:
            return False

        self.append_hex_rows(rows)
        return True

    def append_hex_rows(self, rows):
        line = []
        ascii_line = ""
        base_offset = None

        for offset, value, ascii_v in rows:
            if base_offset is None:
                base_offset = offset - (offset % 16)

            if len(line) == 16 and base_offset not in self.rendered_lines:
                self.rendered_lines.add(base_offset)

                iid = self.hex_tree.insert("", "end", values=line)
                self.offset_tree.insert("", "end", values=(f"0x{base_offset:08X}",), iid=iid)
                self.ascii_tree.insert("", "end", values=list(ascii_line), iid=iid)

                line = []
                ascii_line = ""
                base_offset = offset

            line.append(f"{value:02X}")
            ascii_line += ascii_v

        if len(line) == 16 and base_offset not in self.rendered_lines:
            self.rendered_lines.add(base_offset)

            iid = self.hex_tree.insert("", "end", values=line)
            self.offset_tree.insert("", "end", values=(f"0x{base_offset:08X}",), iid=iid)
            self.ascii_tree.insert("", "end", values=list(ascii_line), iid=iid)

    # ---------------------------------------------------------------------

    def center_window(self, win, width, height):
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        win.geometry(f"{width}x{height}+{x}+{y}")


if __name__ == "__main__":
    app = App()
    app.mainloop()
