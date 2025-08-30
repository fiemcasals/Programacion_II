# =======================
# Patrones de diseño usados:
# Herencia, Polimorfismo, Strategy, Factory, Property, Setter
# =======================

from __future__ import annotations #permite leer objetos aun no creados, sin dar error
from abc import ABC, abstractmethod


# -----------------------------
# 1) Clase base con property + setter
# -----------------------------
class Persona:
    def __init__(self, nombre: str):
        self._nombre = ""           # atributo protegido
        self.nombre = nombre        # usa setter con validación

    @property
    def nombre(self) -> str:
        return self._nombre
    
    # def get_nombre(self) -> str:
    #       if (condicion)
    #     return self._nombre

    @nombre.setter
    def nombre(self, nuevo_nombre: str) -> None:
        if not nuevo_nombre.strip():
            raise ValueError("El nombre no puede estar vacío.")
        self._nombre = nuevo_nombre.strip() #'mauri ' ->'mauri'
    
    # def set_nombre(self, nuevo_nombre: str) -> None:
    #     self._nombre = nuevo_nombre

    def presentarse(self) -> str:
        return f"Hola, soy {self.nombre}."


# -----------------------------
# 2) Subclases (Herencia + Polimorfismo)
# -----------------------------
class Estudiante(Persona): #esta es la manera de heredar 
    def __init__(self, nombre: str, carrera: str):
        super().__init__(nombre)     # llama al constructor de Persona (usa el setter)
        self.carrera = carrera       # nuevo atributo propio de Estudiante

    def presentarse(self) -> str:
        return f"{super().presentarse()} Estudio {self.carrera}."
        

class Profesor(Persona):
    def presentarse(self) -> str:
        return f"Buenas, mi nombre es {self.nombre} y soy profesor."


# -----------------------------
# 3) Strategy: comportamiento variable
# -----------------------------


class ComportamientoSaludo(ABC):
    @abstractmethod
    def saludar(self, persona: Persona) -> str:
        pass

class SaludoFormal(ComportamientoSaludo):
    def saludar(self, persona: Persona) -> str:
        return f"Mucho gusto, {persona.nombre}."

class SaludoInformal(ComportamientoSaludo):
    def saludar(self, persona: Persona) -> str:
        return f"¡Hey {persona.nombre}!"


# -----------------------------
# 4) Fábrica para crear personas
# -----------------------------
class FabricaPersonas:
    
    REGISTRO = {
        "estudiante": Estudiante,
        "profesor": Profesor
    }
    
    @classmethod
    def crear(cls, tipo: str, *args, **kwargs) -> Persona:
        tipo = tipo.lower() #transforma todo a minuscula
        if tipo not in cls.REGISTRO:
            raise ValueError(f"Tipo inválido: {tipo}")
        return cls.REGISTRO[tipo](*args, **kwargs) #retorna un objeto llamado Estudiante o Profesor
"""
args: (1, 2, 3)
kwargs: {'nombre': 'Ana', 'activo': True}
"""

# -----------------------------
# 5) Ejemplo de uso
# -----------------------------
if __name__ == "__main__":
    saludo1 = SaludoFormal()
    saludo2 = SaludoInformal()

    personas = [
        FabricaPersonas.crear("estudiante", "Luna", "Ingeniería"),
        FabricaPersonas.crear("profesor", "Carlos")
    ]

    # Mostrar comportamiento original
    for persona in personas:
        print(persona.presentarse())          # Polimorfismo
        print(saludo2.saludar(persona))       # Strategy (informal)
        print(saludo1.saludar(persona))       # Strategy (formal)
        
        print("---")

    # Usamos el setter para cambiar el nombre de forma controlada
    personas[0].nombre = "Valentina"          # usa el setter (con validación)
    personas[1].nombre = "Dr. Gómez"

    # Mostrar comportamiento luego de cambiar el nombre
    for persona in personas:
        print(persona.presentarse())
        print(saludo1.saludar(persona))
        print("---")
