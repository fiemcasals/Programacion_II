# 04_properties_encapsulation.py — Encapsulación con @property y validación

class CuentaBancaria:
    def __init__(self, titular: str, balance_inicial: float = 0.0):
        self.titular = titular
        self._balance = 0.0    # convención: un subrayado = "protegido" -> print(c._balance)  # ⚠️ se puede, pero no deberías hacerlo, deberias usar un metodo propio de la clase. Ver atributo privado al final del codigo
        # que self.balance ese inicalizado previamente se debe a que en la siguiente linea, si las condiciones no estan dadas no se inicializa la variable.
        self.balance = balance_inicial  # usa setter para validar
        #balance no esta protegido, porque no es un atributo sino mas bien una interfaz que llama a las funciones

    @property #crea un objeto especial de tipo property y lo asocia al nombre balance. Ese objeto guarda internamente un getter
    def balance(self) -> float:
        return self._balance

    @balance.setter #@balance.setter no es un decorador genérico, sino un método del objeto property creado antes.
    def balance(self, valor: float) -> None:
        if valor < 0:
            raise ValueError("El balance no puede ser negativo")
        self._balance = float(valor)

    def depositar(self, monto: float) -> None:
        if monto <= 0:
            raise ValueError("Monto inválido")
        self._balance += monto

    def extraer(self, monto: float) -> None:
    
        try:
            if monto <= 0 or monto > self._balance:
                raise ValueError(f"Extracción inválida, no posee tal impore para retirar, su importe maximo es      {self._balance}")
            self._balance -= monto
        except ValueError as e:
            print(f"ValueError {e}")

if __name__ == "__main__":
    c = CuentaBancaria("Grace", 1000)
    c.depositar(250)
    c.extraer(400)
    print("Balance:", c.balance)  # 850.0
    c.extraer(900)
    
    
"""
class Cuenta:
    def __init__(self):
        self.__secreto = 42

c = Cuenta()
c._balance = -400
# print(c._secreto) 
# print(c.__secreto)  # ❌ falla
print(c._Cuenta__secreto)  # ✅ funciona (name mangling)
"""
# p = Persona("mauricio")
#print (p._Persona__nombre)

"""
🔹 Diferencia clave

Sin property → más claro para principiantes (sé que estoy llamando un método), pero más incómodo de usar.

Con property → se escribe como si fuera un atributo normal (c.balance), pero sigue teniendo validación interna.
"""
