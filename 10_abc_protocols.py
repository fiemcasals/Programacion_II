# 10_abc_protocols.py — Clases abstractas vs Protocol (duck typing)
from abc import ABC, abstractmethod
from typing import Protocol

class Recurso(ABC):
    @abstractmethod
    def abrir(self) -> None: ...
    @abstractmethod
    def cerrar(self) -> None: ...

class Archivo(Recurso):
    def __init__(self, ruta: str):
        self.ruta = ruta
        self._abierto = False

    def abrir(self) -> None:
        self._abierto = True

    def cerrar(self) -> None:
        self._abierto = False

class SoporteLog(Protocol):
    def write(self, msg: str) -> int: ...

def loggear(logger: SoporteLog, msg: str) -> None:
    logger.write(msg + "\n")

if __name__ == "__main__":
    a = Archivo("demo.txt")
    a.abrir(); a.cerrar()
    loggear(logger=open(__file__, "a"), msg="Hola duck typing!")  # usa Protocol
