import streamlit as st
import random
import time

# -----------------------------
# CONFIG
# -----------------------------
st.set_page_config(
    page_title="Cyber OT Range",
    page_icon="🛡️",
    layout="wide"
)

# -----------------------------
# STATE INIT
# -----------------------------
if "score" not in st.session_state:
    st.session_state.score = 0

if "health" not in st.session_state:
    st.session_state.health = 100

if "alerts" not in st.session_state:
    st.session_state.alerts = []

if "incident" not in st.session_state:
    st.session_state.incident = None

# -----------------------------
# STYLE
# -----------------------------
st.markdown("""
<style>
.stApp {
    background-color: #050A18;
    color: #E6F1FF;
}

.panel {
    background: #0B1220;
    padding: 15px;
    border-radius: 12px;
    border: 1px solid #1F2A44;
}

.alert {
    background: #2A0F14;
    border-left: 5px solid red;
    padding: 10px;
    border-radius: 10px;
}

.success {
    background: #0F2A1C;
    border-left: 5px solid #22C55E;
    padding: 10px;
    border-radius: 10px;
}

.warning {
    background: #2A2410;
    border-left: 5px solid #FACC15;
    padding: 10px;
    border-radius: 10px;
}

.stButton>button {
    width: 100%;
    border-radius: 10px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# HEADER
# -----------------------------
st.title("🛡️ CYBER OT DEFENDER - LIVE RANGE")
st.caption("Industrial Network Security Simulation (Real-Time Events)")

# -----------------------------
# SIDEBAR HUD
# -----------------------------
with st.sidebar:
    st.markdown("## 🎮 SYSTEM STATUS")

    st.metric("Score", st.session_state.score)
    st.metric("Health", st.session_state.health)

    st.progress(st.session_state.health / 100)

    st.markdown("---")
    st.write("⚠️ OT Network: MONITORED")

# -----------------------------
# INCIDENT GENERATOR
# -----------------------------
incidents = [
    {
        "title": "🚨 Malware detected in HMI",
        "damage": 15,
        "fix": "Isolate VLAN OT"
    },
    {
        "title": "⚠️ Unauthorized device connected",
        "damage": 10,
        "fix": "Block MAC address"
    },
    {
        "title": "🔥 Lateral movement detected",
        "damage": 20,
        "fix": "Enable segmentation"
    }
]

if st.session_state.incident is None:
    st.session_state.incident = random.choice(incidents)

incident = st.session_state.incident

# -----------------------------
# MAIN UI GRID
# -----------------------------
col1, col2 = st.columns([2, 1])

# -----------------------------
# NETWORK MAP (SIMULATED)
# -----------------------------
with col1:

    st.markdown("## 🌐 OT Network Map")

    st.markdown("""
    ```
    [ INTERNET ]
         |
    [ FIREWALL ]
         |
    ├── [ IT NETWORK ] 🖥️
    |
    ├── [ DMZ ] 🛡️
    |
    └── [ OT NETWORK ] 🏭 ⚠️ ACTIVE THREATS
    ```
    """)

    st.markdown("---")

    st.markdown("## 🚨 Active Incident")

    st.markdown(f'<div class="alert">{incident["title"]}</div>', unsafe_allow_html=True)

    st.markdown("### 🧠 Response Options")

    c1, c2, c3 = st.columns(3)

    with c1:
        if st.button("🛑 Isolate OT VLAN"):
            if incident["fix"] == "Isolate VLAN OT":
                st.session_state.score += 20
                st.session_state.health += 5
                st.markdown('<div class="success">Correct Response</div>', unsafe_allow_html=True)
            else:
                st.session_state.health -= 10

            st.session_state.incident = None
            st.rerun()

    with c2:
        if st.button("🚫 Block Device"):
            if incident["fix"] == "Block MAC address":
                st.session_state.score += 20
                st.session_state.health += 5
                st.markdown('<div class="success">Correct Response</div>', unsafe_allow_html=True)
            else:
                st.session_state.health -= 10

            st.session_state.incident = None
            st.rerun()

    with c3:
        if st.button("🧱 Enable Segmentation"):
            if incident["fix"] == "Enable segmentation":
                st.session_state.score += 20
                st.session_state.health += 5
                st.markdown('<div class="success">Correct Response</div>', unsafe_allow_html=True)
            else:
                st.session_state.health -= 10

            st.session_state.incident = None
            st.rerun()

# -----------------------------
# CONTROL PANEL
# -----------------------------
with col2:

    st.markdown("## 🛠️ Control Panel")

    if st.button("🔍 Scan Network"):
        st.session_state.score += 5
        st.session_state.alerts.append("Scan completed: No critical vulnerabilities found")
        st.rerun()

    if st.button("🧯 Deploy Firewall Rules"):
        st.session_state.score += 10
        st.session_state.health += 5
        st.session_state.alerts.append("Firewall rules updated")
        st.rerun()

    if st.button("📡 Enable Monitoring"):
        st.session_state.score += 5
        st.session_state.alerts.append("Monitoring ac_
