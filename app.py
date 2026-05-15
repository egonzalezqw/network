import streamlit as st

# =================================================
# 🧠 ESTADO
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
# 🎮 PREGUNTAS (BÁSICAS / NO TÉCNICAS)
# =================================================
QUESTIONS = [
    {
        "q": "¿Para qué sirve una red en una empresa?",
        "options": ["Compartir información", "Apagar computadoras", "Romper sistemas"],
        "a": "Compartir información"
    },
    {
        "q": "¿Qué permite separar redes como oficina y producción?",
        "options": ["VLANs", "Mouse inalámbrico", "Bluetooth"],
        "a": "VLANs"
    },
    {
        "q": "¿Qué pasa si todo está en una sola red sin separación?",
        "options": ["Más seguridad", "Más riesgo", "Más orden"],
        "a": "Más riesgo"
    },
    {
        "q": "¿Qué es OT en una fábrica?",
        "options": ["Sistemas industriales", "Red social", "Videojuegos"],
        "a": "Sistemas industriales"
    },
    {
        "q": "¿Por qué se separa IT y OT?",
        "options": ["Para seguridad", "Para jugar mejor", "Para más cables"],
        "a": "Para seguridad"
    },
    {
        "q": "¿Qué ayuda a proteger una red?",
        "options": ["Buenas prácticas y segmentación", "Dejar todo abierto", "Quitar contraseñas"],
        "a": "Buenas prácticas y segmentación"
    }
]


# =================================================
# 🎭 MENSAJES DIVERTIDOS
# =================================================
def msg_correct():
    return [
        "😎 ¡Correcto! Hackeaste el conocimiento con éxito.",
        "🧠 ¡Bien hecho! Eres casi un ingeniero de redes Jedi.",
        "🚀 ¡Excelente! La red está orgullosa de ti."
    ]


def msg_wrong():
    return [
        "😂 No exactamente… pero la red sigue funcionando, respira tranquilo.",
        "🤔 Casi… pero esa respuesta tomó el camino equivocado en la autopista de datos.",
        "🙈 Ups… la red se confundió contigo, pero todo bien."
    ]


# =================================================
# 🎨 UI
# =================================================
st.set_page_config(page_title="Cyber OT Quiz", page_icon="🛡️", layout="wide")

st.title("🛡️ Cyber OT Redes - Quiz Básico")
st.caption("Aprende redes, VLANs y OT de forma sencilla y divertida")

init_state()

q = QUESTIONS[st.session_state.index]

st.sidebar.metric("Puntaje", st.session_state.score)
st.sidebar.progress(st.session_state.index / len(QUESTIONS))


# =================================================
# 🧠 FINAL DEL JUEGO
# =================================================
if st.session_state.finished:

    st.success("🎉 Quiz terminado")

    st.metric("Resultado final", st.session_state.score)

    if st.session_state.score >= 5:
        st.balloons()
        st.markdown("🏆 ¡Buen trabajo! Entiendes lo básico de redes OT.")
    else:
        st.markdown("🙂 ¡Buen intento! La red necesita más práctica contigo.")

    if st.button("🔄 Reiniciar"):
        st.session_state.score = 0
        st.session_state.index = 0
        st.session_state.finished = False
        st.rerun()

# =================================================
# 🎮 JUEGO
# =================================================
else:

    st.subheader(q["q"])

    choice = st.radio("Selecciona una opción:", q["options"])

    if st.button("Responder"):

        if choice == q["a"]:
            import random
            st.success(random.choice(msg_correct()))
            st.session_state.score += 1
        else:
            import random
            st.warning(random.choice(msg_wrong()))

        st.session_state.index += 1

        if st.session_state.index >= len(QUESTIONS):
            st.session_state.finished = True

        st.rerun()
