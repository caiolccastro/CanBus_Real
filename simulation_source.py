"""
simulation_source.py
Simulador de um carro/ECU OBD-II.

Gera valores dinâmicos e relacionados entre si para desenvolvimento
sem carro e sem ELM327 físico.
"""

import math
import random
import time


class SimulationSource:
    def __init__(self):
        self.start_time = time.time()
        self.fuel = 72.0
        self.coolant = 76.0

    def read_once(self):
        t = time.time() - self.start_time

        # Ciclo artificial de aceleração/frenagem.
        cycle = t % 30

        if cycle < 5:
            throttle = 8 + cycle * 8
        elif cycle < 12:
            throttle = 48 + math.sin(t * 1.5) * 12
        elif cycle < 18:
            throttle = 25
        elif cycle < 24:
            throttle = 65 + math.sin(t * 2) * 15
        else:
            throttle = 6

        throttle = max(0, min(100, throttle))

        # RPM acompanha o acelerador, com uma marcha simulada.
        rpm = 750 + throttle * 42 + math.sin(t * 3) * 100
        rpm = max(700, min(5500, rpm))

        # Velocidade responde mais lentamente ao RPM/acelerador.
        target_speed = max(0, (rpm - 700) / 45)
        speed = target_speed * 0.9 + math.sin(t * 0.7) * 3
        speed = max(0, min(140, speed))

        # Temperatura sobe lentamente.
        self.coolant += ((75 + throttle * 0.045) - self.coolant) * 0.012
        coolant = self.coolant + random.uniform(-0.15, 0.15)

        # Combustível cai lentamente.
        self.fuel -= 0.00015
        fuel = max(0, self.fuel)

        return {
            "RPM": round(rpm, 1),
            "SPEED": round(speed, 1),
            "COOLANT_TEMP": round(coolant, 1),
            "THROTTLE_POS": round(throttle, 1),
            "FUEL_LEVEL": round(fuel, 1),
        }

    def listen(self, callback, duration=None, interval=0.2):
        start = time.time()

        while duration is None or time.time() - start < duration:
            values = self.read_once()

            for pid, value in values.items():
                callback(pid, value)

            time.sleep(interval)

    def shutdown(self):
        pass
