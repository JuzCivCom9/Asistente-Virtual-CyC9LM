import streamlit as st
from google import genai
from pathlib import Path
import json

# ?? Configuración de página ??????????????????????????????????????????????????
st.set_page_config(
    page_title="Asistente Virtual IA ? Juzgado Civil y Comercial N° 9",
    page_icon="??",
    layout="centered",
)

# ?? Estilos visuales ?????????????????????????????????????????????????????????
st.markdown("""
<style>
    .stChatMessage { border-radius: 12px; }
    .disclaimer {
        background: #FFF8E1;
        border-left: 4px solid #F9A825;
        padding: 10px 14px;
        border-radius: 6px;
        font-size: 0.82rem;
        color: #5D4037;
        margin-bottom: 1rem;
    }
    .quick-btn-label {
        font-size: 0.85rem;
        color: #555;
        margin-bottom: 4px;
    }
</style>
""", unsafe_allow_html=True)

# ?? Logo y encabezado ?????????????????????????????????????????????????????????
logo_path = Path("assets/logo-juzgado9.png")
if logo_path.exists():
    st.image(str(logo_path), width=110)

st.markdown("<h2 style='color:#1A237E; margin-bottom:0;'>Asistente Virtual IA</h2>", unsafe_allow_html=True)
st.markdown("**Juzgado Civil y Comercial N° 9 ? Departamento Judicial La Matanza**")

st.markdown("""
<div class="disclaimer">
?? <strong>Aviso importante:</strong> Este servicio orienta sobre trámites y consultas frecuentes del juzgado.
No constituye asesoramiento jurídico ni es una vía de contacto procesal válida.
</div>
""", unsafe_allow_html=True)

# ?? Cargar FAQ como contexto ??????????????????????????????????????????????????
@st.cache_data
def cargar_faq():
    faq_path = Path("data/faq.json")
    if faq_path.exists():
        with open(faq_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

faqs = cargar_faq()
faq_texto = "\n".join(
    f"P: {item['pregunta']}\nR: {item['respuesta']}" for item in faqs
)

# ?? System prompt ?????????????????????????????????????????????????????????????
SYSTEM_PROMPT = f"""Sos el asistente virtual oficial del Juzgado Civil y Comercial N° 9 del Departamento Judicial La Matanza, Provincia de Buenos Aires, Argentina.
Tu función es responder consultas sobre trámites, procedimientos y servicios del juzgado de manera clara, amable y precisa.

INFORMACIÓN DEL JUZGADO:
- Titular: Dr. Rodrigo C. Suárez Della Porta
- Secretaria: Dra. María Daniela Marino
- Dirección: Av. Comisionado Indart 2147/57, San Justo, Buenos Aires
- Horario: Lunes a viernes de 8:00 a 14:00 hs
- Instagram: @juzcivcom9lamatanza
- SADyP (atención por Zoom): lunes a viernes de 9 a 13 hs ? https://us05web.zoom.us/j/4715183830?pwd=KzZlVUtjWnZlYlJyWmx2ZGFKTHdmZz09

SERVICIOS DISPONIBLES:
- Declaratoria de herederos (instructivo): https://scbagovar-my.sharepoint.com/:b:/g/personal/rcsdellaporta_scba_gov_ar/EajRyx2zlyJPiYR8jb1h2sABvpMp61o4XFOe1PO8jE3XTw?e=PA4Wcxv
- Expediente como e-book (guía): https://scbagovar-my.sharepoint.com/:b:/g/personal/rcsdellaporta_scba_gov_ar/EbL9wah_T_BEjdV8mPGDFQYBHdMX4V4xOhVtJK61Jf9dWQ?e=6FtcAG
- TICs en audiencias BLSG: https://scbagovar-my.sharepoint.com/:b:/g/personal/rcsdellaporta_scba_gov_ar/EZ8AXylbqQtPjMmQ_VBYJ9EB0Kkis9EPcmonM3ymYDVvTQ?e=WxhwAd
- Encuesta para profesionales: https://docs.google.com/forms/d/e/1FAIpQLSelQUyg_3rns4lk5lEhupU311yxPwfZDXspvreS-GwYnxrSWw/viewform
- Encuesta general: https://docs.google.com/forms/d/e/1FAIpQLSd3ILJSn6i2F-WXT85Ap_-3WWSyYZ6ULjqFFKgt0fc0dmqxiQ/viewform
- Subastas judiciales: https://www.scba.gov.ar/paginas.asp?id=50473
- Valor del IUS: https://www.scba.gov.ar/paginas.asp?id=41320
- Tasa de Justicia: https://www.scba.gov.ar/paginas.asp?id=46791
- Domicilio electrónico: https://www.scba.gov.ar/paginas.asp?id=46690
- Códigos de materias: https://www.scba.gov.ar/paginas.asp?id=41329

PREGUNTAS FRECUENTES DEL JUZGADO:
{faq_texto}

INSTRUCCIONES:
1. Respondé en español rioplatense, con tono formal pero cercano.
2. Si la consulta tiene respuesta en los datos anteriores, respondé con precisión e incluí el enlace relevante cuando corresponda.
3. Si la consulta es ambigua, pedí una aclaración breve.
4. Si la consulta está claramente fuera del ámbito del juzgado (ej: juzgado federal, penal, etc.), indicalo amablemente y orientá al usuario.
5. Nunca brindes asesoramiento jurídico ni opiniones sobre el fondo de un caso.
6. Mantené respuestas concisas (máximo 4-5 oraciones salvo que sea necesario más detalle).
7. Al final de cada respuesta que involucre un trámite complejo, ofrecé la opción de contactar por SADyP.
"""

# ?? Inicializar historial de chat ?????????????????????????????????????????????
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({
        "role": "assistant",
        "content": "¡Hola! Soy el asistente virtual del **Juzgado Civil y Comercial N° 9 ? La Matanza**. ¿En qué puedo ayudarte hoy? Podés preguntarme sobre expedientes, sucesiones, audiencias, trámites y más.",
    })

# ?? Botones de consulta rápida ????????????????????????????????????????????????
st.markdown('<p class="quick-btn-label">?? Consultas frecuentes:</p>', unsafe_allow_html=True)

consultas_rapidas = [
    "?? Iniciar una sucesión",
    "?? Estado de expediente",
    "?? Horarios y contacto",
    "?? Audiencia virtual",
    "?? Tasa de Justicia",
    "?? Hablar con SADyP",
]

cols = st.columns(3)
for i, consulta in enumerate(consultas_rapidas):
    if cols[i % 3].button(consulta, use_container_width=True):
        st.session_state.messages.append({"role": "user", "content": consulta})
        st.rerun()

st.divider()

# ?? Mostrar historial del chat ????????????????????????????????????????????????
for msg in st.session_state.messages:
   with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ?? Input del usuario ?????????????????????????????????????????????????????????
if prompt := st.chat_input("Escribí tu consulta..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

# ?? Llamada a Gemini (nuevo SDK google-genai) ?????????????????????????????????
ultimo_mensaje = st.session_state.messages[-1] if st.session_state.messages else None

if ultimo_mensaje and ultimo_mensaje["role"] == "user":
    with st.chat_message("assistant"):
        with st.spinner("Consultando..."):
            try:
                client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

                # Armar historial completo como texto para el modelo
                historial_texto = ""
                for m in st.session_state.messages[1:]:  # excluye mensaje de bienvenida
                    rol = "Usuario" if m["role"] == "user" else "Asistente"
                    historial_texto += f"{rol}: {m['content']}\n"

                prompt_completo = f"{SYSTEM_PROMPT}\n\nCONVERSACIÓN:\n{historial_texto}\nAsistente:"

                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt_completo,
                )
                respuesta = response.text

            except Exception as e:
                respuesta = (
                    f"?? Ocurrió un error al procesar tu consulta. "
                    f"Por favor intentá nuevamente o contactanos por "
                    f"[SADyP (Zoom)](https://us05web.zoom.us/j/4715183830?pwd=KzZlVUtjWnZlYlJyWmx2ZGFKTHdmZz09).\n\n"
                    f"*Error técnico: {str(e)}*"
                )

        st.markdown(respuesta)
        st.session_state.messages.append({"role": "assistant", "content": respuesta})

# ?? Botón para limpiar conversación ??????????????????????????????????????????
if len(st.session_state.messages) > 1:
    if st.button("??? Nueva consulta", help="Reiniciar la conversación"):
        st.session_state.messages = [{
            "role": "assistant",
            "content": "¡Hola! Soy el asistente virtual del **Juzgado Civil y Comercial N° 9 ? La Matanza**. ¿En qué puedo ayudarte hoy?",
        }]
        st.rerun()

# ?? Footer ????????????????????????????????????????????????????????????????????
st.markdown("---")
st.markdown(
    "<small>Asistente desarrollado por el Juzgado Civil y Comercial N° 9 ? Depto. Judicial La Matanza. "
    "[@juzcivcom9lamatanza](https://www.instagram.com/juzcivcom9lamatanza/)</small>",
    unsafe_allow_html=True,
)
