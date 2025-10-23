import mysql.connector
from conexion import obtener_conexion  # Importa la función para obtener la conexión

class crearEventos:
    def consultar(self):
        """Consulta todos los eventos activos"""
        try:
            conexion = obtener_conexion()  # Obtener una nueva conexión
            mi_cursor = conexion.cursor()  # Crear un cursor a partir de la conexión

            sql = "SELECT * FROM eventos WHERE borrado=0 OR borrado IS NULL"
            mi_cursor.execute(sql)
            resultado = mi_cursor.fetchall()

            # Cerrar el cursor y la conexión
            mi_cursor.close()
            conexion.close()

            return resultado
        except Exception as e:
            print(f"Error al consultar eventos: {e}")
            return []
    
    def buscar(self, id):
        """Busca un evento por su ID"""
        try:
            conexion = obtener_conexion()  # Obtener una nueva conexión
            mi_cursor = conexion.cursor()  # Crear un cursor a partir de la conexión

            sql = f"SELECT * FROM eventos WHERE id='{id}'"
            mi_cursor.execute(sql)
            resultado = mi_cursor.fetchall()

            # Cerrar el cursor y la conexión
            mi_cursor.close()
            conexion.close()

            return resultado
        except Exception as e:
            print(f"Error al buscar evento: {e}")
            return []

    def agregar(self, nombre, descripcion, fecha_evento, hora_inicio, hora_fin):
        """Agrega un nuevo evento"""
        try:
            conexion = obtener_conexion()  # Obtener una nueva conexión
            mi_cursor = conexion.cursor()  # Crear un cursor a partir de la conexión

            # Generar código automático (formato: EVT-XXXX)
            sql = "SELECT MAX(CAST(SUBSTRING(codigo, 5) AS UNSIGNED)) as max_codigo FROM eventos"
            mi_cursor.execute(sql)
            result = mi_cursor.fetchone()
            
            next_num = 1
            if result and result[0]:
                next_num = result[0] + 1
            
            codigo = f"EVT-{next_num:04d}"
            
            # Insertar nuevo evento
            sql = """INSERT INTO eventos 
                    (codigo, nombre, descripcion, fecha_evento, hora_inicio, hora_fin) 
                    VALUES (%s, %s, %s, %s, %s, %s)"""
            valores = (codigo, nombre, descripcion, fecha_evento, hora_inicio, hora_fin)
            
            mi_cursor.execute(sql, valores)
            conexion.commit()

            # Cerrar el cursor y la conexión
            mi_cursor.close()
            conexion.close()

            return {"success": True, "codigo": codigo, "id": mi_cursor.lastrowid}
        except Exception as e:
            print(f"Error al agregar evento: {e}")
            return {"success": False, "error": str(e)}

    def actualizar(self, id, nombre, descripcion, fecha_evento, hora_inicio, hora_fin):
        """Actualiza un evento existente"""
        try:
            conexion = obtener_conexion()  # Obtener una nueva conexión
            mi_cursor = conexion.cursor()  # Crear un cursor a partir de la conexión

            sql = """UPDATE eventos 
                    SET nombre=%s, descripcion=%s, fecha_evento=%s, 
                    hora_inicio=%s, hora_fin=%s 
                    WHERE id=%s"""
            valores = (nombre, descripcion, fecha_evento, hora_inicio, hora_fin, id)
            
            mi_cursor.execute(sql, valores)
            conexion.commit()

            # Cerrar el cursor y la conexión
            mi_cursor.close()
            conexion.close()

            return {"success": True, "filas_afectadas": mi_cursor.rowcount}
        except Exception as e:
            print(f"Error al actualizar evento: {e}")
            return {"success": False, "error": str(e)}
    
    def borrar(self, id):
        """Marca un evento como borrado (borrado lógico)"""
        try:
            conexion = obtener_conexion()  # Obtener una nueva conexión
            mi_cursor = conexion.cursor()  # Crear un cursor a partir de la conexión

            sql = "UPDATE eventos SET borrado=1 WHERE id=%s"
            mi_cursor.execute(sql, (id,))
            conexion.commit()

            # Cerrar el cursor y la conexión
            mi_cursor.close()
            conexion.close()

            return {"success": True, "filas_afectadas": mi_cursor.rowcount}
        except Exception as e:
            print(f"Error al borrar evento: {e}")
            return {"success": False, "error": str(e)}
    
    def eliminar(self, id):
        """Elimina un evento de la base de datos (borrado físico)"""
        try:
            conexion = obtener_conexion()  # Obtener una nueva conexión
            mi_cursor = conexion.cursor()  # Crear un cursor a partir de la conexión

            sql = "DELETE FROM eventos WHERE id=%s"
            mi_cursor.execute(sql, (id,))
            conexion.commit()

            # Cerrar el cursor y la conexión
            mi_cursor.close()
            conexion.close()

            return {"success": True, "filas_afectadas": mi_cursor.rowcount}
        except Exception as e:
            print(f"Error al eliminar evento: {e}")
            return {"success": False, "error": str(e)}
