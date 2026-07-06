# servicios/alquiler_equipo.py
# Servicio especializado para alquiler de equipos tecnológicos
# Implementa polimorfismo y manejo avanzado de excepciones

from servicios.servicio_base import Servicio  # Importamos la clase padre Servicio
from excepciones.excepciones import ParametroFaltanteError, ServicioNoDisponibleError  # Excepciones
from utils.logger import logger  # Importamos el logger para registrar eventos


class AlquilerEquipo(Servicio):
    """Servicio de alquiler de equipos tecnológicos de Software FJ.
    Implementa polimorfismo y manejo de excepciones."""

    def __init__(self, id_entidad, nombre, tipo_equipo):
        # Llamamos al constructor padre con id y nombre
        super().__init__(id=id_entidad, nombre=nombre)
        # Tipo de equipo a alquilar (atributo privado)
        self.__tipo_equipo = tipo_equipo
        # Diccionario con tarifas diarias por tipo de equipo
        self.__tarifas = {"Laptop": 35000, "Proyector": 25000, "Tablet": 15000}

    def validar_parametros(self, **kwargs):
        """Valida que los días/horas sean mayores a cero y el tipo de equipo exista."""
        # Aceptamos tanto 'dias' como 'horas' como parámetro de tiempo
        dias = kwargs.get('dias', kwargs.get('horas', None))
        # Verificamos que el parámetro exista, sea numérico y positivo
        if (
            dias is None
            or not isinstance(dias, (int, float))
            or dias <= 0
        ):
            # Registramos el error en el log antes de lanzar la excepción
            logger.error(
                f"Validación fallida en AlquilerEquipo: {dias} días"
            )
            raise ParametroFaltanteError(
                "Los días de alquiler deben ser un número mayor a 0."
            )

        # Verificamos que el tipo de equipo esté disponible en las tarifas
        if self.__tipo_equipo not in self.__tarifas:
            raise ServicioNoDisponibleError(
                f"El equipo '{self.__tipo_equipo}' no está disponible. "
                f"Opciones: {', '.join(self.__tarifas.keys())}"
            )

    def calcular_costo(self, **kwargs):
        """Calcula el costo del alquiler de equipo.
        Método sobrecargado: acepta días, impuesto y descuento opcionales."""
        # Obtenemos los parámetros con valores por defecto
        dias = kwargs.get('dias', kwargs.get('horas', 1))  # Acepta 'dias' o 'horas'
        impuesto = kwargs.get('impuesto', 0.0)
        descuento = kwargs.get('descuento', 0.0)

        # Obtenemos la tarifa diaria según el tipo de equipo
        tarifa_diaria = self.__tarifas.get(self.__tipo_equipo, 0)
        # Calculamos el costo base
        costo_base = tarifa_diaria * dias
        # Aplicamos descuento e impuesto
        costo_final = costo_base * (1 - descuento) * (1 + impuesto)

        # Registramos en el log
        logger.info(
            f"Costo calculado para alquiler '{self.__tipo_equipo}': "
            f"${costo_final:,.0f} ({dias} días)"
        )
        return costo_final

    def describir(self):
        """Sobrescribe el método describir para incluir tipo y tarifa."""
        tarifa = self.__tarifas.get(self.__tipo_equipo, "N/A")
        return (f"Alquiler de {self.__tipo_equipo} '{self.nombre}' | "
                f"Tarifa/día: ${tarifa:,}")
