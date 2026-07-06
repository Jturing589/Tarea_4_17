# servicios/asesoria.py
# Servicio especializado de asesoría técnica por niveles
# Implementa polimorfismo y manejo de excepciones avanzado

from servicios.servicio_base import Servicio  # Importamos la clase padre Servicio
from excepciones.excepciones import ParametroFaltanteError, ServicioNoDisponibleError  # Excepciones
from utils.logger import logger  # Importamos el logger para registrar eventos


class AsesoriaEspecializada(Servicio):
    """Servicio de asesoría técnica especializada por niveles de Software FJ.
    Implementa polimorfismo y manejo de excepciones avanzado."""

    def __init__(self, id_entidad, nombre, area):
        # Llamamos al constructor padre con id y nombre
        super().__init__(id=id_entidad, nombre=nombre)
        # Área de especialización de la asesoría (atributo privado)
        self.__area = area
        # Tarifas por hora según el nivel del asesor
        self.__tarifas_por_nivel = {"Junior": 80000, "Senior": 150000, "Expert": 250000}

    def validar_parametros(self, **kwargs):
        """Valida que el nivel exista y las horas sean positivas."""
        # Obtenemos el nivel del diccionario de parámetros
        nivel = kwargs.get("nivel")
        horas = kwargs.get("horas", 1)

        # Si se proporciona nivel, verificamos que sea válido
        if nivel is not None and nivel not in self.__tarifas_por_nivel:
            # Registramos advertencia en el log
            logger.warning(f"Intento de uso de nivel inválido: {nivel}")
            raise ParametroFaltanteError(
                f"Nivel '{nivel}' no es válido. "
                f"Opciones: {', '.join(self.__tarifas_por_nivel.keys())}"
            )

        # Verificamos que las horas sean un número positivo
        if not isinstance(horas, (int, float)) or horas <= 0:
            raise ParametroFaltanteError("Las horas de asesoría deben ser mayores a 0.")

    def calcular_costo(self, **kwargs):
        """Calcula el costo de la asesoría especializada.
        Método sobrecargado: acepta horas, nivel, impuesto y descuento opcionales."""
        # Obtenemos los parámetros con valores por defecto
        horas = kwargs.get('horas', 1)
        nivel = kwargs.get('nivel', 'Junior')  # Nivel por defecto: Junior
        impuesto = kwargs.get('impuesto', 0.0)
        descuento = kwargs.get('descuento', 0.0)

        # Obtenemos la tarifa según el nivel
        tarifa_hora = self.__tarifas_por_nivel.get(nivel, 80000)
        # Calculamos el costo base
        costo_base = tarifa_hora * horas
        # Aplicamos descuento e impuesto
        costo_final = costo_base * (1 - descuento) * (1 + impuesto)

        # Registramos en el log
        logger.info(
            f"Costo calculado para asesoría '{self.__area}' nivel {nivel}: "
            f"${costo_final:,.0f} ({horas}h)"
        )
        return costo_final

    def describir(self):
        """Sobrescribe el método describir para incluir área y niveles disponibles."""
        niveles = ", ".join(self.__tarifas_por_nivel.keys())
        return (f"Asesoría en '{self.__area}' - '{self.nombre}' | "
                f"Niveles: {niveles}")
