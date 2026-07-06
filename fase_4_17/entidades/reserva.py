# entidades/reserva.py
# Clase Reserva que integra cliente, servicio, duración y estado
# Implementa confirmación, cancelación y procesamiento con manejo de excepciones

from entidades.entidad_base import Entidad  # Importamos la clase padre
from excepciones.excepciones import ReservaInvalidaError, OperacionNoPermitidaError  # Excepciones
from entidades.cliente import Cliente  # Importamos Cliente para validar tipo
from servicios.servicio_base import Servicio  # Importamos Servicio para validar tipo
from utils.logger import logger  # Importamos el logger para registrar eventos


class Reserva(Entidad):
    """Clase que representa una reserva en el sistema Software FJ.
    Integra un cliente con un servicio por una duración determinada."""

    def __init__(self, id_reserva, nombre, cliente, servicio, duracion):
        # Llamamos al constructor padre con id y nombre de la reserva
        super().__init__(id=id_reserva, nombre=nombre)

        # Validamos que el cliente sea una instancia válida de Cliente
        if not isinstance(cliente, Cliente):
            raise ReservaInvalidaError("El cliente no es válido.")
        # Validamos que el servicio sea una instancia válida de Servicio
        if not isinstance(servicio, Servicio):
            raise ReservaInvalidaError("El servicio proporcionado no es válido.")
        # Validamos que la duración sea un número positivo
        if not isinstance(duracion, (int, float)) or duracion <= 0:
            raise ReservaInvalidaError("La duración debe ser un número positivo.")

        # Almacenamos los datos de la reserva
        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        # Estado inicial de la reserva: pendiente
        self.estado = "pendiente"

    def procesar(self):
        """Procesa la reserva validando parámetros y calculando el costo.
        Usa try/except/else/finally para manejar excepciones."""
        try:
            # Intentamos validar los parámetros del servicio
            self.servicio.validar_parametros(horas=self.duracion)
            # Calculamos el costo del servicio
            costo = self.servicio.calcular_costo(horas=self.duracion)
        except Exception as e:
            # Si ocurre un error, registramos en el log y relanzamos
            logger.error(f"Error al procesar reserva {self.id}: {e}")
            self.estado = "fallida"
            raise ReservaInvalidaError(
                f"No se pudo procesar la reserva: {e}"
            ) from e  # Encadenamiento de excepciones
        else:
            # Si no hubo excepciones, confirmamos la reserva
            self.estado = "confirmada"
            self.cliente.agregar_reserva(self)
            logger.info(f"Reserva {self.id} confirmada. Costo: ${costo:,.0f}")
        finally:
            # Este bloque siempre se ejecuta, haya o no error
            logger.info(f"Procesamiento de reserva {self.id} finalizado. Estado: {self.estado}")

    def cancelar(self):
        """Cancela la reserva si está confirmada."""
        if self.estado != "confirmada":
            raise OperacionNoPermitidaError(
                f"No se puede cancelar una reserva con estado '{self.estado}'."
            )
        self.estado = "cancelada"
        logger.info(f"Reserva {self.id} cancelada exitosamente.")

    def describir(self):
        """Implementación del método abstracto de Entidad."""
        return (f"Reserva [{self.id}]: {self.cliente.nombre} -> "
                f"{self.servicio.nombre} | Duración: {self.duracion}h | "
                f"Estado: {self.estado}")

    def __str__(self):
        """Representación en texto de la reserva."""
        return self.describir()
