# 02_repr_str.py — Representaciones legibles (__repr__ y __str__)

class Usuario:
    def __init__(self, nombre: str, email: str):
        self.nombre = nombre
        self.email = email

    def __repr__(self) -> str:
        # Para depuración / reconstrucción
        return f"Usuario(nombre={self.nombre!r}, email={self.email!r})"

    def __str__(self) -> str:
        # Para usuarios finales
        return f"{self.nombre} <{self.email}>"


if __name__ == "__main__":
    u = Usuario("Ada Lovelace", "ada@example.com")
    print(repr(u))
    print(str(u))
    print(u)  # usa __str__
    
    
    
"""🔹 Diferencias clave
Método	    Público objetivo	    Cuándo se usa	                             Ejemplo salida
__repr__	Desarrolladores	        repr(obj), consola interactiva, debugging	 Usuario(nombre='Ada', email='ada@example.com')
__str__	    Usuarios finales	    print(obj), str(obj)	                     Ada <ada@example.com>"""

