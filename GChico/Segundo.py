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

# usamos property para los atributos de las clases
# usamos strategy para el modoSaludo
# usamos factory para poder variar la strategy
# usamos typing para los tipos de datos
# usamos herencia multiple para que persona herede de biologicos y academicos
# usamos polimorfismo para que las clases de saludo tengan el mismo método saludar
# usamos ValueError para validar los datos de entrada


class DatosBiologicos:
    def __init__(self, altura: int, sexo: str):
        self.altura = altura
        self.sexo = sexo
    @property
    def altura(self):
        return self._altura
    @altura.setter
    def altura(self, value):
        if value <= 0:
            raise ValueError("La altura debe ser un valor positivo")
        self._altura = value
    @property
    def sexo(self):
        return self._sexo
    @sexo.setter
    def sexo(self, value):
        if value not in ["hombre", "mujer", "otro"]:
            raise ValueError("El sexo debe ser 'hombre', 'mujer' o 'otro'")
        self._sexo = value
class AcademicosDatos:
    def __init__(self, secundarioCompleto: bool, nivel: str):
        self.secundarioCompleto = secundarioCompleto
        self.nivelAlcanzado = nivel
    @property
    def secundarioCompleto(self):
        return self._secundarioCompleto
    @secundarioCompleto.setter
    def secundarioCompleto(self, value):
        if not isinstance(value, bool):
            raise ValueError("secundarioCompleto debe ser un valor booleano")
        self._secundarioCompleto = value
    @property
    def nivelAlcanzado(self):
        return self._nivelAlcanzado
    @nivelAlcanzado.setter
    def nivelAlcanzado(self, value):
        if value not in ["primario", "secundario", "universitario", "postgrado"]:
            raise ValueError("El nivel alcanzado debe ser 'primario', 'secundario', 'universitario' o 'postgrado'")
        self._nivelAlcanzado = value
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
            f"{self.saludo.saludar()}, buenos días, mi nombre es {self.nombre}, mi altura es {self.altura}, soy {self.sexo},terminé el secundario: {self.secundarioCompleto}, y mi nivel académico alcanzado es {self.nivelAlcanzado}. Adios!"
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
# Ejemplos de uso
# -----------------------------

persona1 = ConstructorPersona.crear(1.85, "hombre", True, "universitario", "Gaston Chico", "formal")
print(persona1)
persona2 = ConstructorPersona.crear(1.60, "mujer", True, "secundario", "Violencia Rivas", "informal")
print(persona2)
persona3 = ConstructorPersona.crear(1.75, "hombre", True, "postgrado", "Sidharta Kiwi", "informal")
print(persona3)
persona4 = ConstructorPersona.crear(1.90, "hombre", False, "secundario", "Jorge Suspenso", "formal")
print(persona4)
persona5 = ConstructorPersona.crear(1.80, "otro", True, "secundario", "Micky Vainilla", "informal")
print(persona5)



