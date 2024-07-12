from dao.mysql_dao import MySQLCitasDAO, MySQLHistorialesDAO, MySQLUsuariosDAO

class DAOFactory:
    def create_citas_dao(self):
        raise NotImplementedError

    def create_historiales_dao(self):
        raise NotImplementedError

class MySQLDAOFactory:
    def create_citas_dao(self):
        return MySQLCitasDAO()

    def create_historiales_dao(self):
        return MySQLHistorialesDAO()

    def create_usuarios_dao(self):
        return MySQLUsuariosDAO()
