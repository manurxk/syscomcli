"""
Utilidades para validación de políticas de contraseñas
FASE 2: MEJORAS DE SEGURIDAD
"""
import re
from typing import Tuple, Dict, Optional

# Lista de contraseñas comunes (puedes expandir esta lista)
PASSWORDS_COMUNES = [
    'password', '123456', '12345678', 'qwerty', 'abc123', 'monkey',
    '1234567', 'letmein', 'trustno1', 'dragon', 'baseball', 'iloveyou',
    'master', 'sunshine', 'ashley', 'bailey', 'passw0rd', 'shadow',
    '123123', '654321', 'superman', 'qazwsx', 'michael', 'football',
    'welcome', 'jesus', 'ninja', 'mustang', 'password1', '1234567890',
    'admin', 'administrator', 'root', 'toor', '1234', '12345'
]


def validar_politica_password(
    password: str, 
    usuario_data: Optional[Dict] = None,
    username: Optional[str] = None
) -> Tuple[bool, str]:
    """
    Valida una contraseña según las políticas de seguridad.
    
    Políticas:
    - Mínimo 8 caracteres
    - Al menos 1 mayúscula
    - Al menos 1 minúscula
    - Al menos 1 número
    - Al menos 1 carácter especial (!@#$%^&*)
    - No puede ser igual a username
    - No puede contener nombre o apellido del usuario
    - No puede estar en lista de passwords comunes
    
    Args:
        password: Contraseña a validar
        usuario_data: Diccionario con datos del usuario (nombre, apellido, etc.)
        username: Nombre de usuario (opcional, se puede extraer de usuario_data)
    
    Returns:
        Tuple[bool, str]: (True/False, mensaje_error)
    """
    if not password:
        return False, "La contraseña no puede estar vacía"
    
    # 1. Mínimo 8 caracteres
    if len(password) < 8:
        return False, "La contraseña debe tener al menos 8 caracteres"
    
    # 2. Al menos 1 mayúscula
    if not re.search(r'[A-Z]', password):
        return False, "La contraseña debe contener al menos una letra mayúscula"
    
    # 3. Al menos 1 minúscula
    if not re.search(r'[a-z]', password):
        return False, "La contraseña debe contener al menos una letra minúscula"
    
    # 4. Al menos 1 número
    if not re.search(r'\d', password):
        return False, "La contraseña debe contener al menos un número"
    
    # 5. Al menos 1 carácter especial
    if not re.search(r'[!@#$%^&*]', password):
        return False, "La contraseña debe contener al menos un carácter especial (!@#$%^&*)"
    
    # 6. No puede ser igual a username
    if usuario_data and 'usu_nick' in usuario_data:
        username_check = usuario_data['usu_nick']
    elif username:
        username_check = username
    else:
        username_check = None
    
    if username_check and password.lower() == username_check.lower():
        return False, "La contraseña no puede ser igual al nombre de usuario"
    
    # 7. No puede contener nombre o apellido del usuario
    if usuario_data:
        nombre = usuario_data.get('nombre_persona', '')
        if nombre:
            # Dividir nombre completo en partes
            partes_nombre = nombre.lower().split()
            for parte in partes_nombre:
                if len(parte) >= 3 and parte in password.lower():
                    return False, f"La contraseña no puede contener parte de tu nombre ({parte})"
    
    # 8. No puede estar en lista de passwords comunes
    if password.lower() in [p.lower() for p in PASSWORDS_COMUNES]:
        return False, "La contraseña es demasiado común. Por favor elige una más segura"
    
    # Todo OK
    return True, "Contraseña válida"


def verificar_password_en_historial(
    password_hash: str,
    historial_passwords: list
) -> bool:
    """
    Verifica si un hash de contraseña está en el historial.
    
    Args:
        password_hash: Hash de la contraseña a verificar
        historial_passwords: Lista de hashes del historial
    
    Returns:
        bool: True si está en historial, False si no
    """
    return password_hash in [h.get('password_hash') for h in historial_passwords if h.get('password_hash')]


