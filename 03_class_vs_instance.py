# 03_class_vs_instance.py — Atributos de clase vs instancia

class Contador:
    # Atributo de *clase* (compartido por todas las instancias)
    total_instancias = 0

    def __init__(self):
        # lado-efecto: conteo global
        Contador.total_instancias += 1
        # Atributo de *instancia* (propio de cada objeto)
        self.local = 0

    def inc(self):
        self.local += 1

    # def __str__(self):
    #     return "yo soy una objeto de la clase Contador"


if __name__ == "__main__":
    a = Contador()
    b = Contador()
    c = Contador()
    print(a)
    a.inc(); a.inc()#si querés poner más de una instrucción en la misma línea, podés separarlas con ;. Es lo mismo que escribir dos lineas
    b.inc()
    print("a.local:", a.local)             # 2
    print("b.local:", b.local)             # 1
    print("c.local:", c.local)             # 0
    print("total de instancias:", Contador.total_instancias)  # 3
