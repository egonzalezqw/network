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
# 😄 FEEDBACK
# =================================================
def msg_correct():
    return [
        "😎 Red estable. Buen trabajo.",
        "🚀 Decisión correcta en arquitectura de red.",
        "🧠 Nivel OT en progreso positivo."
    ]


def msg_wrong():
    return [
        "⚠️ La red no está feliz con esa decisión.",
        "🤔 Error de diseño, pero recuperable.",
        "😂 Casi… pero la red se desvió un poco."
    ]


# =================================================
# 🎨 UI STYLE
# =================================================
st.set_page_config(
    page_title="Cyber OT Interactive Quiz",
    page_icon="🛡️",
    layout="wide"
)

st.markdown("""
<style>

.stApp {
    background-color: #050816;
    color: #E6F1FF;
}

/* TITLES */
h1, h2, h3 {
    color: #38BDF8 !important;
}

/* CARD STYLE */
.card {
    background: #0B1220;
    padding: 18px;
    border-radius: 14px;
    border: 1px solid #1F2A44;
    margin-bottom: 15px;
}

/* BUTTONS */
.stButton>button {
    width: 100%;
    border-radius: 10px;
    height: 3em;
    font-weight: bold;
    background-color: #1F6FEB;
    color: white;
}

/* PROGRESS */
.stProgress > div > div > div {
    background-color: #38BDF8;
}

</style>
""", unsafe_allow_html=True)


# =================================================
# INIT
# =================================================
init_state()

# progreso seguro
progress = st.session_state.index / len(QUESTIONS)

# =================================================
# SIDEBAR (DASHBOARD)
# =================================================
st.sidebar.markdown("## 🛡️ OT CONTROL PANEL")
st.sidebar.metric("Score", st.session_state.score)
st.sidebar.progress(progress)
st.sidebar.write(f"Pregunta {st.session_state.index + 1} / {len(QUESTIONS)}")


# =================================================
# FIN DEL JUEGO
# =================================================
if st.session_state.index >= len(QUESTIONS):
    st.session_state.finished = True


if st.session_state.finished:

    st.markdown("## 🏁 MISIÓN COMPLETADA")

    st.markdown(f"""
    <div class="card">
    <h3>🎯 Resultado Final</h3>
    <p>Puntaje: {st.session_state.score}</p>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.score >= 5:
        st.success("🏆 Excelente comprensión de redes OT")
        st.balloons()
    else:
        st.info("🙂 Buen intento, sigue practicando redes")

    if st.button("🔄 Reiniciar simulación"):
        st.session_state.score = 0
        st.session_state.index = 0
        st.session_state.finished = False
        st.rerun()

# =================================================
# 🎮 JUEGO INTERACTIVO
# =================================================
else:

    q = QUESTIONS[st.session_state.index]

    # EVENT CARD
    st.markdown(f"""
    <div class="card">
        <h3>🌐 Evento de Red</h3>
        <p>{q["q"]}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 🧠 Toma una decisión")

    col1, col2 = st.columns([2, 1])

    with col1:
        choice = st.radio("Selecciona la mejor opción:", q["options"])

        if st.button("⚡ Ejecutar acción de red"):

            if choice == q["a"]:
                st.success(random.choice(msg_correct()))
                st.session_state.score += 1
            else:
                st.warning(random.choice(msg_wrong()))

            st.session_state.index += 1
            st.rerun()

    with col2:
        st.markdown("""
        <div class="card">
            <h4>🧭 Estado del sistema</h4>
            <p>Simulación OT activa</p>
            <p>Red: Estable</p>
        </div>
        """, unsafe_allow_html=True)
