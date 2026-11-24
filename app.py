import streamlit as st
import requests
import datetime
from zoneinfo import ZoneInfo

# Nueva URL de implementación de Google Apps Script
APPS_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbxTTvzj_UkWAO1vQssmoqOb2WtX07OVqZnIQT8S7LnaKVItaX-g_jKQucIVhSeD7kUsWQ/exec"

# Hora actual en Colombia
ZONA_COLOMBIA = ZoneInfo("America/Bogota")
ahora_col = datetime.datetime.now(ZONA_COLOMBIA)

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="Formato de Traslados",
    page_icon="🚜",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- CONTROL DE VEHÍCULOS DINÁMICOS ---
if "num_equipos" not in st.session_state:
    st.session_state.num_equipos = 1

# --- ESTILOS CSS: TONOS VERDES INGENIO + OPTIMIZACIÓN CELULAR ---
st.markdown("""
    <style>
        /* Fondo general sutil en verde muy claro */
        .stApp {
            background-color: #F6FAF5;
        }

        /* Contenedor adaptado a pantalla de celular */
        .block-container {
            padding-top: 1rem !important;
            padding-bottom: 2.5rem !important;
            padding-left: 1rem !important;
            padding-right: 1rem !important;
            max-width: 600px !important;
        }

        /* Encabezado principal estilo Ingenio */
        .header-ingenio {
            background: linear-gradient(135deg, #1B5E20 0%, #2E7D32 100%);
            padding: 1.1rem 1.2rem;
            border-radius: 14px;
            color: #FFFFFF;
            margin-bottom: 1.1rem;
            box-shadow: 0 3px 10px rgba(27, 94, 32, 0.18);
        }
        .header-ingenio h1 {
            color: #FFFFFF !important;
            font-size: 1.55rem !important;
            margin: 0 !important;
            padding: 0 !important;
            font-weight: 700 !important;
        }
        .header-ingenio p {
            color: #C8E6C9 !important;
            font-size: 0.9rem !important;
            margin: 0.25rem 0 0 0 !important;
        }

        /* Subtítulos de sección en verde bosque */
        h3 {
            color: #1B5E20 !important;
            font-size: 1.15rem !important;
            border-left: 4px solid #2E7D32;
            padding-left: 10px;
            margin-top: 0.6rem !important;
            margin-bottom: 0.6rem !important;
        }

        /* Etiquetas de preguntas */
        label, .stSelectbox label, .stDateInput label, .stTimeInput label, .stTextArea label {
            color: #1B4332 !important;
            font-size: 0.98rem !important;
            font-weight: 600 !important;
            margin-bottom: 0.25rem !important;
        }

        /* Tarjetas de cada vehículo */
        div[data-testid="stVerticalBlockBorderWrapper"] {
            background-color: #FFFFFF !important;
            border: 1.5px solid #A5D6A7 !important;
            border-radius: 12px !important;
            padding: 0.6rem !important;
            margin-bottom: 0.6rem !important;
            box-shadow: 0 2px 5px rgba(46, 125, 50, 0.06);
        }

        /* Inputs y desplegables cómodos para celular (sin zoom automático) */
        div[data-baseweb="select"] > div,
        div[data-baseweb="input"] > div,
        textarea {
            background-color: #FFFFFF !important;
            border-color: #A5D6A7 !important;
            font-size: 16px !important;
            min-height: 48px !important;
            border-radius: 10px !important;
        }

        div[data-baseweb="select"] > div:focus-within,
        div[data-baseweb="input"] > div:focus-within,
        textarea:focus {
            border-color: #2E7D32 !important;
            box-shadow: 0 0 0 2px rgba(46, 125, 50, 0.2) !important;
        }

        input {
            font-size: 16px !important;
        }

        /* Botón principal (Enviar Traslado) en verde cañero */
        div.stButton > button[kind="primary"] {
            background-color: #2E7D32 !important;
            border-color: #2E7D32 !important;
            color: #FFFFFF !important;
            min-height: 54px !important;
            font-size: 1.1rem !important;
            font-weight: 700 !important;
            border-radius: 12px !important;
            margin-top: 0.5rem !important;
            box-shadow: 0 3px 8px rgba(46, 125, 50, 0.25);
        }
        div.stButton > button[kind="primary"]:hover {
            background-color: #1B5E20 !important;
            border-color: #1B5E20 !important;
        }

        /* Botones secundarios (Agregar / Quitar vehículo) */
        div.stButton > button[kind="secondary"] {
            background-color: #E8F5E9 !important;
            border: 1.5px solid #43A047 !important;
            color: #1B5E20 !important;
            min-height: 46px !important;
            font-size: 0.98rem !important;
            font-weight: 600 !important;
            border-radius: 10px !important;
        }
        div.stButton > button[kind="secondary"]:hover {
            background-color: #C8E6C9 !important;
        }

        /* Etiqueta superior de cada tarjeta de vehículo */
        .badge-vehiculo {
            background-color: #E8F5E9;
            color: #1B5E20;
            padding: 4px 10px;
            border-radius: 6px;
            font-weight: 700;
            font-size: 0.9rem;
            display: inline-block;
            margin-bottom: 6px;
        }

        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- ENCABEZADO VERDE ---
st.markdown("""
    <div class="header-ingenio">
        <h1>🚜 Formato de Traslados</h1>
        <p>Control de Maquinaria y Equipos • Técnicos Viales</p>
    </div>
""", unsafe_allow_html=True)

# --- LISTAS DE DATOS DEL FORMULARIO ---
TECNICOS_VIALES = [
    "Seleccione un técnico...",
    "Carlos Humberto Ramirez",
    "Nilson Murillo",
    "Absalón Quintero",
    "Milton Cabrera"
]

TURNOS = [
    "Seleccione un turno...",
    "Turno 1",
    "Turno 2",
    "Turno 3"
]

FRENTES = [
    "Seleccione un frente...",
    "Frente 1",
    "Frente 2",
    "Frente 3",
    "Frente 4",
    "Campo",
    "Taller Agrícola"
]

BASE_EQUIPOS = {
    "Tractor": ["1", "2", "3", "4", "5", "6"],
    "Alzadora": ["7", "8", "9", "10"],
    "Cosechadora": ["4", "5", "6"],
    "Bulldozer": ["Prueba 1", "Prueba 2"],
    "Retroexcavadora": ["Prueba 1", "Prueba 2"],
    "Motoniveladora": ["Prueba 1", "Prueba 2"],
    "Motobomba": ["Prueba 1", "Prueba 2"],
    "Implementos agrícolas": ["Prueba 1", "Prueba 2"],
    "Vagones": ["Prueba 1", "Prueba 2"],
    "Gondolas": ["Prueba 1", "Prueba 2"]
}

HACIENDAS_
