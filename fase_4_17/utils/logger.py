# utils/logger.py
# Configuración del sistema de logging para registrar eventos y errores
# Todos los eventos se guardan en el archivo eventos.log

import logging  # Importamos el módulo de logging de Python

# Configuramos el logger con formato de fecha, nivel y mensaje
logging.basicConfig(
    filename="eventos.log",  # Nombre del archivo donde se guardan los logs
    level=logging.DEBUG,  # Nivel mínimo de registro (DEBUG captura todo)
    format="%(asctime)s | %(levelname)s | %(message)s",  # Formato del mensaje
)

# Creamos una instancia del logger para usar en todo el sistema
logger = logging.getLogger("SoftwareFJ")
