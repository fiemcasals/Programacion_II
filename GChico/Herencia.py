# genera dos clases abstractas (biologicos y academicos) y una clase "persona" que hereda de ambas
# la clase persona tiene un atributo que es una estrategia (modoSaludo)
# la clase persona se instancia a través de una factory (ConstructorPersona) que permite variar la estrategia
# la factory usa un registro para mapear strings a clases de estrategia
# la factory tiene un método de clase "crear" que recibe los parámetros necesarios para instanciar una persona
# y devuelve una instancia de persona con la estrategia adecuada


# vamos a crear una persona que hereda de:
# - datos biológicos
# - datos académicos

# Incluir herencia, polimorfismo, property, strategy, factory, typing

# usamos property para los atributos de las clases (aún no implementado acá)
# usamos strategy para el modoSaludo (aún no implementado acá)

class DatosBiologicos:
    def __init__(self, altura: int, sexo: str):
        self.altura = altura
        self.sexo = sexo
class AcademicosDatos:
    def __init__(self, secundarioCompleto: bool, nivel: str):
        self.secundarioCompleto = secundarioCompleto
        self.nivelAlcanzado = nivel
class MetodoSaludo:
    def saludar(self):
        return f"No esta definido"
class SaludoFormal:
    def saludar(self):
        return f"Mucho gusto"
class SaludoInformal:
    def saludar(self):
        return f"Hola"
class Persona(DatosBiologicos, AcademicosDatos):
    def __init__(self, altura: float, sexo, secundarioCompleto: bool, nivel: str, name: str, formaSaludo: MetodoSaludo):
        DatosBiologicos.__init__(self, altura, sexo)
        AcademicosDatos.__init__(self, secundarioCompleto, nivel)
       
        self.nombre = name
        self.saludo = formaSaludo  
    def __str__(self):
        return (
            f"Buenos días, mi nombre es {self.nombre}, mi altura es {self.altura}, soy {self.sexo},terminé el secundario: {self.secundarioCompleto}, y mi nivel académico alcanzado es {self.nivelAlcanzado}, {self.saludo.saludar()}"
        )
class ConstructorPersona:
    registroModoSaludo = {
        "formal" : SaludoFormal,
        "informal" : SaludoInformal
    }
    @classmethod
    def crear(cls, altura: float, sexo: str, booleano: bool, nivelAcademicoAlcanzado: str, name: str, tipoSaludo: str) -> Persona:
        return Persona(altura, sexo, booleano, nivelAcademicoAlcanzado, name, cls.registroModoSaludo[tipoSaludo]()) 
# -----------------------------
# Ejemplo de uso
# -----------------------------
persona1 = ConstructorPersona.crear(1.85, "hombre", True, "universitario", "Gaston Chico", "formal")
print(persona1)

persona2 = ConstructorPersona.crear(1.60, "mujer", True, "secundario", "Juana Perez", "informal")
print(persona2)

persona3 = ConstructorPersona.crear(1.75, "hombre", True, "terciario", "Sidharta Kiwi", "informal")
print(persona3)

persona4 = ConstructorPersona.crear(1.90, "hombre", False, "ninguno", "Homero Simpson", "formal")
print(persona4)

persona5 = ConstructorPersona.crear(1.80, "no binarie", True, "secundario", "Carolo Casini", "informal")
print(persona5)

