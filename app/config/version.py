"""
Configuración de versión de la aplicación
Sistema de versionado semántico: MAJOR.MINOR.PATCH
"""
__version__ = "2.1.0"
__version_info__ = (2, 1, 0)

# Información adicional de la versión
VERSION_NAME = "AngaSys"
VERSION_FULL = f"{VERSION_NAME} v{__version__}"

# Fecha de lanzamiento de la versión actual
RELEASE_DATE = "2026-03-29"

def get_version():
    """Retorna la versión completa de la aplicación"""
    return __version__

def get_version_info():
    """Retorna la información de versión como tupla"""
    return __version_info__

def get_version_full():
    """Retorna el nombre completo con versión"""
    return VERSION_FULL





