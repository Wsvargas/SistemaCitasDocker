from flask import Flask, render_template, redirect, url_for, session
from routes.auth_routes import auth_blueprint
from routes.citas_routes import citas_blueprint
from routes.historiales_routes import historiales_blueprint
from routes.usuarios_routes import usuarios_blueprint
from config.notifications import send_email

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Registrar los blueprints
app.register_blueprint(auth_blueprint)
app.register_blueprint(citas_blueprint)
app.register_blueprint(historiales_blueprint)
app.register_blueprint(usuarios_blueprint)

@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    else:
        if session['user_role'] == 'doctor':
            return redirect(url_for('auth.doctor_dashboard'))
        elif session['user_role'] == 'paciente':
            return redirect(url_for('auth.paciente_dashboard'))
        elif session['user_role'] == 'administrador':
            return redirect(url_for('auth.admin_dashboard'))
        else:
            return redirect(url_for('auth.login'))

if __name__ == '__main__':
    app.run(debug=True)