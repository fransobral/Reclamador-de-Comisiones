import pandas as pd
import ast
from smtp_mail import enviar_mail

class MailGenerator:
    def __init__(self, mapeo_cuit_mail_path):
        self.mails_dict = self._cargar_mapeo(mapeo_cuit_mail_path)

    def _cargar_mapeo(self, path):
        mails_dict = {}
        with open(path, 'r', encoding='utf-8') as f:
            current_cuit = None
            buffer = []
            bracket_balance = 0

            for raw_line in f:
                line = raw_line.strip()
                if not line:
                    continue

                if current_cuit is None:
                    if '=' not in line:
                        continue
                    cuit, value_start = line.split('=', 1)
                    current_cuit = cuit.strip()
                    buffer = [value_start]
                    bracket_balance = value_start.count('[') - value_start.count(']')

                    if bracket_balance <= 0:
                        text = ''.join(buffer)
                        try:
                            mails_list = ast.literal_eval(text)
                            if isinstance(mails_list, str):
                                mails_list = [mails_list]
                            mails_dict[current_cuit] = ','.join(mails_list)
                        except Exception as e:
                            print(f"Error procesando mails para CUIT {current_cuit}: {e}")
                        finally:
                            current_cuit = None
                            buffer = []
                            bracket_balance = 0
                else:
                    buffer.append(line)
                    bracket_balance += line.count('[') - line.count(']')

                    if bracket_balance <= 0:
                        text = '\n'.join(buffer)
                        try:
                            mails_list = ast.literal_eval(text)
                            if isinstance(mails_list, str):
                                mails_list = [mails_list]
                            mails_dict[current_cuit] = ','.join(mails_list)
                        except Exception as e:
                            print(f"Error procesando mails para CUIT {current_cuit}: {e}")
                        finally:
                            current_cuit = None
                            buffer = []
                            bracket_balance = 0

        return mails_dict

    def enviar_comisiones(self, df):
        # Asegura que la columna CUIT sea string
        df['C.U.I.T.'] = df['C.U.I.T.'].astype(str)
        grupos = df.groupby('C.U.I.T.')

        for cuit, grupo in grupos:
            mails = self.mails_dict.get(cuit, None)
            if not mails:
                print(f"No se encontró mail para CUIT {cuit}, se omite.")
                continue
            encabezado_html = "<p>Estimado,</p><p>Adjuntamos el detalle de comisiones pendientes:</p>"
            items_html = ""
            for _, fila in grupo.iterrows():
                items_html += (
                    "<li>"
                    f"Empresa: {cuit}, "
                    f"Comprobante: {fila['COMPROBANTE']}, "
                    f"Contrato: {fila['CONTRATO']}, "
                    f"Fecha: {fila['FECHA']}, "
                    f"Comisión pendiente: ${fila['COMISION PENDIENTE']:.2f}"
                    "</li>"
                )
            cuerpo = (
                f"{encabezado_html}"
                f"<ul style='margin:0 0 12px 18px'>{items_html}</ul>"
                "<p>Por favor, regularizar a la brevedad.<br>Saludos.</p>"
            )

            #enviar_mail(cuerpo, destinatario=mails, asunto="Comisiones pendientes", es_html=True, logo_path="Logo Rueda Cereales - Edited.png")
            enviar_mail(cuerpo, "fsobral@fi.uba.ar", asunto="Comisioness pendientes", es_html=True, logo_path="Logo Rueda Cereales - Edited.png")
            print(f"Mail enviado a: {mails}")
            
