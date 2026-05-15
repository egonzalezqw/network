import streamlit as st
import time

# -----------------------------
# CONFIG
# -----------------------------
st.set_page_config(
    page_title="Cyber OT Defender",
    page_icon="🛡️",
    layout="wide"
)

# -----------------------------
# STATE SAFE INIT
# -----------------------------
DEFAULT_STATE = {
    "score": 0,
    "mission": 0,
    "finished": False
}

for k, v in DEFAULT_STATE.items():
    if k not in st.session_state:
        st.session_state[k] = v

# -----------------------------
# STYLE (CYBER UI)
# -----------------------------
st.markdown("""
<style>

.stApp {
    background-color: #070B14;
    color: #E6F1FF;
    font-family: Arial;
}

/* HUD PANEL */
.hud {
    background: #0B1220;
    padding: 15px;
    border-radius: 12px;
    border: 1px solid #1F2A44;
}

/* TITLES */
h1, h2, h3 {
    color: #38BDF8 !important;
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

/* ALERT BOX STYLE */
.alert {
    padding: 15px;
    border-radius: 10px;
    background: #1A1020;
    border-left: 5px solid red;
    color: #fff;
}

.success {
    padding: 15px;
    border-radius: 10px;
    background: #0D1F17;
    border-left: 5px solid #22C55E;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# HEADER
# -----------------------------
st.title("🛡️ CYBER OT DEFENDER")
st.caption("Industrial Security Simulation - Protect the Factory Network")

# -----------------------------
# HUD
# -----------------------------
with st.sidebar:
    st.markdown("## 🎮 SYSTEM HUD")

    st.markdown("### 📊 Score")
    st.metric("", st.session_state.score)

    st.markdown("### 🧭 Mission")
    st.metric("", st.session_state.mission)

    progress = min(st.session_state.mission / 4, 1)
    st.progress(progress)

    st.markdown("---")
    st.write("⚠️ OT Network Status: STABLE")

# -----------------------------
# MISSIONS DATA (ENGINE)
# -----------------------------
missions = [
    {
        "title": "🌐 Mission 1: Network Breach Analysis",
        "text": "A new OT network is being deployed in a factory. Identify the correct purpose of a network.",
        "question": "¿Cuál es el objetivo de una red?",
        "options": [
            "Apagar servidores",
            "Compartir información y recursos",
            "Romper sistemas OT"
        ],
        "answer": "Compartir información y recursos",
        "reward": 10
    },
    {
        "title": "🔀 Mission 2: VLAN Segmentation",
        "text": "Se detecta tráfico cruzado entre OT y invitados.",
        "question": "¿Qué tecnología separa redes correctamente?",
        "options": ["VLANs", "Bluetooth", "HDMI"],
        "answer": "VLANs",
        "reward": 20
    },
    {
        "title": "🚨 Mission 3: Attack Detected",
        "text": "Un dispositivo infectado intenta moverse lateralmente.",
        "question": "¿Cómo se contiene el ataque?",
        "options": ["Más cables", "Usar VLANs", "Reiniciar router"],
        "answer": "Usar VLANs",
        "reward": 25
    },
    {
        "title": "🏭 Mission 4: IT vs OT Control",
        "text": "Clasifica el entorno industrial.",
        "question": "¿Qué pertenece a OT?",
        "options": ["Servidor web", "PLC industrial", "Correo corporativo"],
        "answer": "PLC industrial",
        "reward": 30
    }
]

# -----------------------------
# GAME COMPLETED
# -----------------------------
if st.session_state.finished:

    st.markdown("## 🏆 MISSION COMPLETE")

    st.success(f"Puntaje final: {st.session_state.score}")

    if st.session_state.score >= 80:
        st.balloons()
        st.markdown("### 🏆 OT SECURITY ARCHITECT")
    elif st.session_state.score >= 50:
        st.markdown("### 🛡️ OT SECURITY OPERATOR")
    else:
        st.markdown("### ⚠️ NETWORK VULNERABLE")

    if st.button("🔄 Restart Simulation"):
        st.session_state.score = 0
        st.session_state.mission = 0
        st.session_state.finished = False
        st.rerun()

# -----------------------------
# GAME LOOP
# -----------------------------
else:

    m = missions[st.session_state.mission]

    st.markdown(f"## {m['title']}")
    st.write(m["text"])

    st.markdown("---")
    st.subheader(m["question"])

    choice = st.radio("Selecciona una opción:", m["options"])

    if st.button("🚀 Execute Action"):

        if choice == m["answer"]:
            st.markdown('<div class="success">✔ Access Granted - Correct Decision</div>', unsafe_allow_html=True)
            st.session_state.score += m["reward"]
        else:
            st.markdown('<div class="alert">✖ Security Mistake Detected</div>', unsafe_allow_html=True)

        time.sleep(0.8)

        st.session_state.mission += 1

        if st.session_state.mission >= len(missions):
            st.session_state.finished = True

        st.rerun()
