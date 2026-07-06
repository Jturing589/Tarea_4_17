# excepciones/excepciones.py
# Módulo de excepciones personalizadas para el sistema de gestión Software FJ
# Se definen clases de error específicas para cada tipo de problema
# que puede ocurrir durante la ejecución del sistema


class SistemaFJError(Exception):
    """Excepción base del sistema. Todas las excepciones personalizadas heredan de esta."""

    pass


class ClienteInvalidoError(SistemaFJError):
    """Se lanza cuando los datos de un cliente son inválidos o incompletos."""

    pass


class ServicioNoDisponibleError(SistemaFJError):
    """Se lanza cuando un servicio no está disponible o no existe."""

    pass


class ReservaInvalidaError(SistemaFJError):
    """Se lanza cuando una reserva no cumple con las condiciones requeridas."""

    pass


class ParametroFaltanteError(SistemaFJError):
    """Se lanza cuando faltan parámetros obligatorios en una operación."""

    pass


class OperacionNoPermitidaError(SistemaFJError):
    """Se lanza cuando se intenta realizar una operación no permitida en el sistema."""

    pass
