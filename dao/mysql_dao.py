from config.mysql_config import get_mysql_connection
from config.mysqlhistorial_config import get_historial_mysql_connection
from business.models import Cita, Historial, Usuario

class MySQLCitasDAO:
    def __init__(self):
        self.conn = get_mysql_connection()

    def create_cita(self, cita: Cita):
        cursor = self.conn.cursor()
        query = "INSERT INTO citasmedicas (id_usuario_paciente, id_usuario_doctor, fecha, hora, motivo, estado) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (cita.id_usuario_paciente, cita.id_usuario_doctor, cita.fecha, cita.hora, cita.motivo, cita.estado))
        self.conn.commit()
        cursor.close()

    def get_all_citas(self):
        cursor = self.conn.cursor()
        query = "SELECT * FROM citasmedicas"
        cursor.execute(query)
        rows = cursor.fetchall()
        citas = [Cita(*row) for row in rows]
        cursor.close()
        return citas

    def update_cita(self, cita: Cita):
        cursor = self.conn.cursor()
        query = "UPDATE citasmedicas SET id_usuario_paciente = %s, id_usuario_doctor = %s, fecha = %s, hora = %s, motivo = %s, estado = %s WHERE id_cita = %s"
        cursor.execute(query, (cita.id_usuario_paciente, cita.id_usuario_doctor, cita.fecha, cita.hora, cita.motivo, cita.estado, cita.id_cita))
        self.conn.commit()
        cursor.close()

    def delete_cita(self, id_cita: int):
        cursor = self.conn.cursor()
        query = "DELETE FROM citasmedicas WHERE id_cita = %s"
        cursor.execute(query, (id_cita,))
        self.conn.commit()
        cursor.close()

class MySQLHistorialesDAO:
    def __init__(self):
        self.conn = get_historial_mysql_connection()

    def create_historial(self, historial: Historial):
        cursor = self.conn.cursor()
        query = "INSERT INTO historialesmedicos (id_usuario_paciente, descripcion, fecha_creacion, notas, diagnostico, tratamiento) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (historial.id_usuario_paciente, historial.descripcion, historial.fecha_creacion, historial.notas, historial.diagnostico, historial.tratamiento))
        self.conn.commit()
        cursor.close()

    def get_all_historiales(self):
        cursor = self.conn.cursor()
        query = "SELECT * FROM historialesmedicos"
        cursor.execute(query)
        rows = cursor.fetchall()
        historiales = [Historial(*row) for row in rows]
        cursor.close()
        return historiales

    def update_historial(self, historial: Historial):
        cursor = self.conn.cursor()
        query = "UPDATE historialesmedicos SET id_usuario_paciente = %s, descripcion = %s, fecha_creacion = %s, notas = %s, diagnostico = %s, tratamiento = %s WHERE id_historial = %s"
        cursor.execute(query, (historial.id_usuario_paciente, historial.descripcion, historial.fecha_creacion, historial.notas, historial.diagnostico, historial.tratamiento, historial.id_historial))
        self.conn.commit()
        cursor.close()

    def delete_historial(self, id_historial: int):
        cursor = self.conn.cursor()
        query = "DELETE FROM historialesmedicos WHERE id_historial = %s"
        cursor.execute(query, (id_historial,))
        self.conn.commit()
        cursor.close()

    def search_historiales(self, search_term):
        cursor = self.conn.cursor()
        query = "SELECT * FROM historialesmedicos WHERE id_usuario_paciente = %s OR descripcion LIKE %s"
        cursor.execute(query, (search_term, f'%{search_term}%'))
        rows = cursor.fetchall()
        historiales = [Historial(*row) for row in rows]
        cursor.close()
        return historiales


class MySQLUsuariosDAO:
    def __init__(self):
        self.conn = get_mysql_connection()

    def create_usuario(self, usuario: Usuario):
        cursor = self.conn.cursor()
        query = "INSERT INTO usuarios (nombre, username, password, rol, numero_cedula) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query, (usuario.nombre, usuario.username, usuario.password, usuario.rol, usuario.numero_cedula))
        self.conn.commit()
        cursor.close()

    def get_all_usuarios(self):
        cursor = self.conn.cursor()
        query = "SELECT id_usuario, nombre, username, password, rol, numero_cedula FROM usuarios"
        cursor.execute(query)
        rows = cursor.fetchall()
        usuarios = [Usuario(*row) for row in rows]
        cursor.close()
        return usuarios

    def update_usuario(self, usuario: Usuario):
        cursor = self.conn.cursor()
        query = "UPDATE usuarios SET nombre = %s, username = %s, password = %s, rol = %s, numero_cedula = %s WHERE id_usuario = %s"
        cursor.execute(query, (usuario.nombre, usuario.username, usuario.password, usuario.rol, usuario.numero_cedula, usuario.id_usuario))
        self.conn.commit()
        cursor.close()

    def delete_usuario(self, id_usuario: int):
        cursor = self.conn.cursor()
        query = "DELETE FROM usuarios WHERE id_usuario = %s"
        cursor.execute(query, (id_usuario,))
        self.conn.commit()
        cursor.close()

    def cedula_existe(self, numero_cedula):
        cursor = self.conn.cursor()
        query = "SELECT COUNT(*) FROM usuarios WHERE numero_cedula = %s"
        cursor.execute(query, (numero_cedula,))
        count = cursor.fetchone()[0]
        cursor.close()
        return count > 0
