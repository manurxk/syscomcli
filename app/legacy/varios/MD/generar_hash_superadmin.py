#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para generar el hash de contraseña del Superadministrador
Ejecutar: python generar_hash_superadmin.py
"""

from werkzeug.security import generate_password_hash

def generar_hash_contraseña(contraseña):
    """
    Genera el hash de una contraseña usando pbkdf2:sha256
    (mismo método que usa el sistema)
    """
    hash_generado = generate_password_hash(contraseña, method='pbkdf2:sha256')
    return hash_generado

if __name__ == '__main__':
    print("=" * 60)
    print("GENERADOR DE HASH PARA SUPERADMINISTRADOR")
    print("=" * 60)
    print()
    
    # Solicitar contraseña
    contraseña = input("Ingresa la contraseña para el Superadministrador: ")
    
    if not contraseña:
        print("❌ Error: La contraseña no puede estar vacía")
        exit(1)
    
    if len(contraseña) < 6:
        print("⚠️  Advertencia: La contraseña debe tener al menos 6 caracteres")
        respuesta = input("¿Deseas continuar de todas formas? (s/n): ")
        if respuesta.lower() != 's':
            exit(1)
    
    # Generar hash
    hash_contraseña = generar_hash_contraseña(contraseña)
    
    print()
    print("=" * 60)
    print("HASH GENERADO EXITOSAMENTE")
    print("=" * 60)
    print()
    print("Copia este hash y reemplázalo en el archivo SQL:")
    print("crear_superadministrador_completo.sql")
    print()
    print("-" * 60)
    print(hash_contraseña)
    print("-" * 60)
    print()
    print("📋 El hash ya está copiado arriba, pégalo en el SQL donde dice:")
    print("   v_hash_password := '<HASH_CONTRASEÑA_AQUI>';")
    print()
    print("=" * 60)


