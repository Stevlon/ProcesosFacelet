# import pandas as pd
# import numpy as np

# # Variables para el archivo Excel y la hoja de cálculo
# archivo_excel = f'C:/Users/jslondono/Desktop/SB Pruebas/Reporte-Documentos-Equivalentes-2025-04-14.xlsx'
# archivo_resultados = f'C:/Users/jslondono/Desktop/SB Pruebas/Numeros_faltantes.xlsx'
# hoja_excel = 'DOCUMENTOS EQUIVALENTES'

# df = pd.read_excel(archivo_excel, sheet_name=hoja_excel)

# # Función para encontrar los números secuenciales faltantes en un rango específico
# def encontrar_faltantes(grupo, inicio, fin):
#     import pandas as pd
#     import numpy as np
#     grupo = np.sort(grupo)
#     all_numbers = np.arange(inicio, fin + 1)  # Cambiado para usar el rango específico
#     faltantes = np.setdiff1d(all_numbers, grupo)
#     return faltantes.tolist()

# # Definir los rangos para cada prefijo
# rangos = {
#     'RCGS': (4419305, 4436157),  # Rango para RCGS
#     'REAR': (1627307, 1629068)    # Rango para REAR
# }

# # Agrupar por Prefijo y aplicar la función para encontrar los faltantes
# resultados = {}
# for Prefijo, grupo in df.groupby('Prefijo')['Nro. Factura']:
#     rango_inicio, rango_fin = rangos.get(Prefijo, (None, None))  # Obtener el rango correspondiente
#     if rango_inicio is not None and rango_fin is not None:
#         faltantes = encontrar_faltantes(grupo.values, rango_inicio, rango_fin)  # Pasar el rango
#         if faltantes:
#             resultados[Prefijo] = faltantes

# # Crear un DataFrame para los resultados y guardarlos en un nuevo archivo de Excel
# resultados_df = pd.DataFrame.from_dict(resultados, orient='index').transpose()
# resultados_df.to_excel(archivo_resultados, index=False)

# # Guardar el número de faltantes en variables específicas
# numerosRCGS = len(resultados.get('RCGS', []))
# # SetVar("numerosRCGS", numerosRCGS)
# numerosREAR = len(resultados.get('REAR', []))
# # SetVar("numerosREAR", numerosREAR)

# # Imprimir los resultados
# print(f"Total de números faltantes para el prefijo RCGS: {numerosRCGS}")
# print(f"Total de números faltantes para el prefijo REAR: {numerosREAR}")


import pandas as pd
import numpy as np
import streamlit as st

# Título de la aplicación
st.title("Encontrar Números Faltantes")

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