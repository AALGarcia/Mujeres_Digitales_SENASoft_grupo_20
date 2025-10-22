import mysql.connector
from flask import Flask


app = Flask(__name__)
app.secret_key = '12345679'


def obtener_conexion():
    return mysql.connector.connect(
        host="localhost",
        port="3306",
        user="root",
        password="",
        database="hotel_principal"
    )