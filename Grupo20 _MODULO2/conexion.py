import mysql.connector
import os
from datetime import timedelta
from flask import Flask

# Configuración de la base de datos
def obtener_conexion():
    return mysql.connector.connect(
        host="localhost",
        port="3306",
        user="root",
        password="",
        database="festividades"
    )

# Configuración de Flask
programa = Flask(__name__)
programa.config['CARPETAU'] = os.path.join('uploads')
programa.secret_key = "LaMasSegura"
programa.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=30)
