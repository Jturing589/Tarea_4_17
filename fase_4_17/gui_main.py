# gui_main.py
# Interfaz gráfica (Tkinter) con diseño Premium en Modo Oscuro y estructura modular
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
        self.ventana.title("Software FJ - Panel de Control de Reservas")
        self.ventana.geometry("780x560")
        self.ventana.configure(bg="#0f172a")  # Fondo oscuro (Slate 900)
        self.ventana.resizable(False, False)

        # Configuración de estilos para TTK
        self.style = ttk.Style()
        self.style.theme_use("clam")
        
        # Personalizar elementos TTK
        self.style.configure("TCombobox", 
            fieldbackground="#1e293b", 
            background="#334155", 
            foreground="white", 
            arrowcolor="white",
            darkcolor="#1e293b",
            lightcolor="#334155"
        )
        # Asegurar que el menú desplegable tenga fondo oscuro
        self.ventana.option_add("*TCombobox*Listbox.background", "#1e293b")
        self.ventana.option_add("*TCombobox*Listbox.foreground", "white")
        self.ventana.option_add("*TCombobox*Listbox.selectBackground", "#38bdf8")

        # 1. Cabecera (Header Dashboard)
        frame_header = tk.Frame(ventana, bg="#1e293b", height=70)
        frame_header.pack(fill="x", side="top")
        frame_header.pack_propagate(False)

        lbl_logo = tk.Label(
            frame_header, 
            text="SOFTWARE FJ", 
            font=("Helvetica", 14, "bold"), 
            bg="#1e293b", 
            fg="#38bdf8"  # Cyan accent
        )
        lbl_logo.pack(side="left", padx=25, pady=20)

        lbl_titulo = tk.Label(
            frame_header, 
            text="PANEL DE RESERVAS & CONTROL DE EXCEPCIONES", 
            font=("Helvetica", 11, "bold"), 
            bg="#1e293b", 
            fg="#94a3b8"
        )
        lbl_titulo.pack(side="right", padx=25, pady=20)

        # 2. Contenedor Principal (Dos Columnas usando Grid)
        frame_main = tk.Frame(ventana, bg="#0f172a", pady=20, padx=25)
        frame_main.pack(fill="both", expand=True)

        # Columna 1: Información del Cliente (Frame Oscuro Izquierdo)
        col_cliente = tk.LabelFrame(
            frame_main, 
            text=" DATOS DEL CLIENTE ", 
            font=("Helvetica", 10, "bold"), 
            bg="#1e293b", 
            fg="#38bdf8", 
            padx=15, 
            pady=15,
            bd=1,
            relief="solid"
        )
        col_cliente.grid(row=0, column=0, sticky="nsew", padx=(0, 15))

        # Columna 2: Detalles del Servicio (Frame Oscuro Derecho)
        col_servicio = tk.LabelFrame(
            frame_main, 
            text=" DETALLES DEL SERVICIO ", 
            font=("Helvetica", 10, "bold"), 
            bg="#1e293b", 
            fg="#38bdf8", 
            padx=15, 
            pady=15,
            bd=1,
            relief="solid"
        )
        col_servicio.grid(row=0, column=1, sticky="nsew")

        # Configurar anchos proporcionales de columnas del grid principal
        frame_main.columnconfigure(0, weight=1)
        frame_main.columnconfigure(1, weight=1)
        frame_main.rowconfigure(0, weight=1)

        # --- Llenado Columna 1 (Cliente) ---
        lbl_style = {"bg": "#1e293b", "fg": "#cbd5e1", "font": ("Helvetica", 9, "bold")}
        entry_style = {"bg": "#0f172a", "fg": "white", "insertbackground": "white", 
                       "font": ("Helvetica", 10), "bd": 1, "relief": "solid", "highlightthickness": 0}

        tk.Label(col_cliente, text="Nombre Completo:", **lbl_style).pack(anchor="w", pady=(0, 3))
        self.entrada_nombre = tk.Entry(col_cliente, **entry_style)
        self.entrada_nombre.pack(fill="x", pady=(0, 12), ipady=4)

        tk.Label(col_cliente, text="Documento / ID:", **lbl_style).pack(anchor="w", pady=(0, 3))
        self.entrada_id = tk.Entry(col_cliente, **entry_style)
        self.entrada_id.pack(fill="x", pady=(0, 12), ipady=4)

        tk.Label(col_cliente, text="Correo Electrónico:", **lbl_style).pack(anchor="w", pady=(0, 3))
        self.entrada_email = tk.Entry(col_cliente, **entry_style)
        self.entrada_email.insert(0, "ejemplo@softwarefj.com")
        self.entrada_email.pack(fill="x", pady=(0, 12), ipady=4)

        tk.Label(col_cliente, text="Teléfono de Contacto:", **lbl_style).pack(anchor="w", pady=(0, 3))
        self.entrada_telefono = tk.Entry(col_cliente, **entry_style)
        self.entrada_telefono.insert(0, "3001234567")
        self.entrada_telefono.pack(fill="x", ipady=4)

        # --- Llenado Columna 2 (Servicio) ---
        tk.Label(col_servicio, text="Seleccione el Servicio:", **lbl_style).pack(anchor="w", pady=(0, 3))
        self.combo_servicio = ttk.Combobox(
            col_servicio, 
            values=["Reserva de Sala", "Alquiler de Equipo", "Asesoría Especializada"], 
            state="readonly", 
            font=("Helvetica", 10)
        )
        self.combo_servicio.pack(fill="x", pady=(0, 15))
        self.combo_servicio.current(0)
        self.combo_servicio.bind("<<ComboboxSelected>>", self.actualizar_etiqueta_duracion)

        self.label_duracion = tk.Label(col_servicio, text="Duración (Horas):", **lbl_style)
        self.label_duracion.pack(anchor="w", pady=(0, 3))
        self.entrada_duracion = tk.Entry(col_servicio, **entry_style)
        self.entrada_duracion.insert(0, "3")
        self.entrada_duracion.pack(fill="x", pady=(0, 15), ipady=4)

        # Tarjeta Informativa en la parte inferior del servicio
        frame_info = tk.Frame(col_servicio, bg="#334155", bd=0)
        frame_info.pack(fill="both", expand=True, pady=(5, 0))
        
        self.lbl_info_text = tk.Label(
            frame_info,
            text="INFORMACIÓN DEL SERVICIO:\n\n* Salas: Cobro por Horas.\n* Equipos: Cobro por Días.\n* Asesorías: Por hora según Nivel.",
            font=("Helvetica", 8, "italic"),
            bg="#334155",
            fg="#e2e8f0",
            justify="left",
            anchor="w",
            padx=10,
            pady=10
        )
        self.lbl_info_text.pack(fill="both", expand=True)

        # 3. Barra de Botones Inferior (Side by Side)
        frame_buttons = tk.Frame(ventana, bg="#0f172a", pady=15, padx=25)
        frame_buttons.pack(fill="x", side="bottom")

        btn_procesar = tk.Button(
            frame_buttons, 
            text="✔ PROCESAR RESERVA", 
            command=self.procesar_desde_ui,
            bg="#10b981",  # Verde Esmeralda
            fg="white", 
            font=("Helvetica", 10, "bold"), 
            activebackground="#059669",
            activeforeground="white",
            relief="flat",
            bd=0,
            cursor="hand2",
            padx=20, 
            pady=8
        )
        btn_procesar.pack(side="left", fill="x", expand=True, padx=(0, 10))

        btn_simulacion = tk.Button(
            frame_buttons, 
            text="▶ EJECUTAR SIMULACIÓN (10 OPS)", 
            command=self.ejecutar_simulacion,
            bg="#6366f1",  # Indigo
            fg="white", 
            font=("Helvetica", 10, "bold"), 
            activebackground="#4f46e5",
            activeforeground="white",
            relief="flat",
            bd=0,
            cursor="hand2",
            padx=20, 
            pady=8
        )
        btn_simulacion.pack(side="right", fill="x", expand=True, padx=(10, 0))

    def actualizar_etiqueta_duracion(self, event=None):
        """Actualiza dinámicamente la etiqueta de duración y el texto informativo según el servicio."""
        tipo_serv = self.combo_servicio.get()
        if tipo_serv == "Alquiler de Equipo":
            self.label_duracion.config(text="Duración (Días):")
            self.lbl_info_text.config(
                text="INFORMACIÓN DEL SERVICIO:\n\n* Equipos: Cobro por Días.\n* Tarifa diaria base: $35,000 COP.\n* Aplican impuestos estándar."
            )
        elif tipo_serv == "Reserva de Sala":
            self.label_duracion.config(text="Duración (Horas):")
            self.lbl_info_text.config(
                text="INFORMACIÓN DEL SERVICIO:\n\n* Salas: Cobro por Horas.\n* Tarifa por hora base: $50,000 COP.\n* Capacidad de sala estándar: 10 pers."
            )
        else:
            self.label_duracion.config(text="Duración (Horas):")
            self.lbl_info_text.config(
                text="INFORMACIÓN DEL SERVICIO:\n\n* Asesorías: Cobro por Horas.\n* Nivel por defecto: Junior.\n* Soporta tarifas diferenciadas."
            )

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

            # Instanciamos el cliente (esto ejecutará las validaciones de la clase Cliente)
            cliente = Cliente(id_cliente=id_val, nombre=nombre, email=email, telefono=tel)
            
            # Obtenemos el servicio correspondiente
            servicio = self.obtener_servicio_instancia(tipo_serv)
            if not servicio:
                raise ServicioNoDisponibleError("Servicio no reconocido.")

            # Procesamos la reserva
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
                f"Duración: {duracion} {'días' if tipo_serv == 'Alquiler de Equipo' else 'horas'}\n"
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
        print("   SIMULACIÓN DE 10 OPERACIONES - ESTRUCTURA MODULAR (DARK)")
        print("="*70)

        for i, (nom, doc, mail, tel, serv_tipo, dur, valido) in enumerate(datos_prueba, 1):
            try:
                print(f"\nOperación {i:02d}: Cliente='{nom}' | Servicio='{serv_tipo}' | Duración={dur}")
                
                cliente = Cliente(id_cliente=doc, nombre=nom, email=mail, telefono=tel)
                servicio = self.obtener_servicio_instancia(serv_tipo)
                
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
