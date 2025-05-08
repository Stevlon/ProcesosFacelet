import pandas as pd
import numpy as np
import streamlit as st

# Título de la aplicación
st.title("Encontrar Números Faltantes para lucho alfonso y wilmer😂")

# Inicializar el diccionario de rangos vacío
rangos = {}

# Solicitar rangos manualmente
st.sidebar.header("Configuración de Rangos")
st.sidebar.write("Por favor, ingrese los rangos para cada prefijo")

# Solicitar rangos para RCGS
st.sidebar.subheader("Rango RCGS")
inicio_rcgs = st.sidebar.number_input("Inicio RCGS", value=0, step=1)
fin_rcgs = st.sidebar.number_input("Fin RCGS", value=0, step=1)
rangos['RCGS'] = (inicio_rcgs, fin_rcgs)

# Solicitar rangos para REAR
st.sidebar.subheader("Rango REAR")
inicio_rear = st.sidebar.number_input("Inicio REAR", value=0, step=1)
fin_rear = st.sidebar.number_input("Fin REAR", value=0, step=1)
rangos['REAR'] = (inicio_rear, fin_rear)

# Función para encontrar los números secuenciales faltantes en un rango específico
def encontrar_faltantes(grupo, inicio, fin):
    grupo = np.sort(grupo)
    all_numbers = np.arange(inicio, fin + 1)
    faltantes = np.setdiff1d(all_numbers, grupo)
    return faltantes.tolist()

# Cargar el archivo Excel
archivo_excel = st.file_uploader("Cargar archivo Excel", type=["xlsx"])

# Si se carga un archivo
if archivo_excel is not None:
    df = pd.read_excel(archivo_excel, sheet_name='DOCUMENTOS EQUIVALENTES')

    # Agrupar por Prefijo y aplicar la función para encontrar los faltantes
    resultados = {}
    for Prefijo, grupo in df.groupby('Prefijo')['Nro. Factura']:
        rango_inicio, rango_fin = rangos.get(Prefijo, (None, None))
        if rango_inicio is not None and rango_fin is not None and rango_inicio > 0 and rango_fin > 0:
            faltantes = encontrar_faltantes(grupo.values, rango_inicio, rango_fin)
            if faltantes:
                resultados[Prefijo] = faltantes
                st.info(f"Total de números faltantes para el prefijo {Prefijo}: {len(faltantes)}")
                #st.write(f"Números faltantes: {faltantes}")
                if len(faltantes) > 1500:
                    st.warning(f"Números faltantes: Excede el rango limite para mostrar los secuenciales")
                else:
                    st.write(f"Números faltantes: {faltantes}")
            else:
                st.info(f"Sin diferencias para {Prefijo}")
        else:
            st.warning(f"No se ha configurado un rango válido para el prefijo {Prefijo}") 
