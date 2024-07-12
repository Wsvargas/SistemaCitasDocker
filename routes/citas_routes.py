from flask import Blueprint, request, render_template, redirect, url_for, session
from business.models import Cita
from business.business_logic import CitasService
from business.abstract_factory import MySQLDAOFactory
import functools

citas_blueprint = Blueprint('citas', __name__)

# Instanciar la fábrica concreta y el servicio de citas
dao_factory = MySQLDAOFactory()
citas_service = CitasService(dao_factory)

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view

def role_required(roles):
    def decorator(view):
        @functools.wraps(view)
        def wrapped_view(**kwargs):
            if 'user_role' not in session or session['user_role'] not in roles:
                return redirect(url_for('index'))
            return view(**kwargs)
        return wrapped_view
    return decorator

@citas_blueprint.route('/citas', methods=['GET'])
@login_required
def view_citas():
    user_role = session['user_role']
    user_id = session['user_id']

    if user_role == 'doctor':
        citas = [cita for cita in citas_service.get_all_citas() if cita.id_usuario_doctor == user_id]
    elif user_role == 'paciente':
        citas = [cita for cita in citas_service.get_all_citas() if cita.id_usuario_paciente == user_id]
    else:  # administrador
        citas = citas_service.get_all_citas()

    return render_template('list_citas.html', citas=citas)

@citas_blueprint.route('/citas/manage', methods=['GET', 'POST'])
@login_required
@role_required(['doctor', 'administrador'])
def manage_citas():
    if request.method == 'POST':
        id_usuario_paciente = request.form['id_usuario_paciente']
        id_usuario_doctor = request.form['id_usuario_doctor']
        fecha = request.form['fecha']
        hora = request.form['hora']
        motivo = request.form['motivo']
        estado = request.form['estado']
        cita = Cita(None, id_usuario_paciente, id_usuario_doctor, fecha, hora, motivo, estado)
        citas_service.create_cita(cita)
        return redirect(url_for('citas.manage_citas'))

    citas = citas_service.get_all_citas()
    return render_template('manage_citas.html', citas=citas)

@citas_blueprint.route('/citas/delete/<int:id_cita>', methods=['POST'])
@login_required
@role_required(['doctor', 'administrador'])
def delete_cita(id_cita):
    citas_service.delete_cita(id_cita)
    return redirect(url_for('citas.manage_citas'))
