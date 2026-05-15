import streamlit as st
import time

# -----------------------------
# CONFIG
# -----------------------------
st.set_page_config(
    page_title="Network Defender Challenge",
    page_icon="🛡️",
    layout="wide"
)

# -----------------------------
# SESSION STATE INIT
# -----------------------------
if "score" not in st.session_state:
    st.session_state.score = 0

if "level" not in st.session_state:
    st.session_state.level = 1

if "finished" not in st.session_state:
    st.session_state.finished = False

# -----------------------------
# STYLE (FIXED STREAMLIT SELECTORS)
# -----------------------------
st.markdown("""
<style>
.stApp {
    background-color: #0E1117;
    color: white;
}

.block-container {
    padding-top: 2rem;
    color: white;
}

h1, h2, h3, p, label, span {
    color: white !important;
}

.stButton>button {
    width: 100%;
    border-radius: 10px;
    height: 3em;
    font-size: 16px;
    font-weight: bold;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# HEADER
# -----------------------------
st.title("🛡️ Network Defender Challenge")
st.subheader("Aprende Redes, VLAN y OT protegiendo una fábrica digital")

# -----------------------------
# SIDEBAR DEBUG + STATUS
# -----------------------------
with st.sidebar:
    st.header("📊 Estado del Juego")

    st.metric("Puntos", st.session_state.score)
    st.metric("Nivel", st.session_state.level)

    st.write("DEBUG")
    st.write("finished:", st.session_state.finished)

    progress = min(st.session_state.level / 5, 1.0)
    st.progress(progress)

# -----------------------------
# SAFETY VARIABLES
# -----------------------------
level = st.session_state.level
finished = st.session_state.finished

# -----------------------------
# LEVEL FLOW (SAFE)
# -----------------------------
if finished:

    st.title("🏆 Resultado Final")

    st.metric("Puntaje Final", st.session_state.score)

    if st.session_state.score >= 100:
        st.success("🏆 Arquitecto de Redes")
        st.balloons()

    elif st.session_state.score >= 70:
        st.info("🛡️ Administrador Seguro")

    else:
        st.warning("⚠️ Red Vulnerable")

    st.write("""
    Aprendiste:
    - Redes básicas
    - VLANs
    - Seguridad IT/OT
    - Protección industrial
    """)

    if st.button("🔄 Reiniciar"):
        st.session_state.score = 0
        st.session_state.level = 1
        st.session_state.finished = False
        st.rerun()

# -----------------------------
# LEVEL 1
# -----------------------------
elif level == 1:

    st.markdown("## 🌐 Nivel 1 - Redes")

    answer = st.radio(
        "¿Cuál es el objetivo principal de una red?",
        ["Apagar computadoras", "Compartir información y recursos", "Crear virus"]
    )

    if st.button("Validar"):

        if answer == "Compartir información y recursos":
            st.success("Correcto")
            st.session_state.score += 10
        else:
            st.error("Incorrecto")

        st.session_state.level = 2
        st.rerun()

# -----------------------------
# LEVEL 2
# -----------------------------
elif level == 2:

    st.markdown("## 🔀 Nivel 2 - VLANs")

    col1, col2, col3 = st.columns(3)

    with col1:
        oficina = st.selectbox("Oficina", ["Seleccionar", "VLAN 10", "VLAN 20", "VLAN 30"])

    with col2:
        invitados = st.selectbox("Invitados", ["Seleccionar", "VLAN 10", "VLAN 20", "VLAN 30"])

    with col3:
        ot = st.selectbox("Producción OT", ["Seleccionar", "VLAN 10", "VLAN 20", "VLAN 30"])

    if st.button("Configurar"):

        puntos = 0

        if oficina == "VLAN 10":
            puntos += 10
        if invitados == "VLAN 20":
            puntos += 10
        if ot == "VLAN 30":
            puntos += 10

        st.session_state.score += puntos
        st.session_state.level = 3

        st.rerun()

# -----------------------------
# LEVEL 3
# -----------------------------
elif level == 3:

    st.markdown("## 🚨 Nivel 3 - Ataque")

    answer = st.radio(
        "¿Qué evita propagación de ataques?",
        ["Más cables", "Reiniciar internet", "Usar VLANs"]
    )

    if st.button("Responder"):

        if answer == "Usar VLANs":
            st.success("Correcto")
            st.session_state.score += 20
        else:
            st.error("Incorrecto")

        st.session_state.level = 4
        st.rerun()

# -----------------------------
# LEVEL 4
# -----------------------------
elif level == 4:

    st.markdown("## 🏭 Nivel 4 - IT vs OT")

    correo = st.selectbox("Correo", ["Seleccionar", "IT", "OT"])
    plc = st.selectbox("PLC", ["Seleccionar", "IT", "OT"])
    server = st.selectbox("Servidor", ["Seleccionar", "IT", "OT"])
    sensor = st.selectbox("Sensor", ["Seleccionar", "IT", "OT"])

    if st.button("Validar"):

        puntos = 0

        if correo == "IT":
            puntos += 10
        if plc == "OT":
            puntos += 10
        if server == "IT":
            puntos += 10
        if sensor == "OT":
            puntos += 10

        st.session_state.score += puntos
        st.session_state.level = 5

        st.rerun()

# -----------------------------
# LEVEL 5 FINAL
# -----------------------------
elif level == 5:

    st.markdown("## 🛡️ Nivel Final")

    firewall = st.checkbox("Firewall")
    vlan = st.checkbox("VLAN OT")
    invitados = st.checkbox("Permitir invitados OT")
    monitor = st.checkbox("Monitoreo")

    if st.button("Defender"):

        puntos = 0

        if firewall:
            puntos += 20
        if vlan:
            puntos += 30
        if monitor:
            puntos += 20
        if invitados:
            puntos -= 30

        st.session_state.score += puntos
        st.session_state.finished = True

        st.rerun()

# -----------------------------
# SAFETY FALLBACK (NO BLANK SCREEN)
# -----------------------------
else:
    st.error("⚠️ Estado inválido del juego")
    st.write("Level:", st.session_state.level)
    st.write("Finished:", st.session_state.finished)
