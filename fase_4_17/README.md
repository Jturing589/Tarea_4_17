# Programación - Fase 4 - Componente Práctico - Prácticas Simuladas

## Sistema Integral de Gestión de Clientes, Servicios y Reservas

### Descripción
Sistema orientado a objetos desarrollado en Python para la empresa **Software FJ**, que gestiona clientes, servicios y reservas sin uso de bases de datos. Toda la información se maneja mediante objetos, listas y archivos de logs.

### Estructura del Proyecto
```
├── main.py                    # Archivo principal con la demostración del sistema
├── entidades/
│   ├── __init__.py
│   ├── entidad_base.py        # Clase abstracta base (Entidad)
│   ├── cliente.py             # Clase Cliente con validaciones y encapsulación
│   └── reserva.py             # Clase Reserva con procesamiento y cancelación
├── servicios/
│   ├── __init__.py
│   ├── servicio_base.py       # Clase abstracta Servicio
│   ├── reserva_sala.py        # Servicio de reserva de salas
│   ├── alquiler_equipo.py     # Servicio de alquiler de equipos
│   └── asesoria.py            # Servicio de asesoría especializada
├── excepciones/
│   ├── __init__.py
│   └── excepciones.py         # Excepciones personalizadas del sistema
├── utils/
│   ├── __init__.py
│   └── logger.py              # Configuración del sistema de logging
└── README.md
```

### Conceptos Implementados
- **Abstracción**: Clase abstracta `Entidad` y `Servicio`
- **Herencia**: Todas las clases heredan de `Entidad`
- **Polimorfismo**: Métodos sobrescritos en cada servicio (`calcular_costo`, `describir`)
- **Encapsulación**: Atributos privados en `Cliente` con getters
- **Métodos sobrecargados**: `calcular_costo()` acepta parámetros opcionales (impuesto, descuento)
- **Excepciones personalizadas**: `SistemaFJError`, `ClienteInvalidoError`, `ReservaInvalidaError`, etc.
- **Bloques try/except/else/finally**: Manejo completo en procesamiento de reservas
- **Encadenamiento de excepciones**: Uso de `raise ... from e`
- **Archivo de logs**: Registro automático de eventos y errores

### Ejecución
```bash
python main.py
```

### Integrantes
- Grupo 454
