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
# SESSION STATE
# -----------------------------
if "score" not in st.session_state:
    st.session_state.score = 0

if "level" not in st.session_state:
    st.session_state.level = 1

if "finished" not in st.session_state:
    st.session_state.finished = False

# -----------------------------
# STYLE
# -----------------------------
st.markdown("""
<style>
.main {
    background-color: #0E1117;
    color: white;
}

.block-container {
    padding-top: 2rem;
}

.stButton>button {
    width: 100%;
    border-radius: 10px;
    height: 3em;
    font-size: 16px;
    font-weight: bold;
}

.score-box {
    padding: 20px;
    border-radius: 12px;
    background-color: #1E293B;
    text-align: center;
    margin-bottom: 20px;
}

.level-title {
    color: #38BDF8;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# HEADER
# -----------------------------
st.title("🛡️ Network Defender Challenge")
st.subheader("Aprende Redes, VLAN y OT protegiendo una fábrica digital")

# -----------------------------
# SIDEBAR
# -----------------------------
with st.sidebar:
    st.header("📊 Estado del Juego")

    st.metric("Puntos", st.session_state.score)
    st.metric("Nivel", st.session_state.level)

    progress = st.session_state.level / 5
    st.progress(progress)

# -----------------------------
# INTRO
# -----------------------------
if st.session_state.level == 1:

    st.markdown("## 🌐 Nivel 1 - ¿Qué es una red?")
    st.write("""
    Eres el nuevo administrador de red de una empresa industrial.

    Tu primera misión es entender cómo funcionan las redes.
    """)

    answer = st.radio(
        "¿Cuál es el objetivo principal de una red?",
        [
            "Apagar computadoras",
            "Compartir información y recursos",
            "Crear virus"
        ]
    )

    if st.button("Validar Respuesta"):

        if answer == "Compartir información y recursos":
            st.success("✅ Correcto. Las redes conectan dispositivos para compartir información.")
            st.session_state.score += 10
        else:
            st.error("❌ Incorrecto.")

        st.session_state.level = 2
        time.sleep(1)
        st.rerun()

# -----------------------------
# LEVEL 2
# -----------------------------
elif st.session_state.level == 2:

    st.markdown("## 🔀 Nivel 2 - Crear VLANs")

    st.write("""
    La empresa necesita separar:
    - Oficina
    - Invitados
    - Producción OT
    """)

    col1, col2, col3 = st.columns(3)

    with col1:
        oficina = st.selectbox(
            "PCs Oficina",
            ["Seleccionar", "VLAN 10", "VLAN 20", "VLAN 30"]
        )

    with col2:
        invitados = st.selectbox(
            "Visitantes",
            ["Seleccionar", "VLAN 10", "VLAN 20", "VLAN 30"]
        )

    with col3:
        produccion = st.selectbox(
            "Producción OT",
            ["Seleccionar", "VLAN 10", "VLAN 20", "VLAN 30"]
        )

    if st.button("Configurar VLANs"):

        puntos = 0

        if oficina == "VLAN 10":
            puntos += 10

        if invitados == "VLAN 20":
            puntos += 10

        if produccion == "VLAN 30":
            puntos += 10

        st.session_state.score += puntos

        if puntos == 30:
            st.success("✅ Excelente segmentación de red.")
        else:
            st.warning("⚠️ Algunas VLANs no fueron configuradas correctamente.")

        st.session_state.level = 3
        time.sleep(1)
        st.rerun()

# -----------------------------
# LEVEL 3
# -----------------------------
elif st.session_state.level == 3:

    st.markdown("## 🚨 Nivel 3 - Ataque de Red")

    st.error("""
    ALERTA:
    Una laptop infectada fue conectada a la red corporativa.
    """)

    answer = st.radio(
        "¿Qué ayuda a evitar que el ataque llegue a producción?",
        [
            "Más cables",
            "Reiniciar internet",
            "Usar VLANs"
        ]
    )

    if st.button("Responder"):

        if answer == "Usar VLANs":
            st.success("✅ Correcto. Las VLANs ayudan a aislar redes.")
            st.session_state.score += 20
        else:
            st.error("❌ Incorrecto.")

        st.session_state.level = 4
        time.sleep(1)
        st.rerun()

# -----------------------------
# LEVEL 4
# -----------------------------
elif st.session_state.level == 4:

    st.markdown("## 🏭 Nivel 4 - IT vs OT")

    st.write("Clasifica correctamente cada elemento.")

    col1, col2 = st.columns(2)

    with col1:
        correo = st.selectbox(
            "Correo Corporativo",
            ["Seleccionar", "IT", "OT"]
        )

        plc = st.selectbox(
            "Control de Maquinaria",
            ["Seleccionar", "IT", "OT"]
        )

    with col2:
        servidor = st.selectbox(
            "Servidor de Aplicaciones",
            ["Seleccionar", "IT", "OT"]
        )

        sensor = st.selectbox(
            "Sensor Industrial",
            ["Seleccionar", "IT", "OT"]
        )

    if st.button("Validar Clasificación"):

        puntos = 0

        if correo == "IT":
            puntos += 10

        if plc == "OT":
            puntos += 10

        if servidor == "IT":
            puntos += 10

        if sensor == "OT":
            puntos += 10

        st.session_state.score += puntos

        if puntos == 40:
            st.success("✅ Excelente conocimiento de IT y OT.")
        else:
            st.warning("⚠️ Algunas respuestas fueron incorrectas.")

        st.session_state.level = 5
        time.sleep(1)
        st.rerun()

# -----------------------------
# FINAL LEVEL
# -----------------------------
elif st.session_state.level == 5:

    st.markdown("## 🛡️ Nivel Final - Defender la Fábrica")

    st.write("""
    Toma decisiones para proteger la operación industrial.
    """)

    firewall = st.checkbox("Instalar Firewall")
    vlan = st.checkbox("Separar Producción con VLAN")
    invitados = st.checkbox("Permitir invitados en red OT")
    monitoreo = st.checkbox("Habilitar monitoreo de red")

    if st.button("Defender Infraestructura"):

        puntos = 0

        if firewall:
            puntos += 20

        if vlan:
            puntos += 30

        if monitoreo:
            puntos += 20

        if invitados:
            puntos -= 30

        st.session_state.score += puntos
        st.session_state.finished = True
        st.session_state.level = 6

        st.rerun()

# -----------------------------
# RESULTS
# -----------------------------
elif st.session_state.finished:

    st.title("🏆 Resultado Final")

    final_score = st.session_state.score

    st.metric("Puntaje Final", final_score)

    if final_score >= 100:
        st.success("🏆 Arquitecto de Redes")
        st.balloons()

    elif final_score >= 70:
        st.info("🛡️ Administrador Seguro")

    else:
        st.warning("⚠️ Red Vulnerable")

    st.write("""
    Has aprendido:
    - Conceptos básicos de redes
    - Segmentación con VLAN
    - Diferencias entre IT y OT
    - Seguridad en entornos industriales
    """)

    if st.button("🔄 Reiniciar Juego"):
        st.session_state.score = 0
        st.session_state.level = 1
        st.session_state.finished = False
        st.rerun()
