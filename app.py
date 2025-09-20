# 🦙 Contador de Células de Alpaca (Streamlit App)

Esta aplicación web permite contar y clasificar ovocitos o embriones de alpaca desde imágenes usando OpenCV y Streamlit.

## Funcionalidades

-Subida de imágenes (local o GitHub)
-Conteo automático de células
-Clasificación simulada (Ovocito / Embrión)
-Deslizador para ajustar sensibilidad

## Cómo ejecutar localmente

```bash
git clone https://github.com/tu_usuario/alpaca-cell-detector.git
cd alpaca-cell-detector
pip install -r requirements.txt
streamlit run app.py
import streamlit as st
import cv2
import numpy as np
from PIL import Image
import requests
from io import BytesIO
import os

st.set_page_config(page_title="Contador de Células de Alpaca", layout="centered")

st.title("Contador e Identificador de Células de Alpaca")
st.markdown("Esta aplicación permite **contar ovocitos y embriones de alpaca** a partir de imágenes.")

# Slider de sensibilidad
sensitivity = st.slider("Sensibilidad del conteo (umbral binarización)", 0, 255, 127)

# Cargar imagen
st.subheader("Subida de imágenes (local o GitHub)")
img_source = st.radio("Fuente de imagen", ["Subir archivo", "Desde GitHub (URL)"])

image = None
image_name = "No cargada"

if img_source == "Subir archivo":
    uploaded_file = st.file_uploader("Selecciona una imagen", type=["png", "jpg", "jpeg"])
    if uploaded_file:
        image = Image.open(uploaded_file)
        image_name = uploaded_file.name
elif img_source == "Desde GitHub (URL)":
    url = st.text_input("Pega la URL de la imagen (raw.githubusercontent.com/...)", 
                        "https://raw.githubusercontent.com/tu_usuario/tu_repo/main/images/ejemplo_embrión.png")
    if url:
        try:
            response = requests.get(url)
            image = Image.open(BytesIO(response.content))
            image_name = os.path.basename(url)
        except:
            st.error("No se pudo cargar la imagen desde la URL.")

if image:
    st.image(image, caption=f"Imagen cargada: {image_name}", use_column_width=True)

    # Procesamiento OpenCV
    img_np = np.array(image.convert("RGB"))
    gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
    _, thresh = cv2.threshold(gray, sensitivity, 255, cv2.THRESH_BINARY_INV)

    # Encontrar contornos
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cell_count = len(contours)

    # Dibujar contornos
    img_contour = img_np.copy()
    cv2.drawContours(img_contour, contours, -1, (0, 255, 0), 2)

    st.image(img_contour, caption=f"🔎 Células detectadas: {cell_count}", use_column_width=True)

    # Clasificación simulada según cantidad
    st.subheader("Clasificación celular estimada")
    if cell_count <= 3:
        cell_type = "Ovocito"
    elif 4 <= cell_count <= 10:
        cell_type = "Embrión en desarrollo"
    else:
        cell_type = "Múltiples embriones o agrupación celular"

    st.success(f"Clasificación: **{cell_type}**")
    st.info(f"Nombre de imagen: `{image_name}`")

