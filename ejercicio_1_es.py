# =======================
# Patrones de diseño usados:
# Herencia, Polimorfismo, Strategy, Factory, Property
# =======================

from __future__ import annotations  # Permite referirse a clases no definidas. Ej usar el objeto Nodo en la clase Nodo.
from abc import ABC, abstractmethod  # Para definir clases y métodos abstractos (interfaces)
from typing import List, Dict  # Tipado de listas y diccionarios #List[Dict]:

# =======================================
# 1) Cuenta bancaria con @property + setter
# =======================================
class CuentaBancaria:
    """Cuenta bancaria simple con balance protegido, depósito y extracción."""

    def __init__(self, titular_cuenta: str, saldo_inicial: float = 0.0) -> None:
        self._titular = titular_cuenta  # Atributo protegido
        self._saldo = 0.0        # Inicializa saldo en cero
        self.saldo = saldo_inicial  # Usa el setter para validar saldo

    @property
    def titular(self) -> str:
        return self._titular  # Getter del titular

    @property
    def saldo(self) -> float:
        """Saldo disponible. No puede ser negativo."""
        return self._saldo  # Getter del saldo

    @saldo.setter
    def saldo(self, valor: float) -> None:
        # Setter del saldo con validación
        if valor < 0:
            raise ValueError("El saldo no puede ser negativo.")
        self._saldo = float(valor)

    def depositar(self, monto: float) -> None:
        # Método para depositar dinero, valida que sea positivo
        try:
            if monto <= 0:
                raise ValueError("El depósito debe ser mayor a cero.")
            self._saldo += float(monto)
        except ValueError as e:
            print(e)

    def extraer(self, monto: float) -> None:
        # Método para extraer dinero, valida monto y saldo suficiente
        try:
            if monto <= 0:
                raise ValueError("La extracción debe ser mayor a cero.")
            if monto > self._saldo:
                raise ValueError("Fondos insuficientes.")
            self._saldo -= float(monto)
        except ValueError as e:
            print(e)

    def __repr__(self) -> str:
        # Representación legible de la cuenta
        return f"CuentaBancaria(titular={self.titular!r}, saldo={self.saldo:.2f})"

# ========================================
# 2) Estrategias de amortización (Strategy)
# ========================================

class EstrategiaAmortizacion(ABC):
    """Estrategia para generar cronograma de pagos."""

    nombre: str  # Nombre de la estrategia

    @abstractmethod
    def generar_cronograma(self, capital: float, tasa: float, periodos: int) -> List[Dict]:
        # Método abstracto a implementar en subclases
        pass

# ---------- Alemana ----------
class EstrategiaAlemana(EstrategiaAmortizacion):
    nombre = "alemana"

    def generar_cronograma(self, capital: float, tasa: float, periodos: int) -> List[Dict]:
        cronograma = []
        saldo = capital
        amortizacion = capital / periodos  # Amortización fija
        for t in range(1, periodos + 1):
            interes = saldo * tasa
            pago = interes + amortizacion
            saldo = max(0.0, saldo - amortizacion)
            cronograma.append({
                "periodo": t,
                "pago": pago,
                "interes": interes,
                "amortizacion": amortizacion,
                "restante": saldo
            })
        return cronograma #"este es un cronograma propio de una estrategia de credio aleman"

# ---------- Americana ----------
class EstrategiaAmericana(EstrategiaAmortizacion):
    nombre = "americana"

    def generar_cronograma(self, capital: float, tasa: float, periodos: int) -> List[Dict]:
        cronograma = []
        interes_periodico = capital * tasa  # Solo se pagan intereses hasta el último período
        for t in range(1, periodos):
            cronograma.append({
                "periodo": t,
                "pago": interes_periodico,
                "interes": interes_periodico,
                "amortizacion": 0.0,
                "restante": capital
            })
        cronograma.append({
            "periodo": periodos,
            "pago": interes_periodico + capital,
            "interes": interes_periodico,
            "amortizacion": capital,
            "restante": 0.0
        })
        return cronograma

# ---------- Francesa ----------
class EstrategiaFrancesa(EstrategiaAmortizacion):
    nombre = "francesa"

    def generar_cronograma(self, capital: float, tasa: float, periodos: int) -> List[Dict]:
        cronograma = []
        i = tasa
        if i == 0:
            # Si tasa es cero, amortización fija
            amort = capital / periodos
            saldo = capital
            for t in range(1, periodos + 1):
                pago = amort #cuota fija
                saldo = max(0.0, saldo - amort)
                cronograma.append({
                    "periodo": t,
                    "pago": pago,
                    "interes": 0.0,
                    "amortizacion": amort,
                    "restante": saldo
                })
            return cronograma

        # Cuota constante según fórmula de anualidad
        anualidad = capital * i / (1 - (1 + i) ** (-periodos))
        saldo = capital
        for t in range(1, periodos + 1):
            interes = saldo * i
            amortizacion = anualidad - interes
            saldo = max(0.0, saldo - amortizacion)
            cronograma.append({
                "periodo": t,
                "pago": anualidad,
                "interes": interes,
                "amortizacion": amortizacion,
                "restante": saldo
            })
        return cronograma

# =======================================
# 3) Clase base Prestamo con propiedades
# =======================================
class Prestamo(ABC):
    def __init__(self, cuenta: CuentaBancaria, tasa: float, periodos: int, estrategia: EstrategiaAmortizacion) -> None:
        # Constructor base, recibe cuenta, tasa, plazos y estrategia
        self._cuenta = cuenta
        self._tasa = 0.0
        self._periodos = 0
        self.estrategia = estrategia

        self.tasa = tasa         # Setter con validación
        self.periodos = periodos # Setter con validación

    @property
    def cuenta(self) -> CuentaBancaria:
        return self._cuenta

    @property
    def tasa(self) -> float:
        return self._tasa

    @tasa.setter
    def tasa(self, valor: float) -> None:
        if not (0.0 <= valor < 1.0):
            raise ValueError("La tasa debe estar entre 0 y 1. Use 0.03 para 3%.")
        self._tasa = float(valor)

    @property
    def periodos(self) -> int:
        return self._periodos

    @periodos.setter
    def periodos(self, valor: int) -> None:
        if valor <= 0:
            raise ValueError("Los períodos deben ser mayores a cero.")
        self._periodos = int(valor)

    @abstractmethod
    def multiplicador_aprobacion(self) -> float:
        # Método abstracto que define cuánto puede pedir según el saldo
        pass

    def capital_maximo(self) -> float:
        # Devuelve cuánto puede pedir según el saldo
        return self.cuenta.saldo * self.multiplicador_aprobacion()

    def generar_cronograma(self, capital_solicitado: float) -> List[Dict]:
        # Genera el plan de pagos, respetando el capital máximo
        capital = min(capital_solicitado, self.capital_maximo())
        if capital <= 0:
            raise ValueError("Capital solicitado no financiable.")
        return self.estrategia.generar_cronograma(capital, self.tasa, self.periodos)

    def resumen(self, capital_solicitado: float) -> Dict:
        # Devuelve un resumen con el cronograma y totales
        cronograma = self.generar_cronograma(capital_solicitado)
        total_pagado = sum(fila["pago"] for fila in cronograma)
        total_interes = sum(fila["interes"] for fila in cronograma)
        return {
            "tipo": type(self).__name__,
            "estrategia": self.estrategia.nombre,
            "capital_aprobado": min(capital_solicitado, self.capital_maximo()),
            "periodos": self.periodos,
            "tasa": self.tasa,
            "total_pagado": total_pagado,
            "interes_total": total_interes,
            "cronograma": cronograma
        }

# ===================================================
# 4) Clases específicas de préstamo (herencia real)
# ===================================================
class PrestamoAleman(Prestamo):
    def __init__(self, cuenta: CuentaBancaria, tasa: float, periodos: int) -> None:
        # Se pasa directamente la estrategia alemana
        super().__init__(cuenta, tasa, periodos, estrategia=EstrategiaAlemana())

    def multiplicador_aprobacion(self) -> float:
        return 2.0  # Puede pedir hasta 2x el saldo

class PrestamoAmericano(Prestamo):
    def __init__(self, cuenta: CuentaBancaria, tasa: float, periodos: int) -> None:
        super().__init__(cuenta, tasa, periodos, estrategia=EstrategiaAmericana())

    def multiplicador_aprobacion(self) -> float:
        return 1.5  # Puede pedir hasta 1.5x el saldo

class PrestamoFrances(Prestamo):
    def __init__(self, cuenta: CuentaBancaria, tasa: float, periodos: int) -> None:
        super().__init__(cuenta, tasa, periodos, estrategia=EstrategiaFrancesa())

    def multiplicador_aprobacion(self) -> float:
        return 3.0  # Puede pedir hasta 3x el saldo

# ====================
# 5) Fábrica de préstamos (Factory Pattern)
# ====================
class FabricaPrestamos:
    # Diccionario que asocia tipos de préstamo con sus clases
    REGISTRO = {
        "aleman": PrestamoAleman,
        "alemán": PrestamoAleman,
        "americano": PrestamoAmericano,
        "frances": PrestamoFrances,
        "francés": PrestamoFrances
    }

    @classmethod
    def crear(cls, tipo: str, cuenta: CuentaBancaria, tasa: float, periodos: int) -> Prestamo:
        # Método de clase que crea un préstamo según el tipo
        tipo = tipo.strip().lower()
        if tipo not in cls.REGISTRO:
            raise ValueError(f"Tipo desconocido: {tipo!r}. Opciones válidas: {', '.join(cls.REGISTRO)}")
        return cls.REGISTRO[tipo](cuenta, tasa, periodos)

# ============================
# 6) Ejemplo de uso manual
# ============================
if __name__ == "__main__":
    # Creamos una cuenta bancaria
    cuenta = CuentaBancaria("Mauricio", 1000.0)
    cuenta.depositar(500.0)

    # Creamos tres préstamos de tipo diferente
    p1 = FabricaPrestamos.crear("alemán", cuenta, 0.03, 12)
    p2 = FabricaPrestamos.crear("americano", cuenta, 0.03, 12)
    p3 = FabricaPrestamos.crear("francés", cuenta, 0.03, 12)

    solicitado = 10000.0  # Capital que el cliente quiere

    # Mostramos los resúmenes de cada préstamo
    for prestamo in (p1, p2, p3):
        info = prestamo.resumen(solicitado)
        print("\n===============================")
        print(f"Tipo: {info['tipo']} | Estrategia: {info['estrategia']}")
        print(f"Solicitado: {solicitado:.2f} | Aprobado: {info['capital_aprobado']:.2f}")
        print(f"Tasa: {info['tasa']*100:.2f}% | Plazo: {info['periodos']} períodos")
        print(f"Total pagado: {info['total_pagado']:.2f} | Interés total: {info['interes_total']:.2f}")
        print("Primeras cuotas:")
        for fila in info["cronograma"][:3]:  # Muestra solo 3 cuotas
            print(f"  t={fila['periodo']:02d} | pago={fila['pago']:.2f} "
                  f"(interés={fila['interes']:.2f}, amort={fila['amortizacion']:.2f}) restante={fila['restante']:.2f}")
