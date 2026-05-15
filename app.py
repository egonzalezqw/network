import streamlit as st
import random

# =================================================
# 🧠 STATE ENGINE
# =================================================
def init_state():
    defaults = {
        "role": "Alumno",   # Alumno / Instructor
        "health": 100,
        "score": 0,
        "event": None,
        "log": [],
        "running": True
    }

    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


# =================================================
# 🏭 RED INDUSTRIAL (MAPA VISUAL)
# =================================================
def render_network_map():

    st.markdown("## 🏭 Mapa de Red Industrial")

    st.markdown("""
