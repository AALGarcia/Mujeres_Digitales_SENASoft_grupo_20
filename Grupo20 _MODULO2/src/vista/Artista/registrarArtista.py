#El sistema debe contar con un módulo de artistas en el cual se registre un código, 
#nombres y apellidos, genero de música del artista y ciudad natal de artista.


import mysql.connector # type: ignore
from datetime import datetime


class Artistas:
    def consultar(self):
        """Consulta todos los artistas activos"""
        try:
            sql = "SELECT * FROM artistas WHERE borrado=0 OR borrado IS NULL"
            mi_cursor.execute(sql)
            resultado = mi_cursor.fetchall()
            return resultado
        except Exception as e:
            print(f"Error al consultar artistas: {e}")
            return []
    
    def buscar(self, id):
        """Busca un artista por su ID"""
        try:
            sql = f"SELECT * FROM artistas WHERE id='{id}'"         
            mi_cursor.execute(sql)
            resultado = mi_cursor.fetchall()
            return resultado
        except Exception as e:
            print(f"Error al buscar artista: {e}")
            return []

    def agregar(self, nombre, apellido, genero, ciudad):
        """Agrega un nuevo artista"""       
        try:
            # Generar código automático (formato: ART-XXXX)
            sql = "SELECT MAX(CAST(SUBSTRING(codigo, 5) AS UNSIGNED)) as max_codigo FROM artistas"
            mi_cursor.execute(sql)
            result = mi_cursor.fetchone()
            
            next_num = 1
            if result and result[0]:
                next_num = result[0] + 1
            
            codigo = f"ART-{next_num:04d}"
            
            # Insertar nuevo artista
            sql = """INSERT INTO artistas 
                    (codigo, nombre, apellido, genero, ciudad) 
                    VALUES (%s, %s, %s, %s, %s)"""
            valores = (codigo, nombre, apellido, genero, ciudad)
            
            mi_cursor.execute(sql, valores)
            mi_db.commit()
            
            return {"success": True, "codigo": codigo, "id": mi_cursor.lastrowid}
        except Exception as e:
            print(f"Error al agregar artista: {e}")
            return {"success": False, "error": str(e)}

    def actualizar(self, id, nombre, apellido, genero, ciudad):
        """Actualiza un artista existente"""
        try:
            sql = """UPDATE eventos 
                    SET nombre=%s, descripcion=%s, fecha_evento=%s, 
                    hora_inicio=%s, hora_fin=%s 
                    WHERE id=%s"""
            valores = (nombre, apellido, genero, ciudad, id)
            
            mi_cursor.execute(sql, valores)
            mi_db.commit()
            
            return {"success": True, "filas_afectadas": mi_cursor.rowcount}
        except Exception as e:
            print(f"Error al actualizar artista: {e}")
            return {"success": False, "error": str(e)}
    
    def borrar(self, id):
        """Marca un artista como borrado (borrado lógico)"""
        try:
            sql = "UPDATE artistas SET borrado=1 WHERE id=%s"
            mi_cursor.execute(sql, (id,))
            mi_db.commit()
            
            return {"success": True, "filas_afectadas": mi_cursor.rowcount}
        except Exception as e:
            print(f"Error al borrar artista: {e}")      
            return {"success": False, "error": str(e)}
    
    def eliminar(self, id):
        """Elimina un artista de la base de datos (borrado físico)"""
        try:
            sql = "DELETE FROM artistas WHERE id=%s"
            mi_cursor.execute(sql, (id,))
            mi_db.commit()
            
            return {"success": True, "filas_afectadas": mi_cursor.rowcount}
        except Exception as e:
            print(f"Error al eliminar artista: {e}")
            return {"success": False, "error": str(e)}

# Instancia global para usar en la aplicación
mi_artistas = Artistas()
