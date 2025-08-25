import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

SMTP_SERVER = os.environ.get('SMTP_SERVER', 'mail.smtp2go.com')
SMTP_PORT = int(os.environ.get('SMTP_PORT', 2525))
SMTP_USERNAME = os.environ.get('SMTP_USERNAME', 'ruedacereales.com.ar')
PASSWORD = os.environ.get('PASSWORD', 'rueda2024')
MAIL_ENVIO = os.environ.get('MAIL_ENVIO', 'contratos@ruedacereales.com.ar')
ASUNTO_DEFECTO = os.environ.get('ASUNTO', 'Comisiones pendientes')

def enviar_mail(texto, destinatario=None, asunto=None, es_html=False):
    """
    Envía un email con soporte para HTML y texto plano usando configuración del .env
    """
    asunto = asunto or ASUNTO_DEFECTO

    mensaje = MIMEMultipart()
    mensaje["From"] = MAIL_ENVIO
    mensaje["To"] = destinatario
    mensaje["Subject"] = asunto

    if es_html:
        mensaje.attach(MIMEText(texto, 'html', 'utf-8'))
    else:
        mensaje.attach(MIMEText(texto, 'plain', 'utf-8'))

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.login(SMTP_USERNAME, PASSWORD)
        server.send_message(mensaje)