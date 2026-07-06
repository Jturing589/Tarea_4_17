# entidades/entidad_base.py
# Clase abstracta base que representa cualquier entidad del sistema
# Todas las entidades del sistema heredan de esta clase

from abc import ABC, abstractmethod  # Importamos ABC para definir clases abstractas
from datetime import datetime  # Importamos datetime para registrar la fecha de creación


class Entidad(ABC):
    """Clase abstracta que sirve como base para todas las entidades del sistema."""

    def __init__(self, id, nombre):
        # Almacenamos el identificador único de la entidad
        self.id = id
        # Almacenamos el nombre descriptivo de la entidad
        self.nombre = nombre
        # Registramos la fecha y hora en que se creó la entidad
        self.fecha_creacion = datetime.now()

    @abstractmethod
    def describir(self):
        """Método abstracto que obliga a las subclases a implementar su propia descripción."""
        pass

    def __str__(self):
        """Representación en texto de la entidad con su id y nombre."""
        return f"[{self.id}] {self.nombre}"
