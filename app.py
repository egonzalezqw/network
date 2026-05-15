import streamlit as st
import random

# =================================================
# 🧠 STATE ENGINE (SIEMPRE CONSISTENTE)
# =================================================
def init_state():
    defaults = {
        "score": 0,
        "health": 100,
        "incident_id": None,
        "logs": [],
        "running": True
    }

    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


# =================================================
# 🚨 INCIDENT ENGINE (SIN STRINGS FRÁGILES)
# =================================================
INCIDENTS = [
    {
        "id": "malware_hmi",
        "title": "Malware detected in HMI",
        "options": ["Isolate OT VLAN", "Ignore alert", "Reboot PLC"],
        "correct": "Isolate OT VLAN",
        "impact": 20
    },
    {
        "id": "unauth_device",
        "title": "Unauthorized device detected",
        "options": ["Block MAC address", "Disable firewall", "Open port 80"],
        "correct": "Block MAC address",
        "impact": 20
    },
    {
        "id": "lateral_movement",
        "title": "Lateral movement detected in OT network",
        "options": ["Enable segmentation", "Increase bandwidth", "Disable logs"],
        "correct": "Enable segmentation",
        "impact": 25
    }
]


def get_incident():
    return random.choice(INCIDENTS)


# =================================================
# ⚙️ ACTION ENGINE
# =================================================
def apply_action(selected, incident):

    if selected == incident["correct"]:
        st.session_state.score += incident["impact"]
        st.session_state.health = min(100, st.session_state.health + 5)
        st.session_state.logs.append(f"✔ Correct response: {incident['title']}")
        return True
    else:
        st.session_state.health -= 10
        st.session_state.logs.append(f"✖ Wrong response: {incident['title']}")
        return False


def next_incident():
    st.session_state.incident_id = get_incident()


# =================================================
# 🎨 UI ENGINE
# =================================================
def render_hud():

    st.sidebar.title("🛡️ SOC CONTROL PANEL")
    st.sidebar.metric("Score", st.session_state.score)
    st.sidebar.metric("Health", st.session_state.health)

    st.sidebar.progress(st.session_state.health / 100)

    st.sidebar.markdown("---")
    st.sidebar.write("📜 Logs")

    for log in st.session_state.logs[-6:]:
        st.sidebar.write("•", log)


def render_incident(incident):

    st.title("🛡️ CYBER OT SOC SIMULATOR")

    st.markdown("## 🚨 Active Incident")
    st.error(incident["title"])

    choice = st.radio("Select response:", incident["options"])

    if st.button("Execute Response"):

        result = apply_action(choice, incident)

        if result:
            st.success("Correct mitigation applied")
        else:
            st.warning("Incorrect action taken")

        next_incident()
        st.rerun()


# =================================================
# 🧠 SAFETY CHECK (NO BLACK SCREEN EVER)
# =================================================
def safe_state():
    if st.session_state.health <= 0:
        st.session_state.running = False

    if st.session_state.incident_id is None:
        next_incident()


# =================================================
# 🚀 APP ENTRY POINT
# =================================================
init_state()
safe_state()
render_hud()

if not st.session_state.running:
    st.error("💀 SYSTEM COMPROMISED")
    st.write("Final Score:", st.session_state.score)

    if st.button("Restart Simulation"):
        for k in st.session_state.keys():
            del st.session_state[k]
        st.rerun()

else:
    incident = st.session_state.incident_id
    render_incident(incident)
