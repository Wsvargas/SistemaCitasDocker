from flask import Blueprint, render_template, request, redirect, url_for, session
from config.mysql_config import get_mysql_connection
import functools

auth_blueprint = Blueprint('auth', __name__)

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

@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_mysql_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id_usuario, nombre, password, rol FROM usuarios WHERE username = %s', (username,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        if user and user[2] == password:
            session.clear()
            session['user_id'] = user[0]
            session['user_name'] = user[1]
            session['user_role'] = user[3]
            if user[3] == 'doctor':
                return redirect(url_for('auth.doctor_dashboard'))
            elif user[3] == 'paciente':
                return redirect(url_for('auth.paciente_dashboard'))
            elif user[3] == 'administrador':
                return redirect(url_for('auth.admin_dashboard'))
        return render_template('login.html', error='Invalid username or password')
    return render_template('login.html')

@auth_blueprint.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@auth_blueprint.route('/doctor_dashboard')
@login_required
@role_required(['doctor'])
def doctor_dashboard():
    return render_template('doctor_dashboard.html')

@auth_blueprint.route('/paciente_dashboard')
@login_required
@role_required(['paciente'])
def paciente_dashboard():
    return render_template('paciente_dashboard.html')

@auth_blueprint.route('/admin_dashboard')
@login_required
@role_required(['administrador'])
def admin_dashboard():
    return render_template('admin_dashboard.html')
