import streamlit as st
import random

# =================================================
# 🧠 STATE ENGINE
# =================================================
def init_state():
    defaults = {
        "score": 0,
        "health": 100,
        "logs": [],
        "incident": None,
        "running": True
    }

    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


# =================================================
# 🌐 INCIDENTS (REDES / VLAN / OT)
# =================================================
INCIDENTS = [
    {
        "id": "vlan_misconfig",
        "title": "⚠️ VLAN Misconfiguration detected between IT and OT",
        "question": "¿Qué solución es correcta para separar tráfico IT y OT?",
        "options": ["Routing dinámico", "VLANs", "DNS interno compartido"],
        "correct": "VLANs",
        "impact": 20
    },
    {
        "id": "broadcast_domain",
        "title": "📡 Excessive broadcast traffic in production network",
        "question": "¿Qué reduce dominios de broadcast?",
        "options": ["Switching L2 sin VLAN", "Segmentación VLAN", "Aumentar cables"],
        "correct": "Segmentación VLAN",
        "impact": 20
    },
    {
        "id": "ot_exposure",
        "title": "🏭 OT network exposed to corporate users",
        "question": "¿Cómo aislar correctamente la red OT?",
        "options": ["Firewall + VLAN segmentation", "WiFi abierto", "Public IP directo"],
        "correct": "Firewall + VLAN segmentation",
        "impact": 25
    },
    {
        "id": "flat_network",
        "title": "🔴 Flat network detected (no segmentation)",
        "question": "¿Cuál es el mayor riesgo de una red plana?",
        "options": ["Alta latencia", "Movimiento lateral fácil", "Más velocidad"],
        "correct": "Movimiento lateral fácil",
        "impact": 25
    },
    {
        "id": "industrial_protocol_risk",
        "title": "⚙️ Unsecured industrial protocol detected (OT)",
        "question": "¿Qué mejora la seguridad en OT networks?",
        "options": [
            "Segmentación + firewalls industriales",
            "Más usuarios",
            "DHCP abierto"
        ],
        "correct": "Segmentación + firewalls industriales",
        "impact": 30
    }
]


# =================================================
# 😄 FEEDBACK DIVERTIDO
# =================================================
def msg_correct():
    return [
        "😎 ¡Perfecto! Estás configurando la red como un pro.",
        "🧠 Correcto! El tráfico OT está bajo control, bien hecho.",
        "🚀 ¡Excelente! La red está orgullosa de ti.",
        "🔥 Buen trabajo, esa VLAN está feliz ahora mismo."
    ]


def msg_wrong():
    return [
        "😅 No del todo… pero la red aún no colapsa, tranquilo.",
        "🤔 Ups… esa configuración necesita un poco más de cariño.",
        "🙈 Casi… pero la red está mirando con preocupación.",
        "⚠️ No es la mejor decisión… pero se puede mejorar bastante."
    ]


# =================================================
# ⚙️ ENGINE
# =================================================
def get_incident():
    return random.choice(INCIDENTS)


def apply_action(choice, incident):

    if choice == incident["correct"]:
        st.session_state.score += incident["impact"]
        st.session_state.health = min(100, st.session_state.health + 5)

        st.session_state.logs.append(
            f"✔ Correcto: {incident['title']}"
        )

        st.success(random.choice(msg_correct()))
        return True

    else:
        st.session_state.health -= 10

        st.session_state.logs.append(
            f"✖ Incorrecto: {incident['title']}"
        )

        st.warning(random.choice(msg_wrong()))
        return False


def next_incident():
    st.session_state.incident = get_incident()


# =================================================
# 🎨 UI
# =================================================
def render_hud():
    st.sidebar.title("🛡️ OT NETWORK HUD")

    st.sidebar.metric("Score", st.session_state.score)
    st.sidebar.metric("Health", st.session_state.health)

    st.sidebar.progress(st.session_state.health / 100)

    st.sidebar.markdown("---")
    st.sidebar.write("📜 Network Logs")

    for log in st.session_state.logs[-6:]:
        st.sidebar.write("•", log)


def render_incident(incident):

    st.title("🌐 OT NETWORK TRAINING SIMULATOR")

    st.markdown("## 🚨 Network Event")
    st.error(incident["title"])

    st.markdown("### 🧠 Concept Question")
    st.write(incident["question"])

    choice = st.radio("Select answer:", incident["options"])

    if st.button("Apply Network Action"):

        apply_action(choice, incident)

        next_incident()
        st.rerun()


def game_over():
    st.error("💀 NETWORK CRITICAL FAILURE")
    st.write("Final Score:", st.session_state.score)

    if st.button("Restart"):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.rerun()


# =================================================
# 🚀 APP
# =================================================
init_state()

if st.session_state.incident is None:
    next_incident()

render_hud()

if st.session_state.health <= 0:
    game_over()
else:
    render_incident(st.session_state.incident)
