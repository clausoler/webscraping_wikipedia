# Extracción datos sobre la plataforma Netflix a través de la web Wikipedia


# El objetivo es construir un DataFrame que incluya los siguientes datos:
  # Ubicacicón de la empresa Netflix
  # Los servicios que ofrece
  # Beneficios
  # Nº de empleados
  # Productos en español con mayor éxito mundial
 
from bs4 import BeautifulSoup
import requests
import pandas as pd

def web_scraping_netflix(url):
    """
    Función para realizar web scraping en la página de Wikipedia sobre Netflix.

    Parámetros:
    - url (str): URL de la página web de Netflix en Wikipedia.

    Retorno:
    - dict: Diccionario con los datos extraídos.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"
    }

    # Realizamos la solicitud
    response = requests.get(url, headers=headers)

    # Verificamos el estado de la solicitud
    if response.status_code != 200:
        print(f"Error en la solicitud: {response.status_code}")
        return None

    # Analizamos el contenido HTML con BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")

    # Extraer datos específicos
    data = {}

    # Ubicación de la empresa Netflix
    infobox = soup.find("table", class_="infobox vcard")
    if infobox:
        for row in infobox.find_all("tr"):
            header = row.find("th")
            if header and "Headquarters" in header.text:
                data["Ubicación"] = row.find("td").text.strip()

    # Servicios que ofrece
    services = soup.find_all("p")
    servicios_text = ""
    for paragraph in services:
        if "streaming" in paragraph.text.lower():
            servicios_text += paragraph.text.strip() + " "
    data["Servicios"] = servicios_text if servicios_text else "No especificado"

    # Beneficios
    for row in infobox.find_all("tr"):
        header = row.find("th")
        if header and "Revenue" in header.text:
            data["Beneficios"] = row.find("td").text.strip()

    # Número de empleados
    for row in infobox.find_all("tr"):
        header = row.find("th")
        if header and "Number of employees" in header.text:
            data["Número de empleados"] = row.find("td").text.strip()

    # Productos en español con mayor éxito mundial
    productos_exito = ""
    for paragraph in services:
        if "series en español" in paragraph.text.lower() or "productos en español" in paragraph.text.lower():
            productos_exito += paragraph.text.strip() + " "
    data["Productos en español de mayor éxito mundial"] = productos_exito if productos_exito else "No especificado"

    return data

# URL de la página de Netflix en Wikipedia
url_netflix = "https://en.wikipedia.org/wiki/Netflix"

# Ejecutar la función y construir el DataFrame
data_netflix = web_scraping_netflix(url_netflix)

# Convertir los datos en un DataFrame
df_netflix = pd.DataFrame([data_netflix])

# Mostrar el DataFrame
print(df_netflix)

# Guardamos el DataFrame en un archivo CSV
ruta_guardado = "netflix_wikipedia.csv"
df_netflix.to_csv(ruta_guardado, index=False, encoding="utf-8")
print(f"Datos guardados en {ruta_guardado}")



# importamos las librerías que necesitamos

# Visualización
# ------------------------------------------------------------------------------
import matplotlib.pyplot as plt
import seaborn as sns

# Configuración
# -----------------------------------------------------------------------
pd.set_option('display.max_columns', None) # para poder visualizar todas las columnas de los DataFrames 

# Datos extraídos simulados para representar en el gráfico
data = {
    "Ubicación": "Los Gatos, California, USA",
    "Servicios": "Streaming de películas y series, producción de contenido original",
    "Beneficios": "$31.6 billion (2022)",
    "Número de empleados": "12,800 (2022)",
    "Productos en español más exitosos": "La Casa de Papel, Élite, Narcos"
}

# Big numbers a graficar
keys = ["Beneficios", "Número de empleados"]
values = [31.6, 12.8]  # En miles de millones para beneficios y miles para empleados

# Crear el gráfico de barras
plt.figure(figsize=(8, 5))
plt.bar(keys, values)
plt.title("Indicadores Clave de Netflix")
plt.ylabel("Millones (Beneficios) y Miles (Empleados)")
plt.xticks(rotation=45)
plt.tight_layout()

# Mostrar el gráfico
plt.show()
