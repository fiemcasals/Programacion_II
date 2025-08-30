# 11_mixins_mro.py — Mixins y orden de resolución de métodos (MRO)

class LogMixin:
    def log(self, msg: str) -> None:
        print(f"[LOG] {msg}")

class PersistenciaMixin:
    def save(self) -> None:
        # demo: guardar no implementado
        print("Guardado (demo)")

class Modelo(LogMixin, PersistenciaMixin):
    def __init__(self, nombre: str):
        self.nombre = nombre
        self.log("Modelo inicializado")  # método del mixin

if __name__ == "__main__":
    m = Modelo("Cliente")
    m.save()
    # Mostramos el MRO
    print(Modelo.mro())
