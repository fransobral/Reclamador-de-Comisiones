# Reclamador de Comisiones

Este proyecto automatiza el filtrado de comisiones pendientes y el envío de correos electrónicos a los destinatarios correspondientes, utilizando archivos CSV de comisiones y un mapeo de CUIT a emails.

## ¿Qué hace?

1. **Limpia y filtra** los archivos de comisiones (`Comisiones Betcom.CSV`, `Comisiones Rueda.CSV`) para obtener solo las filas con comisiones pendientes.
2. **Genera y envía emails** a los destinatarios definidos en un archivo de mapeo (`mapeo_cuit_mail.txt`), adjuntando el detalle de las comisiones pendientes por CUIT.
3. Utiliza un servicio SMTP configurable mediante un archivo `.env` para el envío de correos.

---

## Estructura del proyecto

```
.env
main.py
limpiar_comisiones.py
generar_mails.py
smtp_mail.py
mapeo_cuit_mail.txt
Comisiones Betcom.CSV
Comisiones Rueda.CSV
Comisiones_Betcom_filtrado.csv
Comisiones_Rueda_filtrado.csv
```

---

## Uso

1. **Configura el archivo `.env`** con los datos de tu servidor SMTP (ver formato más abajo).
2. **Completa el archivo `mapeo_cuit_mail.txt`** con el mapeo de CUIT a emails.
3. **Coloca los archivos CSV de comisiones** en la carpeta del proyecto.
4. **Ejecuta el script principal**:

   ```sh
   python main.py
   ```

   Esto generará los archivos filtrados y enviará los correos automáticamente.

---

## Formato de los archivos

### `mapeo_cuit_mail.txt`

Cada línea debe tener el siguiente formato:

```
CUIT=[lista_de_emails]
```

Ejemplo:

```
24125318114=["contratos@ruedacereales.com.ar"]
30611267386=["contratos@ruedacereales.com.ar","otro@ejemplo.com"]
```

- El CUIT debe ser numérico, sin comillas.
- La lista de emails debe estar entre corchetes y cada email entre comillas dobles, separados por comas si hay más de uno.

---

### `.env`

Debes crear un archivo `.env` con las siguientes variables para la configuración del envío de emails:

```
SMTP_SERVER=smtp.tuservidor.com
SMTP_PORT=587
SMTP_USERNAME=usuario@tuservidor.com
PASSWORD=tu_contraseña
MAIL_ENVIO=usuario@tuservidor.com
ASUNTO_DEFECTO=Comisiones pendientes
```

- `SMTP_SERVER`: Dirección del servidor SMTP.
- `SMTP_PORT`: Puerto del servidor SMTP (usualmente 587 para TLS).
- `SMTP_USERNAME`: Usuario para autenticación SMTP.
- `PASSWORD`: Contraseña del usuario SMTP.
- `MAIL_ENVIO`: Email que aparecerá como remitente.
- `ASUNTO_DEFECTO`: Asunto por defecto para los correos.

---

## Notas

- Los archivos CSV deben tener el formato esperado (ver ejemplos en los archivos incluidos).
- El script solo enviará correos para los CUIT que tengan mapeo en `mapeo_cuit_mail.txt`.
- Los archivos filtrados (`Comisiones_Betcom_filtrado.csv`, etc.) se generan automáticamente.

---

## Dependencias

- Python 3.x
- pandas
- python-dotenv

Instala las dependencias con:

```sh
pip install pandas python-dotenv
```

---

## Licencia

Uso interno. Adaptar según necesidades.
