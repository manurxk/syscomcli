from flask import Blueprint, request, jsonify
from app.conexion.Conexion import connection
from datetime import datetime

avisos_api = Blueprint('avisos_api', __name__)

# Crear aviso recordatorio
@avisos_api.route('/api/v1/avisos_recordatorios', methods=['POST'])
def crear_aviso_recordatorio():
    data = request.get_json()

    id_cita = data.get('id_cita')
    medio_envio = data.get('medio_envio')
    estado_envio = data.get('estado_envio', 'pendiente')
    fecha_programada = data.get('fecha_programada')
    observacion = data.get('observacion', '')

    if not id_cita or not medio_envio or not fecha_programada:
        return jsonify({'error': 'Faltan datos obligatorios'}), 400

    try:
        conn = connection()
        cur = conn.cursor()

        sql = """
            INSERT INTO avisos_recordatorios (id_cita, medio_envio, estado_envio, fecha_programada, observacion)
            VALUES (%s, %s, %s, %s, %s)
        """
        cur.execute(sql, (id_cita, medio_envio, estado_envio, fecha_programada, observacion))
        conn.commit()

        return jsonify({'success': True, 'message': 'Aviso creado exitosamente'})
    except Exception as e:
        print("Error al crear aviso:", e)
        return jsonify({'error': 'Error al crear el aviso'}), 500
    finally:
        cur.close()
        conn.close()

# Editar aviso recordatorio por id
@avisos_api.route('/api/v1/avisos_recordatorios/<int:id_aviso>', methods=['PUT'])
def editar_aviso_recordatorio(id_aviso):
    data = request.get_json()

    medio_envio = data.get('medio_envio')
    estado_envio = data.get('estado_envio')
    fecha_programada = data.get('fecha_programada')
    observacion = data.get('observacion')

    try:
        conn = connection()
        cur = conn.cursor()

        # Validar si existe el aviso
        cur.execute("SELECT id FROM avisos_recordatorios WHERE id = %s", (id_aviso,))
        if not cur.fetchone():
            return jsonify({'error': 'Aviso no encontrado'}), 404

        # Construir query dinámico para actualizar solo campos enviados
        campos = []
        valores = []

        if medio_envio:
            campos.append("medio_envio = %s")
            valores.append(medio_envio)
        if estado_envio:
            campos.append("estado_envio = %s")
            valores.append(estado_envio)
        if fecha_programada:
            campos.append("fecha_programada = %s")
            valores.append(fecha_programada)
        if observacion is not None:
            campos.append("observacion = %s")
            valores.append(observacion)

        if not campos:
            return jsonify({'error': 'No se enviaron campos para actualizar'}), 400

        sql = f"UPDATE avisos_recordatorios SET {', '.join(campos)} WHERE id = %s"
        valores.append(id_aviso)
        cur.execute(sql, valores)
        conn.commit()

        return jsonify({'success': True, 'message': 'Aviso actualizado correctamente'})
    except Exception as e:
        print("Error al editar aviso:", e)
        return jsonify({'error': 'Error al actualizar el aviso'}), 500
    finally:
        cur.close()
        conn.close()

# Eliminar aviso recordatorio por id
@avisos_api.route('/api/v1/avisos_recordatorios/<int:id_aviso>', methods=['DELETE'])
def eliminar_aviso_recordatorio(id_aviso):
    try:
        conn = connection()
        cur = conn.cursor()

        cur.execute("SELECT id FROM avisos_recordatorios WHERE id = %s", (id_aviso,))
        if not cur.fetchone():
            return jsonify({'error': 'Aviso no encontrado'}), 404

        cur.execute("DELETE FROM avisos_recordatorios WHERE id = %s", (id_aviso,))
        conn.commit()

        return jsonify({'success': True, 'message': 'Aviso eliminado correctamente'})
    except Exception as e:
        print("Error al eliminar aviso:", e)
        return jsonify({'error': 'Error al eliminar el aviso'}), 500
    finally:
        cur.close()
        conn.close()
