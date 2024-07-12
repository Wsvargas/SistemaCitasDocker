from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from config.mysql_config import get_mysql_connection
from business.business_logic import UsuariosService
from business.abstract_factory import MySQLDAOFactory
from business.models import Usuario
from config.notifications import send_email  # Importa send_email
import functools

usuarios_blueprint = Blueprint('usuarios', __name__)

dao_factory = MySQLDAOFactory()
usuarios_service = UsuariosService(dao_factory)

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

def validar_cedula_ecuatoriana(cedula):
    if len(cedula) != 10:
        return False

    try:
        coeficientes = [2, 1, 2, 1, 2, 1, 2, 1, 2]
        suma = 0

        for i in range(9):
            valor = int(cedula[i]) * coeficientes[i]
            if valor >= 10:
                valor -= 9
            suma += valor

        digito_verificador = 10 - (suma % 10)
        if digito_verificador == 10:
            digito_verificador = 0

        return digito_verificador == int(cedula[9])
    except ValueError:
        return False


@usuarios_blueprint.route('/usuarios', methods=['GET', 'POST'])
@login_required
@role_required(['administrador'])
def manage_usuarios():
    conn = get_mysql_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        if 'buscar' in request.form:
            search_term = request.form['search']
            cursor.execute(
                'SELECT id_usuario, nombre, username, password, rol, numero_cedula FROM usuarios WHERE id_usuario = %s OR nombre LIKE %s',
                (search_term, f'%{search_term}%'))
            usuarios = cursor.fetchall()
        else:
            nombre = request.form['nombre']
            username = request.form['username']
            password = request.form['password']
            rol = request.form['rol']
            numero_cedula = request.form['numero_cedula']

            print("Datos del nuevo usuario:", nombre, username, password, rol, numero_cedula)  # Depuración

            if not validar_cedula_ecuatoriana(numero_cedula):
                flash('Cédula de identidad inválida', 'error')
            else:
                cursor.execute('SELECT * FROM usuarios WHERE numero_cedula = %s', (numero_cedula,))
                existing_cedula = cursor.fetchone()
                if existing_cedula:
                    flash('La cédula ya está registrada', 'error')
                else:
                    cursor.execute('SELECT * FROM usuarios WHERE username = %s', (username,))
                    existing_user = cursor.fetchone()
                    if existing_user:
                        flash('El nombre de usuario ya existe', 'error')
                    else:
                        try:
                            cursor.execute(
                                'INSERT INTO usuarios (nombre, username, password, rol, numero_cedula) VALUES (%s, %s, %s, %s, %s)',
                                (nombre, username, password, rol, numero_cedula))
                            conn.commit()
                            flash('Usuario agregado exitosamente', 'success')
                            print("Usuario agregado exitosamente")  # Depuración

                            # Enviar notificación por correo electrónico
                            send_email(
                                'Nuevo usuario creado',
                                'admin@example.com',
                                f'Se ha creado un nuevo usuario: {nombre} con el rol de {rol}.'
                            )
                        except Exception as e:
                            print("Error al agregar usuario:", e)  # Depuración
                            flash('Error al agregar usuario', 'error')

            cursor.execute('SELECT id_usuario, nombre, username, password, rol, numero_cedula FROM usuarios')
            usuarios = cursor.fetchall()
    else:
        cursor.execute('SELECT id_usuario, nombre, username, password, rol, numero_cedula FROM usuarios')
        usuarios = cursor.fetchall()

    cursor.close()
    conn.close()

    # Mensajes de depuración para revisar la estructura de las tuplas
    print("Usuarios recuperados de la base de datos:")
    for usuario in usuarios:
        print(usuario)
        if len(usuario) != 6:
            print("Error: Tupla con longitud incorrecta:", usuario)

    # Convertir las tuplas en objetos Usuario
    usuarios = [Usuario(*usuario) for usuario in usuarios if len(usuario) == 6]

    return render_template('list_usuarios.html', usuarios=usuarios)



@usuarios_blueprint.route('/usuarios/edit/<int:id_usuario>', methods=['GET', 'POST'])
@login_required
@role_required(['administrador'])
def edit_usuario(id_usuario):
    conn = get_mysql_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        nombre = request.form['nombre']
        username = request.form['username']
        password = request.form['password']
        rol = request.form['rol']
        numero_cedula = request.form['numero_cedula']
        cursor.execute('UPDATE usuarios SET nombre=%s, username=%s, password=%s, rol=%s, numero_cedula=%s WHERE id_usuario=%s',
                       (nombre, username, password, rol, numero_cedula, id_usuario))
        conn.commit()
        return redirect(url_for('usuarios.manage_usuarios'))

    cursor.execute('SELECT id_usuario, nombre, username, rol, numero_cedula FROM usuarios WHERE id_usuario = %s', (id_usuario,))
    usuario = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template('edit_usuario.html', usuario=usuario)

@usuarios_blueprint.route('/usuarios/delete/<int:id_usuario>', methods=['POST'])
@login_required
@role_required(['administrador'])
def delete_usuario(id_usuario):
    conn = get_mysql_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM usuarios WHERE id_usuario = %s', (id_usuario,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('usuarios.manage_usuarios'))
