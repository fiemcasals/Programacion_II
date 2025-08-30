# =======================
# Patrones de diseño usados:
# Herencia, Polimorfismo, Strategy, Factory
# =======================

from __future__ import annotations
from abc import ABC, abstractmethod


class Persona:
    def __init__(self, nombre: str, FormaDeSaludo: ComportamientoSaludo):
        self.nombre = nombre
        self.saludo = FormaDeSaludo   # objeto que implementa ComportamientoSaludo
    
    def saludar(self) -> str:
        return self.saludo.saludar()  # devolver el string


# -----------------------------
# 3) Strategy: comportamiento variable
# -----------------------------
class ComportamientoSaludo(ABC):
    @abstractmethod
    def saludar(self) -> str:
        pass


class SaludoFormal(ComportamientoSaludo):
    def saludar(self) -> str:
        return f"Mucho gusto"


class SaludoInformal(ComportamientoSaludo):
    def saludar(self) -> str:
        return f"¡Hey!"


# -----------------------------
# 4) Fábrica para crear personas
# -----------------------------
class FabricaPersonas:
    REGISTRO = {
        "formal": SaludoFormal,
        "informal": SaludoInformal
    }

    @classmethod
    def crear(cls, tipo: str, name: str) -> Persona:
        tipo = tipo.lower()
        if tipo not in cls.REGISTRO:
            raise ValueError(f"Tipo inválido: {tipo}")
        return Persona(name, cls.REGISTRO[tipo]())  
        # 👆 importante: acá instanciamos el objeto (SaludoFormal())


# -----------------------------
# 6) Ejemplo de uso
# -----------------------------
if __name__ == "__main__":
    personas = [
        FabricaPersonas.crear("formal", "Juan"),
        FabricaPersonas.crear("informal", "Carlos")
    ]

    for persona in personas:
        print(f"{persona.nombre} dice: {persona.saludar()}")
        print("---")
