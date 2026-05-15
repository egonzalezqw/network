import streamlit as st
import random

# =================================================
# 📦 CONFIG INICIAL (OBLIGATORIO PRIMERO)
# =================================================
st.set_page_config(
    page_title="OT Factory Simulator",
    page_icon="🏭",
    layout="wide"
)

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
# 🏭 EVENTOS
# =================================================
EVENTS = [
    {
        "title": "⚠️ Acceso no autorizado en OT",
        "question": "¿Acción correcta?",
        "options": ["Bloquear dispositivo", "Ignorar", "Abrir acceso"],
        "correct": "Bloquear dispositivo",
        "impact_zone": "ot",
        "impact": 20
    },
    {
        "title": "🚨 Tráfico IT → OT sospechoso",
        "question": "¿Qué aplicar?",
        "options": ["Segmentación VLAN", "Más ancho de banda", "Desactivar firewall"],
        "correct": "Segmentación VLAN",
        "impact_zone": "it",
        "impact": 25
    },
    {
        "title": "🔥 Malware en OT detectado",
        "question": "¿Cómo contenerlo?",
        "options": ["Segmentación de red", "Red plana", "WiFi abierto"],
        "correct": "Segmentación de red",
        "impact_zone": "ot",
        "impact": 30
    },
    {
        "title": "⚠️ DMZ expuesta sin firewall",
        "question": "¿Mejor acción?",
        "options": ["Firewall perimetral", "IP pública directa", "Más usuarios"],
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
        st.session_state.health += 5

        if zone == "it":
            st.session_state.it_risk = max(0, st.session_state.it_risk - 10)
        elif zone == "ot":
            st.session_state.ot_risk = max(0, st.session_state.ot_risk - 10)
        elif zone == "dmz":
            st.session_state.dmz_risk = max(0, st.session_state.dmz_risk - 10)

        st.session_state.log.append(f"✔ OK: {event['title']}")
    else:
        st.session_state.health -= 15

        if zone == "it":
            st.session_state.it_risk += 15
        elif zone == "ot":
            st.session_state.ot_risk += 15
        elif zone == "dmz":
            st.session_state.dmz_risk += 15

        st.session_state.log.append(f"✖ FAIL: {event['title']}")

    # 🔒 HARDENING CRÍTICO
    st.session_state.health = max(0, min(100, st.session_state.health))


# =================================================
# 🏭 MAPA VISUAL
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
        st.metric("IT", status(st.session_state.it_risk))
        st.progress(min(st.session_state.it_risk / 100, 1.0))

    with col2:
        st.metric("DMZ", status(st.session_state.dmz_risk))
        st.progress(min(st.session_state.dmz_risk / 100, 1.0))

    with col3:
        st.metric("OT", status(st.session_state.ot_risk))
        st.progress(min(st.session_state.ot_risk / 100, 1.0))


# =================================================
# 🚀 INIT
# =================================================
init_state()

if st.session_state.event is None:
    st.session_state.event = get_event()

event = st.session_state.event


# =================================================
# 💀 FALLA CRÍTICA
# =================================================
if st.session_state.health <= 0:
    st.error("💀 FÁBRICA COMPROMETIDA")

    if st.button("🔄 Reiniciar"):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.rerun()


# =================================================
# 🎛️ SIDEBAR SOC (FIX + HUD PRO)
# =================================================
st.sidebar.title("🧭 Control SOC OT")

st.session_state.role = st.sidebar.selectbox(
    "Modo",
    ["Alumno", "Instructor"]
)

health = st.session_state.health
progress_value = max(0.0, min(health / 100, 1.0))

st.sidebar.metric("Health", f"{health}%")
st.sidebar.metric("Score", st.session_state.score)

if health > 70:
    st.sidebar.success("🟢 Sistema estable")
elif health > 40:
    st.sidebar.warning("🟡 Riesgo medio")
else:
    st.sidebar.error("🔴 Sistema degradado")

st.sidebar.progress(progress_value)

st.sidebar.markdown("---")
st.sidebar.write("📜 Logs")

for l in st.session_state.log[-6:]:
    st.sidebar.write("•", l)


# =================================================
# 🏭 SIMULADOR
# =================================================
render_map()

st.markdown("## 🚨 Evento Industrial")
st.error(event["title"])

choice = st.radio(event["question"], event["options"])

if st.button("⚡ Ejecutar acción"):

    apply_action(choice, event)
    st.session_state.event = get_event()
    st.rerun()


# =================================================
# 👨‍🏫 INSTRUCTOR MODE
# =================================================
if st.session_state.role == "Instructor":
    st.markdown("## 🧑‍🏫 Explicación OT")

    st.info("""
    - IT: usuarios corporativos
    - DMZ: zona intermedia
    - OT: sistemas industriales

    La segmentación evita movimiento lateral y ataques en cadena.
    """)
