import streamlit as st
import random

# =================================================
# 🧠 MOTOR DE ESTADO
# =================================================
def init_state():
    defaults = {
        "puntos": 0,
        "salud": 100,
        "logs": [],
        "incidente": None,
        "activo": True
    }

    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


# =================================================
# 🌐 INCIDENTES (REDES / VLAN / OT)
# =================================================
INCIDENTES = [
    {
        "id": "vlan_mala_configuracion",
        "titulo": "⚠️ Mala configuración de VLAN entre IT y OT",
        "pregunta": "¿Cuál es la solución correcta para separar el tráfico IT y OT?",
        "opciones": ["Routing dinámico", "VLANs", "DNS compartido"],
        "correcta": "VLANs",
        "puntos": 20
    },
    {
        "id": "broadcast_excesivo",
        "titulo": "📡 Tráfico broadcast excesivo en la red de producción",
        "pregunta": "¿Qué ayuda a reducir los dominios de broadcast?",
        "opciones": ["Switching sin VLAN", "Segmentación VLAN", "Más cables"],
        "correcta": "Segmentación VLAN",
        "puntos": 20
    },
    {
        "id": "exposicion_ot",
        "titulo": "🏭 Red OT expuesta a usuarios corporativos",
        "pregunta": "¿Cómo se debe aislar correctamente la red OT?",
        "opciones": ["Firewall + VLANs", "WiFi abierto", "IP pública directa"],
        "correcta": "Firewall + VLANs",
        "puntos": 25
    },
    {
        "id": "red_plana",
        "titulo": "🔴 Red plana detectada (sin segmentación)",
        "pregunta": "¿Cuál es el principal riesgo de una red plana?",
        "opciones": ["Más velocidad", "Movimiento lateral fácil", "Menos latencia"],
        "correcta": "Movimiento lateral fácil",
        "puntos": 25
    },
    {
        "id": "protocolo_industrial",
        "titulo": "⚙️ Protocolo industrial sin seguridad detectado",
        "pregunta": "¿Qué mejora la seguridad en redes OT?",
        "opciones": [
            "Segmentación + firewalls industriales",
            "Más usuarios conectados",
            "DHCP abierto"
        ],
        "correcta": "Segmentación + firewalls industriales",
        "puntos": 30
    }
]


# =================================================
# ⚙️ MOTOR DEL JUEGO
# =================================================
def obtener_incidente():
    return random.choice(INCIDENTES)


def aplicar_accion(seleccion, incidente):

    if seleccion == incidente["correcta"]:
        st.session_state.puntos += incidente["puntos"]
        st.session_state.salud = min(100, st.session_state.salud + 5)
        st.session_state.logs.append(f"✔ Correcto: {incidente['titulo']}")
        return True
    else:
        st.session_state.salud -= 10
        st.session_state.logs.append(f"✖ Incorrecto: {incidente['titulo']}")
        return False


def siguiente_incidente():
    st.session_state.incidente = obtener_incidente()


# =================================================
# 🎨 INTERFAZ
# =================================================
def mostrar_hud():

    st.sidebar.title("🛡️ PANEL OT / REDES")

    st.sidebar.metric("Puntos", st.session_state.puntos)
    st.sidebar.metric("Salud de Red", st.session_state.salud)

    st.sidebar.progress(st.session_state.salud / 100)

    st.sidebar.markdown("---")
    st.sidebar.write("📜 Registro de eventos")

    for log in st.session_state.logs[-6:]:
        st.sidebar.write("•", log)


def mostrar_incidente(incidente):

    st.title("🌐 SIMULADOR DE REDES OT")

    st.markdown("## 🚨 Evento de Red")
    st.error(incidente["titulo"])

    st.markdown("### 🧠 Pregunta de arquitectura de red")
    st.write(incidente["pregunta"])

    opcion = st.radio("Selecciona una respuesta:", incidente["opciones"])

    if st.button("Aplicar acción de red"):

        correcto = aplicar_accion(opcion, incidente)

        if correcto:
            st.success("✔ Decisión correcta de red")
        else:
            st.warning("✖ Decisión incorrecta")

        siguiente_incidente()
        st.rerun()


def game_over():

    st.error("💀 FALLA CRÍTICA EN LA RED OT")
    st.write("Puntaje final:", st.session_state.puntos)

    if st.button("Reiniciar simulación"):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.rerun()


# =================================================
# 🚀 EJECUCIÓN PRINCIPAL
# =================================================
init_state()

if st.session_state.incidente is None:
    siguiente_incidente()

mostrar_hud()

if st.session_state.salud <= 0:
    game_over()
else:
    mostrar_incidente(st.session_state.incidente)
