import pandas as pd

class ComisionCleaner:
    def __init__(self, archivo_entrada, archivo_salida):
        self.archivo_entrada = archivo_entrada
        self.archivo_salida = archivo_salida

    def limpiar(self):
        df = pd.read_csv(self.archivo_entrada, skiprows=2, encoding='latin1', sep=';', engine='python')
        df.columns = df.columns.str.strip()
        df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
        columnas = list(df.columns)
        col_b = columnas[1]
        df[col_b] = df[col_b].astype(str)
        col_e = columnas[4]
        df[col_e] = pd.to_datetime(df[col_e], errors='coerce', dayfirst=True)
        for idx in [6, 7, 8]:
            col = columnas[idx]
            df[col] = df[col].astype(str).str.replace('$', '', regex=False).str.replace('.', '', regex=False).str.replace(',', '.', regex=False)
            df[col] = pd.to_numeric(df[col], errors='coerce')
        for i, col in enumerate(columnas):
            if i not in [1, 4, 6, 7, 8]:
                df[col] = pd.to_numeric(df[col], errors='coerce').astype('Int64')
        columna_comision = 'COMISION PENDIENTE'
        df_filtrado = df[df[columna_comision] > 0]
        df_filtrado.to_csv(self.archivo_salida, index=False)
        return df_filtrado
