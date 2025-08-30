# 13_pattern_strategy.py — Patrón Estrategia aplicado a dirección de un VAE

from typing import Protocol

class EstrategiaDireccion(Protocol):
    def decidir(self, distancia_frontal: float) -> str: ...

class EstrategiaConservadora:
    def decidir(self, d: float) -> str:
        return "Frenar" if d < 2.0 else "Avanzar"

class EstrategiaAgresiva:
    def decidir(self, d: float) -> str:
        if d < 1.0: return "Frenar"
        if d < 3.0: return "Esquivar"
        return "Avanzar"

class Controlador:
    def __init__(self, estrategia: EstrategiaDireccion):
        self.estrategia = estrategia
    def tick(self, d_frente: float) -> str:
        return self.estrategia.decidir(d_frente)

if __name__ == "__main__":
    c = Controlador(EstrategiaConservadora())
    print(c.tick(2.5))  # Avanzar
    c.estrategia = EstrategiaAgresiva()
    print(c.tick(2.5))  # Esquivar
