"""
main.py
Ponto de entrada do projeto.

Simulador:
    python main.py --mode simulation

ELM327 físico:
    python main.py --mode physical

ELM327 físico em uma porta específica:
    python main.py --mode physical --port COM5

O banco telemetry.db é usado nos dois modos.
"""

import argparse
import sqlite3
from datetime import datetime

from obd_decoder import ObdDecoder
from simulation_source import SimulationSource
from physical_source import PhysicalSource


DB_FILE = "telemetry.db"


def create_database():
    conn = sqlite3.connect(DB_FILE)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS telemetry (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            pid TEXT NOT NULL,
            value REAL
        )
    """)

    conn.commit()
    return conn


def create_source(mode, port):
    if mode == "simulation":
        print("\n=== MODO SIMULAÇÃO ===")
        print("Carro virtual iniciado.\n")
        return SimulationSource()

    print("\n=== MODO FÍSICO ===")
    return PhysicalSource(port=port)


def main():
    parser = argparse.ArgumentParser(
        description="Sistema OBD-II com simulador e ELM327 físico."
    )

    parser.add_argument(
        "--mode",
        choices=["simulation", "physical"],
        default="simulation",
        help="Modo de execução."
    )

    parser.add_argument(
        "--port",
        default=None,
        help="Porta COM do ELM327, por exemplo COM5."
    )

    parser.add_argument(
        "--duration",
        type=float,
        default=None,
        help="Duração da coleta em segundos. Sem valor, roda continuamente."
    )

    args = parser.parse_args()

    source = create_source(args.mode, args.port)
    decoder = ObdDecoder(source)
    conn = create_database()

    print("Iniciando coleta. Pressione Ctrl+C para parar.\n")

    def callback(pid, value):
        timestamp = datetime.now().isoformat(timespec="seconds")

        print(f"[{timestamp}] {pid:<18} -> {value}")

        conn.execute(
            "INSERT INTO telemetry(timestamp, pid, value) VALUES (?, ?, ?)",
            (timestamp, pid, value)
        )

        conn.commit()

    try:
        decoder.listen(
            callback=callback,
            duration=args.duration,
            interval=0.2
        )

    except KeyboardInterrupt:
        print("\nColeta interrompida pelo usuário.")

    finally:
        decoder.shutdown()
        conn.close()
        print(f"\nDados salvos em {DB_FILE}")


if __name__ == "__main__":
    main()
