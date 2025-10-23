import mysql.connector
from datetime import datetime

# Configuración de la conexión a la base de datos
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="festividades"
        )
        return connection
    except mysql.connector.Error as error:
        print(f"Error al conectar a la base de datos: {error}")
        return None

# Función para verificar si hay conflicto de horarios para un artista
def verificar_conflicto_horario(id_artista, id_evento):
    connection = get_db_connection()
    if not connection:
        return {"error": "Error de conexión a la base de datos"}, False
    
    try:
        cursor = connection.cursor(dictionary=True)
        
        # Obtener información del evento que se quiere asociar
        cursor.execute("""
            SELECT fecha, hora_inicio, hora_fin 
            FROM eventos 
            WHERE `id eventos` = %s
        """, (id_evento,))
        
        nuevo_evento = cursor.fetchone()
        if not nuevo_evento:
            return {"error": "El evento no existe"}, False
        
        # Obtener eventos asociados al artista
        cursor.execute("""
            SELECT e.fecha, e.hora_inicio, e.hora_fin, e.`id eventos`, e.nombre
            FROM eventos e
            JOIN artistas_eventos ae ON e.`id eventos` = ae.id_evento
            WHERE ae.id_artista = %s
        """, (id_artista,))
        
        eventos_artista = cursor.fetchall()
        
        # Verificar conflictos de horario
        for evento in eventos_artista:
            # Si es el mismo día
            if evento['fecha'] == nuevo_evento['fecha']:
                # Verificar si hay solapamiento de horarios
                if (nuevo_evento['hora_inicio'] < evento['hora_fin'] and 
                    nuevo_evento['hora_fin'] > evento['hora_inicio']):
                    return {
                        "error": f"Conflicto de horario con el evento '{evento['nombre']}' (ID: {evento['id eventos']})",
                        "evento_conflicto": evento
                    }, False
        
        return {"mensaje": "No hay conflictos de horario"}, True
        
    except mysql.connector.Error as error:
        return {"error": f"Error al verificar conflictos de horario: {error}"}, False
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Función para asociar un artista a un evento
def asociar_artista_evento(id_artista, id_evento):
    # Verificar si existe conflicto de horario
    resultado, sin_conflicto = verificar_conflicto_horario(id_artista, id_evento)
    
    if not sin_conflicto:
        return resultado
    
    connection = get_db_connection()
    if not connection:
        return {"error": "Error de conexión a la base de datos"}
    
    try:
        cursor = connection.cursor()
        
        # Verificar si el artista existe
        cursor.execute("SELECT * FROM artistas WHERE `id artistas` = %s", (id_artista,))
        if not cursor.fetchone():
            return {"error": "El artista no existe"}
        
        # Verificar si el evento existe
        cursor.execute("SELECT * FROM eventos WHERE `id eventos` = %s", (id_evento,))
        if not cursor.fetchone():
            return {"error": "El evento no existe"}
        
        # Verificar si ya existe la asociación
        cursor.execute("""
            SELECT * FROM artistas_eventos 
            WHERE id_artista = %s AND id_evento = %s
        """, (id_artista, id_evento))
        
        if cursor.fetchone():
            return {"error": "El artista ya está asociado a este evento"}
        
        # Crear la tabla artistas_eventos si no existe
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS artistas_eventos (
                id INT AUTO_INCREMENT PRIMARY KEY,
                id_artista VARCHAR(20) NOT NULL,
                id_evento VARCHAR(15) NOT NULL,
                fecha_asociacion DATETIME NOT NULL,
                FOREIGN KEY (id_artista) REFERENCES artistas(`id artistas`),
                FOREIGN KEY (id_evento) REFERENCES eventos(`id eventos`)
            )
        """)
        
        # Asociar el artista al evento
        cursor.execute("""
            INSERT INTO artistas_eventos (id_artista, id_evento, fecha_asociacion)
            VALUES (%s, %s, %s)
        """, (id_artista, id_evento, datetime.now()))
        
        connection.commit()
        return {"mensaje": "Artista asociado al evento exitosamente"}
        
    except mysql.connector.Error as error:
        connection.rollback()
        return {"error": f"Error al asociar artista al evento: {error}"}
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Función para obtener todos los eventos asociados a un artista
def obtener_eventos_artista(id_artista):
    connection = get_db_connection()
    if not connection:
        return {"error": "Error de conexión a la base de datos"}
    
    try:
        cursor = connection.cursor(dictionary=True)
        
        # Verificar si el artista existe
        cursor.execute("SELECT * FROM artistas WHERE `id artistas` = %s", (id_artista,))
        if not cursor.fetchone():
            return {"error": "El artista no existe"}
        
        # Obtener eventos asociados al artista
        cursor.execute("""
            SELECT e.`id eventos`, e.nombre, e.descripción, e.fecha, 
                e.hora_inicio, e.hora_fin, ae.fecha_asociacion
            FROM eventos e
            JOIN artistas_eventos ae ON e.`id eventos` = ae.id_evento
            WHERE ae.id_artista = %s
            ORDER BY e.fecha, e.hora_inicio
        """, (id_artista,))
        
        eventos = cursor.fetchall()
        return {"eventos": eventos}
        
    except mysql.connector.Error as error:
        return {"error": f"Error al obtener eventos del artista: {error}"}
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Función para eliminar la asociación de un artista a un evento
def eliminar_asociacion_artista_evento(id_artista, id_evento):
    connection = get_db_connection()
    if not connection:
        return {"error": "Error de conexión a la base de datos"}
    
    try:
        cursor = connection.cursor()
        
        # Verificar si existe la asociación
        cursor.execute("""
            SELECT * FROM artistas_eventos 
            WHERE id_artista = %s AND id_evento = %s
        """, (id_artista, id_evento))
        
        if not cursor.fetchone():
            return {"error": "El artista no está asociado a este evento"}
        
        # Eliminar la asociación
        cursor.execute("""
            DELETE FROM artistas_eventos 
            WHERE id_artista = %s AND id_evento = %s
        """, (id_artista, id_evento))
        
        connection.commit()
        return {"mensaje": "Asociación eliminada exitosamente"}
        
    except mysql.connector.Error as error:
        connection.rollback()
        return {"error": f"Error al eliminar la asociación: {error}"}
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
