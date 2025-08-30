# 08_magic_methods.py — Dunders: igualdad, orden, hash, iteración

class Vector2D:
    __slots__ = ("x", "y")  # opcional: menor memoria, inmuta nombres, # solo se permitirán 'x' y 'y' en cada objeto
    """p = Vector2D(1, 2); p.z = 3        # ❌ AttributeError: no se puede crear 'z'"""
                            

    def __init__(self, x: float, y: float):
        self.x, self.y = x, y

    def __repr__(self):
        return f"Vector2D({self.x}, {self.y})"

    # igualdad / hashing
    def __eq__(self, other): # __eq__ define cómo se comparan tus objetos con ==, y los “doble guiones” indican que es un método mágico que el intérprete invoca automáticamente para ese operador.
        return isinstance(other, Vector2D) and (self.x, self.y) == (other.x, other.y)
        
    def __hash__(self): #__hash__(self) -> int devuelve un entero que representa tu objeto en estructuras
        return hash((self.x, self.y))

    # suma (operador +)
    def __add__(self, other):  #identico a carga de operadores
        if not isinstance(other, Vector2D):
            return NotImplemented
        return Vector2D(self.x + other.x, self.y + other.y)

    # iteración
    def __iter__(self):
        yield self.x
        yield self.y


if __name__ == "__main__":
    a = Vector2D(1, 2)
    b = Vector2D(3, 4)
    print(a + b)            # Vector2D(4, 6)
    print(set([a, b, a]))   # {Vector2D(1, 2), Vector2D(3, 4)}
    x, y = a #se puede desempaquetar en dos si y solo si existe def __iter__(self);, que establece el orden de desempaquetado
    print(x, y)             # 1 2
