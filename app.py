import streamlit as st
import random

# =================================================
# 🧠 ESTADO SEGURO
# =================================================
def init_state():
    defaults = {
        "score": 0,
        "index": 0,
        "finished": False
    }

    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


# =================================================
# 🎮 PREGUNTAS (6 FIJAS)
# =================================================
QUESTIONS = [
    {
        "q": "¿Para qué sirve una red en una empresa?",
        "options": ["Compartir información", "Apagar computadoras", "Romper sistemas"],
        "a": "Compartir información"
    },
    {
        "q": "¿Qué permite separar redes como oficina y producción?",
        "options": ["VLANs", "Bluetooth", "HDMI"],
        "a": "VLANs"
    },
    {
        "q": "¿Qué pasa si no hay separación de redes?",
        "options": ["Más seguridad", "Más riesgo", "Más velocidad"],
        "a": "Más riesgo"
    },
    {
        "q": "¿Qué es OT en una fábrica?",
        "options": ["Sistemas industriales", "Red social", "Juego"],
        "a": "Sistemas industriales"
    },
    {
        "q": "¿Por qué se separa IT y OT?",
        "options": ["Para seguridad", "Para jugar", "Para decorar la red"],
        "a": "Para seguridad"
    },
    {
        "q": "¿Qué ayuda a proteger una red?",
        "options": ["Segmentación y buenas prácticas", "Dejar todo abierto", "Quitar contraseñas"],
        "a": "Segmentación y buenas prácticas"
    }
]


# =================================================
# 😄 MENSAJES DIVERTIDOS
# =================================================
def msg_correct():
    return [
        "😎 ¡Correcto! La red te aplaude en silencio.",
        "🚀 ¡Bien! Nivel de ingeniero en progreso.",
        "🧠 ¡Excelente! Casi eres administrador de redes OT."
    ]


def msg_wrong():
    return [
        "😂 Ups… la red se confundió, pero sigue viva.",
        "🤔 Casi… pero esa ruta no es la correcta.",
        "🙈 No exactamente… la red sobrevivirá a tu intento."
    ]


# =================================================
# CONFIG STREAMLIT
# =================================================
st.set_page_config(
    page_title="Cyber OT Quiz",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ Cyber OT Redes - Quiz Básico")
st.caption("Aprende redes, VLANs e IT/OT de forma simple")

init_state()

# =================================================
# 🔐 CONTROL DE FIN SEGURO (EVITA INDEX ERROR)
# =================================================
if st.session_state.index >= len(QUESTIONS):
    st.session_state.finished = True


# =================================================
# 🏁 PANTALLA FINAL
# =================================================
if st.session_state.finished:

    st.success("🎉 Quiz terminado")

    st.metric("Puntaje final", st.session_state.score)

    if st.session_state.score >= 5:
        st.balloons()
        st.markdown("🏆 ¡Buen trabajo! Entiendes lo básico de redes OT.")
    else:
        st.markdown("🙂 Buen intento. Sigue practicando redes.")

    if st.button("🔄 Reiniciar"):
        st.session_state.score = 0
        st.session_state.index = 0
        st.session_state.finished = False
        st.rerun()

# =================================================
# 🎮 JUEGO PRINCIPAL
# =================================================
else:

    q = QUESTIONS[st.session_state.index]

    st.sidebar.metric("Puntaje", st.session_state.score)
    st.sidebar.progress(st.session_state.index / len(QUESTIONS))

    st.subheader(q["q"])

    choice = st.radio("Selecciona una opción:", q["options"])

    if st.button("Responder"):

        if choice == q["a"]:
            st.success(random.choice(msg_correct()))
            st.session_state.score += 1
        else:
            st.warning(random.choice(msg_wrong()))

        # avanzar seguro sin romper índice
        st.session_state.index += 1

        if st.session_state.index >= len(QUESTIONS):
            st.session_state.finished = True

        st.rerun()
