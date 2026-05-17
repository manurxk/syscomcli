#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script simple para actualizar contraseñas de usuarios
Ejecutar desde la raíz del proyecto: python actualizar_passwords.py
"""

import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from werkzeug.security import generate_password_hash
from app.conexion.Conexion import Conexion

def actualizar_contraseñas(force=False):
    """
    Actualiza las contraseñas de los usuarios de ejemplo
    Solo actualiza si la contraseña es inválida (placeholder) o si force=True
    
    Args:
        force: Si es True, fuerza la actualización incluso si la contraseña es válida
    """
    
    # Contraseñas por defecto
    usuarios_contraseñas = {
        'admin': 'admin123',
        'recep1': 'recep123',
        'psico1': 'psico123',
        'psico2': 'psico2123',
        'ventas1': 'ventas123'
    }
    
    # Usuarios que no deben tener expiración de contraseña (admin)
    usuarios_sin_expiracion = ['admin']
    
    conexion = Conexion()
    con = conexion.getConexion()
    cur = con.cursor()
    
    try:
        print("=" * 80)
        print("ACTUALIZANDO CONTRASEÑAS DE USUARIOS")
        print("=" * 80)
        if force:
            print("[MODO FORZADO] Se actualizaran todas las contrasenas")
        else:
            print("[MODO SEGURO] Solo se actualizaran contrasenas invalidas")
        print()
        
        for usuario, contraseña in usuarios_contraseñas.items():
            # Verificar si el usuario existe y qué contraseña tiene
            check_sql = "SELECT usu_clave FROM usuarios WHERE usu_nick = %s"
            cur.execute(check_sql, (usuario,))
            resultado = cur.fetchone()
            
            if not resultado:
                print(f"[ADVERTENCIA] Usuario '{usuario}' no encontrado")
                print()
                continue
            
            hash_actual = resultado[0]
            
            # Verificar si la contraseña es inválida (placeholder)
            # Aceptar tanto pbkdf2 como scrypt como válidos (ambos son de werkzeug)
            es_invalida = (
                hash_actual is None or 
                hash_actual == '' or
                'REEMPLAZAR_CON_HASH_REAL' in str(hash_actual) or
                (not hash_actual.startswith('pbkdf2:sha256:') and 
                 not hash_actual.startswith('scrypt:') and
                 not hash_actual.startswith('pbkdf2:'))
            )
            
            if not force and not es_invalida:
                print(f"[OMITIDO] Usuario '{usuario}' ya tiene una contrasena valida")
                print(f"          Si quieres actualizarla, ejecuta con force=True")
                print()
                continue
            
            # Generar nuevo hash usando pbkdf2:sha256 para mantener consistencia
            # Esto asegura que todos los hashes en la BD sean del mismo tipo
            hash_generado = generate_password_hash(contraseña, method='pbkdf2:sha256')
            
            # Actualizar contraseña y configurar campos de seguridad
            if usuario in usuarios_sin_expiracion:
                # Para admin: contraseña nunca expira
                sql = """
                    UPDATE usuarios 
                    SET usu_clave = %s,
                        fecha_cambio_password = NOW(),
                        requiere_cambio_password = FALSE,
                        password_nunca_expira = TRUE
                    WHERE usu_nick = %s
                """
            else:
                # Para otros usuarios: contraseña expira en 90 días
                sql = """
                    UPDATE usuarios 
                    SET usu_clave = %s,
                        fecha_cambio_password = NOW(),
                        requiere_cambio_password = FALSE,
                        password_nunca_expira = FALSE,
                        dias_validez_password = 90
                    WHERE usu_nick = %s
                """
            
            cur.execute(sql, (hash_generado, usuario))
            
            if cur.rowcount > 0:
                if es_invalida:
                    print(f"[OK] Usuario '{usuario}' actualizado (contrasena invalida detectada)")
                else:
                    print(f"[OK] Usuario '{usuario}' actualizado (modo forzado)")
                print(f"     Contrasena: {contraseña}")
                print(f"     Hash: {hash_generado[:50]}...")
            else:
                print(f"[ADVERTENCIA] Usuario '{usuario}' no encontrado")
            print()
        
        con.commit()
        print("=" * 80)
        print("[OK] ACTUALIZACION COMPLETADA")
        print("=" * 80)
        print()
        print("Ahora puedes iniciar sesión con:")
        print("  - admin / admin123")
        print("  - recep1 / recep123")
        print("  - psico1 / psico123")
        print("  - psico2 / psico2123")
        print("  - ventas1 / ventas123")
        
    except Exception as e:
        con.rollback()
        print(f"[ERROR] Error al actualizar contrasenas: {str(e)}")
        import traceback
        traceback.print_exc()
        raise
    finally:
        cur.close()
        con.close()

if __name__ == "__main__":
    import sys
    # Si se pasa --force como argumento, fuerza la actualización
    force = '--force' in sys.argv
    actualizar_contraseñas(force=force)

