class RecordatorioDao:

    @staticmethod
    def crear_aviso(conn, id_cita, medio_envio, estado_envio, fecha_programada, observacion):
        cur = conn.cursor()
        sql = """
            INSERT INTO avisos_recordatorios (id_cita, medio_envio, estado_envio, fecha_programada, observacion)
            VALUES (%s, %s, %s, %s, %s)
        """
        cur.execute(sql, (id_cita, medio_envio, estado_envio, fecha_programada, observacion))
        cur.close()

    @staticmethod
    def obtener_aviso(conn, id_aviso):
        cur = conn.cursor()
        cur.execute("SELECT * FROM avisos_recordatorios WHERE id = %s", (id_aviso,))
        aviso = cur.fetchone()
        cur.close()
        return aviso

    @staticmethod
    def actualizar_aviso(conn, id_aviso, campos, valores):
        cur = conn.cursor()
        sql = f"UPDATE avisos_recordatorios SET {', '.join(campos)} WHERE id = %s"
        valores.append(id_aviso)
        cur.execute(sql, valores)
        cur.close()

    @staticmethod
    def eliminar_aviso(conn, id_aviso):
        cur = conn.cursor()
        cur.execute("DELETE FROM avisos_recordatorios WHERE id = %s", (id_aviso,))
        cur.close()
