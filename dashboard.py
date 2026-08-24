"""
Dashboard Flask.

Execute:
    python dashboard.py

Abra:
    http://127.0.0.1:5000
"""

import sqlite3
from pathlib import Path

from flask import Flask, jsonify, render_template_string

app = Flask(__name__)
DB_FILE = Path("telemetry.db")

HTML = """
<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">

<title>OBD-II Dashboard</title>

<style>
body {
    font-family: Arial, sans-serif;
    background: #111;
    color: #eee;
    margin: 0;
    padding: 30px;
}

h1 {
    margin-bottom: 5px;
}

.status {
    color: #aaa;
    margin-bottom: 25px;
}

.grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 18px;
}

.card {
    background: #1e1e1e;
    border-radius: 14px;
    padding: 24px;
}

.label {
    color: #aaa;
    font-size: 14px;
}

.value {
    font-size: 36px;
    font-weight: bold;
    margin-top: 10px;
}

.unit {
    color: #777;
    font-size: 13px;
}
</style>
</head>

<body>

<h1>Dashboard OBD-II</h1>
<div class="status">
    Dados atualizados automaticamente
</div>

<div class="grid">

<div class="card">
    <div class="label">RPM</div>
    <div id="RPM" class="value">--</div>
    <div class="unit">rpm</div>
</div>

<div class="card">
    <div class="label">Velocidade</div>
    <div id="SPEED" class="value">--</div>
    <div class="unit">km/h</div>
</div>

<div class="card">
    <div class="label">Temperatura</div>
    <div id="COOLANT_TEMP" class="value">--</div>
    <div class="unit">°C</div>
</div>

<div class="card">
    <div class="label">Acelerador</div>
    <div id="THROTTLE_POS" class="value">--</div>
    <div class="unit">%</div>
</div>

<div class="card">
    <div class="label">Combustível</div>
    <div id="FUEL_LEVEL" class="value">--</div>
    <div class="unit">%</div>
</div>

</div>

<script>

async function atualizar() {

    const response = await fetch("/api/latest");
    const data = await response.json();

    const pids = [
        "RPM",
        "SPEED",
        "COOLANT_TEMP",
        "THROTTLE_POS",
        "FUEL_LEVEL"
    ];

    for (const pid of pids) {

        const element = document.getElementById(pid);

        if (data[pid] !== undefined) {
            element.textContent = Number(data[pid]).toFixed(1);
        }
        else {
            element.textContent = "--";
        }
    }
}

atualizar();

setInterval(atualizar, 1000);

</script>

</body>
</html>
"""


@app.route("/")
def index():
    return render_template_string(HTML)


@app.route("/api/latest")
def latest():

    if not DB_FILE.exists():
        return jsonify({})

    conn = sqlite3.connect(DB_FILE)

    rows = conn.execute("""
        SELECT t.pid, t.value
        FROM telemetry t
        INNER JOIN (
            SELECT pid, MAX(id) AS max_id
            FROM telemetry
            GROUP BY pid
        ) latest
        ON latest.max_id = t.id
    """).fetchall()

    conn.close()

    return jsonify({
        pid: value
        for pid, value in rows
    })


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False
    )
