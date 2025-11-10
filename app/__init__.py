import logging
from .core.config import settings

# Configuración básica de logging, nivel por entorno
logging.basicConfig(
    level=getattr(logging, settings.log_level.upper(), logging.INFO),
    format='%(asctime)s %(levelname)s %(name)s: %(message)s'
)

