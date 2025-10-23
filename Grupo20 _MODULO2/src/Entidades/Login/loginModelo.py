import mysql.connector
import hashlib
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

# Función para autenticar un usuario
def autenticar_usuario(username, password):
    connection = get_db_connection()
    if not connection:
        return {"error": "Error de conexión a la base de datos"}, None
    
    try:
        cursor = connection.cursor(dictionary=True)
                
        # Encriptar la contraseña para comparar
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        # Buscar el usuario en la base de datos
        cursor.execute("""
            SELECT id, username, nombre, apellido, email
            FROM usuarios
            WHERE username = %s AND password = %s AND activo = TRUE
        """, (username, hashed_password))
        
        usuario = cursor.fetchone()
        
        if usuario:
            # Actualizar último acceso
            cursor.execute("""
                UPDATE usuarios
                SET ultimo_acceso = %s
                WHERE id = %s
            """, (datetime.now(), usuario['id']))
            
            connection.commit()
            return {"mensaje": "Autenticación exitosa"}, usuario
        else:
            return {"error": "Usuario o contraseña incorrectos"}, None
        
    except mysql.connector.Error as error:
        return {"error": f"Error al autenticar usuario: {error}"}, None
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Función para registrar un nuevo usuario
def registrar_usuario(username, password, nombre, apellido, email):
    connection = get_db_connection()
    if not connection:
        return {"error": "Error de conexión a la base de datos"}
    
    try:
        cursor = connection.cursor()
        
        # Verificar si el usuario ya existe
        cursor.execute("SELECT * FROM usuarios WHERE username = %s", (username,))
        if cursor.fetchone():
            return {"error": "El nombre de usuario ya está en uso"}
        
        # Encriptar la contraseña
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        # Registrar el nuevo usuario
        cursor.execute("""
            INSERT INTO usuarios (username, password, nombre, apellido, email, fecha_registro)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (username, hashed_password, nombre, apellido, email, datetime.now()))
        
        connection.commit()
        return {"mensaje": "Usuario registrado exitosamente"}
        
    except mysql.connector.Error as error:
        connection.rollback()
        return {"error": f"Error al registrar usuario: {error}"}
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Función para verificar si un usuario tiene acceso a un módulo específico
def verificar_acceso(num_documento, modulo):
    # En este caso, todos los usuarios autenticados tienen acceso a todos los módulos
    # Se podría implementar una lógica más compleja con roles y permisos si fuera necesario
    if num_documento:
        return True
    return False

# Función para cambiar la contraseña de un usuario
def cambiar_password(num_documento, password_actual, password_nueva):
    connection = get_db_connection()
    if not connection:
        return {"error": "Error de conexión a la base de datos"}
    
    try:
        cursor = connection.cursor()
        
        # Encriptar las contraseñas
        hashed_password_actual = hashlib.sha256(password_actual.encode()).hexdigest()
        hashed_password_nueva = hashlib.sha256(password_nueva.encode()).hexdigest()
        
        # Verificar la contraseña actual
        cursor.execute("""
            SELECT * FROM usuarios
            WHERE id = %s AND password = %s
        """, (num_documento, hashed_password_actual))
        
        if not cursor.fetchone():
            return {"error": "La contraseña actual es incorrecta"}
        
        # Actualizar la contraseña
        cursor.execute("""
            UPDATE usuarios
            SET password = %s
            WHERE id = %s
        """, (hashed_password_nueva, num_documento))
        
        connection.commit()
        return {"mensaje": "Contraseña actualizada exitosamente"}
        
    except mysql.connector.Error as error:
        connection.rollback()
        return {"error": f"Error al cambiar la contraseña: {error}"}
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

