#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para generar hashes de contraseñas para usuarios del sistema
Ejecutar: python generar_hashes_contraseñas.py
"""

from werkzeug.security import generate_password_hash

# Contraseñas por defecto
contraseñas = {
    'admin': 'admin123',
    'recep1': 'recep123',
    'psico1': 'psico123',
    'psico2': 'psico2123',
    'ventas1': 'ventas123'
}

print("=" * 80)
print("HASHES DE CONTRASEÑAS PARA USUARIOS DEL SISTEMA")
print("=" * 80)
print()

for usuario, contraseña in contraseñas.items():
    hash_generado = generate_password_hash(contraseña, method='pbkdf2:sha256')
    print(f"Usuario: {usuario}")
    print(f"Contraseña: {contraseña}")
    print(f"Hash: {hash_generado}")
    print()

print("=" * 80)
print("INSTRUCCIONES:")
print("1. Copia los hashes generados")
print("2. Reemplázalos en el archivo 12_CREAR_USUARIOS_EJEMPLO_UNIFICADO.sql")
print("3. Busca 'REEMPLAZAR_CON_HASH_REAL' y reemplázalo con el hash correspondiente")
print("4. O ejecuta este script y actualiza manualmente")
print("=" * 80)
print()
print("SQL LISTO PARA COPIAR:")
print("-" * 80)
for usuario, contraseña in contraseñas.items():
    hash_generado = generate_password_hash(contraseña, method='pbkdf2:sha256')
    print(f"-- {usuario}: {hash_generado}")
print("-" * 80)








