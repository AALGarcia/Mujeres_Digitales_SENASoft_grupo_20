from conexion import mi_db, mi_cursor
from datetime import datetime
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class artistasModelo:
    
    def consultar_eventos(self):
        sql = "SELECT * FROM eventos WHERE borrado=0"
        mi_cursor.execute(sql)
        return mi_cursor.fetchall()

    
    def buscar_evento(self, id_evento):
        sql = f"SELECT * FROM eventos WHERE id='{id_evento}' AND borrado=0"
        mi_cursor.execute(sql)
        return mi_cursor.fetchall()

    def registrar_artista(self, codigo, nombres, apellidos, genero_musica, ciudad_natal):
        sql = f"""
            INSERT INTO artistas (codigo, nombres, apellidos, genero_musica, ciudad_natal)
            VALUES ('{codigo}', '{nombres}', '{apellidos}', '{genero_musica}', '{ciudad_natal}')
        """
        mi_cursor.execute(sql)
        mi_db.commit()

   
    def registrar_evento(self, nombre, descripcion, fecha, hora_inicio, hora_fin):
        sql = f"""
            INSERT INTO eventos (nombre, descripcion, fecha_evento, hora_inicio, hora_fin, borrado)
            VALUES ('{nombre}', '{descripcion}', '{fecha}', '{hora_inicio}', '{hora_fin}', 0)
        """
        mi_cursor.execute(sql)
        mi_db.commit()

    
    def actualizar_evento(self, id_evento, nombre, descripcion, fecha, hora_inicio, hora_fin):
        sql = f"""
            UPDATE eventos 
            SET nombre='{nombre}', descripcion='{descripcion}', fecha_evento='{fecha}', 
                hora_inicio='{hora_inicio}', hora_fin='{hora_fin}'
            WHERE id='{id_evento}'
        """
        mi_cursor.execute(sql)
        mi_db.commit()


    def borrar_evento(self, id_evento):
        sql = f"UPDATE eventos SET borrado=1 WHERE id='{id_evento}'"
        mi_cursor.execute(sql)
        mi_db.commit()

    
    def enviar_mail(self, destinatario, asunto, cuerpo):
        remitente = "festividadesapp@outlook.com"
        password = "tu_clave_segura_aqui"

        mensaje = MIMEMultipart()
        mensaje['From'] = remitente
        mensaje['To'] = destinatario
        mensaje['Subject'] = asunto
        mensaje.attach(MIMEText(cuerpo, 'plain'))

        server = smtplib.SMTP('smtp.office365.com:587')
        server.starttls()
        server.login(remitente, password)
        server.sendmail(remitente, destinatario, mensaje.as_string())
        server.quit()
        print("Correo enviado exitosamente.")


mi_festividades = festividades()
