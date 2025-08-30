# 01_basics.py — Clase mínima, objetos, __init__, métodos
# Ejecutá: python3 01_basics.py

class Punto:
    """Un punto en 2D simple."""
    def __init__(self, x: float, y: float): #type hints (anotaciones de tipos) 
                                            #Los hints mejoran legibilidad + herramientas de análisis.
        # Atributos de *instancia*
        self.x = x
        self.y = y

    def mover(self, dx: float, dy: float) -> None: #no devuelve nada
        self.x += dx
        self.y += dy

    def distancia_origen(self) -> float: #devuelve un float
        return (self.x**2 + self.y**2) ** 0.5 #esto lo devuelve con respecto al punto de origen (0,0)


if __name__ == "__main__":
    p = Punto(3, 4)
    print("Coordenadas:", p.x, p.y)  # 3 4
    print("Distancia al origen:", p.distancia_origen())  # 5.0
    p.mover(-1, 2)
    print("Movido a:", (p.x, p.y))
