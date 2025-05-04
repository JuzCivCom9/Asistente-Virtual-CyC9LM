
import streamlit as st
import json
import difflib
from pathlib import Path

# Configuración de página
st.set_page_config(page_title="Asistente Virtual IA - Juzgado Civil y Comercial N° 9", layout="centered")

# Cargar logo
st.image("assets/logo-juzgado9.png", width=120)

# Título y bienvenida
st.markdown("<h1 style='color:#1A237E;'>Asistente Virtual IA</h1>", unsafe_allow_html=True)
st.markdown("**Juzgado Civil y Comercial N° 9 – Departamento Judicial La Matanza**")

st.markdown("""
**Bienvenido/a al Asistente Virtual IA del Juzgado Civil y Comercial N° 9 – Departamento Judicial La Matanza.**  
A través de este asistente podrá evacuar las consultas más frecuentes.  
Seleccione una opción o escriba su duda.  
**Este servicio no implica ningún tipo de asesoramiento jurídico ni constituye una vía de contacto procesal.**
""")

# Opciones guiadas
st.subheader("📌 Consulta guiada:")
opciones = [
    "Requisitos para inscribir declaratoria de herederos",
    "Visualización de expediente como e-book",
    "Uso de TICs en audiencias (BLSG)",
    "Redes sociales del juzgado",
    "Encuestas de satisfacción",
    "Contacto con SADyP (Zoom)"
]
consulta = st.selectbox("Seleccione un tema:", opciones)

if consulta == opciones[0]:
    st.markdown("[Ver instructivo (OneDrive)](https://scbagovar-my.sharepoint.com/:b:/g/personal/rcsdellaporta_scba_gov_ar/EajRyx2zlyJPiYR8jb1h2sABvpMp61o4XFOe1PO8jE3XTw?e=PA4Wcxv)")
elif consulta == opciones[1]:
    st.markdown("[Guía paso a paso (OneDrive)](https://scbagovar-my.sharepoint.com/:b:/g/personal/rcsdellaporta_scba_gov_ar/EbL9wah_T_BEjdV8mPGDFQYBHdMX4V4xOhVtJK61Jf9dWQ?e=6FtcAG)")
elif consulta == opciones[2]:
    st.markdown("[Acceder a la guía (OneDrive)](https://scbagovar-my.sharepoint.com/:b:/g/personal/rcsdellaporta_scba_gov_ar/EZ8AXylbqQtPjMmQ_VBYJ9EB0Kkis9EPcmonM3ymYDVvTQ?e=WxhwAd)")
elif consulta == opciones[3]:
    st.markdown("Instagram: [@juzcivcom9lamatanza](https://www.instagram.com/juzcivcom9lamatanza/)")
elif consulta == opciones[4]:
    st.markdown("📋 [Encuesta para profesionales](https://docs.google.com/forms/d/e/1FAIpQLSelQUyg_3rns4lk5lEhupU311yxPwfZDXspvreS-GwYnxrSWw/viewform)  \n📋 [Encuesta general](https://docs.google.com/forms/d/e/1FAIpQLSd3ILJSn6i2F-WXT85Ap_-3WWSyYZ6ULjqFFKgt0fc0dmqxiQ/viewform)")
elif consulta == opciones[5]:
    st.markdown("🔗 [Ingresar a SADyP (Zoom - lun a vie de 9 a 13 hs)](https://us05web.zoom.us/j/4715183830?pwd=KzZlVUtjWnZlYlJyWmx2ZGFKTHdmZz09)")

# Carga de preguntas frecuentes
st.subheader("🔎 Consulta libre:")
with open("data/faq.json", "r", encoding="utf-8") as f:
    faqs = json.load(f)

pregunta_usuario = st.text_input("Escriba su consulta:")

if pregunta_usuario:
    preguntas = [faq["pregunta"] for faq in faqs]
    mejor_match = difflib.get_close_matches(pregunta_usuario, preguntas, n=1, cutoff=0.4)
    if mejor_match:
        for faq in faqs:
            if faq["pregunta"] == mejor_match[0]:
                st.success(f"**{faq['pregunta']}**\n\n{faq['respuesta']}")
                break
    else:
        st.warning("No encontramos coincidencias. Podés usar SADyP para una consulta personalizada.")
        st.markdown("🔗 [Ingresar a SADyP (Zoom)](https://us05web.zoom.us/j/4715183830?pwd=KzZlVUtjWnZlYlJyWmx2ZGFKTHdmZz09)")

# Footer
st.markdown("---")
st.markdown("<small>Asistente desarrollado por el Juzgado Civil y Comercial N° 9 – Depto. Judicial La Matanza.</small>", unsafe_allow_html=True)
