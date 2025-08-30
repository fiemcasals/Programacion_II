# 09_dataclasses.py — Modelos inmutables/ordenables con dataclasses
from dataclasses import dataclass

@dataclass(frozen=True, order=True, slots=True) #Trae el decorador @dataclass, que automatiza la creación de clases de datos (genera __init__, __repr__, __eq__, etc. automáticamente).
class Punto3D:
    x: float
    y: float
    z: float = 0.0

if __name__ == "__main__":
    p1 = Punto3D(1, 2, 3)
    p2 = Punto3D(1, 2, 3)
    print(p1 == p2)  # True
    # p1.x = 10  # ERROR: objeto congelado
    print(sorted([Punto3D(0,0), Punto3D(1,0), Punto3D(0,1)]))

"""@dataclass(...) → transforma la clase para que sea más concisa:

frozen=True → los objetos son inmutables: no podés cambiar sus atributos después de creados.

order=True → agrega operadores de comparación (<, <=, >, >=) basados en el orden de los atributos (x, luego y, luego z).

slots=True → optimiza memoria y evita que se agreguen atributos que no estén definidos (x, y, z son los únicos permitidos)."""