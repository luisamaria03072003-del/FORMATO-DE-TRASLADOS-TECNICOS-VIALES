import streamlit as st
import requests
import datetime
import base64
from zoneinfo import ZoneInfo

# URL de implementación de Google Apps Script
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
        .stApp {
            background-color: #F6FAF5;
        }

        .block-container {
            padding-top: 3.2rem !important;
            padding-bottom: 2.5rem !important;
            padding-left: 1rem !important;
            padding-right: 1rem !important;
            max-width: 600px !important;
        }

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

        h3 {
            color: #1B5E20 !important;
            font-size: 1.15rem !important;
            border-left: 4px solid #2E7D32;
            padding-left: 10px;
            margin-top: 0.6rem !important;
            margin-bottom: 0.6rem !important;
        }

        label, .stSelectbox label, .stDateInput label, .stTimeInput label, .stTextArea label, .stMultiSelect label, .stFileUploader label, .stCameraInput label {
            color: #1B4332 !important;
            font-size: 0.98rem !important;
            font-weight: 600 !important;
            margin-bottom: 0.25rem !important;
        }

        div[data-testid="stVerticalBlockBorderWrapper"] {
            background-color: #FFFFFF !important;
            border: 1.5px solid #A5D6A7 !important;
            border-radius: 12px !important;
            padding: 0.6rem !important;
            margin-bottom: 0.6rem !important;
            box-shadow: 0 2px 5px rgba(46, 125, 50, 0.06);
        }

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

ESCOLTAS_INTERNOS = [
    "5712",
    "5713",
    "4604",
    "Pwt 030"
]

CAMABAJAS_INTERNOS = [
    "5",
    "6",
    "8",
    "9"
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
    "547 LA AURORA", "548 BRASILAR", "549 ARGENTINA", "550 TABLACITO",
    "551 EL EDEN", "552 PRAGA", "553 BELLAVISTA", "554 EL ALBERGUE",
    "556 SAN MATEO", "557 LAS TRES MARIAS", "558 BELLAVISTA P", "561 LA PALMA TAFUR",
    "564 CAMPOALEGRE", "567 LA BOLA TAFUR", "571 CHAMBIMBE G",
    "572 LA MORENITA CASTELLANO", "576 LA FLORESTA Z", "577 SACRISTIA",
    "578 ZABALETAS ARANGO", "581 TESORITO G", "582 TAYRONA", "583 TAYRONA TAFUR",
    "584 LA MARGARITA", "585 LA ESPINOSA", "586 EL ALTERON", "587 VILLA SARAÍ",
    "588 BOLA ROJA", "590 ARMONIA A", "591 CHAMBIMBE A", "592 MIEL",
    "593 LA FLORESTA C", "709 TESORITO", "715 EL PLACER", "720 TESORITO (2)",
    "721 VIVERO", "731 MALAGA", "732 LOMA LINDA", "735 SAN SEBASTIAN",
    "736 SANTA-ANA", "737 BUENOS AIRES", "738 EL TREBOL", "748 LA NUBIA",
    "790 LA ISABELLA", "791 PORVENIR ANDRADE", "792 EL CLAVO",
    "793 VILLA ELVIRA Y OTROS", "794 BRASILAR R", "795 LA FERNANDA",
    "796 EL MADRONO", "797 PARCELAS ROLDANILLO", "798 TAPIAS", "799 VISTA HERMOSA"
]

# --- DATOS GENERALES ---
st.subheader("Datos del Turno")
fecha = st.date_input("Fecha *", value=ahora_col.date(), format="MM/DD/YYYY")
hora_salida = st.time_input("Hora de salida *", value=ahora_col.time().replace(second=0, microsecond=0))

tecnico = st.selectbox("Nombre del técnico Vial *", TECNICOS_VIALES)
turno = st.selectbox("Turno *", TURNOS)
frente = st.selectbox("Frente *", FRENTES)

# --- ESCOLTAS (ENCIMA DE MAQUINARIA A TRASLADAR) ---
st.subheader("Escoltas")
escolta_sel = st.selectbox(
    "Seleccione escoltas",
    ["Seleccione escoltas"] + ESCOLTAS_INTERNOS
)
escoltas_seleccionados = [escolta_sel] if escolta_sel != "Seleccione escoltas" else []

# --- MAQUINARIA / VEHÍCULOS A TRASLADAR (1 O VARIOS) ---
st.subheader("Maquinaria a Trasladar")

equipos_lista = []
errores_equipos = []

for i in range(st.session_state.num_equipos):
    with st.container(border=True):
        if st.session_state.num_equipos > 1:
            st.markdown(f'<div class="badge-vehiculo">🚜 Vehículo #{i + 1}</div>', unsafe_allow_html=True)

        tipo_equipo = st.selectbox(
            "Tipo de equipo *",
            ["Seleccione tipo..."] + list(BASE_EQUIPOS.keys()),
            key=f"tipo_eq_{i}"
        )

        if tipo_equipo != "Seleccione tipo...":
            num_interno = st.selectbox(
                f"Número interno ({tipo_equipo}) *",
                ["Seleccione número..."] + BASE_EQUIPOS[tipo_equipo],
                key=f"num_int_{i}"
            )
            if num_interno == "Seleccione número...":
                errores_equipos.append(f"Número interno (Vehículo #{i + 1})" if st.session_state.num_equipos > 1 else "Número interno")
            else:
                equipos_lista.append({
                    "tipo_equipo": tipo_equipo,
                    "numero_interno": num_interno
                })
        else:
            st.selectbox(
                "Número interno *",
                ["Seleccione primero el tipo de equipo"],
                disabled=True,
                key=f"num_int_disabled_{i}"
            )
            errores_equipos.append(f"Tipo de equipo (Vehículo #{i + 1})" if st.session_state.num_equipos > 1 else "Tipo de equipo")

if st.button("➕ Agregar otro vehículo al traslado", type="secondary", use_container_width=True):
    st.session_state.num_equipos += 1
    st.rerun()

if st.session_state.num_equipos > 1:
    if st.button("🗑️ Quitar último vehículo", type="secondary", use_container_width=True):
        st.session_state.num_equipos -= 1
        st.rerun()

# --- CAMABAJAS (DEBAJO DE MAQUINARIA A TRASLADAR) ---
st.subheader("Cama baja")
camabaja_sel = st.selectbox(
    "Seleccione cama baja",
    ["Seleccione cama baja"] + CAMABAJAS_INTERNOS
)
camabajas_seleccionadas = [camabaja_sel] if camabaja_sel != "Seleccione cama bajas" else []

# --- DESTINO Y OBSERVACIONES ---
st.subheader("Destino y Novedades")
hacienda_destino = st.selectbox(
    "Hacienda de destino *",
    HACIENDAS_DESTINO
)

observaciones = st.text_area(
    "Observaciones o novedades durante el traslado",
    height=100
)

# --- FOTO DE NOVEDADES (TOMAR O SUBIR) ---
opcion_foto = st.radio(
    "Foto de novedades",
    ["Sin foto", "Tomar foto", "Subir foto"],
    horizontal=True
)

foto_bytes = None
foto_nombre = ""
foto_mime = "image/jpeg"

if opcion_foto == "Tomar foto":
    foto_capturada = st.camera_input("Tomar foto")
    if foto_capturada is not None:
        foto_bytes = foto_capturada.getvalue()
        foto_nombre = f"novedad_{ahora_col.strftime('%Y%m%d_%H%M%S')}.jpg"
        foto_mime = "image/jpeg"
elif opcion_foto == "Subir foto":
    foto_subida = st.file_uploader(
        "Subir foto",
        type=["jpg", "jpeg", "png", "webp"]
    )
    if foto_subida is not None:
        foto_bytes = foto_subida.getvalue()
        foto_nombre = foto_subida.name
        foto_mime = foto_subida.type or "image/jpeg"

# --- BOTÓN DE ENVÍO ---
if st.button("📤 Enviar Traslado", type="primary", use_container_width=True):
    errores = []
    if tecnico == "Seleccione un técnico...":
        errores.append("Nombre del técnico Vial")
    if turno == "Seleccione un turno...":
        errores.append("Turno")
    if frente == "Seleccione un frente...":
        errores.append("Frente")
    errores.extend(errores_equipos)
    if hacienda_destino == "Seleccione hacienda de destino...":
        errores.append("Hacienda de destino")

    if errores:
        st.error(f"⚠️ Completa los campos obligatorios: **{', '.join(errores)}**.")
    else:
        escoltas_texto = ", ".join(escoltas_seleccionados) if escoltas_seleccionados else "N/A"
        camabajas_texto = ", ".join(camabajas_seleccionadas) if camabajas_seleccionadas else "N/A"

        foto_base64 = base64.b64encode(foto_bytes).decode("utf-8") if foto_bytes else ""

        payload = {
            "fecha": fecha.strftime("%Y-%m-%d"),
            "tecnico": tecnico,
            "turno": turno,
            "frente": frente,
            "escoltas": escoltas_texto,
            "cantidad_equipos": len(equipos_lista),
            "equipos": equipos_lista,
            "camabajas": camabajas_texto,
            "hacienda_destino": hacienda_destino,
            "hora_salida": hora_salida.strftime("%H:%M"),
            "observaciones": observaciones,
            "foto_nombre": foto_nombre,
            "foto_mime": foto_mime,
            "foto_base64": foto_base64
        }

        try:
            with st.spinner("Guardando traslado en Google Sheets..."):
                respuesta = requests.post(APPS_SCRIPT_URL, json=payload, timeout=25)
                if respuesta.status_code == 200 and "ok" in respuesta.text:
                    resumen = ", ".join([f"{e['tipo_equipo']} #{e['numero_interno']}" for e in equipos_lista])
                    st.success(f"✅ ¡Traslado guardado! ({resumen}).")
                elif respuesta.status_code == 200:
                    st.warning("⚠️ Google bloqueó la escritura. Verifica en Apps Script que el acceso sea para 'Cualquier persona'.")
                else:
                    st.error(f"⚠️ Error al guardar (Código {respuesta.status_code}): {respuesta.text}")
        except Exception as e:
            st.error(f"❌ Error de conexión con Google Sheets: {e}")
