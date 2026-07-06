# Programación - Fase 4 - Componente Práctico (Prácticas Simuladas)

## Sistema Integral de Gestión de Clientes, Servicios y Reservas - Software FJ

Este proyecto implementa una solución robusta orientada a objetos en Python para la gestión de clientes, reservas y servicios especializados (Reserva de Salas, Alquiler de Equipos y Asesoría Técnica) sin el uso de bases de datos.

### Características y Conceptos de POO Implementados
* **Abstracción y Herencia:** Uso de clases base y derivadas para estructurar entidades y servicios.
* **Polimorfismo:** Métodos sobreescritos para calcular costos específicos y describir servicios.
* **Encapsulación:** Atributos privados con métodos getters/setters para proteger datos sensibles de clientes.
* **Manejo de Excepciones:** Control de flujo mediante bloques `try-except-else-finally` y excepciones personalizadas.
* **Sistema de Logs:** Registro automático de eventos y errores en un archivo log local.

### Estructura del Proyecto
* `entidades/`: Contiene la lógica del Cliente y la Reserva.
* `servicios/`: Implementación de los 3 servicios especializados.
* `excepciones/`: Excepciones personalizadas del negocio.
* `utils/`: Módulo para la configuración del logger de eventos.
* `gui_main.py`: Punto de inicio del sistema con interfaz gráfica (Tkinter).
* `main.py`: Ejecución de simulación automática por consola.

### Cómo ejecutar el programa
Puedes arrancar la interfaz gráfica interactiva ejecutando: python gui_main.py
