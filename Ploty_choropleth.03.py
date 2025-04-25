import plotly.figure_factory as ff
import pandas as pd
import numpy as np

# 📌 Cargar los datos de tu Excel
file_path = "Book3.xlsx"  # ← Cambia esto con la ruta real
df = pd.read_excel(file_path)

# 📌 Descargar base de datos de condados con códigos FIPS
df_fips = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/laucnty16.csv")

# Asegurar que los nombres coincidan
df_fips = df_fips.rename(columns={"County Name": "County"})
df["County"] = df["County"].str.strip()  # Eliminar espacios extra

# Unir los datos de capacidad con los códigos FIPS
df_merged = df_fips.merge(df, on="County", how="left")

# 📌 Asegurar formato correcto de FIPS
df_merged['State FIPS Code'] = df_merged['State FIPS Code'].apply(lambda x: str(x).zfill(2))
df_merged['County FIPS Code'] = df_merged['County FIPS Code'].apply(lambda x: str(x).zfill(3))
df_merged['FIPS'] = df_merged['State FIPS Code'] + df_merged['County FIPS Code']

# Filtrar condados con datos válidos
df_merged = df_merged.dropna(subset=["Capacity(MW)"])

# 📌 Crear el mapa con Plotly
colorscale = ["#f7fbff","#ebf3fb","#deebf7","#d2e3f3","#c6dbef","#b3d2e9","#9ecae1",
              "#85bcdb","#6baed6","#57a0ce","#4292c6","#3082be","#2171b5","#1361a9",
              "#08519c","#0b4083","#08306b"]
endpts = list(np.linspace(df_merged["Capacity(MW)"].min(), df_merged["Capacity(MW)"].max(), len(colorscale) - 1))

fips = df_merged['FIPS'].tolist()
values = df_merged['Capacity(MW)'].tolist()

fig = ff.create_choropleth(
    fips=fips, values=values,
    binning_endpoints=endpts,
    colorscale=colorscale,
    show_state_data=False,
    show_hover=True, centroid_marker={'opacity': 0},
    asp=2.9, title='Capacidad en MW por Condado en EE.UU.',
    legend_title='Capacidad (MW)'
)

fig.layout.template = None
fig.show()
