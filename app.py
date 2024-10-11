import requests
from bs4 import BeautifulSoup
import pandas as pd
import streamlit as st
from urllib.parse import quote

def obtener_descripcion_completa(url_producto):
    # Hacer una nueva solicitud HTTP para la página del producto
    response = requests.get(url_producto)
    if response.status_code != 200:
        return "Descripción no disponible"
    
    # Analizar el HTML
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Buscar la descripción completa
    descripcion = soup.find('p', {'class': 'ui-pdp-description__content'})
    
    return descripcion.text.strip() if descripcion else "Descripción no disponible"

def obtener_informacion_producto(producto):
    producto_codificado = quote(producto)
    url_busqueda = f'https://www.mercadolibre.cl/jm/search?as_word={producto_codificado}'
    
    # Hacer la solicitud HTTP a la página de búsqueda
    response = requests.get(url_busqueda)
    if response.status_code != 200:
        st.error("Error al acceder a Mercado Libre")
        return None
    
    # Analizar el HTML de la búsqueda
    soup = BeautifulSoup(response.text, 'html.parser')
    items = soup.find_all('li', {'class': 'ui-search-layout__item'})
    
    productos = []
    
    for item in items:
        nombre_producto = item.find('h2', {'class': 'ui-search-item__title'}).text.strip() if item.find('h2', {'class': 'ui-search-item__title'}) else 'N/A'
        nombre_vendedor = item.find('span', {'class': ''}).text.strip() if item.find('span', {'class': ''}) else 'N/A'
        ubicacion_venta = item.find('span', {'class': 'ui-search-item__location'}).text.strip() if item.find('span', {'class': 'ui-search-item__location'}) else 'N/A'
        tipo_venta = 'Internacional' if 'internacional' in ubicacion_venta.lower() else 'Nacional'
        
        # Obtener la URL del producto
        enlace_producto = item.find('a', {'class': 'ui-search-link'})
        url_producto = enlace_producto['href'] if enlace_producto else 'N/A'
        
        precio = item.find('span', {'class': 'andes-money-amount__fraction'}).text.strip() if item.find('span', {'class': 'andes-money-amount__fraction'}) else 'N/A'
        
        # Si existe la URL del producto, buscar la descripción completa
        if url_producto != 'N/A':
            descripcion_completa = obtener_descripcion_completa(url_producto)
        else:
            descripcion_completa = "Descripción no disponible"
        
        productos.append({
            'nombre_producto': nombre_producto,
            'descripcion_completa': descripcion_completa,
            'nombre_vendedor': nombre_vendedor,
            'ubicacion_venta': ubicacion_venta,
            'tipo_venta': tipo_venta,
            'url_producto': url_producto,
            'precio': precio
        })
    
    # Convertir la lista de productos a un DataFrame
    df_productos = pd.DataFrame(productos)
    
    return df_productos

# Configurar la aplicación de Streamlit
st.title("Web Scraping de Mercado Libre")
st.write("commit de prueba desde el celu version de pana 🎛")
st.write("aro aro aro, esta aplicación ha comenzaoo 🇨🇱🇨🇱")
st.write("by pastenes matias, aplicación de prueba")
st.write("WEEEEENAAA")
st.write("Ingrese el nombre del producto que desea buscar:")
    

# Widget de entrada para el nombre del producto
nombre_producto = st.text_input("Nombre del producto", "")

if st.button("Buscar"):
    # Obtener la información de los productos
    df_productos = obtener_informacion_producto(nombre_producto)

    # Mostrar la información obtenida
    if df_productos is not None and not df_productos.empty:
        st.dataframe(df_productos)
        # Guardar la información en un archivo CSV
        df_productos.to_csv(f'producto_{nombre_producto}.csv', index=False)
        st.success(f"La información ha sido guardada en 'producto_{nombre_producto}.csv'")
    else:
        st.warning("No se pudo obtener la información de los productos o no se encontraron productos.")
    
#st.download_button('descarga la data',producto_{nombre_producto}.csv)
