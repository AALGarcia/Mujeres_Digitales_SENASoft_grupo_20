from flask import Flask, request, jsonify
import mysql.connector
import sys
import os

# Agregar la ruta del proyecto al path para importar módulos
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

# Importar la conexión a la base de datos
from conexion import obtener_conexion

# Crear una instancia de la aplicación Flask
app = Flask(__name__)

# Configurar CORS para permitir solicitudes desde cualquier origen
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

# Función para obtener todos los eventos
def get_eventos():
    conn = obtener_conexion()
    cursor = conn.cursor(dictionary=True)
    
    try:
        sql = "SELECT * FROM eventos ORDER BY fecha_evento DESC"
        cursor.execute(sql)
        eventos = cursor.fetchall()
        
        return jsonify(eventos)
    except mysql.connector.Error as e:
        return jsonify({'error': f'Error al obtener eventos: {str(e)}'}), 500
    finally:
        cursor.close()
        conn.close()

# Función para obtener un evento específico
def get_evento(id):
    conn = obtener_conexion()
    cursor = conn.cursor(dictionary=True)
    
    try:
        sql = "SELECT * FROM eventos WHERE id = %s"
        cursor.execute(sql, (id,))
        evento = cursor.fetchone()
        
        if evento:
            return jsonify(evento)
        else:
            return jsonify({'error': 'Evento no encontrado'}), 404
    except mysql.connector.Error as e:
        return jsonify({'error': f'Error al obtener el evento: {str(e)}'}), 500
    finally:
        cursor.close()
        conn.close()

# Función para crear un nuevo evento
def crear_evento():
    conn = obtener_conexion()
    cursor = conn.cursor(dictionary=True)
    
    # Obtener datos del cuerpo de la solicitud
    data = request.get_json()
    
    # Validar datos requeridos
    if not all(key in data for key in ['nombre', 'descripcion', 'fecha_evento', 'hora_inicio', 'hora_fin']):
        return jsonify({'error': 'Faltan datos requeridos'}), 400
    
    try:
        # Generar código automático (formato: EVT-XXXX)
        sql = "SELECT MAX(CAST(SUBSTRING(codigo, 5) AS UNSIGNED)) as max_codigo FROM eventos"
        cursor.execute(sql)
        result = cursor.fetchone()
        
        next_num = 1
        if result and result['max_codigo']:
            next_num = result['max_codigo'] + 1
        
        codigo = f'EVT-{next_num:04d}'
        
        # Insertar nuevo evento
        sql = """INSERT INTO eventos (codigo, nombre, descripcion, fecha_evento, hora_inicio, hora_fin) 
                VALUES (%s, %s, %s, %s, %s, %s)"""
        
        cursor.execute(sql, (
            codigo,
            data['nombre'],
            data['descripcion'],
            data['fecha_evento'],
            data['hora_inicio'],
            data['hora_fin']
        ))
        
        conn.commit()
        id = cursor.lastrowid
        
        return jsonify({
            'id': id,
            'codigo': codigo,
            'mensaje': 'Evento creado exitosamente'
        }), 201
    except mysql.connector.Error as e:
        conn.rollback()
        return jsonify({'error': f'Error al crear el evento: {str(e)}'}), 500
    finally:
        cursor.close()
        conn.close()

# Función para actualizar un evento existente
def actualizar_evento():
    conn = obtener_conexion()
    cursor = conn.cursor()
    
    # Obtener datos del cuerpo de la solicitud
    data = request.get_json()
    
    # Validar datos requeridos
    if not all(key in data for key in ['id', 'nombre', 'descripcion', 'fecha_evento', 'hora_inicio', 'hora_fin']):
        return jsonify({'error': 'Faltan datos requeridos'}), 400
    
    try:
        sql = """UPDATE eventos 
                SET nombre = %s, 
                    descripcion = %s, 
                    fecha_evento = %s, 
                    hora_inicio = %s, 
                    hora_fin = %s 
                WHERE id = %s"""
        
        cursor.execute(sql, (
            data['nombre'],
            data['descripcion'],
            data['fecha_evento'],
            data['hora_inicio'],
            data['hora_fin'],
            data['id']
        ))
        
        conn.commit()
        
        if cursor.rowcount > 0:
            return jsonify({'mensaje': 'Evento actualizado exitosamente'})
        else:
            return jsonify({'error': 'Evento no encontrado o sin cambios'}), 404
    except mysql.connector.Error as e:
        conn.rollback()
        return jsonify({'error': f'Error al actualizar el evento: {str(e)}'}), 500
    finally:
        cursor.close()
        conn.close()

# Función para eliminar un evento
def eliminar_evento(id):
    conn = obtener_conexion()
    cursor = conn.cursor()
    
    try:
        sql = "DELETE FROM eventos WHERE id = %s"
        cursor.execute(sql, (id,))
        
        conn.commit()
        
        if cursor.rowcount > 0:
            return jsonify({'mensaje': 'Evento eliminado exitosamente'})
        else:
            return jsonify({'error': 'Evento no encontrado'}), 404
    except mysql.connector.Error as e:
        conn.rollback()
        return jsonify({'error': f'Error al eliminar el evento: {str(e)}'}), 500
    finally:
        cursor.close()
        conn.close()

# Rutas para la API
@app.route('/api/eventos', methods=['GET'])
def api_get_eventos():
    return get_eventos()

@app.route('/api/eventos/<int:id>', methods=['GET'])
def api_get_evento(id):
    return get_evento(id)

@app.route('/api/eventos', methods=['POST'])
def api_crear_evento():
    return crear_evento()

@app.route('/api/eventos', methods=['PUT'])
def api_actualizar_evento():
    return actualizar_evento()

@app.route('/api/eventos/<int:id>', methods=['DELETE'])
def api_eliminar_evento(id):
    return eliminar_evento(id)

# Si este archivo se ejecuta directamente
if __name__ == '__main__':
    app.run(debug=True, port=5001)