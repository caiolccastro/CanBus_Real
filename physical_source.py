"""
physical_source.py
Fonte para ELM327 físico usando python-obd.

Windows:
    COM3, COM4, COM5...

Se port=None, tenta detectar automaticamente.
"""

from typing import Optional

import obd


class PhysicalSource:
    COMMANDS = [
        obd.commands.RPM,
        obd.commands.SPEED,
        obd.commands.COOLANT_TEMP,
        obd.commands.THROTTLE_POS,
        obd.commands.FUEL_LEVEL,
    ]

    def __init__(self, port: Optional[str] = None, fast=True):
        self.connection = self._connect(port, fast)

        if not self.connection.is_connected():
            raise ConnectionError(
                "ELM327 não conectado. Verifique a porta COM, "
                "driver, Bluetooth/USB e a ignição."
            )

        self.commands = [
            cmd for cmd in self.COMMANDS
            if self.connection.supports(cmd)
        ]

        if not self.commands:
            raise ConnectionError(
                "O ELM327 conectou, mas nenhum PID configurado foi suportado."
            )

        print(f"[OK] ELM327 conectado em {self.connection.port_name()}")

    def _connect(self, port, fast):
        if port:
            print(f"[OBD] Conectando em {port}...")
            return obd.OBD(portstr=port, fast=fast)

        from serial.tools import list_ports

        ports = [p.device for p in list_ports.comports()]

        if not ports:
            raise ConnectionError(
                "Nenhuma porta COM foi encontrada."
            )

        print("[OBD] Portas encontradas:", ", ".join(ports))

        for candidate in ports:
            print(f"[OBD] Testando {candidate}...")
            try:
                connection = obd.OBD(portstr=candidate, fast=fast)

                if connection.is_connected():
                    return connection

                connection.close()
            except Exception as exc:
                print(f"[OBD] Falha em {candidate}: {exc}")

        raise ConnectionError(
            "Nenhuma porta COM conseguiu conectar ao ELM327."
        )

    def read_once(self):
        values = {}

        for cmd in self.commands:
            response = self.connection.query(cmd)

            if response.is_null():
                continue

            value = response.value

            if hasattr(value, "magnitude"):
                value = value.magnitude

            values[cmd.name] = float(value)

        return values

    def listen(self, callback, duration=None, interval=0.2):
        import time

        start = time.time()

        while duration is None or time.time() - start < duration:
            values = self.read_once()

            for pid, value in values.items():
                callback(pid, value)

            time.sleep(interval)

    def shutdown(self):
        self.connection.close()
