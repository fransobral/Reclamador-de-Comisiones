from limpiar_comisiones import ComisionCleaner
from generar_mails import MailGenerator

def main():
    archivo_entrada = 'Comisiones Betcom.CSV'
    archivo_salida = 'Comisiones_Betcom_filtrado.csv'
    mapeo_cuit_mail_path = 'mapeo_cuit_mail.txt'

    cleaner = ComisionCleaner(archivo_entrada, archivo_salida)
    df_filtrado = cleaner.limpiar()

    mailer = MailGenerator(mapeo_cuit_mail_path)
    mailer.enviar_comisiones(df_filtrado)

if __name__ == "__main__":
    main()