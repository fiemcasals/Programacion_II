# 07_composition_vehicle_lidar_abc.py — Composición con ABC (@abstractmethod)  # Título y enfoque del ejemplo

from abc import ABC, abstractmethod  # Importa ABC para clases abstractas y @abstractmethod para métodos obligatorios

class SensorABC(ABC):                 # Define una clase base abstracta (no se puede instanciar directamente)
    @abstractmethod                   # Indica que el siguiente método es abstracto: las subclases DEBEN implementarlo
    def leer(self) -> float:          # Firma del método requerido: debe devolver un float (distancia en metros)
        ...                           # Cuerpo vacío a propósito (placeholder); aquí no hay implementación

class LidarSim(SensorABC):            # Simulador concreto de sensor: hereda de SensorABC
    def __init__(self, distancia_fija: float):  # Constructor: recibe una distancia constante simulada
        self.distancia_fija = distancia_fija    # Guarda la distancia en un atributo de la instancia
    def leer(self) -> float:                    # Implementa el método abstracto: ahora la clase ya no es abstracta
        return self.distancia_fija              # Devuelve la distancia simulada (float)

class RadarSim(SensorABC):            # Otro simulador concreto de sensor: también hereda de SensorABC
    def __init__(self, eco: float):             # Constructor: recibe el valor de “eco” (distancia simulada)
        self.eco = eco                           # Asigna el valor recibido al atributo de instancia
    def leer(self) -> float:                    # Implementa el método abstracto requerido por la ABC
        return self.eco                         # Devuelve la lectura simulada (float)

class Vehiculo:                         # Clase que compone (contiene) una colección de sensores
    def __init__(self, sensores: list[SensorABC]):  # Recibe una lista de objetos que sean subclases de SensorABC
        self.sensores = sensores                 # Guarda la lista de sensores para uso posterior
        self.velocidad = 0.0                     # Inicializa la velocidad del vehículo en 0.0 (float)

    def decidir(self) -> str:                    # Determina la acción a tomar según las lecturas de los sensores
        d_min = min(s.leer() for s in self.sensores)  # Calcula la distancia mínima leída entre todos los sensores
        if d_min < 1.0:                          # Si hay un obstáculo muy cercano (< 1.0 m)
            self.velocidad = 0.0                 #   -> establece velocidad en 0.0
            return "Frenar"                      #   -> acción: frenar
        elif d_min < 3.0:                        # Si el obstáculo está próximo (>=1.0 m y <3.0 m)
            self.velocidad = 10.0                #   -> reduce la velocidad a 10.0 (valor de ejemplo)
            return "Reducir"                     #   -> acción: reducir
        else:                                    # Si la distancia es segura (>= 3.0 m)
            self.velocidad = 25.0                #   -> fija la velocidad en 25.0 (valor de ejemplo)
            return "Avanzar"                     #   -> acción: avanzar

if __name__ == "__main__":                       # Punto de entrada: se ejecuta solo al correr este archivo directamente
    # SensorABC()  # ❌ ERROR si se descomenta: no se puede instanciar una clase abstracta (TypeError)
    v = Vehiculo([LidarSim(2.2), RadarSim(10.0)])  # Crea un vehículo con un Lidar (2.2 m) y un Radar (10.0 m)
    accion = v.decidir()                           # Ejecuta la lógica de decisión usando la distancia mínima de los sensores
    print("Acción:", accion, "| Velocidad:", v.velocidad)  # Muestra la acción resultante y la velocidad fijada

