#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para actualizar contraseñas de usuarios en la base de datos
Ejecutar desde Flask: python -c "from app.varios.SQL.actualizar_contraseñas_usuarios import actualizar_contraseñas; actualizar_contraseñas()"
O desde la consola de Flask: python
>>> from app.varios.SQL.actualizar_contraseñas_usuarios import actualizar_contraseñas
>>> actualizar_contraseñas()
"""

from werkzeug.security import generate_password_hash
from app.conexion.Conexion import Conexion

def actualizar_contraseñas():
    """Actualiza las contraseñas de los usuarios de ejemplo"""
    
    # Contraseñas por defecto
    usuarios_contraseñas = {
        'admin': 'admin123',
        'recep1': 'recep123',
        'psico1': 'psico123',
        'psico2': 'psico2123',
        'ventas1': 'ventas123'
    }
    
    conexion = Conexion()
    con = conexion.getConexion()
    cur = con.cursor()
    
    try:
        print("=" * 80)
        print("ACTUALIZANDO CONTRASEÑAS DE USUARIOS")
        print("=" * 80)
        print()
        
        for usuario, contraseña in usuarios_contraseñas.items():
            hash_generado = generate_password_hash(contraseña, method='pbkdf2:sha256')
            
            # Actualizar contraseña
            sql = """
                UPDATE usuarios 
                SET usu_clave = %s
                WHERE usu_nick = %s
            """
            
            cur.execute(sql, (hash_generado, usuario))
            
            if cur.rowcount > 0:
                print(f"✅ Usuario '{usuario}' actualizado correctamente")
                print(f"   Contraseña: {contraseña}")
                print(f"   Hash: {hash_generado[:50]}...")
            else:
                print(f"⚠️  Usuario '{usuario}' no encontrado")
            print()
        
        con.commit()
        print("=" * 80)
        print("✅ ACTUALIZACIÓN COMPLETADA")
        print("=" * 80)
        
    except Exception as e:
        con.rollback()
        print(f"❌ Error al actualizar contraseñas: {str(e)}")
        raise
    finally:
        cur.close()
        con.close()

if __name__ == "__main__":
    actualizar_contraseñas()









