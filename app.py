import streamlit as st
import random

# =================================================
# 🧠 STATE ENGINE
# =================================================
def init_state():
    defaults = {
        "role": "Alumno",
        "health": 100,
        "score": 0,
        "event": None,
        "log": [],
        "it_risk": 0,
        "ot_risk": 0,
        "dmz_risk": 0
    }

    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


# =================================================
# 🏭 EVENTOS OT / IT
# =================================================
EVENTS = [
    {
        "title": "⚠️ Acceso no autorizado detectado en OT",
        "question": "¿Qué acción es más segura?",
        "options": ["Bloquear dispositivo", "Ignorar", "Abrir acceso"],
        "correct": "Bloquear dispositivo",
        "impact_zone": "ot",
        "impact": 20
    },
    {
        "title": "🚨 Tráfico sospechoso IT → OT",
        "question": "¿Qué solución reduce el riesgo?",
        "options": ["Segmentación VLAN", "Más ancho de banda", "Desactivar firewall"],
        "correct": "Segmentación VLAN",
        "impact_zone": "it",
        "impact": 25
    },
    {
        "title": "🔥 Malware propagándose en red OT",
        "question": "¿Qué ayuda a contenerlo?",
        "options": ["Segmentación de red", "Red plana", "WiFi abierto"],
        "correct": "Segmentación de red",
        "impact_zone": "ot",
        "impact": 30
    },
    {
        "title": "⚠️ DMZ expuesta sin firewall",
        "question": "¿Qué mejora la seguridad?",
        "options": ["Firewall perimetral", "Más usuarios", "IP pública directa"],
        "correct": "Firewall perimetral",
        "impact_zone": "dmz",
        "impact": 25
    }
]


def get_event():
    return random.choice(EVENTS)


# =================================================
# ⚙️ ENGINE DE IMPACTO
# =================================================
def apply_action(choice, event):

    zone = event["impact_zone"]

    if choice == event["correct"]:
        st.session_state.score += event["impact"]
        st.session_state.health = min(100, st.session_state.health + 5)

        if zone == "it":
            st.session_state.it_risk = max(0, st.session_state.it_risk - 10)
        elif zone == "ot":
            st.session_state.ot_risk = max(0, st.session_state.ot_risk - 10)
        elif zone == "dmz":
            st.session_state.dmz_risk = max(0, st.session_state.dmz_risk - 10)

        st.session_state.log.append(f"✔ OK: {event['title']}")
        return True

    else:
        st.session_state.health -= 15

        if zone == "it":
            st.session_state.it_risk += 15
        elif zone == "ot":
            st.session_state.ot_risk += 15
        elif zone == "dmz":
            st.session_state.dmz_risk += 15

        st.session_state.log.append(f"✖ FAIL: {event['title']}")
        return False


# =================================================
# 🏭 MAPA VISUAL MEJORADO
# =================================================
def render_map():

    def status(val):
        if val < 20:
            return "🟢 OK"
        elif val < 50:
            return "🟡 RIESGO"
        else:
            return "🔴 CRÍTICO"

    st.markdown("## 🏭 Estado de la Fábrica OT")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("IT NETWORK", status(st.session_state.it_risk))
        st.progress(min(st.session_state.it_risk / 100, 1))

    with col2:
        st.metric("DMZ", status(st.session_state.dmz_risk))
        st.progress(min(st.session_state.dmz_risk / 100, 1))

    with col3:
        st.metric("OT NETWORK", status(st.session_state.ot_risk))
        st.progress(min(st.session_state.ot_risk / 100, 1))


# =================================================
# 🎨 UI
# =================================================
st.set_page_config(page_title="OT Factory Simulator", layout="wide")

st.title("🏭🛡️ OT Factory Simulator - Digital Twin")

init_state()

# =================================================
# 🎛️ CONTROL PANEL
# =================================================
st.sidebar.title("🧭 Control SOC")

st.session_state.role = st.sidebar.selectbox(
    "Modo",
    ["Alumno", "Instructor"]
)

st.sidebar.metric("Health", st.session_state.health)
st.sidebar.metric("Score", st.session_state.score)

st.sidebar.progress(st.session_state.health / 100)

st.sidebar.markdown("### 📜 Logs")
for l in st.session_state.log[-6:]:
    st.sidebar.write("•", l)


# =================================================
# EVENT INIT
# =================================================
if st.session_state.event is None:
    st.session_state.event = get_event()

event = st.session_state.event


# =================================================
# 💀 FAILURE STATE
# =================================================
if st.session_state.health <= 0:
    st.error("💀 FÁBRICA EN ESTADO CRÍTICO")

    if st.button("🔄 Reiniciar"):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.rerun()


# =================================================
# 🏭 MAIN SIMULATOR
# =================================================
else:

    render_map()

    st.markdown("## 🚨 Evento Industrial")
    st.error(event["title"])

    st.markdown("### 🧠 Decisión del operador")

    choice = st.radio(event["question"], event["options"])

    if st.button("⚡ Ejecutar acción"):

        apply_action(choice, event)
        st.session_state.event = get_event()
        st.rerun()


# =================================================
# 👨‍🏫 INSTRUCTOR MODE
# =================================================
if st.session_state.role == "Instructor":
    st.markdown("## 🧑‍🏫 Explicación")

    st.info("""
    - IT: usuarios corporativos
    - DMZ: servicios intermedios
    - OT: sistemas industriales críticos

    La segmentación reduce movimiento lateral y riesgo de malware.
    """)
