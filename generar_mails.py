import pandas as pd
from smtp_mail import enviar_mail

class MailGenerator:
    def __init__(self, mapeo_cuit_mail_path):
        self.mails_dict = self._cargar_mapeo(mapeo_cuit_mail_path)

    def _cargar_mapeo(self, path):
        mails_dict = {}
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or '=' not in line:
                    continue
                cuit, mails = line.split('=', 1)
                cuit = cuit.strip()
                try:
                    mails_list = eval(mails, {"__builtins__": None}, {})
                    if isinstance(mails_list, str):
                        mails_list = [mails_list]
                    mails_dict[cuit] = ','.join(mails_list)
                except Exception as e:
                    print(f"Error procesando mails para CUIT {cuit}: {e}")
                    continue
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
            cuerpo = f"Estimado,\n\nAdjuntamos el detalle de comisiones pendientes:\n\n"
            for _, fila in grupo.iterrows():
                cuerpo += (
                    f"Empresa: {cuit},"
                    f"Comprobante: {fila['COMPROBANTE']}, "
                    f"Contrato: {fila['CONTRATO']}, "
                    f"Fecha: {fila['FECHA']}, "
                    f"Comisión pendiente: ${fila['COMISION PENDIENTE']:.2f}\n\n"
                )
            cuerpo += "\nPor favor, regularizar a la brevedad.\nSaludos."
            enviar_mail(cuerpo, destinatario=mails, asunto="Comisiones pendientes", es_html=False)
            print(f"Mail enviado a: {mails}")