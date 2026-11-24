 import streamlit as st
import requests
import datetime
from zoneinfo import ZoneInfo

# URL de implementación de Google Apps Script
APPS_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbwRmq614HFCv-imhc_63hjoT9sM7qRlcJP6Do5ErkjFWBBfjXQj5T5S6zpoW80Hbkh5-w/exec"

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

# --- ESTILOS CSS PARA OPTIMIZACIÓN MÓVIL (CELULARES) ---
st.markdown("""
    <style>
        /* Reducir espacio superior innecesario en pantallas pequeñas */
        .block-container {
            padding-top: 1.2rem !important;
            padding-bottom: 2.5rem !important;
            padding-left: 1rem !important;
            padding-right: 1rem !important;
            max-width: 600px !important;
        }

        /* Título más compacto para móviles */
        h1 {
            font-size: 1.65rem !important;
            margin-bottom: 0.2rem !important;
        }

        h3 {
            font-size: 1.2rem !important;
            margin-top: 0.5rem !important;
            margin-bottom: 0.5rem !important;
        }

        /* Etiquetas de preguntas más claras y legibles bajo el sol */
        label, .stSelectbox label, .stDateInput label, .stTimeInput label, .stTextArea label {
            font-size: 1rem !important;
            font-weight: 600 !important;
            margin-bottom: 0.25rem !important;
        }

        /* Evitar zoom automático en iPhone/Android (fuente mínima 16px) y ampliar área táctil */
        div[data-baseweb="select"] > div,
        div[data-baseweb="input"] > div,
        textarea {
            font-size: 16px !important;
            min-height: 48px !important;
            border-radius: 10px !important;
        }

        input {
            font-size: 16px !important;
        }

        /* Botón principal grande y fácil de presionar con el pulgar */
        div.stButton > button[kind="primary"] {
            min-height: 54px !important;
            font-size: 1.1rem !important;
            font-weight: 700 !important;
            border-radius: 12px !important;
            margin-top: 0.5rem !important;
        }

        /* Ocultar menú superior innecesario para ganar espacio en celular */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

st.title("🚜 Formato de Traslados")
st.caption("Registro operativo de movimiento de maquinaria - Técnicos Viales")

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

HACIENDAS_DESTINO = [
    "Seleccione hacienda de destino...",
    "101 SAN MARTIN", "102 INGENIO", "103 ALTAMIRA", "104 MALABAR", "105 RHIN",
    "106 CARMEN I", "107 MANDARINO", "108 SAN JOSE", "109 FENICIA", "110 SEMILLAS",
    "111 LA MORENITA", "112 LA VALENTINA", "113 PORVENIR INGENIO", "114 INGENIO JAGUAL",
    "202 JULIA", "203 LA BERTHA", "204 COREA", "205 RHIN HURTADO", "206 PORCE ALVAREZ",
    "207 ESTRELLA CARVAJAL", "208 PORCE BLUM", "300 LAS BRISAS", "301 CARMELITA",
    "302 EL CARMEN", "303 LA SUIZA", "304 HAROLD", "305 ESTABLE", "306 HELENA",
    "307 GRACIELA", "308 EL COROCITO", "309 EL RETIRO", "310 MACARENA", "311 ESTRELLA",
    "312 MAYORCA", "313 PORCE MARICEL", "314 PRIMAVERA", "315 LA ISLA", "317 GARRIDOS",
    "318 EL POTRERO", "319 LA DELFINA", "321 PIEDRAS NEGRAS", "322 EL JAZMIN",
    "323 EL RECREO", "324 YARUMAL", "325 YARUMAL S", "326 SANTA RITA", "327 EL CHAMBIMBE",
    "328 SANTINO S", "329 REMOLINOS", "330 PLAYAS G", "331 RECUERDO MD",
    "332 ALTAMIRA DMD", "333 LA MILAGROSA MD", "334 MARGARITA MD", "335 PIEDRAS MD",
    "336 PORVENIR MONTOYA MD", "338 MARGARITA MONTOYA MD 2", "339 COROZAL MD",
    "341 EL CANEY", "342 MALABAR NAVIA", "344 GAVIOTA O", "348 PALMA MONTOYA MD",
    "349 TRINIDAD", "350 NATIVIDAD", "351 VILLAPAOLA", "352 LA LUISA AL",
    "353 BOMBAY MD", "355 COROZAL J", "356 COROZAL C", "401 GARZONERO",
    "402 LA VICTORIA", "407 PORTACHUELO", "408 LAS PIEDRAS", "409 ALEJANDRIA",
    "410 LA MORENITA B 2", "415 ALVARADO", "417 LA PALMA", "429 SAN JUANITO",
    "434 LIMONERO", "435 EL TABLAZO", "436 TIERRAGRATA", "437 PLAYAS",
    "439 EL SAMAN", "440 SABALETAS O", "441 HERIBERTO", "442 ALICIA",
    "443 ARAGON", "444 EL DIAMANTE", "445 LA FLORESTA R", "448 EL JARDIN",
    "452 LA GUAIRA", "466 LA CABAÑA", "467 SAN CARLOS", "468 LA MARCHA",
    "469 HOLGUINES", "496 SAN JERONIMO", "499 RUMOR", "530 SANTINO",
    "531 PORVENIR", "533 LOS NARANJOS", "534 LA PISTA R", "535 LA SUERTE",
    "536 LA GUADALUPE", "542 EL PORVENIR R", "543 BIZERTA", "545 LOS MANGOS",
    "547 LA AURORA", "548 BRASILAR
