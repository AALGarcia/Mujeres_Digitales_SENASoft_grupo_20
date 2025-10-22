from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import sys

# Agregar la ruta del modelo al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'modelo')))

# Importar la clase Eventos desde crearEvento.py
from crearEvento import mi_eventos

app = Flask(__name__, 
            static_folder=os.path.join(os.path.dirname(__file__), 'controlador'),
            template_folder=os.path.join(os.path.dirname(__file__), 'vista'))

# Ruta para servir archivos estáticos (JavaScript, CSS)
@app.route('/controlador/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.static_folder, filename)

# Ruta principal que muestra la página de eventos
@app.route('/')
def index():
    return render_template('Evento/crearEvento.html')

# API para gestionar eventos
@app.route('/api/eventos', methods=['GET', 'POST', 'PUT', 'DELETE'])
def api_eventos():
    # Obtener todos los eventos
    if request.method == 'GET':
        id = request.args.get('id')
        if id:
            # Buscar un evento específico por ID
            evento = mi_eventos.buscar(id)
            if evento and len(evento) > 0:
                # Convertir el resultado de la consulta a un diccionario
                evento_dict = {
                    'id': evento[0][0],
                    'codigo': evento[0][1],
                    'nombre': evento[0][2],
                    'descripcion': evento[0][3],
                    'fecha_evento': evento[0][4],
                    'hora_inicio': evento[0][5],
                    'hora_fin': evento[0][6]
                }
                return jsonify(evento_dict)
            else:
                return jsonify({'error': 'Evento no encontrado'}), 404
        else:
            # Obtener todos los eventos
            eventos = mi_eventos.consultar()
            eventos_list = []
            for evento in eventos:
                eventos_list.append({
                    'id': evento[0],
                    'codigo': evento[1],
                    'nombre': evento[2],
                    'descripcion': evento[3],
                    'fecha_evento': evento[4],
                    'hora_inicio': evento[5],
                    'hora_fin': evento[6]
                })
            return jsonify(eventos_list)
    
    # Crear un nuevo evento
    elif request.method == 'POST':
        data = request.json
        resultado = mi_eventos.agregar(
            data['nombre'],
            data['descripcion'],
            data['fecha_evento'],
            data['hora_inicio'],
            data['hora_fin']
        )
        return jsonify(resultado)
    
    # Actualizar un evento existente
    elif request.method == 'PUT':
        data = request.json
        resultado = mi_eventos.actualizar(
            data['id'],
            data['nombre'],
            data['descripcion'],
            data['fecha_evento'],
            data['hora_inicio'],
            data['hora_fin']
        )
        return jsonify(resultado)
    
    # Eliminar un evento
    elif request.method == 'DELETE':
        id = request.args.get('id')
        if not id:
            return jsonify({'error': 'Se requiere el ID del evento'}), 400
        
        resultado = mi_eventos.borrar(id)
        return jsonify(resultado)

if __name__ == '__main__':
    app.run(debug=True, port=5000)