from flask import request, jsonify, session, redirect, url_for, render_template
import sys
import os

# Agregar la ruta del directorio padre al path para poder importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modelo.login import autenticar_usuario, verificar_acceso

# Función para manejar el inicio de sesión
def login():
    if request.method == 'GET':
        # Si ya hay una sesión activa, redirigir al dashboard
        if 'usuario_id' in session:
            return redirect(url_for('dashboard'))
        
        # Mostrar la página de login
        return render_template('Login/login.html')
    
    elif request.method == 'POST':
        # Obtener datos del formulario
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        # Validar que se proporcionaron los datos necesarios
        if not username or not password:
            return jsonify({"error": "Usuario y contraseña son requeridos"}), 400
        
        # Autenticar al usuario
        resultado, usuario = autenticar_usuario(username, password)
        
        if usuario:
            # Guardar información del usuario en la sesión
            session['usuario_id'] = usuario['id']
            session['username'] = usuario['username']
            session['nombre'] = usuario['nombre']
            session['apellido'] = usuario['apellido']
            
            return jsonify({"mensaje": "Autenticación exitosa", "usuario": usuario['username']}), 200
        else:
            return jsonify({"error": resultado.get('error', 'Error de autenticación')}), 401

# Función para cerrar sesión
def logout():
    # Eliminar datos de la sesión
    session.pop('usuario_id', None)
    session.pop('username', None)
    session.pop('nombre', None)
    session.pop('apellido', None)
    
    return redirect(url_for('login'))

# Función para verificar si el usuario está autenticado
def requiere_autenticacion(f):
    def decorated_function(*args, **kwargs):
        if 'usuario_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Función para verificar si el usuario tiene acceso a un módulo específico
def requiere_acceso(modulo):
    def decorator(f):
        def decorated_function(*args, **kwargs):
            if 'usuario_id' not in session:
                return redirect(url_for('login'))
            
            if not verificar_acceso(session['usuario_id'], modulo):
                return jsonify({"error": "No tiene permisos para acceder a este módulo"}), 403
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# Función para mostrar el dashboard después del login
def dashboard():
    # Verificar si el usuario está autenticado
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
    
    # Mostrar el dashboard
    return render_template('dashboard.html', 
                          usuario=session.get('nombre', '') + ' ' + session.get('apellido', ''))