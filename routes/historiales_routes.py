from flask import Blueprint, request, render_template, redirect, url_for, session
from business.models import Historial
from business.business_logic import HistorialesService
from business.abstract_factory import MySQLDAOFactory

historiales_blueprint = Blueprint('historiales', __name__)

dao_factory = MySQLDAOFactory()
historiales_service = HistorialesService(dao_factory)

@historiales_blueprint.route('/historiales/manage', methods=['GET', 'POST'])
def manage_historiales():
    if request.method == 'POST':
        id_usuario_paciente = request.form['id_usuario_paciente']
        descripcion = request.form['descripcion']
        fecha_creacion = request.form['fecha_creacion']
        notas = request.form['notas']
        diagnostico = request.form['diagnostico']
        tratamiento = request.form['tratamiento']
        historial = Historial(None, id_usuario_paciente, descripcion, fecha_creacion, notas, diagnostico, tratamiento)
        historiales_service.create_historial(historial)
        return redirect(url_for('historiales.manage_historiales'))

    historiales = historiales_service.get_all_historiales()
    return render_template('manage_historiales.html', historiales=historiales)

@historiales_blueprint.route('/historiales/delete/<int:id_historial>', methods=['POST'])
def delete_historial(id_historial):
    historiales_service.delete_historial(id_historial)
    return redirect(url_for('historiales.manage_historiales'))

@historiales_blueprint.route('/historiales/search', methods=['GET', 'POST'])
def search_historial():
    historiales = []
    paciente = None
    if request.method == 'POST':
        search_term = request.form['search_term']
        historiales = historiales_service.search_historiales(search_term)

    return render_template('search_historial.html', historiales=historiales, paciente=paciente)
