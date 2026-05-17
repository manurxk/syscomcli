# Data access object - DAO para Items/Servicios de ventas
import re
from flask import current_app as app
from app.conexion.Conexion import Conexion


class ItemServicioDao:
    """
    Catálogo de productos/servicios facturables.
    Pensado para consultas psicológicas, estudios, materiales, etc.
    """

    def getItems(self):
        sql = """
        SELECT id_item,
               cod_item,
               des_item,
               id_tipo_item,
               unidad_medida,
               precio_referencial,
               id_tipo_impuesto,
               porcentaje_impuesto,
               est_item
        FROM items_servicios
        ORDER BY des_item ASC
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql)
            rows = cur.fetchall()
            return [
                {
                    "id": r[0],
                    "codigo": r[1] or "",
                    "descripcion": r[2],
                    "id_tipo_item": r[3],
                    "unidad_medida": r[4] or "SERVICIO",
                    "precio_referencial": r[5] or 0,
                    "id_tipo_impuesto": r[6],
                    "porcentaje_impuesto": float(r[7]) if r[7] is not None else 0,
                    "estado": r[8],
                }
                for r in rows
            ]
        except Exception as e:
            app.logger.error(f"Error al obtener items_servicios: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()

    def getItemById(self, id_item):
        sql = """
        SELECT id_item,
               cod_item,
               des_item,
               id_tipo_item,
               unidad_medida,
               precio_referencial,
               id_tipo_impuesto,
               porcentaje_impuesto,
               est_item
        FROM items_servicios
        WHERE id_item = %s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (id_item,))
            r = cur.fetchone()
            if not r:
                return None
            return {
                "id": r[0],
                "codigo": r[1] or "",
                "descripcion": r[2],
                "id_tipo_item": r[3],
                "unidad_medida": r[4] or "SERVICIO",
                "precio_referencial": r[5] or 0,
                "id_tipo_impuesto": r[6],
                "porcentaje_impuesto": float(r[7]) if r[7] is not None else 0,
                "estado": r[8],
            }
        except Exception as e:
            app.logger.error(f"Error al obtener item_servicio: {str(e)}")
            return None
        finally:
            cur.close()
            con.close()

    # ============================
    # VALIDACIONES
    # ============================

    def itemExiste(self, descripcion):
        sql = "SELECT 1 FROM items_servicios WHERE LOWER(des_item)=LOWER(%s)"
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (descripcion,))
            return cur.fetchone() is not None
        finally:
            cur.close()
            con.close()

    def validarDescripcion(self, descripcion):
        """Permite letras, números, acentos, espacios y algunos signos básicos."""
        patron = r"^[A-Za-zÁÉÍÓÚáéíóúÑñ0-9 .,/()-]+$"
        return bool(re.match(patron, descripcion))

    # ============================
    # CRUD
    # ============================

    def guardarItem(
        self,
        descripcion,
        codigo=None,
        id_tipo_item=None,
        unidad_medida="SERVICIO",
        precio_referencial=0,
        id_tipo_impuesto=None,
        porcentaje_impuesto=0,
        estado="A",
    ):
        if not descripcion or descripcion.strip() == "":
            return False
        if not self.validarDescripcion(descripcion):
            app.logger.warning("Descripción de item inválida")
            return False
        if self.itemExiste(descripcion):
            app.logger.warning("El item/servicio ya existe")
            return False
        if estado not in ["A", "I"]:
            return False

        sql = """
        INSERT INTO items_servicios(
            cod_item,
            des_item,
            id_tipo_item,
            unidad_medida,
            precio_referencial,
            id_tipo_impuesto,
            porcentaje_impuesto,
            est_item,
            usuario_creacion
        )
        VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id_item
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            usuario = app.config.get("USUARIO_ACTUAL", "SISTEMA")
            cur.execute(
                sql,
                (
                    codigo.upper() if codigo else None,
                    descripcion.upper(),
                    id_tipo_item,
                    unidad_medida.upper() if unidad_medida else "SERVICIO",
                    precio_referencial or 0,
                    id_tipo_impuesto,
                    porcentaje_impuesto or 0,
                    estado,
                    usuario,
                ),
            )
            id_item = cur.fetchone()[0]
            con.commit()
            return id_item
        except Exception as e:
            app.logger.error(f"Error al insertar item_servicio: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()

    def updateItem(
        self,
        id_item,
        descripcion,
        codigo=None,
        id_tipo_item=None,
        unidad_medida="SERVICIO",
        precio_referencial=0,
        id_tipo_impuesto=None,
        porcentaje_impuesto=0,
        estado="A",
    ):
        if not descripcion or descripcion.strip() == "":
            return False
        if not self.validarDescripcion(descripcion):
            return False
        if estado not in ["A", "I"]:
            return False

        sql = """
        UPDATE items_servicios
        SET cod_item=%s,
            des_item=%s,
            id_tipo_item=%s,
            unidad_medida=%s,
            precio_referencial=%s,
            id_tipo_impuesto=%s,
            porcentaje_impuesto=%s,
            est_item=%s,
            usuario_modificacion=%s,
            fecha_modificacion=CURRENT_TIMESTAMP
        WHERE id_item=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            usuario = app.config.get("USUARIO_ACTUAL", "SISTEMA")
            cur.execute(
                sql,
                (
                    codigo.upper() if codigo else None,
                    descripcion.upper(),
                    id_tipo_item,
                    unidad_medida.upper() if unidad_medida else "SERVICIO",
                    precio_referencial or 0,
                    id_tipo_impuesto,
                    porcentaje_impuesto or 0,
                    estado,
                    usuario,
                    id_item,
                ),
            )
            filas = cur.rowcount
            con.commit()
            return filas > 0
        except Exception as e:
            app.logger.error(f"Error al actualizar item_servicio: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()

    def deleteItem(self, id_item):
        sql = "DELETE FROM items_servicios WHERE id_item=%s"
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (id_item,))
            filas = cur.rowcount
            con.commit()
            return filas > 0
        except Exception as e:
            app.logger.error(f"Error al eliminar item_servicio: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()




