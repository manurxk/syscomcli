import sys
import os
import logging
from flask import Flask

# Ensure the root directory is in python path if ran from subfolder
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

app = Flask(__name__)
app.logger.setLevel(logging.INFO)

with app.app_context():
    from app.dao.modulos.ventas.libro_ventas.LibroVentasDao import LibroVentasDao
    from app.conexion.Conexion import Conexion

    def migrate():
        print("Starting migration inside safe standalone Flask app context...")
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            # Find facturas without libro_ventas entry
            cur.execute('''
                SELECT f.id_factura, f.fecha_factura, f.factura_total, f.factura_subtotal, f.factura_impuestos, f.id_paciente, f.factura_numero
                FROM facturas f
                LEFT JOIN libro_ventas lv ON lv.id_factura = f.id_factura
                WHERE lv.id_factura IS NULL AND f.est_factura IN (1, 2)
            ''')
            rows = cur.fetchall()
            if not rows:
                print('No missing entries to migrate.')
                return
            libro_dao = LibroVentasDao()
            for row in rows:
                id_factura, fecha_factura, total, subtotal, iva, id_paciente, numero = row
                try:
                    libro_dao.registrarEntradaLibroVentas(
                        libro_fecha=fecha_factura,
                        tipo_comprobante='FACTURA',
                        numero_comprobante=numero,
                        id_paciente=id_paciente,
                        monto_gravado=subtotal,
                        monto_exento=0,
                        monto_iva=iva,
                        monto_total=total,
                        id_factura=id_factura
                    )
                    print(f'Migrated factura {id_factura}')
                except Exception as e:
                    print(f'Error migrating factura {id_factura}: {e}', file=sys.stderr)
        except Exception as e:
            print('Error during migration query:', e, file=sys.stderr)
        finally:
            cur.close()
            con.close()

if __name__ == '__main__':
    migrate()
