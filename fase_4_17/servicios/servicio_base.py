# servicios/servicio_base.py
# Clase abstracta Servicio que hereda de Entidad
# Define los métodos abstractos que todos los servicios deben implementar

from abc import abstractmethod  # Importamos abstractmethod para definir métodos abstractos
from entidades.entidad_base import Entidad  # Importamos la clase padre Entidad


class Servicio(Entidad):
    """Clase abstracta que representa un servicio ofrecido por Software FJ.
    Todos los servicios específicos deben heredar de esta clase."""

    @abstractmethod
    def calcular_costo(self, **kwargs):
        """Método abstracto para calcular el costo del servicio.
        Cada servicio implementa su propia lógica de cálculo."""
        pass

    @abstractmethod
    def validar_parametros(self, **kwargs):
        """Método abstracto para validar los parámetros del servicio.
        Cada servicio define qué parámetros necesita y cómo validarlos."""
        pass

    def describir(self):
        """Implementación del método abstracto de Entidad.
        Retorna una descripción básica del servicio."""
        return f"Servicio [{self.id}]: {self.nombre}"
