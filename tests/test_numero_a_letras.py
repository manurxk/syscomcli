from decimal import Decimal
import sys
import os

# Añadir el path del proyecto para importar FacturaDao
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.dao.modulos.ventas.factura.FacturaDao import numero_a_letras

def test_numero_a_letras_basico():
    assert numero_a_letras(950000) == "Novecientos cincuenta mil Guaraníes"
    assert numero_a_letras(1) == "Un Guaraní"
    assert numero_a_letras(2) == "Dos Guaraníes"
    assert numero_a_letras(100) == "Cien Guaraníes"
    assert numero_a_letras(101) == "Ciento un Guaraníes"
    assert numero_a_letras(21) == "Veintiún Guaraníes"
    assert numero_a_letras(31) == "Treinta y un Guaraníes"

def test_numero_a_letras_millones():
    assert numero_a_letras(1000000) == "Un millón Guaraníes"
    assert numero_a_letras(2000000) == "Dos millones Guaraníes"
    assert numero_a_letras(1500300) == "Un millón quinientos mil trescientos Guaraníes"

def test_numero_a_letras_cero():
    assert numero_a_letras(0) == "Cero Guaraníes"

def test_numero_a_letras_decimal():
    assert numero_a_letras(Decimal('950000.4')) == "Novecientos cincuenta mil Guaraníes"
    assert numero_a_letras(Decimal('950000.6')) == "Novecientos cincuenta mil un Guaraníes"

if __name__ == "__main__":
    # Test manual simple
    print(f"950,000 -> {numero_a_letras(950000)}")
    print(f"1,500,300 -> {numero_a_letras(1500300)}")
    print(f"1 -> {numero_a_letras(1)}")
    print(f"21 -> {numero_a_letras(21)}")
    print(f"0 -> {numero_a_letras(0)}")
