# 05_class_static_methods.py — @classmethod y @staticmethod

class Temperatura:  
    def __init__(self, celsius: float): 
        self.celsius = celsius

    @classmethod  # Decorador: define un método de clase (recibe la clase como primer parámetro)
    def desde_fahrenheit(cls, f: float) -> "Temperatura":  # 'cls' es la clase (Temperatura); retorna un objeto Temperatura
        c = (f - 32) * 5/9  # Convierte de Fahrenheit a Celsius
        return cls(c)  # Crea y devuelve una instancia de la clase (equivale a Temperatura(c))

    @staticmethod  # Decorador: define un método estático (no recibe 'self' ni 'cls'). Son funciones “sueltas” pero agrupadas dentro de la clase por organización.
    def es_valida(c: float) -> bool:  # Recibe un número 'c' (float) y devuelve un booleano indicando si es un valor aceptable
        
        return -273.15 <= c <= 1e6  # Retorna True si c está en el rango permitido; False en caso contrario

# Bloque de prueba: solo se ejecuta si este archivo se corre directamente (no si se importa como módulo)
if __name__ == "__main__": 
    t = Temperatura.desde_fahrenheit(98.6)  # Llama al método de clase con 98.6 °F; devuelve un objeto Temperatura en Celsius
    print("Celsius:", t.celsius)  # Imprime el valor de 'celsius' del objeto 't'
    print("¿Válida?:", Temperatura.es_valida(t.celsius))  # Llama al método estático pasando el celsius y muestra True/False
    
