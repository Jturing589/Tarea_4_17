# main.py
# Archivo principal del Sistema Integral de Gestion de Clientes, Servicios y Reservas
# Empresa: Software FJ
# Este archivo demuestra el funcionamiento completo del sistema con al menos
# 10 operaciones incluyendo casos validos e invalidos

import sys  # Importamos sys para configurar la codificacion de salida
sys.stdout.reconfigure(encoding='utf-8')  # Configuramos UTF-8 para la consola

from entidades.cliente import Cliente  # Importamos la clase Cliente
from entidades.reserva import Reserva  # Importamos la clase Reserva
from servicios.reserva_sala import ReservaSala  # Servicio de reserva de salas
from servicios.alquiler_equipo import AlquilerEquipo  # Servicio de alquiler de equipos
from servicios.asesoria import AsesoriaEspecializada  # Servicio de asesoría
from excepciones.excepciones import (  # Importamos todas las excepciones personalizadas
    SistemaFJError,
    ClienteInvalidoError,
    ServicioNoDisponibleError,
    ReservaInvalidaError,
    ParametroFaltanteError,
    OperacionNoPermitidaError,
)

from utils.logger import logger  # Importamos el logger para registrar eventos


class SistemaFJ:
    """Clase principal que gestiona clientes, servicios y reservas del sistema."""

    def __init__(self):
        # Listas internas para almacenar las entidades del sistema
        self.clientes = []
        self.servicios = []
        self.reservas = []

    def registrar_cliente(self, cliente):
        """Registra un nuevo cliente en el sistema."""
        self.clientes.append(cliente)
        print(f"  [OK] Cliente registrado: {cliente.nombre}")
        logger.info(f"Cliente registrado: {cliente.nombre}")

    def agregar_servicio(self, servicio):
        """Agrega un nuevo servicio disponible en el sistema."""
        self.servicios.append(servicio)
        print(f"  [OK] Servicio disponible: {servicio.nombre}")
        logger.info(f"Servicio agregado: {servicio.nombre}")

    def crear_reserva(self, reserva):
        """Crea y procesa una nueva reserva en el sistema."""
        reserva.procesar()
        self.reservas.append(reserva)
        print(f"  [OK] Reserva confirmada para: {reserva.cliente.nombre}")
        logger.info(f"Reserva creada para {reserva.cliente.nombre}")


# ==========================================================================
#  DEMOSTRACION DEL SISTEMA - 12 OPERACIONES (validas e invalidas)
# ==========================================================================

if __name__ == "__main__":

    # Creamos la instancia principal del sistema
    sistema = SistemaFJ()

    print("=" * 65)
    print("   SISTEMA INTEGRAL DE GESTION - SOFTWARE FJ")
    print("=" * 65)

    # -- OPERACION 1: Registro valido de cliente --------------------------
    print("\n>> Operacion 1: Registro valido de cliente")
    try:
        cliente1 = Cliente(1, "Carlos Martínez", "carlos@email.com", "3101234567")
        sistema.registrar_cliente(cliente1)
    except ClienteInvalidoError as e:
        logger.error(f"Op 1 - Error al registrar cliente: {e}")
        print(f"  [ERROR] {e}")

    # -- OPERACION 2: Registro invalido de cliente (email malo) -----------
    print("\n>> Operacion 2: Registro invalido de cliente (email incorrecto)")
    try:
        cliente_malo = Cliente(2, "Ana López", "correo-invalido", "3209876543")
        sistema.registrar_cliente(cliente_malo)
    except ClienteInvalidoError as e:
        logger.error(f"Op 2 - Error al registrar cliente: {e}")
        print(f"  [ERROR] Capturado: {e}")

    # -- OPERACION 3: Registro invalido de cliente (nombre vacio) ---------
    print("\n>> Operacion 3: Registro invalido de cliente (nombre vacio)")
    try:
        cliente_vacio = Cliente(3, "   ", "test@email.com", "3001112233")
        sistema.registrar_cliente(cliente_vacio)
    except ClienteInvalidoError as e:
        logger.error(f"Op 3 - Error al registrar cliente: {e}")
        print(f"  [ERROR] Capturado: {e}")

    # -- OPERACION 4: Registro valido de segundo cliente ------------------
    print("\n>> Operacion 4: Registro valido de segundo cliente")
    try:
        cliente2 = Cliente(4, "María García", "maria@email.com", "3154567890")
        sistema.registrar_cliente(cliente2)
    except ClienteInvalidoError as e:
        logger.error(f"Op 4 - Error al registrar cliente: {e}")
        print(f"  [ERROR] {e}")

    # -- OPERACION 5: Creacion valida de servicio (Sala) ------------------
    print("\n>> Operacion 5: Creacion valida de servicio - Reserva de Sala")
    try:
        sala1 = ReservaSala(101, "Sala de Conferencias A", capacidad=20)
        sistema.agregar_servicio(sala1)
        print(f"  Descripción: {sala1.describir()}")
    except SistemaFJError as e:
        logger.error(f"Op 5 - Error al crear servicio: {e}")
        print(f"  [ERROR] {e}")

    # -- OPERACION 6: Creacion valida de servicio (Alquiler) --------------
    print("\n>> Operacion 6: Creacion valida de servicio - Alquiler de Equipo")
    try:
        alquiler1 = AlquilerEquipo(102, "Laptop HP ProBook", tipo_equipo="Laptop")
        sistema.agregar_servicio(alquiler1)
        print(f"  Descripción: {alquiler1.describir()}")
    except SistemaFJError as e:
        logger.error(f"Op 6 - Error al crear servicio: {e}")
        print(f"  [ERROR] {e}")

    # -- OPERACION 7: Creacion valida de servicio (Asesoria) --------------
    print("\n>> Operacion 7: Creacion valida de servicio - Asesoria Especializada")
    try:
        asesoria1 = AsesoriaEspecializada(103, "Consultoría en Python", area="Desarrollo")
        sistema.agregar_servicio(asesoria1)
        print(f"  Descripción: {asesoria1.describir()}")
    except SistemaFJError as e:
        logger.error(f"Op 7 - Error al crear servicio: {e}")
        print(f"  [ERROR] {e}")

    # -- OPERACION 8: Reserva exitosa (Sala) ------------------------------
    print("\n>> Operacion 8: Reserva exitosa de sala")
    try:
        reserva1 = Reserva(201, "Reserva Sala A", cliente1, sala1, duracion=3)
        sistema.crear_reserva(reserva1)
        print(f"  Detalle: {reserva1.describir()}")
    except (ReservaInvalidaError, SistemaFJError) as e:
        logger.error(f"Op 8 - Error en reserva: {e}")
        print(f"  [ERROR] {e}")

    # -- OPERACION 9: Reserva fallida (duracion negativa) -----------------
    print("\n>> Operacion 9: Reserva fallida (duracion negativa)")
    try:
        reserva_mala = Reserva(202, "Reserva Inválida", cliente1, sala1, duracion=-2)
        sistema.crear_reserva(reserva_mala)
    except ReservaInvalidaError as e:
        logger.error(f"Op 9 - Error en reserva: {e}")
        print(f"  [ERROR] Capturado: {e}")

    # -- OPERACION 10: Reserva exitosa (Alquiler de equipo) ---------------
    print("\n>> Operacion 10: Reserva exitosa de alquiler de equipo")
    try:
        reserva2 = Reserva(203, "Alquiler Laptop", cliente2, alquiler1, duracion=5)
        sistema.crear_reserva(reserva2)
        print(f"  Detalle: {reserva2.describir()}")
    except (ReservaInvalidaError, SistemaFJError) as e:
        logger.error(f"Op 10 - Error en reserva: {e}")
        print(f"  [ERROR] {e}")

    # -- OPERACION 11: Cancelar reserva confirmada ------------------------
    print("\n>> Operacion 11: Cancelar reserva confirmada")
    try:
        reserva1.cancelar()
        print(f"  [OK] Reserva cancelada: {reserva1.describir()}")
    except OperacionNoPermitidaError as e:
        logger.error(f"Op 11 - Error al cancelar: {e}")
        print(f"  [ERROR] {e}")

    # -- OPERACION 12: Intentar cancelar reserva ya cancelada -------------
    print("\n>> Operacion 12: Intentar cancelar reserva ya cancelada")
    try:
        reserva1.cancelar()
    except OperacionNoPermitidaError as e:
        logger.error(f"Op 12 - Error al cancelar: {e}")
        print(f"  [ERROR] Capturado: {e}")

    # ======================================================================
    #  RESUMEN FINAL
    # ======================================================================
    print("\n" + "=" * 65)
    print("   RESUMEN DEL SISTEMA")
    print("=" * 65)
    print("=" * 65)
    print(f"  Clientes registrados: {len(sistema.clientes)}")
    print(f"  Servicios disponibles: {len(sistema.servicios)}")
    print(f"  Reservas procesadas: {len(sistema.reservas)}")
    print("=" * 65)
    print("  Sistema finalizado correctamente. Revise 'eventos.log' para detalles.")
    print("=" * 65)
