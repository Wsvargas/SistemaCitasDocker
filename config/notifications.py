import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import subprocess
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

def send_email(subject, body):
    sender_email = os.getenv('EMAIL_SENDER')
    sender_password = os.getenv('EMAIL_PASSWORD')
    recipient_email = os.getenv('EMAIL_RECIPIENT')
    smtp_server = os.getenv('SMTP_SERVER')
    smtp_port = os.getenv('SMTP_PORT')

    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = recipient_email
    message['Subject'] = subject

    message.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, message.as_string())
            print("Correo enviado exitosamente")
    except Exception as e:
        print(f"Error al enviar correo electrónico: {e}")

def monitor_docker_events():
    cmd = ['docker', 'events', '--filter', 'event=stop']
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            output_str = output.strip()
            print(f"Datos recibidos: {output_str}")  # Para depuración
            if "container stop" in output_str:
                parts = output_str.split()
                container_id = parts[4]
                container_name = next((part.split('=')[1] for part in parts if part.startswith('name=')), "desconocido")
                send_email(
                    'Contenedor detenido',
                    f'El contenedor {container_name} (ID: {container_id}) se ha detenido.'
                )

if __name__ == "__main__":
    monitor_docker_events()
