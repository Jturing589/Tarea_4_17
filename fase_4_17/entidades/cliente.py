# entidades/cliente.py
# Clase Cliente que hereda de Entidad
# Implementa encapsulación de datos personales y validaciones robustas

import re  # Importamos re para validar formatos con expresiones regulares
from entidades.entidad_base import Entidad  # Importamos la clase padre Entidad
from excepciones.excepciones import ClienteInvalidoError  # Importamos la excepción específica


class Cliente(Entidad):
    """Clase que representa un cliente del sistema Software FJ.
    Hereda de Entidad e implementa validaciones y encapsulación."""

    def __init__(self, id_cliente, nombre, email, telefono):
        # Llamamos al constructor de la clase padre pasando id y nombre
        super().__init__(id=id_cliente, nombre=nombre)

        # Validamos el nombre antes de almacenarlo
        self.nombre = self.validar_nombre(nombre)
        # Atributos privados (encapsulados con doble guion bajo)
        self.__email = self.validar_email(email)
        self.__telefono = self.validar_telefono(telefono)
        # Lista interna de reservas del cliente (privada)
        self.__reservas = []

    # ── Validaciones ──────────────────────────────────────────────────────────

    def validar_nombre(self, nombre):
        """Valida que el nombre no sea vacío ni contenga solo espacios."""
        if not nombre or nombre.strip() == "":
            raise ClienteInvalidoError("El nombre no puede estar vacío.")
        return nombre.strip()

    def validar_email(self, email):
        """Valida que el email tenga un formato válido usando expresión regular."""
        # Patrón básico de email: texto@dominio.extensión
        patron = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not email or not re.match(patron, email):
            raise ClienteInvalidoError(f"El email '{email}' no es válido.")
        return email.strip()

    def validar_telefono(self, telefono):
        """Valida que el teléfono contenga solo dígitos y tenga al menos 7 caracteres."""
        if not telefono or not telefono.strip().isdigit():
            raise ClienteInvalidoError("El teléfono debe contener solo números.")
        if len(telefono.strip()) < 7:
            raise ClienteInvalidoError("El teléfono debe tener al menos 7 dígitos.")
        return telefono.strip()

    # ── Propiedades (getters) para acceder a atributos privados ──────────────

    @property
    def email(self):
        """Getter para obtener el email del cliente."""
        return self.__email

    @property
    def telefono(self):
        """Getter para obtener el teléfono del cliente."""
        return self.__telefono

    @property
    def reservas(self):
        """Getter para obtener la lista de reservas del cliente."""
        return self.__reservas.copy()  # Devolvemos una copia para proteger la lista original

    # ── Métodos ──────────────────────────────────────────────────────────────

    def agregar_reserva(self, reserva):
        """Agrega una reserva a la lista interna del cliente."""
        self.__reservas.append(reserva)

    def describir(self):
        """Implementación del método abstracto de Entidad.
        Retorna una descripción completa del cliente."""
        return (f"Cliente: {self.nombre} | Email: {self.__email} | "
                f"Tel: {self.__telefono} | Reservas: {len(self.__reservas)}")

    def __str__(self):
        """Representación en texto del cliente."""
        return f"Cliente [{self.id}]: {self.nombre} - {self.__email}"
