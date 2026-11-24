import streamlit as st
import requests
import datetime
from zoneinfo import ZoneInfo

# URL de tu implementación de Google Apps Script
APPS_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbzaeC4tI9uz-NrZxE2bKAu3HEDKR1Z9Pi-20iPksudbJqLmTfUEhx1lpWz1CpZqbWMNkw/exec"

# Hora actual en Colombia (evita desfases de fecha en servidores en la nube)
ZONA_COLOMBIA = ZoneInfo("America/Bogota")
ahora_col = datetime.datetime.now(ZONA_COLOMBIA)

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Formato de Traslados", page_icon="🚜", layout="centered")
st.title("🚜 Formato de Traslados")
st.caption("Registro operativo de movimiento de maquinaria y equipos - Técnicos Viales")

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

# Diccionario de Tipos de Equipo -> Números Internos
# (Incluye los de prueba y opciones temporales para los demás tipos)
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

# --- CAMPOS DEL FORMULARIO ---
col_fecha, col_hora = st.columns(2)
with col_fecha:
    fecha = st.date_input("Fecha *", value=ahora_col.date(), format="MM/DD/YYYY")
with col_hora:
    hora_salida = st.time_input("Hora de salida *", value=ahora_col.time().replace(second=0, microsecond=0))

tecnico = st.selectbox("Nombre del técnico Vial *", TECNICOS_VIALES)

col_turno, col_frente = st.columns(2)
with col_turno:
    turno = st.selectbox("Turno *", TURNOS)
with col_frente:
    frente = st.selectbox("Frente *", FRENTES)

hacienda_destino = st.selectbox(
    "Hacienda de destino * (Puedes escribir el código o nombre para buscar)",
    HACIENDAS_DESTINO
)

st.markdown("---")
st.subheader("Maquinaria / Equipos a Trasladar")

cantidad_equipos = st.number_input(
    "Cantidad de maquinaria del traslado *",
    min_value=1,
    max_value=15,
    value=1,
    step=1
)

equipos_lista = []
faltan_equipos = False

for i in range(int(cantidad_equipos)):
    if cantidad_equipos > 1:
        st.markdown(f"**Equipo #{i + 1}**")
        
    c1, c2 = st.columns(2)
    with c1:
        tipo_equipo = st.selectbox(
            "Tipo de equipo *",
            ["Seleccione tipo..."] + list(BASE_EQUIPOS.keys()),
            key=f"tipo_eq_{i}"
        )
    with c2:
        if tipo_equipo != "Seleccione tipo...":
            num_interno = st.selectbox(
                f"Número interno ({tipo_equipo}) *",
                ["Seleccione número..."] + BASE_EQUIPOS[tipo_equipo],
                key=f"num_int_{i}"
            )
            if num_interno == "Seleccione número...":
                faltan_equipos = True
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
            faltan_equipos = True

st.markdown("---")
observaciones = st.text_area("Observaciones o novedades durante el traslado")

# --- BOTÓN DE ENVÍO ---
if st.button("📤 Enviar Traslado", type="primary", use_container_width=True):
    # Validación de campos obligatorios
    errores = []
    if tecnico == "Seleccione un técnico...":
        errores.append("Nombre del técnico Vial")
    if turno == "Seleccione un turno...":
        errores.append("Turno")
    if frente == "Seleccione un frente...":
        errores.append("Frente")
    if hacienda_destino == "Seleccione hacienda de destino...":
        errores.append("Hacienda de destino")
    if faltan_equipos:
        errores.append("Tipo de equipo y Número interno en todos los equipos")

    if errores:
        st.error(f"⚠️ Por favor completa los siguientes campos obligatorios: **{', '.join(errores)}**.")
    else:
        payload = {
            "fecha": fecha.strftime("%Y-%m-%d"),
            "tecnico": tecnico,
            "turno": turno,
            "frente": frente,
            "cantidad_equipos": int(cantidad_equipos),
            "equipos": equipos_lista,
            "hacienda_destino": hacienda_destino,
            "hora_salida": hora_salida.strftime("%H:%M"),
            "observaciones": observaciones
        }

        try:
            with st.spinner("Registrando traslado en Google Sheets..."):
                respuesta = requests.post(APPS_SCRIPT_URL, json=payload, timeout=15)
                if respuesta.status_code == 200:
                    st.success(f"✅ ¡Traslado registrado exitosamente! ({cantidad_equipos} equipo(s) enviado(s)).")
                else:
                    st.error(f"⚠️ Error al guardar (Código {respuesta.status_code}): {respuesta.text}")
        except Exception as e:
            st.error(f"❌ No se pudo conectar con Google Sheets: {e}")