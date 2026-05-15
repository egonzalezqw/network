# =================================================
# 🎛️ CONTROL PANEL (SIDEBAR SOC)
# =================================================
st.sidebar.title("🧭 Control SOC OT")

st.session_state.role = st.sidebar.selectbox(
    "Modo",
    ["Alumno", "Instructor"]
)

# =================================================
# 🧠 METRICS
# =================================================
health = st.session_state.health

# 🔒 FIX CRÍTICO (evita error Streamlit 0.0 - 1.0)
progress_value = max(0.0, min(health / 100, 1.0))

st.sidebar.metric("Health", f"{health}%")
st.sidebar.metric("Score", st.session_state.score)

# =================================================
# 🚦 ESTADO SOC VISUAL
# =================================================
if health > 70:
    st.sidebar.success("🟢 Sistema estable")
elif health > 40:
    st.sidebar.warning("🟡 Riesgo medio")
else:
    st.sidebar.error("🔴 Sistema degradado")

st.sidebar.progress(progress_value)

st.sidebar.markdown("---")
st.sidebar.write("📜 Logs SOC")

for l in st.session_state.log[-6:]:
    st.sidebar.write("•", l)
