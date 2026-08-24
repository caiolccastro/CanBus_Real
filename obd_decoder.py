"""
obd_decoder.py
Camada comum de leitura OBD-II.

A aplicação não precisa saber se os dados vêm do simulador ou de um
ELM327 físico. Ambos implementam a mesma interface.
"""

from typing import Callable, Optional


class ObdDecoder:
    DEFAULT_PIDS = [
        "RPM",
        "SPEED",
        "COOLANT_TEMP",
        "THROTTLE_POS",
        "FUEL_LEVEL",
    ]

    def __init__(self, source):
        self.source = source

    def read_once(self):
        return self.source.read_once()

    def listen(self, callback: Callable, duration: Optional[float] = None,
               interval: float = 0.2):
        return self.source.listen(callback, duration, interval)

    def shutdown(self):
        self.source.shutdown()
