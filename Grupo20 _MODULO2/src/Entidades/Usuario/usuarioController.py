import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from src.modelo.usuarioModelo import Usuario

# Crear el blueprint para usuarios
usuario_bp = Blueprint('usuario', __name__)

# Instancia del modelo Usuario
usuario_modelo = Usuario()

@usuario_bp.route('/usuario', methods=['GET'])
def mostrar_formulario_usuario():
    """
    Mostrar el formulario de registro de usuario
    """
    return render_template('Usuario/usuario.html')

@usuario_bp.route('/usuario/crear', methods=['POST'])
def crear_usuario():
    """
    Crear un nuevo usuario
    """
    try:
        # Obtener datos del formulario
        num_documento = request.form.get('num_documento')
        nombre = request.form.get('nombre')
        apellidos = request.form.get('apellidos')
        tipo_documento = request.form.get('tipo_documento')
        num_documento = request.form.get('num_documento')
        email = request.form.get('email')
        contraseña = request.form.get('contraseña')
        num_telefono = request.form.get('num_telefono')
        
        # Validar que todos los campos estén presentes
        if not all([num_documento, nombre, apellidos, tipo_documento, num_documento, email, contraseña, num_telefono]):
            return jsonify({"success": False, "message": "Todos los campos son obligatorios"}), 400
        
        # Crear el usuario
        resultado = usuario_modelo.crear_usuario(
            num_documento, nombre, apellidos, tipo_documento, 
            num_documento, email, contraseña, num_telefono
        )
        
        if resultado["success"]:
            return jsonify(resultado), 201
        else:
            return jsonify(resultado), 400
            
    except Exception as e:
        return jsonify({"success": False, "message": f"Error interno del servidor: {str(e)}"}), 500

@usuario_bp.route('/usuarios', methods=['GET'])
def obtener_usuarios():
    """
    Obtener todos los usuarios
    """
    try:
        resultado = usuario_modelo.obtener_todos_usuarios()
        
        if resultado["success"]:
            return jsonify(resultado), 200
        else:
            return jsonify(resultado), 400
            
    except Exception as e:
        return jsonify({"success": False, "message": f"Error interno del servidor: {str(e)}"}), 500

@usuario_bp.route('/usuario/<num_documento>', methods=['GET'])
def obtener_usuario(num_documento):
    """
    Obtener un usuario específico por ID
    """
    try:
        resultado = usuario_modelo.obtener_usuario_por_id(num_documento)
        
        if resultado["success"]:
            return jsonify(resultado), 200
        else:
            return jsonify(resultado), 404
            
    except Exception as e:
        return jsonify({"success": False, "message": f"Error interno del servidor: {str(e)}"}), 500

@usuario_bp.route('/usuario/<num_documento>', methods=['PUT'])
def actualizar_usuario(num_documento):
    """
    Actualizar un usuario existente
    """
    try:
        # Obtener datos del JSON
        data = request.get_json()
        
        if not data:
            return jsonify({"success": False, "message": "No se proporcionaron datos"}), 400
        
        nombre = data.get('nombre')
        apellidos = data.get('apellidos')
        tipo_documento = data.get('tipo_documento')
        num_documento = data.get('num_documento')
        email = data.get('email')
        num_telefono = data.get('num_telefono')
        
        # Validar que todos los campos estén presentes
        if not all([nombre, apellidos, tipo_documento, num_documento, email, num_telefono]):
            return jsonify({"success": False, "message": "Todos los campos son obligatorios"}), 400
        
        # Actualizar el usuario
        resultado = usuario_modelo.actualizar_usuario(
            num_documento, nombre, apellidos, tipo_documento, 
            num_documento, email, num_telefono
        )
        
        if resultado["success"]:
            return jsonify(resultado), 200
        else:
            return jsonify(resultado), 400
            
    except Exception as e:
        return jsonify({"success": False, "message": f"Error interno del servidor: {str(e)}"}), 500

@usuario_bp.route('/usuario/<num_documento>', methods=['DELETE'])
def eliminar_usuario(num_documento):
    """
    Eliminar un usuario
    """
    try:
        resultado = usuario_modelo.eliminar_usuario(num_documento)
        
        if resultado["success"]:
            return jsonify(resultado), 200
        else:
            return jsonify(resultado), 404
            
    except Exception as e:
        return jsonify({"success": False, "message": f"Error interno del servidor: {str(e)}"}), 500

@usuario_bp.route('/usuario/verificar', methods=['POST'])
def verificar_credenciales():
    """
    Verificar las credenciales de un usuario
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"success": False, "message": "No se proporcionaron datos"}), 400
        
        email = data.get('email')
        contraseña = data.get('contraseña')
        
        if not email or not contraseña:
            return jsonify({"success": False, "message": "Email y contraseña son obligatorios"}), 400
        
        resultado = usuario_modelo.verificar_credenciales(email, contraseña)
        
        if resultado["success"]:
            return jsonify(resultado), 200
        else:
            return jsonify(resultado), 401
            
    except Exception as e:
        return jsonify({"success": False, "message": f"Error interno del servidor: {str(e)}"}), 500

# Rutas adicionales para vistas HTML
@usuario_bp.route('/usuarios/lista', methods=['GET'])
def mostrar_lista_usuarios():
    """
    Mostrar la lista de usuarios en una vista HTML
    """
    try:
        resultado = usuario_modelo.obtener_todos_usuarios()
        
        if resultado["success"]:
            usuarios = resultado["data"]
            return render_template('Usuario/usuarioLista.html', usuarios=usuarios)
        else:
            flash(resultado["message"], 'error')
            return render_template('Usuario/usuarioLista.html', usuarios=[])
            
    except Exception as e:
        flash(f"Error interno del servidor: {str(e)}", 'error')
        return render_template('Usuario/usuarioLista.html', usuarios=[])

@usuario_bp.route('/usuario/editar/<num_documento>', methods=['GET'])
def mostrar_formulario_editar(num_documento):
    """
    Mostrar el formulario de edición de usuario
    """
    try:
        resultado = usuario_modelo.obtener_usuario_por_id(num_documento)
        
        if resultado["success"]:
            usuario = resultado["data"]
            return render_template('Usuario/usuarioEditar.html', usuario=usuario)
        else:
            flash(resultado["message"], 'error')
            return redirect(url_for('usuario.mostrar_lista_usuarios'))
            
    except Exception as e:
        flash(f"Error interno del servidor: {str(e)}", 'error')
        return redirect(url_for('usuario.mostrar_lista_usuarios'))