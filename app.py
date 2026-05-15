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
# 🎮 PREGUNTAS (MISMAS)
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
        "😎 ¡Correcto! La red está orgullosa de ti.",
        "🚀 ¡Bien hecho! Nivel ingeniero activado.",
        "🧠 ¡Excelente! Esto ya suena a redes OT reales."
    ]


def msg_wrong():
    return [
        "😂 Ups… la red sobrevivió, pero estuvo cerca del caos.",
        "🤔 Casi… pero esa ruta no es la ideal.",
        "🙈 No del todo… la red necesita un café y otro intento."
    ]


# =================================================
# 🎨 ESTÉTICA CYBER OT
# =================================================
st.set_page_config(
    page_title="Cyber OT Quiz",
    page_icon="🛡️",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background-color: #070B14;
    color: #E6F1FF;
}

h1, h2, h3, p, label {
    color: #E6F1FF !important;
}

.block-container {
    padding-top: 2rem;
}

.stButton>button {
    width: 100%;
    border-radius: 10px;
    height: 3em;
    font-weight: bold;
    background-color: #1F6FEB;
    color: white;
}

.stProgress > div > div > div {
    background-color: #38BDF8;
}
</style>
""", unsafe_allow_html=True)


st.title("🛡️ Cyber OT Redes - Quiz Básico")
st.caption("Simulación educativa de redes, VLANs e IT/OT")

init_state()

# =================================================
# 🔐 CONTROL SEGURO
# =================================================
if st.session_state.index >= len(QUESTIONS):
    st.session_state.finished = True


# =================================================
# 🏁 FINAL
# =================================================
if st.session_state.finished:

    st.success("🎉 Quiz completado")

    st.metric("Puntaje final", st.session_state.score)

    if st.session_state.score >= 5:
        st.balloons()
        st.markdown("🏆 ¡Buen trabajo! Entiendes lo básico de redes OT.")
    else:
        st.markdown("🙂 Buen intento, sigue practicando redes.")

    if st.button("🔄 Reiniciar"):
        st.session_state.score = 0
        st.session_state.index = 0
        st.session_state.finished = False
        st.rerun()

# =================================================
# 🎮 JUEGO
# =================================================
else:

    q = QUESTIONS[st.session_state.index]

    st.sidebar.title("🛡️ PANEL OT")
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

        st.session_state.index += 1

        if st.session_state.index >= len(QUESTIONS):
            st.session_state.finished = True

        st.rerun()
