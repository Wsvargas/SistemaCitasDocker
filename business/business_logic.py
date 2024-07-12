class CitasService:
    def __init__(self, dao_factory):
        self.dao = dao_factory.create_citas_dao()

    def get_all_citas(self):
        return self.dao.get_all_citas()

    def create_cita(self, cita):
        return self.dao.create_cita(cita)

    def update_cita(self, cita):
        return self.dao.update_cita(cita)

    def delete_cita(self, id_cita):
        return self.dao.delete_cita(id_cita)

class HistorialesService:
    def __init__(self, dao_factory):
        self.dao = dao_factory.create_historiales_dao()

    def get_all_historiales(self):
        return self.dao.get_all_historiales()

    def create_historial(self, historial):
        return self.dao.create_historial(historial)

    def update_historial(self, historial):
        return self.dao.update_historial(historial)

    def delete_historial(self, id_historial):
        return self.dao.delete_historial(id_historial)

    def search_historiales(self, search_term):
        return self.dao.search_historiales(search_term)

class UsuariosService:
    def __init__(self, dao_factory):
        self.dao = dao_factory.create_usuarios_dao()

    def get_all_usuarios(self):
        return self.dao.get_all_usuarios()

    def create_usuario(self, usuario):
        return self.dao.create_usuario(usuario)

    def update_usuario(self, usuario):
        return self.dao.update_usuario(usuario)

    def delete_usuario(self, id_usuario):
        return self.dao.delete_usuario(id_usuario)

    def cedula_existe(self, numero_cedula):
        return self.dao.cedula_existe(numero_cedula)
