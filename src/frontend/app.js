const API = "http://localhost:8000";
const PAGE = 16 * 50;

let start = 0, loading = false;

document.getElementById("loadBtn").onclick = loadRom;
document.querySelector(".hex-container").addEventListener("scroll", onScroll);

async function loadRom() {
    const file = document.getElementById("romfile").files[0];
    if (!file) return alert("Select a ROM");

    reset();
    status("Uploading ROM...");
    progress(30);

    const fd = new FormData();
    fd.append("file", file);
    await fetch(API + "/load", { method: "POST", body: fd });

    status("Loading bytes...");
    progress(70);

    await loadNext();
    status("Ready");
    progress(100);
    setTimeout(() => progress(0), 1500);
}

function reset() {
    start = 0;
    document.getElementById("hexbody").innerHTML = "";
}

async function loadNext() {
    if (loading) return;
    loading = true;
    const s = Math.floor(start / 16) * 16;
    const r = await fetch(`${API}/page?start=${s}&count=${PAGE}`);
    const data = await r.json();
    render(data);
    start += data.length;
    loading = false;
}

function render(data) {
    const body = document.getElementById("hexbody");
    for (let i = 0; i < data.length; i += 16) {
        const row = data.slice(i, i + 16);
        if (row.length < 16) continue;

        const tr = document.createElement("tr");

        const o = document.createElement("td");
        o.className = "offset";
        o.textContent = "0x" + row[0].offset.toString(16).padStart(8, "0");
        tr.appendChild(o);

        row.forEach(c => {
            const td = document.createElement("td");
            td.className = "byte";
            td.textContent = c.value.toString(16).padStart(2, "0");
            td.dataset.offset = c.offset;
            td.onclick = () => select(c.offset);
            tr.appendChild(td);
        });

        row.forEach(c => {
            const td = document.createElement("td");
            td.className = "ascii-cell";
            td.textContent = c.value >= 32 && c.value <= 126 ? String.fromCharCode(c.value) : ".";
            td.dataset.offset = c.offset;
            td.onclick = () => select(c.offset);
            tr.appendChild(td);
        });

        body.appendChild(tr);
    }
}

function select(offset) {
    document.querySelectorAll(".selected").forEach(e => e.classList.remove("selected"));
    document.querySelectorAll(`[data-offset='${offset}']`).forEach(e => e.classList.add("selected"));
}

function status(t) { document.getElementById("status").textContent = t; }
function progress(p) { document.getElementById("progress").style.width = p + "%"; }

function onScroll(e) {
    const el = e.target;
    if (el.scrollTop + el.clientHeight >= el.scrollHeight - 200) loadNext();
}
