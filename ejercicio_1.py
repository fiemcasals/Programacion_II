#Herencia y polimorfismo (clases hijas de Loan y estrategias de amortización).
#@property y @…setter (validaciones de balance, interest_rate, periods).
#Strategy (estrategias de amortización: Alemán, Americano, Francés).
#Factory (creación de créditos según el tipo pedido).

from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Dict


# ==============================
# 1) Cuenta bancaria con property
# ==============================
class BankAccount:
    """Cuenta bancaria simple con balance protegido, depósito y extracción."""

    def __init__(self, owner: str, balance: float = 0.0) -> None:
        self._owner = owner
        self._balance = 0.0
        self.balance = balance  # valida por setter

    @property
    def owner(self) -> str:
        return self._owner

    @property
    def balance(self) -> float:
        """Balance disponible. No puede ser negativo."""
        return self._balance

    @balance.setter
    def balance(self, value: float) -> None:
        if value < 0:
            raise ValueError("El balance no puede ser negativo.")
        self._balance = float(value)

    def deposit(self, amount: float) -> None:
        try:
            if amount <= 0:
                raise ValueError("El depósito debe ser > 0.")
            self._balance += float(amount)
        except ValueError as e:
            print(e)

    def withdraw(self, amount: float) -> None: #withdraw = extraccion
        try:
            if amount <= 0:
                raise ValueError("La extracción debe ser > 0.")
            if amount > self._balance:
                raise ValueError("Fondos insuficientes.")
            self._balance -= float(amount)
        except ValueError as e:
            print(e)

    def __repr__(self) -> str:
        return f"BankAccount(owner={self.owner!r}, balance={self.balance:.2f})"


# ======================================================
# 2) Strategy pattern: estrategias de amortización (ABC)
# ======================================================
class RepaymentStrategy(ABC):
    """Estrategia de amortización: arma el cronograma de pagos."""
    name: str

    @abstractmethod
    def build_schedule(self, principal: float, interest_rate: float, periods: int) -> List[Dict]:
        # """
        # Devuelve una lista de dicts con:
        # period, payment, interest, amortization, remaining
        # """
        ...   # Aún no implementado

# Esto NO da error


class GermanStrategy(RepaymentStrategy):
    """
    Crédito Alemán: amortización de capital constante (P/n).
    Pago = interés del saldo + amortización constante. Cuota decreciente.
    """
    name = "aleman"

    def build_schedule(self, principal: float, interest_rate: float, periods: int) -> List[Dict]:
        schedule = []
        remaining = principal
        amort = principal / periods
        for k in range(1, periods + 1):
            interest = remaining * interest_rate
            payment = interest + amort
            remaining = max(0.0, remaining - amort) #se asegura que el sando "remaining" no sea negativo
            schedule.append({
                "period": k,
                "payment": payment,
                "interest": interest,
                "amortization": amort,
                "remaining": remaining
            })
        return schedule


class AmericanStrategy(RepaymentStrategy):
    """
    Crédito Americano: sólo intereses cada período; al final, capital + último interés.
    Cuotas planas (interés) y una última grande (bullet).
    """
    name = "americano"

    def build_schedule(self, principal: float, interest_rate: float, periods: int) -> List[Dict]:
        schedule = []
        interest_payment = principal * interest_rate
        # Períodos 1..(n-1): sólo interés
        for k in range(1, periods):
            schedule.append({
                "period": k,
                "payment": interest_payment,
                "interest": interest_payment,
                "amortization": 0.0,
                "remaining": principal
            })
        # Último período: interés + capital
        final_interest = principal * interest_rate
        schedule.append({
            "period": periods,
            "payment": final_interest + principal,
            "interest": final_interest,
            "amortization": principal,
            "remaining": 0.0
        })
        return schedule


class FrenchStrategy(RepaymentStrategy):
    """
    Crédito Francés: cuota constante (sistema de anualidades).
    A = P * i / (1 - (1+i)^-n)
    """
    name = "frances"

    def build_schedule(self, principal: float, interest_rate: float, periods: int) -> List[Dict]:
        schedule = []
        i = interest_rate
        if i == 0:
            # Sin interés: pagos iguales de capital
            amort = principal / periods
            remaining = principal
            for k in range(1, periods + 1):
                payment = amort
                remaining = max(0.0, remaining - amort)
                schedule.append({
                    "period": k,
                    "payment": payment,
                    "interest": 0.0,
                    "amortization": amort,
                    "remaining": remaining
                })
            return schedule

        annuity = principal * i / (1 - (1 + i) ** (-periods))
        remaining = principal
        for k in range(1, periods + 1):
            interest = remaining * i
            amort = annuity - interest
            remaining = max(0.0, remaining - amort)
            schedule.append({
                "period": k,
                "payment": annuity,
                "interest": interest,
                "amortization": amort,
                "remaining": remaining
            })
        return schedule


# ===================================================
# 3) Loan base: usa Strategy + validaciones (@property)
# ===================================================
class Loan(ABC):
    """
    Préstamo genérico que usa una estrategia de amortización (Strategy)
    y un Factory para instanciar variantes.
    Todas las variantes deben validar interés y períodos por @property.
    """

    def __init__(self, account: BankAccount, interest_rate: float, periods: int, strategy: RepaymentStrategy) -> None:
        self._account = account
        self._interest_rate = 0.0
        self._periods = 0
        self.strategy = strategy

        self.interest_rate = interest_rate  # valida (setter)
        self.periods = periods              # valida (setter)

    @property
    def account(self) -> BankAccount:
        return self._account

    @property
    def interest_rate(self) -> float:
        """Tasa por período (ej: 0.03 = 3% mensual). Debe estar entre 0 y 1."""
        return self._interest_rate

    @interest_rate.setter
    def interest_rate(self, value: float) -> None:
        if not (0.0 <= value < 1.0):
            raise ValueError("interest_rate debe estar en [0, 1). Use 0.03 para 3% por período.")
        self._interest_rate = float(value)

    @property
    def periods(self) -> int:
        return self._periods

    @periods.setter
    def periods(self, value: int) -> None:
        if value <= 0:
            raise ValueError("periods debe ser un entero positivo.")
        self._periods = int(value)

    # --- Reglas de aprobación por balance ---
    @abstractmethod
    def approval_multiplier(self) -> float:
        """
        Multiplicador de balance permitido para determinar el monto máximo prestable.
        Ej.: return 3.0 => monto máximo = 3 * balance de la cuenta.
        """
        ...

    def max_principal_allowed(self) -> float:
        """Calcula cuánto se puede prestar en función del balance de la cuenta."""
        return self.account.balance * self.approval_multiplier()

    # --- Cronograma de pagos ---
    def build_schedule(self, requested_principal: float) -> List[Dict]:
        """Limita el capital al máximo permitible y arma el cronograma con la Strategy."""
        principal = min(requested_principal, self.max_principal_allowed())
        if principal <= 0:
            raise ValueError("El principal solicitado no es financiable (verifique el balance).")
        return self.strategy.build_schedule(principal, self.interest_rate, self.periods)

    def summary(self, requested_principal: float) -> Dict:
        schedule = self.build_schedule(requested_principal)
        total_paid = sum(row["payment"] for row in schedule)
        total_interest = sum(row["interest"] for row in schedule)
        return {
            "type": type(self).__name__,
            "strategy": self.strategy.name,
            "approved_principal": min(requested_principal, self.max_principal_allowed()),
            "periods": self.periods,
            "interest_rate": self.interest_rate,
            "total_paid": total_paid,
            "total_interest": total_interest,
            "schedule": schedule,
        }


# ===========================================================
# 4) Clases concretas de Loan (herencia + polimorfismo real)
# ===========================================================
class GermanLoan(Loan):
    """Hereda de Loan y fija Strategy Alemana. Multiplicador conservador."""
    def __init__(self, account: BankAccount, interest_rate: float, periods: int) -> None:
        super().__init__(account, interest_rate, periods, strategy=GermanStrategy())

    def approval_multiplier(self) -> float:
        # Ejemplo: conservador (2x el balance)
        return 2.0


class AmericanLoan(Loan):
    """Hereda de Loan y fija Strategy Americana."""
    def __init__(self, account: BankAccount, interest_rate: float, periods: int) -> None:
        super().__init__(account, interest_rate, periods, strategy=AmericanStrategy())

    def approval_multiplier(self) -> float:
        # Ejemplo: más restrictivo (1.5x) por alto pago final (bullet)
        return 1.5


class FrenchLoan(Loan):
    """Hereda de Loan y fija Strategy Francesa."""
    def __init__(self, account: BankAccount, interest_rate: float, periods: int) -> None:
        super().__init__(account, interest_rate, periods, strategy=FrenchStrategy())

    def approval_multiplier(self) -> float:
        # Ejemplo: algo más flexible (3x) por cuota nivelada
        return 3.0


# =======================
# 5) Loan Factory (Simple)
# =======================
class LoanFactory:
    """
    Crea instancias de préstamos en base a una etiqueta.
    Integra con Strategy (cada Loan fija su estrategia).
    """
    REGISTRY = {
        "aleman": GermanLoan,
        "alemán": GermanLoan, 
        "americano": AmericanLoan,
        "frances": FrenchLoan, 
        "francés": FrenchLoan, 
    }

    @classmethod
    def create(cls, kind: str, account: BankAccount, interest_rate: float, periods: int) -> Loan:
        kind = kind.strip().lower()
        if kind not in cls.REGISTRY:
            raise ValueError(f"Tipo de crédito desconocido: {kind!r}. "
                             f"Use uno de: {', '.join(sorted(cls.REGISTRY))}")
        return cls.REGISTRY[kind](account, interest_rate, periods)


# ======================================
# 6) Ejemplo de uso (demo rápida/manual)
# ======================================
if __name__ == "__main__":
    # 1) Cuenta y depósitos (property + setter validando)
    cuenta = BankAccount(owner="Mauricio", balance=1000.0)
    cuenta.deposit(500.0)   # balance = 1500
    # cuenta.balance = -10   # -> ValueError

    # 2) Crear préstamos por Factory (cada uno con Strategy distinta)
    prestamo_aleman   = LoanFactory.create("alemán",   cuenta, interest_rate=0.03, periods=12)
    prestamo_americano= LoanFactory.create("americano",cuenta, interest_rate=0.03, periods=12)
    prestamo_frances  = LoanFactory.create("francés",  cuenta, interest_rate=0.03, periods=12)

    # 3) Solicitar $10.000 y ver cuánto aprueban según balance y tipo
    requested = 10_000.0

    for loan in (prestamo_aleman, prestamo_americano, prestamo_frances):
        info = loan.summary(requested)
        print("\n==========================")
        print(f"Tipo: {info['type']} (estrategia: {info['strategy']})")
        print(f"Balance cuenta: {cuenta.balance:.2f}")
        print(f"Solicitado: {requested:.2f}")
        print(f"Aprobado según balance: {info['approved_principal']:.2f}")
        print(f"Tasa: {info['interest_rate']*100:.2f}% por período - Plazo: {info['periods']} períodos")
        print(f"Total pagado: {info['total_paid']:.2f} | Interés total: {info['total_interest']:.2f}")

        # Mostrar primeras 3 filas del cronograma
        print("Primeros períodos:")
        for row in info["schedule"][:3]:
            print(f"  t={row['period']:02d} | pago={row['payment']:.2f} "
                  f"(interés={row['interest']:.2f}, amort={row['amortization']:.2f}) "
                  f"restante={row['remaining']:.2f}")

