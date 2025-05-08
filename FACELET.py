import pandas as pd
import numpy as np
import streamlit as st

# Título de la aplicación
st.title("Encontrar Números Faltantes para lucho alfonso y wilmer😂")

# Cargar el archivo Excel
archivo_excel = st.file_uploader("Cargar archivo Excel", type=["xlsx"])

# Definir los rangos para cada prefijo
rangos = {
    'RCGS': (4419305, 4436157),  # Rango para RCGS
    'REAR': (1627307, 1629068)    # Rango para REAR
}

# Función para encontrar los números secuenciales faltantes en un rango específico
def encontrar_faltantes(grupo, inicio, fin):
    grupo = np.sort(grupo)
    all_numbers = np.arange(inicio, fin + 1)
    faltantes = np.setdiff1d(all_numbers, grupo)
    return faltantes.tolist()

# Si se carga un archivo
if archivo_excel is not None:
    df = pd.read_excel(archivo_excel, sheet_name='DOCUMENTOS EQUIVALENTES')

    # Agrupar por Prefijo y aplicar la función para encontrar los faltantes
    resultados = {}
    for Prefijo, grupo in df.groupby('Prefijo')['Nro. Factura']:
        rango_inicio, rango_fin = rangos.get(Prefijo, (None, None))
        if rango_inicio is not None and rango_fin is not None:
            faltantes = encontrar_faltantes(grupo.values, rango_inicio, rango_fin)
            if faltantes:
                resultados[Prefijo] = faltantes

    # Mostrar resultados
    st.write("Resultados:")
    for prefijo, faltantes in resultados.items():
        st.write(f"Total de números faltantes para el prefijo {prefijo}: {len(faltantes)}")
        st.write(f"Números faltantes: {faltantes}")

# Opción para especificar rangos manualmente
st.sidebar.header("Especificar Rangos")
for prefijo in rangos.keys():
    inicio = st.sidebar.number_input(f"Inicio para {prefijo}", value=rangos[prefijo][0])
    fin = st.sidebar.number_input(f"Fin para {prefijo}", value=rangos[prefijo][1])
    rangos[prefijo] = (inicio, fin)
