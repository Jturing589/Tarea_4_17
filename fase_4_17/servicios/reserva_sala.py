# servicios/reserva_sala.py
# Servicio especializado para reserva de salas físicas
# Implementa polimorfismo, validación de parámetros y cálculo de costos

from servicios.servicio_base import Servicio  # Importamos la clase padre Servicio
from excepciones.excepciones import ParametroFaltanteError, ServicioNoDisponibleError  # Excepciones
from utils.logger import logger  # Importamos el logger para registrar eventos


class ReservaSala(Servicio):
    """Servicio de reserva de salas físicas de Software FJ.
    Implementa polimorfismo y manejo de excepciones."""

    def __init__(self, id_entidad, nombre, capacidad):
        # Llamamos al constructor padre pasando id y nombre
        super().__init__(id=id_entidad, nombre=nombre)
        # Capacidad máxima de personas en la sala (atributo privado)
        self.__capacidad = capacidad
        # Precio base por hora de la sala
        self.__precio_hora_base = 50000

    def validar_parametros(self, **kwargs):
        """Valida las horas y la cantidad de personas para la reserva."""
        # Obtenemos los parámetros del diccionario kwargs
        horas = kwargs.get('horas', 0)
        personas = kwargs.get('personas', 0)

        # Verificamos que las horas sean un número positivo
        if not isinstance(horas, (int, float)) or horas <= 0:
            raise ParametroFaltanteError("El tiempo de reserva debe ser mayor a 0 horas.")

        # Verificamos que no se exceda la capacidad de la sala
        if personas > self.__capacidad:
            raise ServicioNoDisponibleError(
                f"La sala tiene capacidad para {self.__capacidad} personas, "
                f"se solicitaron {personas}."
            )

    def calcular_costo(self, **kwargs):
        """Calcula el costo de la reserva de sala.
        Método sobrecargado: acepta horas, impuesto y descuento opcionales."""
        # Obtenemos los parámetros con valores por defecto
        horas = kwargs.get('horas', 1)
        impuesto = kwargs.get('impuesto', 0.0)  # Porcentaje de impuesto (ej: 0.19)
        descuento = kwargs.get('descuento', 0.0)  # Porcentaje de descuento (ej: 0.10)

        # Calculamos el costo base multiplicando precio por horas
        costo_base = self.__precio_hora_base * horas
        # Aplicamos el descuento al costo base
        costo_con_descuento = costo_base * (1 - descuento)
        # Aplicamos el impuesto sobre el costo con descuento
        costo_final = costo_con_descuento * (1 + impuesto)

        # Registramos el cálculo en el log
        logger.info(f"Costo calculado para sala '{self.nombre}': ${costo_final:,.0f}")
        return costo_final

    def describir(self):
        """Sobrescribe el método describir para incluir capacidad y precio."""
        return (f"Sala '{self.nombre}' | Capacidad: {self.__capacidad} personas | "
                f"Precio/hora: ${self.__precio_hora_base:,.0f}")
