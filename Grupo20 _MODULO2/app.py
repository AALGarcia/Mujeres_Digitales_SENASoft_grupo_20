from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
import sys

# Agregar la ruta src al path para importar los módulos
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Importar controladores
from src.controlador.login_controller import login_bp, requiere_autenticacion, requiere_acceso
from src.modelo.login import crear_tabla_usuarios

app = Flask(__name__, template_folder='src/vista', static_folder='src/static')
app.secret_key = 'clave_secreta_festividades'  # Clave para las sesiones

# Registrar blueprints
app.register_blueprint(login_bp)

# Rutas principales
@app.route('/')
def index():
    if 'usuario_id' in session:
        return redirect(url_for('index'))
    return redirect(url_for('login_bp.login'))

@app.route('/index')
@requiere_autenticacion
def index():
    return render_template('index.html', usuario=session.get('usuario_nombre', 'Usuario'))

# Gestión de Eventos
@app.route('/eventos')
@requiere_autenticacion
@requiere_acceso('eventos')
def eventos():
    return render_template('eventos.html')

# Módulo de Boletería
@app.route('/boleteria')
@requiere_autenticacion
@requiere_acceso('boleteria')
def boleteria():
    return render_template('boleteria.html')

# Gestión de Localidades
@app.route('/localidades')
@requiere_autenticacion
@requiere_acceso('localidades')
def localidades():
    return render_template('localidades.html')

# Módulo de Artistas
@app.route('/artistas')
@requiere_autenticacion
@requiere_acceso('artistas')
def artistas():
    return render_template('artistas.html')

# Asociación de Artistas a Eventos
@app.route('/asociar-artistas')
@requiere_autenticacion
@requiere_acceso('asociar_artistas')
def asociar_artistas():
    return render_template('asociar_artistas.html')

# Inicializar la base de datos
@app.before_first_request
def inicializar_bd():
    crear_tabla_usuarios()

@app.route('/usuario')
def usuario():
    return render_template('Usuario/usuario.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)