class Cita:
    def __init__(self, id_cita, id_usuario_paciente, id_usuario_doctor, fecha, hora, motivo, estado):
        self.id_cita = id_cita
        self.id_usuario_paciente = id_usuario_paciente
        self.id_usuario_doctor = id_usuario_doctor
        self.fecha = fecha
        self.hora = hora
        self.motivo = motivo
        self.estado = estado

class Historial:
    def __init__(self, id_historial, id_usuario_paciente, descripcion, fecha_creacion, notas, diagnostico, tratamiento):
        self.id_historial = id_historial
        self.id_usuario_paciente = id_usuario_paciente
        self.descripcion = descripcion
        self.fecha_creacion = fecha_creacion
        self.notas = notas
        self.diagnostico = diagnostico
        self.tratamiento = tratamiento


class Usuario:
    def __init__(self, id_usuario, nombre, username, password, rol, numero_cedula):
        self.id_usuario = id_usuario
        self.nombre = nombre
        self.username = username
        self.password = password
        self.rol = rol
        self.numero_cedula = numero_cedula

