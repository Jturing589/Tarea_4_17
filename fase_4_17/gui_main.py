# gui_main.py
# Interfaz gráfica (Tkinter) integrada con la arquitectura modular del sistema
# Empresa: Software FJ

import tkinter as tk
from tkinter import messagebox, ttk
import logging
from entidades.cliente import Cliente
from entidades.reserva import Reserva
from servicios.reserva_sala import ReservaSala
from servicios.alquiler_equipo import AlquilerEquipo
from servicios.asesoria import AsesoriaEspecializada
from excepciones.excepciones import (
    SistemaFJError,
    ClienteInvalidoError,
    ServicioNoDisponibleError,
    ReservaInvalidaError,
    ParametroFaltanteError,
    OperacionNoPermitidaError,
)
from utils.logger import logger

class InterfazApp:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Software FJ - Gestión Modular de Reservas")
        self.ventana.geometry("520x680")
        self.ventana.configure(bg="#f5f6f8")

        # Configuración de estilos
        self.style = ttk.Style()
        self.style.theme_use("clam")
        
        # Título Principal
        titulo = tk.Label(
            ventana, 
            text="SISTEMA FJ - FASE 4 (MODULAR)", 
            font=("Helvetica", 16, "bold"), 
            bg="#f5f6f8", 
            fg="#2c3e50"
        )
        titulo.pack(pady=15)

        # Contenedor del Formulario
        self.frame_form = tk.LabelFrame(
            ventana, 
            text=" Registrar Nueva Reserva ", 
            font=("Helvetica", 10, "bold"), 
            bg="#f5f6f8", 
            fg="#34495e", 
            padx=15, 
            pady=15
        )
        self.frame_form.pack(pady=10, padx=20, fill="both", expand=True)

        self.crear_formulario()

        # Botón para Procesar Reserva
        btn_procesar = tk.Button(
            ventana, 
            text="✔ PROCESAR RESERVA", 
            command=self.procesar_desde_ui,
            bg="#2ecc71", 
            fg="white", 
            font=("Helvetica", 11, "bold"), 
            activebackground="#27ae60",
            activeforeground="white",
            relief="flat",
            padx=15, 
            pady=8
        )
        btn_procesar.pack(pady=10)

        # Botón para Simulación
        btn_simulacion = tk.Button(
            ventana, 
            text="▶ EJECUTAR SIMULACIÓN (10 OPERACIONES)", 
            command=self.ejecutar_simulacion,
            bg="#3498db", 
            fg="white", 
            font=("Helvetica", 10, "bold"), 
            activebackground="#2980b9",
            activeforeground="white",
            relief="flat",
            padx=15, 
            pady=8
        )
        btn_simulacion.pack(pady=15)

        # Pie de página
        footer = tk.Label(
            ventana, 
            text="Desarrollado según la Guía de Actividades - Programación UNAD", 
            font=("Helvetica", 8, "italic"), 
            bg="#f5f6f8", 
            fg="#7f8c8d"
        )
        footer.pack(pady=5)

    def crear_formulario(self):
        # Nombre
        tk.Label(self.frame_form, text="Nombre del Cliente:", bg="#f5f6f8", fg="#2c3e50", font=("Helvetica", 9, "bold")).pack(anchor="w", pady=2)
        self.entrada_nombre = tk.Entry(self.frame_form, font=("Helvetica", 10), width=40)
        self.entrada_nombre.pack(pady=2, fill="x")

        # ID Cliente
        tk.Label(self.frame_form, text="Identificación (ID):", bg="#f5f6f8", fg="#2c3e50", font=("Helvetica", 9, "bold")).pack(anchor="w", pady=2)
        self.entrada_id = tk.Entry(self.frame_form, font=("Helvetica", 10), width=40)
        self.entrada_id.pack(pady=2, fill="x")

        # Email
        tk.Label(self.frame_form, text="Correo Electrónico:", bg="#f5f6f8", fg="#2c3e50", font=("Helvetica", 9, "bold")).pack(anchor="w", pady=2)
        self.entrada_email = tk.Entry(self.frame_form, font=("Helvetica", 10), width=40)
        self.entrada_email.insert(0, "ejemplo@softwarefj.com")
        self.entrada_email.pack(pady=2, fill="x")

        # Teléfono
        tk.Label(self.frame_form, text="Teléfono:", bg="#f5f6f8", fg="#2c3e50", font=("Helvetica", 9, "bold")).pack(anchor="w", pady=2)
        self.entrada_telefono = tk.Entry(self.frame_form, font=("Helvetica", 10), width=40)
        self.entrada_telefono.insert(0, "3001234567")
        self.entrada_telefono.pack(pady=2, fill="x")

        # Tipo de Servicio
        tk.Label(self.frame_form, text="Servicio Solicitado:", bg="#f5f6f8", fg="#2c3e50", font=("Helvetica", 9, "bold")).pack(anchor="w", pady=2)
        self.combo_servicio = ttk.Combobox(
            self.frame_form, 
            values=["Reserva de Sala", "Alquiler de Equipo", "Asesoría Especializada"], 
            state="readonly", 
            font=("Helvetica", 10)
        )
        self.combo_servicio.pack(pady=2, fill="x")
        self.combo_servicio.current(0)

        # Duración / Horas
        tk.Label(self.frame_form, text="Duración (Horas o Días):", bg="#f5f6f8", fg="#2c3e50", font=("Helvetica", 9, "bold")).pack(anchor="w", pady=2)
        self.entrada_duracion = tk.Entry(self.frame_form, font=("Helvetica", 10), width=40)
        self.entrada_duracion.insert(0, "3")
        self.entrada_duracion.pack(pady=2, fill="x")

    def obtener_servicio_instancia(self, tipo_serv):
        if tipo_serv == "Reserva de Sala":
            return ReservaSala(101, "Sala Ejecutiva A", capacidad=10)
        elif tipo_serv == "Alquiler de Equipo":
            return AlquilerEquipo(102, "Laptop Corporativa", tipo_equipo="Laptop")
        elif tipo_serv == "Asesoría Especializada":
            return AsesoriaEspecializada(103, "Asesoría de Software", area="Desarrollo")
        return None

    def procesar_desde_ui(self):
        try:
            nombre = self.entrada_nombre.get().strip()
            id_val = self.entrada_id.get().strip()
            email = self.entrada_email.get().strip()
            tel = self.entrada_telefono.get().strip()
            tipo_serv = self.combo_servicio.get()
            duracion_str = self.entrada_duracion.get().strip()

            if not duracion_str:
                raise ParametroFaltanteError("Debe ingresar una duración.")

            try:
                duracion = float(duracion_str)
            except ValueError:
                raise ParametroFaltanteError("La duración debe ser un número válido.")

            # Instanciamos el cliente (esto ejecutará las validaciones internas de la clase Cliente)
            cliente = Cliente(id_cliente=id_val, nombre=nombre, email=email, telefono=tel)
            
            # Obtenemos la instancia del servicio
            servicio = self.obtener_servicio_instancia(tipo_serv)
            if not servicio:
                raise ServicioNoDisponibleError("Servicio no reconocido.")

            # Creamos y procesamos la reserva
            reserva = Reserva(id_reserva=201, nombre=f"Reserva de {nombre}", cliente=cliente, servicio=servicio, duracion=duracion)
            reserva.procesar()

            # Costo calculado final
            costo_final = servicio.calcular_costo(horas=duracion)

            messagebox.showinfo(
                "Reserva Confirmada", 
                f"✔ ¡Reserva procesada exitosamente!\n\n"
                f"Cliente: {cliente.nombre}\n"
                f"Servicio: {servicio.nombre}\n"
                f"Detalle: {servicio.describir()}\n"
                f"Duración: {duracion} horas/días\n"
                f"Costo Total: ${costo_final:,.0f} COP\n"
                f"Estado: {reserva.estado.capitalize()}"
            )
        except (ClienteInvalidoError, ReservaInvalidaError, ParametroFaltanteError, ServicioNoDisponibleError, SistemaFJError) as e:
            messagebox.showwarning("Error en Datos", f"✘ {e}")
            logger.warning(f"Intento fallido desde UI: {e}")
        except Exception as e:
            messagebox.showerror("Error Inesperado", f"✘ Ocurrió un error no controlado:\n{e}")
            logger.error(f"Error crítico en UI: {e}")

    def ejecutar_simulacion(self):
        """Ejecuta una simulación interactiva de 10 operaciones."""
        logger.info("Iniciando simulación de 10 operaciones desde interfaz gráfica.")
        
        datos_prueba = [
            # (Nombre, ID, Email, Teléfono, Servicio, Duración, ¿Es válido?)
            ("Juan Pérez", "1", "juan@gmail.com", "3101112233", "Reserva de Sala", 4, True),
            ("", "2", "ana@gmail.com", "3123334455", "Reserva de Sala", 3, False), # Nombre vacío
            ("María Gómez", "3", "maria-invalido", "3156667788", "Alquiler de Equipo", 2, False), # Email inválido
            ("Carlos Ruiz", "4", "carlos@gmail.com", "abc", "Asesoría Especializada", 5, False), # Teléfono inválido
            ("Lucía Díaz", "5", "lucia@gmail.com", "3004445566", "Asesoría Especializada", -1, False), # Duración negativa
            ("Pedro Páez", "6", "pedro@gmail.com", "3118889900", "Alquiler de Equipo", 5, True),
            ("Diana Silva", "7", "diana@gmail.com", "3195556677", "Reserva de Sala", 2, True),
            ("Andrés Soto", "8", "andres@gmail.com", "3201119999", "Asesoría Especializada", 3, True),
            ("Sofía Rincón", "9", "sofia@gmail.com", "3005552211", "Alquiler de Equipo", 1, True),
            ("Laura Vaca", "10", "laura@gmail.com", "3144445555", "Reserva de Sala", 8, True),
        ]

        exitos = 0
        fallas_controladas = 0

        print("\n" + "="*70)
        print("   SIMULACIÓN DE 10 OPERACIONES - ESTRUCTURA MODULAR")
        print("="*70)

        for i, (nom, doc, mail, tel, serv_tipo, dur, valido) in enumerate(datos_prueba, 1):
            try:
                print(f"\nOperación {i:02d}: Cliente='{nom}' | Servicio='{serv_tipo}' | Duración={dur}")
                
                # Intentamos registrar cliente
                cliente = Cliente(id_cliente=doc, nombre=nom, email=mail, telefono=tel)
                
                # Obtener servicio
                servicio = self.obtener_servicio_instancia(serv_tipo)
                
                # Crear y procesar reserva
                reserva = Reserva(id_reserva=500+i, nombre=f"Sim Reserva {i}", cliente=cliente, servicio=servicio, duracion=dur)
                reserva.procesar()
                
                costo = servicio.calcular_costo(horas=dur)
                print(f"   ✔ [ÉXITO] Costo total: ${costo:,.0f} | Estado: {reserva.estado}")
                exitos += 1
            except (ClienteInvalidoError, ReservaInvalidaError, ParametroFaltanteError, ServicioNoDisponibleError) as e:
                print(f"   ✘ [ERROR CONTROLADO] {e}")
                if e.__cause__:
                    print(f"      └─ Causa original: {e.__cause__}")
                fallas_controladas += 1
            except Exception as e:
                print(f"   ✘ [ERROR CRÍTICO] {e}")

        print("\n" + "="*70)
        print(f"   RESUMEN: {exitos} exitosas, {fallas_controladas} fallas controladas.")
        print("="*70 + "\n")

        messagebox.showinfo(
            "Simulación Finalizada",
            f"La simulación de 10 operaciones se ejecutó exitosamente.\n\n"
            f"✔ Operaciones exitosas: {exitos}\n"
            f"✘ Errores detectados y controlados: {fallas_controladas}\n\n"
            f"Los resultados detallados se han impreso en la consola y se registraron en 'eventos.log'."
        )

if __name__ == "__main__":
    root = tk.Tk()
    app = InterfazApp(root)
    root.mainloop()
