# 06_inheritance_polymorphism.py — Herencia, super(), polimorfismo

class Animal:
    def __init__(self, nombre: str):
        self.nombre = nombre

    def hablar(self) -> str:
        # Método "abstracto" por contrato (sin ABC)
        raise NotImplementedError("Animal es una clase base; 'hablar' debe ser redefinido en las subclases.")
        #return "falta definir el comportamiento en las clases hijas"

class Perro(Animal):
    def __init__(self, nombre: str, raza: str):
        # Llamo al inicializador de la clase base
        super().__init__(nombre)
        self.raza = raza
        
    def hablar(self) -> str:
        # Podrías usar super().hablar() si quisieras verificar/registrar algo antes,
        # pero acá simplemente implementamos el comportamiento concreto.
        return "guau"

class Gato(Animal):
    def __init__(self, nombre: str, color: str):
        # Reutilizo la inicialización de Animal
        super().__init__(nombre)
        self.color = color

    def hablar(self) -> str:
        return "miau"

def coro_animal(animals: list[Animal]) -> None:
    for a in animals:
        print(f"{a.nombre} dice {a.hablar()}")

if __name__ == "__main__":
    p = Perro("Toby", raza="Labrador")
    g = Gato("Mishi", color="gris")
    

    coro_animal([p, g])

    # Si intentás instanciar Animal y llamar a hablar(), lanzará NotImplementedError.
    try:
        z = Animal("Zuquer")
        print(z.hablar())
    except NotImplementedError as e:
        print(f"Error esperado: {e}")

    print("terminó el programa con éxito")