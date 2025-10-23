import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from src.modelo.conexion import obtener_conexion
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

class Usuario:
    def __init__(self):
        pass
    
    def crear_usuario(self, num_documento, nombre, apellidos, tipo_documento, email, contraseña, num_telefono):
        """
        Crear un nuevo usuario en la base de datos
        """
        conn = obtener_conexion()
        cursor = conn.cursor()
        
        try:
            # Encriptar la contraseña
            contraseña_hash = generate_password_hash(contraseña)
            
            sql = """INSERT INTO usuarios (num_documento, nombre, apellidos, `tipo documento`, `num_documento`, email, contraseña, `num_telefono`) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
            
            cursor.execute(sql, (num_documento, nombre, apellidos, tipo_documento, num_documento, email, contraseña_hash, num_telefono))
            conn.commit()
            
            return {"success": True, "message": "Usuario creado exitosamente"}
            
        except mysql.connector.Error as e:
            conn.rollback()
            return {"success": False, "message": f"Error al crear usuario: {str(e)}"}
        finally:
            cursor.close()
            conn.close()
    
    def obtener_todos_usuarios(self):
        """
        Obtener todos los usuarios de la base de datos
        """
        conn = obtener_conexion()
        cursor = conn.cursor(dictionary=True)
        
        try:
            sql = "SELECT num_documento, nombre, apellidos, `tipo documento`, `num_documento`, email, `num_telefono` FROM usuarios"
            cursor.execute(sql)
            usuarios = cursor.fetchall()
            
            return {"success": True, "data": usuarios}
            
        except mysql.connector.Error as e:
            return {"success": False, "message": f"Error al obtener usuarios: {str(e)}"}
        finally:
            cursor.close()
            conn.close()
    
    def obtener_usuario_por_id(self, num_documento):
        """
        Obtener un usuario específico por ID
        """
        conn = obtener_conexion()
        cursor = conn.cursor(dictionary=True)
        
        try:
            sql = "SELECT num_documento, nombre, apellidos, `tipo documento`, `num_documento`, email, `num_telefono` FROM usuarios WHERE num_documento = %s"
            cursor.execute(sql, (num_documento,))
            usuario = cursor.fetchone()
            
            if usuario:
                return {"success": True, "data": usuario}
            else:
                return {"success": False, "message": "Usuario no encontrado"}
                
        except mysql.connector.Error as e:
            return {"success": False, "message": f"Error al obtener usuario: {str(e)}"}
        finally:
            cursor.close()
            conn.close()
    
    def actualizar_usuario(self, num_documento, nombre, apellidos, tipo_documento, email, num_telefono):
        """
        Actualizar un usuario existente
        """
        conn = obtener_conexion()
        cursor = conn.cursor()
        
        try:
            sql = """UPDATE usuarios 
                SET nombre = %s, apellidos = %s, `tipo documento` = %s, `num_documento` = %s, email = %s, `num_telefono` = %s 
                WHERE num_documento = %s"""
            
            cursor.execute(sql, (nombre, apellidos, tipo_documento, num_documento, email, num_telefono, num_documento))
            conn.commit()
            
            if cursor.rowcount > 0:
                return {"success": True, "message": "Usuario actualizado exitosamente"}
            else:
                return {"success": False, "message": "Usuario no encontrado"}
                
        except mysql.connector.Error as e:
            conn.rollback()
            return {"success": False, "message": f"Error al actualizar usuario: {str(e)}"}
        finally:
            cursor.close()
            conn.close()
    
    def eliminar_usuario(self, num_documento):
        """
        Eliminar un usuario de la base de datos
        """
        conn = obtener_conexion()
        cursor = conn.cursor()
        
        try:
            sql = "DELETE FROM usuarios WHERE num_documento = %s"
            cursor.execute(sql, (num_documento,))
            conn.commit()
            
            if cursor.rowcount > 0:
                return {"success": True, "message": "Usuario eliminado exitosamente"}
            else:
                return {"success": False, "message": "Usuario no encontrado"}
                
        except mysql.connector.Error as e:
            conn.rollback()
            return {"success": False, "message": f"Error al eliminar usuario: {str(e)}"}
        finally:
            cursor.close()
            conn.close()
    
    def verificar_credenciales(self, email, contraseña):
        """
        Verificar las credenciales de un usuario para login
        """
        conn = obtener_conexion()
        cursor = conn.cursor(dictionary=True)
        
        try:
            sql = "SELECT num_documento, nombre, apellidos, email, contraseña FROM usuarios WHERE email = %s"
            cursor.execute(sql, (email,))
            usuario = cursor.fetchone()
            
            if usuario and check_password_hash(usuario['contraseña'], contraseña):
                return {"success": True, "data": {
                    "num_documento": usuario['num_documento'],
                    "nombre": usuario['nombre'],
                    "apellidos": usuario['apellidos'],
                    "email": usuario['email']
                }}
            else:
                return {"success": False, "message": "Credenciales inválidas"}
                
        except mysql.connector.Error as e:
            return {"success": False, "message": f"Error al verificar credenciales: {str(e)}"}
        finally:
            cursor.close()
            conn.close()
