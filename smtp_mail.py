import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import os
from dotenv import load_dotenv
import html

# Cargar variables de entorno desde .env
load_dotenv()

SMTP_SERVER = os.environ.get('SMTP_SERVER', 'mail.smtp2go.com')
SMTP_PORT = int(os.environ.get('SMTP_PORT', 2525))
SMTP_USERNAME = os.environ.get('SMTP_USERNAME', 'ruedacereales.com.ar')
PASSWORD = os.environ.get('PASSWORD', 'rueda2024')
MAIL_ENVIO = os.environ.get('MAIL_ENVIO', 'contratos@ruedacereales.com.ar')
ASUNTO_DEFECTO = os.environ.get('ASUNTO', 'Comisiones pendientes')

# Firma (footer) configurable por archivo o variables de entorno
SIGNATURE_HTML_PATH = os.environ.get('SIGNATURE_HTML_PATH', 'firma.html')
SIGNATURE_TEXT_PATH = os.environ.get('SIGNATURE_TEXT_PATH', 'firma.txt')
INCLUDE_SIGNATURE = os.environ.get('INCLUDE_SIGNATURE', '1') not in ('0', 'false', 'False')

def _read_file_if_exists(path):
    try:
        if path and os.path.isfile(path):
            with open(path, 'r', encoding='utf-8') as f:
                return f.read()
    except Exception:
        pass
    return None


def enviar_mail(texto, destinatario=None, asunto=None, es_html=False, incluir_firma=None, logo_path=None):
    """
    Envía un email con partes texto y HTML (multipart/alternative).

    - Si `es_html` es False, el cuerpo HTML se genera a partir del texto (\n -> <br>).
    - Firma opcional: si existen `firma.html` y/o `firma.txt`, se agregan al final.
      Se puede configurar con SIGNATURE_HTML_PATH / SIGNATURE_TEXT_PATH y desactivar con INCLUDE_SIGNATURE=0.
    - `incluir_firma` permite forzar on/off por envío.
    """
    asunto = asunto or ASUNTO_DEFECTO
    usar_firma = INCLUDE_SIGNATURE if incluir_firma is None else bool(incluir_firma)

    # Cargar firmas
    firma_html = _read_file_if_exists(SIGNATURE_HTML_PATH) if usar_firma else None
    firma_txt = _read_file_if_exists(SIGNATURE_TEXT_PATH) if usar_firma else None

    # Construir variantes plain y html
    if es_html:
        cuerpo_html = texto
        # Versión texto básica: sin etiquetas
        cuerpo_txt = html.unescape(texto)
    else:
        cuerpo_txt = texto
        cuerpo_html = '<br>'.join(html.escape(texto).splitlines())

    if usar_firma:
        if firma_txt:
            cuerpo_txt = f"{cuerpo_txt}\n\n{firma_txt}"
        if firma_html:
            cuerpo_html = f"{cuerpo_html}<br><br>{firma_html}"

    # Mensaje multipart/alternative: primero texto plano, luego HTML
    # Si hay imagen inline necesitaremos un contenedor 'related'
    root = MIMEMultipart('related')
    mensaje = MIMEMultipart('alternative')
    root["From"] = MAIL_ENVIO
    root["To"] = destinatario or ''
    root["Subject"] = asunto

    mensaje.attach(MIMEText(cuerpo_txt, 'plain', 'utf-8'))

    # Reemplazar referencia al logo local por CID si corresponde
    cid = 'logo-empresa'
    html_con_cid = cuerpo_html
    if logo_path and os.path.isfile(logo_path):
        # Detectar el src en firma.html si usa el mismo nombre
        basename = os.path.basename(logo_path)
        html_con_cid = html_con_cid.replace(f'src="{basename}"', f'src="cid:{cid}"')
        html_con_cid = html_con_cid.replace(f"src='{basename}'", f"src='cid:{cid}'")

    mensaje.attach(MIMEText(html_con_cid, 'html', 'utf-8'))

    root.attach(mensaje)

    # Adjuntar imagen inline si existe
    if logo_path and os.path.isfile(logo_path):
        with open(logo_path, 'rb') as f:
            img = MIMEImage(f.read())
            img.add_header('Content-ID', f'<{cid}>')
            img.add_header('Content-Disposition', 'inline', filename=os.path.basename(logo_path))
            root.attach(img)

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.login(SMTP_USERNAME, PASSWORD)
        server.send_message(root)
