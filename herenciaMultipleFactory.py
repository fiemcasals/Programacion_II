# vamos a crear una persona que hereda de:
# - datos biológicos
# - datos académicos
# 
# usamos strategy para el modoSaludo (aún no implementado acá)
# usamos factory para poder variar la strategy (aún no implementado acá)

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
        return f"Hey"

class Persona(DatosBiologicos, AcademicosDatos):
    def __init__(self, altura, sexo, secundarioCompleto: bool, nivel: str, name: str, formaSaludo: MetodoSaludo):
        #no llamamos con sudo() a la clase padre, porque usa herencia multiple, tiene varios padres
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
    def crear(cls, altura, sexo: str, booleano: bool, nivelAcademicoAlcanzado: str, name: str, tipoSaludo: str) -> Persona:
        return Persona(altura, sexo, booleano, nivelAcademicoAlcanzado, name, cls.registroModoSaludo[tipoSaludo]()) 
        

# -----------------------------
# Ejemplo de uso
# -----------------------------
persona1 = ConstructorPersona.crear(1.82, "hombre", True, "universitario", "Mauri", "formal")
print(persona1)

