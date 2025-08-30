# =======================
# Ejemplo de Herencia Múltiple en Python
# =======================

# Clase base 1
class Volador:
    def volar(self) -> str:
        return "Estoy volando."


# Clase base 2
class Nadador:
    def nadar(self) -> str:
        return "Estoy nadando."


# Clase hija que hereda de ambas (herencia múltiple)
class Pato(Volador, Nadador):
    def hacer_sonido(self) -> str:
        return "¡Cuac cuac!"


# -----------------------------
# Ejemplo de uso
# -----------------------------
if __name__ == "__main__":
    pato = Pato()

    print(pato.hacer_sonido())   # Método propio
    print(pato.volar())          # Heredado de Volador
    print(pato.nadar())          # Heredado de Nadador
