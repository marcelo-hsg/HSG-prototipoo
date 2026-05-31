import streamlit as st
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Hospital San Gabriel — Sistema de Confirmacion",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Forzar tema claro
st.markdown("""
    <style>
        html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
            background-color: #f5f7fa !important;
            color: #1a3a6b !important;
        }
        [data-testid="stHeader"] { background-color: #f5f7fa !important; }
        .stSelectbox label, .stTextInput label, .stRadio label { color: #1a3a6b !important; }
        .stDataFrame { background-color: white !important; }
        p, span, div, label, h1, h2, h3 { color: #1a3a6b !important; }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
    [data-testid="stSidebar"] {display: none;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    .stApp { background-color: #f5f7fa !important; }
    .main .block-container {
        padding-top: 0px !important;
        padding-left: 0px !important;
        padding-right: 0px !important;
        max-width: 100% !important;
        background-color: #f5f7fa !important;
    }

    .hsg-header {
        background: white;
        padding: 18px 48px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        border-bottom: 1px solid #dde3ec;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    }
    .hsg-logo-wrap { display:flex; align-items:center; gap:20px; }
    .hsg-logo-text span.top { display:block; font-size:12px; font-weight:500; color:#5f7a9e; letter-spacing:2px; text-transform:uppercase; }
    .hsg-logo-text span.bottom { display:block; font-size:36px; font-weight:900; color:#1a3a6b; letter-spacing:-1px; line-height:1; }
    .hsg-header-right { text-align:right; font-size:12px; color:#666; }
    .hsg-header-right b { color:#1a3a6b; font-size:13px; }

    .hero-section { background: linear-gradient(135deg, #1a3a6b 0%, #1565c0 60%, #1a73e8 100%); padding: 60px 48px 50px; color: white; }
    .hero-title { font-size:38px; font-weight:800; margin-bottom:10px; letter-spacing:-0.5px; }
    .hero-sub { font-size:16px; opacity:0.85; max-width:600px; line-height:1.6; margin-bottom:32px; }
    .hero-stats { display:flex; gap:32px; flex-wrap:wrap; }
    .hero-stat { text-align:center; }
    .hero-stat-num { font-size:36px; font-weight:800; line-height:1; }
    .hero-stat-label { font-size:12px; opacity:0.75; text-transform:uppercase; letter-spacing:1px; margin-top:4px; }
    .hero-divider { width:1px; background:rgba(255,255,255,0.25); height:50px; align-self:center; }

    .info-section { padding:40px 48px; background:#f5f7fa; }
    .info-grid { display:grid; grid-template-columns:repeat(3,1fr); gap:20px; margin-bottom:32px; }
    .info-card { background:white; border-radius:12px; padding:28px 24px; box-shadow:0 1px 6px rgba(0,0,0,0.06); border-top:4px solid #1a73e8; }
    .info-card.verde { border-top-color:#34a853; }
    .info-card.naranja { border-top-color:#f9ab00; }
    .info-card.rojo { border-top-color:#ea4335; }
    .info-card.morado { border-top-color:#7c4dff; }
    .info-card.celeste { border-top-color:#00acc1; }
    .info-card-title { font-size:13px; font-weight:700; color:#1a3a6b; text-transform:uppercase; letter-spacing:0.8px; margin-bottom:12px; }
    .info-card-body { font-size:13.5px; color:#444; line-height:1.7; }

    .esp-grid { display:grid; grid-template-columns:repeat(5,1fr); gap:12px; margin-top:8px; }
    .esp-item { background:white; border-radius:8px; padding:14px 12px; text-align:center; font-size:12px; color:#1a3a6b; font-weight:600; box-shadow:0 1px 4px rgba(0,0,0,0.06); border:1px solid #e8eaed; }
    .esp-dot { width:10px; height:10px; background:#1a73e8; border-radius:50%; margin:0 auto 8px; }

    .hsg-section-title { font-size:22px; font-weight:700; color:#1a3a6b; margin-bottom:4px; }
    .hsg-section-sub { font-size:13px; color:#666; margin-bottom:22px; }

    .badge-confirmada { background:#e6f4ea; color:#137333; padding:4px 14px; border-radius:20px; font-size:12px; font-weight:700; }
    .badge-pendiente  { background:#fef7e0; color:#b06000; padding:4px 14px; border-radius:20px; font-size:12px; font-weight:700; }
    .badge-cancelada  { background:#fce8e6; color:#c5221f; padding:4px 14px; border-radius:20px; font-size:12px; font-weight:700; }
    .badge-ausente    { background:#f1f3f4; color:#444;    padding:4px 14px; border-radius:20px; font-size:12px; font-weight:700; }

    .urg-alta  { background:#fce8e6; color:#c5221f; padding:3px 12px; border-radius:20px; font-size:12px; font-weight:700; border:1px solid #f5c6c6; }
    .urg-media { background:#fef7e0; color:#b06000; padding:3px 12px; border-radius:20px; font-size:12px; font-weight:700; border:1px solid #fde9a2; }
    .urg-baja  { background:#e6f4ea; color:#137333; padding:3px 12px; border-radius:20px; font-size:12px; font-weight:700; border:1px solid #b7dfbf; }

    .cita-card { background:white; border-radius:10px; border-left:5px solid #1a73e8; padding:18px 22px; margin-bottom:12px; box-shadow:0 1px 4px rgba(0,0,0,0.07); }
    .cita-card.confirmada { border-left-color:#34a853; }
    .cita-card.pendiente  { border-left-color:#f9ab00; }
    .cita-card.cancelada  { border-left-color:#ea4335; }
    .cita-card.ausente    { border-left-color:#9aa0a6; }
    .cita-card-header { display:flex; justify-content:space-between; align-items:center; margin-bottom:12px; }
    .cita-nombre { font-size:15px; font-weight:700; color:#1a3a6b; }
    .cita-badges { display:flex; gap:8px; align-items:center; }
    .cita-info { font-size:13px; color:#555; margin-bottom:2px; }

    /* AGENDA MEDICO */
    .medico-card { background:white; border-radius:10px; padding:16px 20px; margin-bottom:10px; box-shadow:0 1px 4px rgba(0,0,0,0.07); border-left:4px solid #1a73e8; }
    .medico-nombre { font-size:14px; font-weight:700; color:#1a3a6b; margin-bottom:8px; }
    .slot-grid { display:flex; flex-wrap:wrap; gap:6px; }
    .slot-libre { background:#e6f4ea; color:#137333; padding:4px 10px; border-radius:6px; font-size:12px; font-weight:600; cursor:pointer; }
    .slot-ocupado { background:#fce8e6; color:#c5221f; padding:4px 10px; border-radius:6px; font-size:12px; font-weight:600; text-decoration:line-through; }

    hr { border-color:#e8eaed; margin:16px 0; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# MEDICOS POR ESPECIALIDAD
# ─────────────────────────────────────────────
MEDICOS = {
    "Cardiologia": ["Dr. Roberto Fuentes", "Dra. Carmen Ortega"],
    "Traumatologia": ["Dr. Felipe Rojas", "Dr. Andres Vega"],
    "Neurologia": ["Dra. Patricia Medina", "Dr. Carlos Silva"],
    "Ginecologia": ["Dra. Valentina Torres", "Dra. Isabel Reyes"],
    "Oftalmologia": ["Dr. Diego Morales", "Dra. Elena Castro"],
    "Urologia": ["Dr. Marcelo Diaz", "Dr. Hector Espinoza"],
    "Dermatologia": ["Dra. Sofia Alvarez", "Dr. Gabriel Munoz"],
    "Endocrinologia": ["Dra. Claudia Vargas", "Dr. Nicolas Herrera"],
    "Gastroenterologia": ["Dr. Rodrigo Lopez", "Dra. Francisca Jimenez"],
    "Reumatologia": ["Dra. Ana Gonzalez", "Dr. Sebastian Cortez"],
}

DIAS_SEMANA = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes"]
HORARIOS = ["08:30", "09:00", "09:30", "10:00", "10:30", "11:00",
            "11:30", "14:00", "14:30", "15:00", "15:30", "16:00"]

def sync_agenda():
    """Reconstruye la agenda completa desde el estado actual de las citas."""
    if "agenda" not in st.session_state:
        return
    # Limpiar y reconstruir
    hoy_s = datetime.today().replace(hour=0,minute=0,second=0,microsecond=0)
    todas_fechas = [(hoy_s + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(60)]
    # Reiniciar todas las fechas futuras a None
    for medico in st.session_state.agenda:
        for fecha in todas_fechas:
            if fecha not in st.session_state.agenda[medico]:
                st.session_state.agenda[medico][fecha] = {h: None for h in HORARIOS}
            else:
                for hora in HORARIOS:
                    st.session_state.agenda[medico][fecha][hora] = None
    # Recargar desde citas actuales (solo Confirmada y Pendiente)
    for _, row in st.session_state.citas[
        st.session_state.citas["estado"].isin(["Confirmada","Pendiente"])
    ].iterrows():
        medico = row.get("medico","")
        fecha  = row.get("fecha","")
        hora   = row.get("hora","")
        if medico in st.session_state.agenda:
            if fecha not in st.session_state.agenda[medico]:
                st.session_state.agenda[medico][fecha] = {h: None for h in HORARIOS}
            if hora in HORARIOS:
                st.session_state.agenda[medico][fecha][hora] = row["nombre_paciente"]

def get_semana_actual():
    hoy = datetime.today()
    lunes = hoy - timedelta(days=hoy.weekday())
    return [(lunes + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(5)]

@st.cache_data
def generar_datos():
    random.seed(42)
    np.random.seed(42)
    nombres = ["Ana","Maria","Juan","Carlos","Luis","Rosa","Pedro","Elena","Jorge","Carmen",
               "Felipe","Isabel","Diego","Claudia","Rodrigo","Patricia","Andres","Veronica",
               "Tomas","Francisca","Gabriel","Valentina","Ignacio","Sofia","Sebastian","Daniela",
               "Matias","Camila","Nicolas","Alejandra","Cristobal","Javiera","Mauricio","Lorena",
               "Roberto","Cecilia","Marcelo","Pilar","Hector","Beatriz"]
    apellidos = ["Gonzalez","Munoz","Rodriguez","Lopez","Martinez","Perez","Sanchez","Ramirez",
                 "Torres","Flores","Rivera","Morales","Jimenez","Ortega","Herrera","Medina",
                 "Castro","Rojas","Vargas","Alvarez","Reyes","Diaz","Vega","Contreras","Ramos",
                 "Espinoza","Fuentes","Cortes","Miranda","Silva"]
    especialidades = list(MEDICOS.keys())
    comunas = ["Concepcion","Talcahuano","San Pedro","Chiguayante","Penco","Tome","Coronel",
               "Lota","Lebu","Los Angeles","Chillan","Arauco","Canete","Tirua","Curanilahue"]
    causas_ausencia = ["No sabia que tenia hora","Olvido la cita","Problemas de transporte",
                       "Trabajaba y no pudo ausentarse","Enfermedad intercurrente",
                       "Contacto invalido","Error de agenda"]
    pacientes = []
    for i in range(1, 2001):
        pacientes.append({
            "id_paciente": f"P{i:04d}",
            "nombre": f"{random.choice(nombres)} {random.choice(apellidos)} {random.choice(apellidos)}",
            "edad": random.randint(18, 85),
            "rut": f"{random.randint(5000000,25000000)}-{random.randint(0,9)}",
            "telefono": f"+569{random.randint(10000000,99999999)}",
            "comuna": random.choice(comunas),
            "contacto_valido": random.random() > 0.15
        })
    df_pac = pd.DataFrame(pacientes)
    hoy = datetime.today().replace(hour=0,minute=0,second=0,microsecond=0)
    citas = []
    for j in range(1,601):
        pac = df_pac.sample(1).iloc[0]
        estado = random.choices(["Pendiente","Confirmada","Cancelada","Ausente"],weights=[45,30,15,10])[0]
        urgencia = random.choices(["Alta","Media","Baja"],weights=[20,45,35])[0]
        esp = random.choice(especialidades)
        medico = random.choice(MEDICOS[esp])
        citas.append({
            "id_cita": f"C{j:04d}",
            "nombre_paciente": pac["nombre"],
            "edad": pac["edad"],
            "rut": pac["rut"],
            "telefono": pac["telefono"],
            "comuna": pac["comuna"],
            "especialidad": esp,
            "medico": medico,
            "fecha": (hoy+timedelta(days=random.randint(0,29))).strftime("%Y-%m-%d"),
            "hora": random.choice(HORARIOS),
            "estado": estado,
            "urgencia": urgencia if urgencia in ["Alta","Media","Baja"] else "Media",
            "causa_ausencia": random.choice(causas_ausencia) if estado=="Ausente" else "",
            "contacto_valido": pac["contacto_valido"]
        })
    df_citas = pd.DataFrame(citas)
    espera = []
    for k in range(1,301):
        pac = df_pac.sample(1).iloc[0]
        esp = random.choice(especialidades)
        espera.append({
            "id_espera": f"E{k:04d}",
            "nombre": pac["nombre"],
            "rut": pac["rut"],
            "telefono": pac["telefono"],
            "comuna": pac["comuna"],
            "especialidad": esp,
            "fecha_ingreso_espera": (hoy-timedelta(days=random.randint(1,180))).strftime("%Y-%m-%d"),
            "prioridad": random.choices(["Alta","Media","Baja"],weights=[25,45,30])[0],
            "estado_espera": random.choices(["Esperando","Asignado"],weights=[80,20])[0]
        })
        df_citas["urgencia"] = df_citas["urgencia"].replace({"Media":"Media","Media":"Media"})
    return df_pac, df_citas, pd.DataFrame(espera)

if "citas" not in st.session_state:
    _, df_c, df_e = generar_datos()
    df_c['urgencia'] = df_c['urgencia'].replace({'Media': 'Media', 'Media': 'Media'})
    st.session_state.citas = df_c.copy()
    st.session_state.citas["urgencia"] = st.session_state.citas["urgencia"].apply(
        lambda x: x if x in ["Alta","Media","Baja"] else "Media"
    )
    st.session_state.citas["urgencia"] = st.session_state.citas["urgencia"].map(
        lambda x: "Media" if x not in ["Alta","Media","Baja"] else x
    )
    st.session_state.espera = df_e.copy()

    # Agenda cubre los proximos 30 dias
    hoy_ag = datetime.today().replace(hour=0,minute=0,second=0,microsecond=0)
    todas_fechas = [(hoy_ag+timedelta(days=i)).strftime("%Y-%m-%d") for i in range(30)]

    st.session_state.agenda = {}
    for esp, medicos in MEDICOS.items():
        for medico in medicos:
            st.session_state.agenda[medico] = {}
            for fecha in todas_fechas:
                st.session_state.agenda[medico][fecha] = {h: None for h in HORARIOS}

    # Cargar TODAS las citas confirmadas en la agenda
    for _, row in st.session_state.citas[st.session_state.citas["estado"]=="Confirmada"].iterrows():
        medico = row.get("medico","")
        fecha  = row.get("fecha","")
        hora   = row.get("hora","")
        if medico in st.session_state.agenda:
            if fecha not in st.session_state.agenda[medico]:
                st.session_state.agenda[medico][fecha] = {h: None for h in HORARIOS}
            if hora in st.session_state.agenda[medico][fecha]:
                st.session_state.agenda[medico][fecha][hora] = row["nombre_paciente"]

if "modulo" not in st.session_state:
    st.session_state.modulo = "inicio"

df_citas  = st.session_state.citas
df_espera = st.session_state.espera

# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
st.markdown(f"""
<div class="hsg-header">
  <div class="hsg-logo-wrap">
    <svg width="58" height="58" viewBox="0 0 58 58" xmlns="http://www.w3.org/2000/svg">
      <rect width="58" height="58" rx="12" fill="#1a3a6b"/>
      <rect x="25" y="10" width="8" height="38" rx="3" fill="white"/>
      <rect x="10" y="25" width="38" height="8" rx="3" fill="white"/>
      <circle cx="29" cy="29" r="25" fill="none" stroke="#1a73e8" stroke-width="2.5"/>
    </svg>
    <div class="hsg-logo-text">
      <span class="top">Red Asistencial Sur &nbsp;·&nbsp; Servicio de Salud Biobio</span>
      <span class="bottom">Hospital San Gabriel</span>
    </div>
  </div>
  <div class="hsg-header-right">
    <b>Sistema de Gestion de Consultas</b><br>
    {datetime.today().strftime('%d/%m/%Y')} &nbsp;|&nbsp; Usuario: Admin OIRS
  </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# NAVEGACION
# ─────────────────────────────────────────────
modulos_nav = [
    ("inicio","Inicio"),("dashboard","Panel de Control"),
    ("confirmacion","Confirmacion de Citas"),
    ("espera","Lista de Espera"),("reportes","Reportes de Ausentismo"),
    ("agenda_semana","Agenda Proxima Semana"),
    ("calendario","Calendario Anual"),
]
cols_nav = st.columns(len(modulos_nav))
for i,(key,label) in enumerate(modulos_nav):
    with cols_nav[i]:
        if st.button(label, key=f"nav_{key}", use_container_width=True,
                     type="primary" if st.session_state.modulo==key else "secondary"):
            st.session_state.modulo = key
            st.rerun()

st.markdown("<hr style='margin:0;border-color:#dde3ec;'>", unsafe_allow_html=True)
modulo = st.session_state.modulo

# ─────────────────────────────────────────────
# INICIO
# ─────────────────────────────────────────────
if modulo == "inicio":
    st.markdown("""
    <div class="hero-section">
        <div class="hero-title">Bienvenido al Hospital San Gabriel</div>
        <div class="hero-sub">Hospital publico de alta complejidad al servicio de la comunidad del sur de Chile. Comprometidos con la salud, el acceso equitativo y la calidad de atencion de mas de 420.000 personas de la region del Biobio.</div>
        <div class="hero-stats">
            <div class="hero-stat"><div class="hero-stat-num">320</div><div class="hero-stat-label">Camas disponibles</div></div>
            <div class="hero-divider"></div>
            <div class="hero-stat"><div class="hero-stat-num">6</div><div class="hero-stat-label">Pabellones quirurgicos</div></div>
            <div class="hero-divider"></div>
            <div class="hero-stat"><div class="hero-stat-num">1.800+</div><div class="hero-stat-label">Funcionarios</div></div>
            <div class="hero-divider"></div>
            <div class="hero-stat"><div class="hero-stat-num">420.000</div><div class="hero-stat-label">Personas atendidas</div></div>
            <div class="hero-divider"></div>
            <div class="hero-stat"><div class="hero-stat-num">10</div><div class="hero-stat-label">Especialidades medicas</div></div>
        </div>
    </div>
    <div class="info-section">
        <div class="info-grid">
            <div class="info-card"><div class="info-card-title">Nuestra Mision</div><div class="info-card-body">Proveer atencion medica integral, oportuna y de calidad a la poblacion del sur de Chile, con enfasis en la equidad, el respeto a la dignidad del paciente y la mejora continua de los procesos clinicos y administrativos.</div></div>
            <div class="info-card verde"><div class="info-card-title">Nuestra Vision</div><div class="info-card-body">Ser el hospital publico de referencia del sur de Chile, reconocido por la excelencia clinica, la innovacion en gestion hospitalaria y el compromiso con el bienestar de las comunidades que atendemos.</div></div>
            <div class="info-card naranja"><div class="info-card-title">Nuestros Valores</div><div class="info-card-body"><ul style="padding-left:16px;margin:0;"><li>Compromiso con el paciente</li><li>Transparencia y probidad</li><li>Trabajo colaborativo</li><li>Mejora continua</li><li>Respeto e inclusion</li></ul></div></div>
            <div class="info-card rojo"><div class="info-card-title">Urgencias 24/7</div><div class="info-card-body">Nuestro servicio de urgencias opera las 24 horas del dia, los 7 dias de la semana, con equipos clinicos especializados en atencion de emergencias y trauma. Contamos con 2 pabellones de urgencia permanentes.</div></div>
            <div class="info-card morado"><div class="info-card-title">Red Asistencial</div><div class="info-card-body">Recibimos derivaciones desde mas de 15 CESFAM y hospitales comunitarios de la red asistencial del Biobio, coordinando la atencion de pacientes desde comunas como Tirua, Canete y Lebu.</div></div>
            <div class="info-card celeste"><div class="info-card-title">Acreditacion</div><div class="info-card-body">Hospital acreditado por la Superintendencia de Salud bajo los estandares de calidad del Ministerio de Salud de Chile. En proceso de certificacion ISO 9001 en procesos de gestion clinica y administrativa.</div></div>
        </div>
        <div style="background:white;border-radius:12px;padding:28px 24px;box-shadow:0 1px 6px rgba(0,0,0,0.06);margin-bottom:20px;">
            <div class="info-card-title" style="margin-bottom:16px;">Especialidades Medicas Disponibles</div>
            <div class="esp-grid">
                <div class="esp-item"><div class="esp-dot"></div>Cardiologia</div>
                <div class="esp-item"><div class="esp-dot" style="background:#34a853"></div>Traumatologia</div>
                <div class="esp-item"><div class="esp-dot" style="background:#ea4335"></div>Neurologia</div>
                <div class="esp-item"><div class="esp-dot" style="background:#f9ab00"></div>Ginecologia</div>
                <div class="esp-item"><div class="esp-dot" style="background:#7c4dff"></div>Oftalmologia</div>
                <div class="esp-item"><div class="esp-dot" style="background:#00acc1"></div>Urologia</div>
                <div class="esp-item"><div class="esp-dot" style="background:#e91e63"></div>Dermatologia</div>
                <div class="esp-item"><div class="esp-dot" style="background:#ff7043"></div>Endocrinologia</div>
                <div class="esp-item"><div class="esp-dot" style="background:#43a047"></div>Gastroenterologia</div>
                <div class="esp-item"><div class="esp-dot" style="background:#1a3a6b"></div>Reumatologia</div>
            </div>
        </div>
        <div style="background:#1a3a6b;border-radius:12px;padding:24px 28px;color:white;display:flex;justify-content:space-between;align-items:center;">
            <div>
                <div style="font-size:15px;font-weight:700;margin-bottom:4px;">Horario de Atencion</div>
                <div style="font-size:13px;opacity:0.8;">Consultas de especialidad: Lunes a Viernes, 08:00 - 17:00 hrs &nbsp;|&nbsp; Urgencias: 24 horas &nbsp;|&nbsp; Cirugias electivas: Lunes a Viernes, 07:30 - 16:00 hrs</div>
            </div>
            <div style="text-align:right;font-size:13px;opacity:0.8;">
                <div style="font-weight:700;font-size:15px;margin-bottom:4px;">Contacto OIRS</div>
                <div>+56 41 234 5678</div>
                <div>oirs@hospitalsangabriel.cl</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# PANEL DE CONTROL
# ─────────────────────────────────────────────
elif modulo == "dashboard":
    st.markdown("<div style='padding:24px 8px;'>", unsafe_allow_html=True)
    st.markdown("<div class='hsg-section-title'>Panel de Control</div>", unsafe_allow_html=True)
    st.markdown("<div class='hsg-section-sub'>Resumen de actividad — proximos 7 dias</div>", unsafe_allow_html=True)

    hoy_str = datetime.today().strftime("%Y-%m-%d")
    prox7   = (datetime.today()+timedelta(days=7)).strftime("%Y-%m-%d")
    semana  = df_citas[(df_citas["fecha"]>=hoy_str)&(df_citas["fecha"]<=prox7)]
    total = len(semana); conf=len(semana[semana["estado"]=="Confirmada"])
    pend=len(semana[semana["estado"]=="Pendiente"]); ausen=len(semana[semana["estado"]=="Ausente"])

    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Total citas semana", total)
    c2.metric("Confirmadas", conf, f"{round(conf/total*100) if total else 0}%")
    c3.metric("Pendientes de confirmar", pend, delta_color="inverse", delta=f"-{pend}")
    c4.metric("Ausencias registradas", ausen)
    st.divider()

    col_a,col_b = st.columns(2)
    with col_a:
        st.markdown("**Citas por especialidad**")
        esp = semana.groupby("especialidad").size().reset_index(name="Total")
        esp = esp.sort_values("Total",ascending=True)
        colores_esp=["#1a3a6b","#1565c0","#1a73e8","#2196f3","#42a5f5","#64b5f6","#90caf9","#34a853","#00acc1","#7c4dff"]
        fig=px.bar(esp,x="Total",y="especialidad",orientation="h",color="especialidad",
                   color_discrete_sequence=colores_esp,text="Total")
        fig.update_traces(textposition="outside",textfont_size=12)
        fig.update_layout(margin=dict(l=0,r=40,t=10,b=0),height=340,xaxis_title="",yaxis_title="",
                          plot_bgcolor="white",paper_bgcolor="white",showlegend=False,
                          xaxis=dict(showgrid=True,gridcolor="#f0f0f0"),
                          yaxis=dict(tickfont=dict(size=13,color="#1a3a6b")))
        st.plotly_chart(fig,use_container_width=True)
    with col_b:
        st.markdown("**Distribucion de estados**")
        ec=semana["estado"].value_counts().reset_index(); ec.columns=["estado","cantidad"]
        cm={"Confirmada":"#34a853","Pendiente":"#f9ab00","Cancelada":"#ea4335","Ausente":"#9aa0a6"}
        fig2=px.pie(ec,names="estado",values="cantidad",color="estado",color_discrete_map=cm,hole=0.45)
        fig2.update_traces(textposition="inside",textinfo="percent+label",textfont_size=13)
        fig2.update_layout(margin=dict(l=0,r=0,t=10,b=0),height=340,paper_bgcolor="white",
                           legend=dict(orientation="h",y=-0.1))
        st.plotly_chart(fig2,use_container_width=True)

    st.markdown("**Citas pendientes de confirmar esta semana**")
    pdf=semana[semana["estado"]=="Pendiente"][["id_cita","nombre_paciente","rut","especialidad","urgencia","fecha","hora","telefono","comuna"]].copy()
    pdf.columns=["ID","Paciente","RUT","Especialidad","Urgencia","Fecha","Hora","Telefono","Comuna"]
    st.dataframe(pdf,use_container_width=True,hide_index=True)

# ─────────────────────────────────────────────
# CONFIRMACION DE CITAS
# ─────────────────────────────────────────────
elif modulo == "confirmacion":
    st.markdown("<div style='padding:24px 8px;'>", unsafe_allow_html=True)
    st.markdown("<div class='hsg-section-title'>Confirmacion de Citas</div>", unsafe_allow_html=True)
    st.markdown("<div class='hsg-section-sub'>Busca una cita para confirmar, cancelar o registrar ausencia</div>", unsafe_allow_html=True)

    col_f1,col_f2,col_f3,col_f4=st.columns([2,1.5,1,1])
    with col_f1: busqueda=st.text_input("Buscar por nombre, RUT o ID",placeholder="Ej: Gonzalez / 12345678-9 / C0023")
    with col_f2: filtro_esp=st.selectbox("Especialidad",["Todas"]+sorted(df_citas["especialidad"].unique().tolist()), key="conf_esp")
    with col_f3: filtro_estado=st.selectbox("Estado",["Todos","Pendiente","Confirmada","Cancelada","Ausente"], key="conf_estado")
    with col_f4: filtro_urg=st.selectbox("Urgencia",["Todas","Alta","Media","Baja"], key="conf_urg")

    mask=pd.Series([True]*len(df_citas),index=df_citas.index)
    if busqueda:
        b=busqueda.lower()
        mask=(df_citas["nombre_paciente"].str.lower().str.contains(b)|
              df_citas["rut"].str.lower().str.contains(b)|
              df_citas["id_cita"].str.lower().str.contains(b))
    if filtro_esp!="Todas": mask=mask&(df_citas["especialidad"]==filtro_esp)
    if filtro_estado!="Todos": mask=mask&(df_citas["estado"]==filtro_estado)
    if filtro_urg!="Todas": mask=mask&(df_citas["urgencia"]==filtro_urg)

    resultados = df_citas[mask].reset_index(drop=True).head(30)
    st.caption(f"{len(resultados)} resultado(s) encontrados")

    for _,row in resultados.iterrows():
        estado=row["estado"]; urgencia=row["urgencia"]
        clase=estado.lower(); urg_clase=urgencia.lower()
        contacto_color="#137333" if row["contacto_valido"] else "#c5221f"
        contacto_txt="Valido" if row["contacto_valido"] else "Invalido — actualizar"
        st.markdown(f"""
        <div class="cita-card {clase}">
            <div class="cita-card-header">
                <div class="cita-nombre">{row['nombre_paciente']}</div>
                <div class="cita-badges">
                    <span style="font-size:12px;color:#666;margin-right:4px;">Urgencia:</span>
                    <span class="urg-{urg_clase}">{urgencia}</span>
                    &nbsp;&nbsp;
                    <span style="font-size:12px;color:#666;margin-right:4px;">Estado:</span>
                    <span class="badge-{clase}">{estado}</span>
                </div>
            </div>
            <div style="display:flex;gap:36px;flex-wrap:wrap;">
                <div class="cita-info"><b>Especialidad:</b> {row['especialidad']}</div>
                <div class="cita-info"><b>Medico:</b> {row.get('medico','—')}</div>
                <div class="cita-info"><b>Fecha:</b> {datetime.strptime(row['fecha'], '%Y-%m-%d').strftime('%d de %B de %Y')} — {row['hora']} hrs</div>
                <div class="cita-info"><b>RUT:</b> {row['rut']}</div>
                <div class="cita-info"><b>Telefono:</b> {row['telefono']}</div>
                <div class="cita-info"><b>Comuna:</b> {row['comuna']}</div>
                <div class="cita-info"><b>Edad:</b> {row['edad']} anos</div>
                <div class="cita-info"><b>Contacto:</b> <span style="color:{contacto_color};font-weight:600;">{contacto_txt}</span></div>
                <div class="cita-info"><b>ID:</b> {row['id_cita']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        # ── Disponibilidad del medico asignado
        medico_actual = row.get("medico","")
        esp_actual    = row["especialidad"]
        if medico_actual and medico_actual in st.session_state.agenda:
            # Semana de la cita
            fecha_cita = datetime.strptime(row["fecha"], "%Y-%m-%d")
            dia_semana = fecha_cita.weekday()
            # Siempre ir al lunes de esa semana (sin importar fin de semana)
            lunes_cita = fecha_cita - timedelta(days=dia_semana)
            fechas_semana_cita = [(lunes_cita + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(5)]
            dias_labels  = ["Lunes","Martes","Miercoles","Jueves","Viernes"]
            semana_label = f"{lunes_cita.strftime('%d/%m')} al {(lunes_cita+timedelta(days=4)).strftime('%d/%m/%Y')}"
            agenda_med   = st.session_state.agenda[medico_actual]

            # Sincronizar agenda antes de mostrar
            sync_agenda()
            agenda_med = st.session_state.agenda[medico_actual]

            # Asegurar que las fechas de la semana existan
            for fecha in fechas_semana_cita:
                if fecha not in agenda_med:
                    agenda_med[fecha] = {h: None for h in HORARIOS}

            with st.expander(f"Ver disponibilidad de {medico_actual} — semana del {semana_label}"):
                tabla_data = []
                for hora in HORARIOS:
                    fila = {"Hora": hora}
                    for i, fecha in enumerate(fechas_semana_cita):
                        ocupado = agenda_med.get(fecha, {}).get(hora, None)
                        fila[dias_labels[i]] = f"Ocupado: {str(ocupado)[:14]}..." if ocupado else "Disponible"
                    tabla_data.append(fila)

                df_ag = pd.DataFrame(tabla_data).set_index("Hora")

                def color_ag(val):
                    if "Ocupado" in str(val):
                        return "background-color:#fce8e6;color:#c5221f;font-weight:600;"
                    return "background-color:#e6f4ea;color:#137333;font-weight:600;"

                st.dataframe(df_ag.style.map(color_ag), use_container_width=True, height=380)

                # Reasignar hora
                st.markdown("**Reasignar hora para este paciente**")
                st.caption("Se muestran solo fechas con horas disponibles. Si no aparece la semana de la cita es porque el medico no tiene horas libres esa semana.")
                rc1, rc2, rc3 = st.columns(3)
                dias_libres = []
                for i, fecha in enumerate(fechas_semana_cita):
                    horas_libres = [h for h,p in agenda_med.get(fecha,{}).items() if p is None]
                    if horas_libres:
                        label = f"{dias_labels[i]} {datetime.strptime(fecha,'%Y-%m-%d').strftime('%d/%m')}"
                        dias_libres.append((label, fecha))

                if dias_libres:
                    dia_r   = rc1.selectbox("Dia", [d[0] for d in dias_libres], key=f"dia_r_{row['id_cita']}")
                    fecha_r = dict(dias_libres)[dia_r]
                    horas_r = [h for h,p in agenda_med.get(fecha_r,{}).items() if p is None]
                    hora_r  = rc2.selectbox("Hora disponible", horas_r, key=f"hora_r_{row['id_cita']}")
                    if rc3.button("Reasignar", key=f"reasig_{row['id_cita']}"):
                        hora_ant  = row["hora"]; fecha_ant = row["fecha"]
                        if fecha_ant in agenda_med and hora_ant in agenda_med.get(fecha_ant,{}):
                            st.session_state.agenda[medico_actual][fecha_ant][hora_ant] = None
                        if fecha_r not in st.session_state.agenda[medico_actual]:
                            st.session_state.agenda[medico_actual][fecha_r] = {h: None for h in HORARIOS}
                        st.session_state.agenda[medico_actual][fecha_r][hora_r] = row["nombre_paciente"]
                        idx = st.session_state.citas[st.session_state.citas["id_cita"]==row["id_cita"]].index
                        st.session_state.citas.loc[idx,"fecha"]  = fecha_r
                        st.session_state.citas.loc[idx,"hora"]   = hora_r
                        st.session_state.citas.loc[idx,"estado"] = "Confirmada"
                        st.success(f"Hora reasignada: {dia_r} {hora_r}")
                        st.rerun()
                else:
                    st.warning(f"{medico_actual} no tiene horas disponibles en la semana de la cita.")

                # Otros medicos misma especialidad
                otros_medicos = [m for m in MEDICOS.get(esp_actual,[]) if m != medico_actual]
                if otros_medicos:
                    st.markdown("**Disponibilidad de otros medicos en la misma especialidad**")
                    for otro in otros_medicos:
                        agenda_otro = st.session_state.agenda.get(otro, {})
                        horas_tot   = sum(1 for f in fechas_semana_cita for h,p in agenda_otro.get(f,{}).items() if p is None)
                        color_disp  = "#137333" if horas_tot > 0 else "#c5221f"
                        st.markdown(f"<span style='color:{color_disp};font-weight:600;'>{otro}</span> — {horas_tot} horas disponibles esa semana", unsafe_allow_html=True)

        b1,b2,b3,_=st.columns([1,1,1,2])
        if b1.button("Confirmar asistencia",key=f"conf_{row['id_cita']}"):
            st.session_state.citas.loc[st.session_state.citas["id_cita"]==row["id_cita"],"estado"]="Confirmada"
            sync_agenda()
            st.success(f"Cita de {row['nombre_paciente']} confirmada.")
            st.rerun()
        if b2.button("Cancelar y liberar cupo",key=f"canc_{row['id_cita']}"):
            st.session_state.citas.loc[st.session_state.citas["id_cita"]==row["id_cita"],"estado"]="Cancelada"
            sync_agenda()
            st.warning(f"Cupo de {row['nombre_paciente']} liberado.")
            st.rerun()
        if b3.button("Registrar ausencia",key=f"aus_{row['id_cita']}"):
            st.session_state.citas.loc[st.session_state.citas["id_cita"]==row["id_cita"],"estado"]="Ausente"
            sync_agenda()
            st.error(f"Ausencia de {row['nombre_paciente']} registrada.")
            st.rerun()
        st.markdown("<hr>",unsafe_allow_html=True)

# ─────────────────────────────────────────────
# LISTA DE ESPERA + AGENDA MEDICO
# ─────────────────────────────────────────────
elif modulo == "espera":
    st.markdown("<div style='padding:24px 8px;'>", unsafe_allow_html=True)
    st.markdown("<div class='hsg-section-title'>Lista de Espera</div>", unsafe_allow_html=True)
    st.markdown("<div class='hsg-section-sub'>Reasignacion de cupos — agenda de medicos disponibles</div>", unsafe_allow_html=True)

    # ── Pacientes en espera
    ea = df_espera[df_espera["estado_espera"]=="Esperando"].copy()
    ea["orden"] = ea["prioridad"].map({"Alta":0,"Media":1,"Baja":2})
    ea = ea.sort_values(["orden","fecha_ingreso_espera"])

    col1, col2 = st.columns([1,2])

    with col1:
        st.markdown("**Pacientes en lista de espera**")
        filtro_esp_e = st.selectbox("Filtrar por especialidad",
            ["Todas"]+sorted(df_espera["especialidad"].unique().tolist()), key="esp_espera")
        if filtro_esp_e != "Todas":
            ea = ea[ea["especialidad"]==filtro_esp_e]

        def color_p(val):
            return {"Alta":"background-color:#fce8e6;color:#c5221f",
                    "Media":"background-color:#fef7e0;color:#b06000",
                    "Baja":"background-color:#e6f4ea;color:#137333"}.get(val,"")

        styled = ea[["nombre","especialidad","prioridad","fecha_ingreso_espera","comuna"]]\
                   .rename(columns={"nombre":"Paciente","especialidad":"Especialidad",
                                    "prioridad":"Prioridad","fecha_ingreso_espera":"En espera desde",
                                    "comuna":"Comuna"}).head(20)\
                   .style.map(color_p, subset=["Prioridad"])
        st.dataframe(styled, use_container_width=True, hide_index=True)

    with col2:
        st.markdown("**Agenda de disponibilidad medica**")

        # Seleccion de especialidad y medico
        esp_sel    = st.selectbox("Especialidad", sorted(MEDICOS.keys()), key="esp_agenda")
        medico_sel = st.selectbox("Medico", MEDICOS[esp_sel], key="med_agenda")
        agenda_medico = st.session_state.agenda.get(medico_sel, {})

        # Selector de semana por fecha
        hoy_esp = datetime.today().replace(hour=0,minute=0,second=0,microsecond=0)
        semanas_disponibles = []
        for i in range(5):  # proximas 5 semanas
            lunes = hoy_esp + timedelta(days=(7*i - hoy_esp.weekday()))
            viernes = lunes + timedelta(days=4)
            label = f"{lunes.strftime('%d %b')} — {viernes.strftime('%d %b %Y')}"
            semanas_disponibles.append((label, lunes))

        semana_label = st.selectbox(
            "Semana a visualizar",
            [s[0] for s in semanas_disponibles],
            key="semana_agenda"
        )
        lunes_sel = dict(semanas_disponibles)[semana_label]
        fechas_semana_esp = [(lunes_sel + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(5)]

        # Asegurar fechas en agenda
        for fecha in fechas_semana_esp:
            if fecha not in agenda_medico:
                agenda_medico[fecha] = {h: None for h in HORARIOS}

        st.markdown(f"**Disponibilidad — {medico_sel} — semana del {semana_label}**")

        dias_labels = ["Lunes","Martes","Miercoles","Jueves","Viernes"]
        # Agregar fecha real debajo del dia
        dias_con_fecha = [
            f"{dias_labels[i]}\n{(lunes_sel+timedelta(days=i)).strftime('%d/%m')}"
            for i in range(5)
        ]

        tabla_data = []
        for hora in HORARIOS:
            fila = {"Hora": hora}
            for i, fecha in enumerate(fechas_semana_esp):
                ocupado = agenda_medico.get(fecha, {}).get(hora, None)
                col_key = f"{dias_labels[i]} {(lunes_sel+timedelta(days=i)).strftime('%d/%m')}"
                fila[col_key] = f"Ocupado: {str(ocupado)[:16]}..." if ocupado else "Disponible"
            tabla_data.append(fila)

        df_agenda = pd.DataFrame(tabla_data).set_index("Hora")

        def color_celda(val):
            if "Ocupado" in str(val):
                return "background-color:#fce8e6;color:#c5221f;font-weight:600;"
            return "background-color:#e6f4ea;color:#137333;font-weight:600;"

        st.dataframe(
            df_agenda.style.map(color_celda),
            use_container_width=True, height=430
        )

        # Resumen de ocupacion
        total_slots = len(HORARIOS) * 5
        ocupados = sum(1 for f in fechas_semana_esp for h,p in agenda_medico.get(f,{}).items() if p)
        libres = total_slots - ocupados
        c_res1, c_res2, c_res3 = st.columns(3)
        c_res1.metric("Total horarios semana", total_slots)
        c_res2.metric("Ocupados", ocupados)
        c_res3.metric("Disponibles", libres)

    st.divider()

    # ── Asignacion de hora
    st.markdown("### Asignar hora a paciente en espera")
    st.caption("Selecciona el paciente, el medico, el dia y la hora disponible. Las horas ocupadas no pueden seleccionarse.")

    ca, cb, cc = st.columns([2,2,2])
    pa, pb, pc, pd_ = st.columns([2,2,2,1])

    pac_opciones = ea["nombre"].head(20).tolist() if len(ea)>0 else ["Sin pacientes"]
    pac_sel  = ca.selectbox("Paciente en espera", pac_opciones, key="pac_asignar")
    esp_asig = cb.selectbox("Especialidad", sorted(MEDICOS.keys()), key="esp_asignar")
    med_sel  = cc.selectbox("Medico", MEDICOS[esp_asig], key="med_asignar")

    # Buscar dias disponibles en los proximos 30 dias
    hoy_asig = datetime.today().replace(hour=0,minute=0,second=0,microsecond=0)
    todas_fechas_asig = [(hoy_asig+timedelta(days=i)).strftime("%Y-%m-%d") for i in range(30)
                         if (hoy_asig+timedelta(days=i)).weekday() < 5]
    dias_opciones = []
    for fecha in todas_fechas_asig:
        if fecha not in st.session_state.agenda.get(med_sel,{}):
            st.session_state.agenda.setdefault(med_sel,{})[fecha] = {h: None for h in HORARIOS}
        horas_libres = [h for h,p in st.session_state.agenda[med_sel][fecha].items() if p is None]
        if horas_libres:
            dt = datetime.strptime(fecha, "%Y-%m-%d")
            label = dt.strftime("%A %d de %B de %Y").capitalize()
            dias_opciones.append((label, fecha))

    if dias_opciones:
        dia_label = pa.selectbox("Fecha disponible", [d[0] for d in dias_opciones], key="dia_asignar")
        fecha_sel = dict(dias_opciones)[dia_label]
        horas_libres = [h for h,p in st.session_state.agenda[med_sel][fecha_sel].items() if p is None]
        hora_sel = pb.selectbox("Hora disponible", horas_libres, key="hora_asignar")

        if pc.button("Confirmar asignacion de hora", type="primary"):
            st.session_state.agenda[med_sel][fecha_sel][hora_sel] = pac_sel
            idx_esp = st.session_state.espera[st.session_state.espera["nombre"]==pac_sel].index
            if len(idx_esp)>0:
                st.session_state.espera.loc[idx_esp[0],"estado_espera"] = "Asignado"
            nueva_cita = {
                "id_cita": f"C{len(st.session_state.citas)+1:04d}",
                "nombre_paciente": pac_sel,
                "edad": 0, "rut": "—", "telefono": "—", "comuna": "—",
                "especialidad": esp_asig, "medico": med_sel,
                "fecha": fecha_sel, "hora": hora_sel,
                "estado": "Confirmada", "urgencia": "Media",
                "causa_ausencia": "", "contacto_valido": True
            }
            st.session_state.citas = pd.concat(
                [st.session_state.citas, pd.DataFrame([nueva_cita])], ignore_index=True)
            st.success(f"Cita asignada: {pac_sel} — {med_sel} — {dia_label} a las {hora_sel} hrs")
            st.rerun()
    else:
        st.warning(f"{med_sel} no tiene horas disponibles en los proximos 30 dias.")

# ─────────────────────────────────────────────
# REPORTES
# ─────────────────────────────────────────────
elif modulo == "reportes":
    st.markdown("<div style='padding:24px 8px;'>", unsafe_allow_html=True)
    st.markdown("<div class='hsg-section-title'>Reportes de Ausentismo</div>", unsafe_allow_html=True)
    st.markdown("<div class='hsg-section-sub'>Analisis estadistico basado en encuesta a pacientes ausentes (n=400)</div>", unsafe_allow_html=True)

    ausentes=df_citas[df_citas["estado"]=="Ausente"]
    total=len(df_citas); tasa=round(len(ausentes)/total*100,1) if total>0 else 0
    c1,c2,c3=st.columns(3)
    c1.metric("Total citas registradas",total)
    c2.metric("Total ausencias",len(ausentes))
    c3.metric("Tasa de ausentismo",f"{tasa}%")
    st.divider()

    causas_caso={"No sabia que tenia hora":92,"Olvido la cita":74,"Problemas de transporte":68,
                 "Trabajaba y no pudo":51,"Enfermedad intercurrente":46,
                 "Contacto invalido":39,"Error de agenda":20,"Otros":10}
    df_c2=pd.DataFrame(list(causas_caso.items()),columns=["Causa","Frecuencia"])
    df_c2=df_c2.sort_values("Frecuencia",ascending=False)
    df_c2["% acumulado"]=(df_c2["Frecuencia"].cumsum()/df_c2["Frecuencia"].sum()*100).round(1)

    col_a,col_b=st.columns(2)
    with col_a:
        st.markdown("**Diagrama de Pareto — Causas de ausentismo**")
        fig=go.Figure()
        fig.add_bar(x=df_c2["Causa"],y=df_c2["Frecuencia"],name="Frecuencia",marker_color="#1a73e8")
        fig.add_scatter(x=df_c2["Causa"],y=df_c2["% acumulado"],name="% acumulado",
                        yaxis="y2",line=dict(color="#ea4335",width=2),mode="lines+markers")
        fig.update_layout(yaxis=dict(title="Frecuencia"),
                          yaxis2=dict(title="% acumulado",overlaying="y",side="right",range=[0,110]),
                          legend=dict(orientation="h",y=-0.25),
                          margin=dict(l=0,r=0,t=10,b=0),height=360,
                          plot_bgcolor="white",paper_bgcolor="white")
        st.plotly_chart(fig,use_container_width=True)
    with col_b:
        st.markdown("**Tasa de ausentismo por especialidad**")
        ae=df_citas.groupby("especialidad").apply(
            lambda x: round(len(x[x["estado"]=="Ausente"])/len(x)*100,1)).reset_index()
        ae.columns=["Especialidad","Tasa (%)"]
        ae=ae.sort_values("Tasa (%)",ascending=True)
        fig3=px.bar(ae,x="Tasa (%)",y="Especialidad",orientation="h",
                    color="Tasa (%)",color_continuous_scale=["#e6f4ea","#ea4335"],text="Tasa (%)")
        fig3.update_traces(texttemplate="%{text}%",textposition="outside")
        fig3.update_layout(margin=dict(l=0,r=40,t=10,b=0),height=360,
                           coloraxis_showscale=False,plot_bgcolor="white",paper_bgcolor="white",
                           yaxis=dict(tickfont=dict(size=13,color="#1a3a6b")))
        st.plotly_chart(fig3,use_container_width=True)

    sc=df_citas[(df_citas["estado"]=="Ausente")&(~df_citas["contacto_valido"])]
    pct=round(len(sc)/len(ausentes)*100) if len(ausentes)>0 else 0
    st.info(f"De los {len(ausentes)} pacientes ausentes, {len(sc)} ({pct}%) tenian datos de contacto invalidos.")
    csv=df_citas.to_csv(index=False).encode("utf-8")
    st.download_button("Descargar base de datos (CSV)",csv,"citas_hsg.csv","text/csv")

# ─────────────────────────────────────────────
# AGENDA PROXIMA SEMANA
# ─────────────────────────────────────────────
elif modulo == "agenda_semana":
    st.markdown("<div style='padding:24px 8px;'>", unsafe_allow_html=True)
    st.markdown("<div class='hsg-section-title'>Agenda Proxima Semana</div>", unsafe_allow_html=True)
    st.markdown("<div class='hsg-section-sub'>Listado de pacientes con hora la semana siguiente — para llamada de confirmacion proactiva</div>", unsafe_allow_html=True)

    # Calcular semana proxima (lunes a viernes)
    hoy_ag = datetime.today()
    dias_hasta_lunes = (7 - hoy_ag.weekday()) % 7
    if dias_hasta_lunes == 0:
        dias_hasta_lunes = 7
    lunes_prox = hoy_ag + timedelta(days=dias_hasta_lunes)
    lunes_prox = lunes_prox.replace(hour=0, minute=0, second=0, microsecond=0)
    viernes_prox = lunes_prox + timedelta(days=4)

    fechas_prox = [(lunes_prox + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(5)]
    dias_nombres = ["Lunes","Martes","Miercoles","Jueves","Viernes"]

    st.markdown(f"""
    <div style="background:#1a3a6b;border-radius:10px;padding:16px 24px;color:white;margin-bottom:20px;display:flex;justify-content:space-between;align-items:center;">
        <div>
            <div style="font-size:13px;opacity:0.75;text-transform:uppercase;letter-spacing:1px;">Semana a confirmar</div>
            <div style="font-size:20px;font-weight:700;">{lunes_prox.strftime('%d de %B')} al {viernes_prox.strftime('%d de %B de %Y')}</div>
        </div>
        <div style="text-align:right;">
            <div style="font-size:13px;opacity:0.75;">Llamadas sugeridas el viernes</div>
            <div style="font-size:18px;font-weight:700;">{hoy_ag.strftime('%d/%m/%Y')}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Filtrar citas de la semana proxima
    citas_prox = df_citas[(df_citas["fecha"].isin(fechas_prox)) & (df_citas["estado"].isin(["Pendiente","Confirmada"]))].copy()
    citas_prox["dia_semana"] = citas_prox["fecha"].apply(
        lambda f: dias_nombres[datetime.strptime(f, "%Y-%m-%d").weekday()]
    )
    citas_prox["fecha_display"] = citas_prox["fecha"].apply(
        lambda f: datetime.strptime(f, "%Y-%m-%d").strftime("%d de %B de %Y")
    )

    # Metricas
    total_prox   = len(citas_prox)
    confirmadas  = len(citas_prox[citas_prox["estado"]=="Confirmada"])
    pendientes   = len(citas_prox[citas_prox["estado"]=="Pendiente"])
    sin_contacto = len(citas_prox[~citas_prox["contacto_valido"]])

    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Total citas proxima semana", total_prox)
    c2.metric("Ya confirmadas", confirmadas)
    c3.metric("Pendientes de llamar", pendientes)
    c4.metric("Sin contacto valido", sin_contacto, delta_color="inverse", delta=f"-{sin_contacto}")

    st.divider()

    # Tabs por dia de la semana
    tabs = st.tabs([f"{dias_nombres[i]} {(lunes_prox+timedelta(days=i)).strftime('%d/%m')}" for i in range(5)])

    for i, tab in enumerate(tabs):
        with tab:
            fecha_tab = fechas_prox[i]
            citas_dia = citas_prox[citas_prox["fecha"]==fecha_tab].sort_values("hora")

            if len(citas_dia) == 0:
                st.info(f"No hay citas programadas para este dia.")
                continue

            st.caption(f"{len(citas_dia)} paciente(s) con hora este dia")

            for _, row in citas_dia.iterrows():
                estado  = row["estado"]
                clase   = estado.lower()
                urgencia = row.get("urgencia","Media")
                urgencia = urgencia if urgencia in ["Alta","Media","Baja"] else "Media"
                urg_clase = urgencia.lower()
                contacto_color = "#137333" if row["contacto_valido"] else "#c5221f"
                contacto_txt   = "Valido" if row["contacto_valido"] else "Invalido"
                telefono = row["telefono"]

                st.markdown(f"""
                <div class="cita-card {clase}" style="margin-bottom:8px;">
                    <div class="cita-card-header">
                        <div style="display:flex;align-items:center;gap:12px;">
                            <div style="font-size:18px;font-weight:800;color:#1a3a6b;min-width:50px;">{row['hora']}</div>
                            <div class="cita-nombre">{row['nombre_paciente']}</div>
                        </div>
                        <div class="cita-badges">
                            <span class="urg-{urg_clase}">{urgencia}</span>
                            &nbsp;
                            <span class="badge-{clase}">{estado}</span>
                        </div>
                    </div>
                    <div style="display:flex;gap:32px;flex-wrap:wrap;margin-top:6px;">
                        <div class="cita-info"><b>Especialidad:</b> {row['especialidad']}</div>
                        <div class="cita-info"><b>Medico:</b> {row.get('medico','—')}</div>
                        <div class="cita-info"><b>Comuna:</b> {row['comuna']}</div>
                        <div class="cita-info"><b>Edad:</b> {row['edad']} anos</div>
                        <div class="cita-info"><b>Telefono:</b> 
                            <span style="color:{contacto_color};font-weight:700;">{telefono}</span>
                            &nbsp;<span style="font-size:11px;color:{contacto_color};">({contacto_txt})</span>
                        </div>
                        <div class="cita-info"><b>ID:</b> {row['id_cita']}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # Acciones rapidas de confirmacion
                ba, bb, bc, _ = st.columns([1,1,1,2])
                if ba.button("Confirmar", key=f"aps_conf_{row['id_cita']}"):
                    st.session_state.citas.loc[st.session_state.citas["id_cita"]==row["id_cita"],"estado"]="Confirmada"
                    medico=row.get("medico",""); fecha=row["fecha"]; hora=row["hora"]
                    if medico in st.session_state.agenda:
                        if fecha not in st.session_state.agenda[medico]:
                            st.session_state.agenda[medico][fecha]={h:None for h in HORARIOS}
                        st.session_state.agenda[medico][fecha][hora]=row["nombre_paciente"]
                    st.success(f"{row['nombre_paciente']} confirmado para el {row['hora']} hrs.")
                    st.rerun()
                if bb.button("Cancelar cupo", key=f"aps_canc_{row['id_cita']}"):
                    st.session_state.citas.loc[st.session_state.citas["id_cita"]==row["id_cita"],"estado"]="Cancelada"
                    medico=row.get("medico",""); fecha=row["fecha"]; hora=row["hora"]
                    if medico in st.session_state.agenda:
                        if fecha in st.session_state.agenda.get(medico,{}):
                            st.session_state.agenda[medico][fecha][hora]=None
                    st.warning(f"Cupo de {row['nombre_paciente']} liberado.")
                    st.rerun()
                if bc.button("No contesta", key=f"aps_nc_{row['id_cita']}"):
                    st.info(f"Registrado: {row['nombre_paciente']} no contesta. Intentar nuevamente.")

                st.markdown("<hr style='margin:8px 0;border-color:#f0f0f0;'>", unsafe_allow_html=True)

    st.divider()

    # Resumen de llamadas pendientes
    st.markdown("**Resumen de llamadas pendientes**")
    pendientes_df = citas_prox[citas_prox["estado"]=="Pendiente"][
        ["nombre_paciente","especialidad","fecha_display","hora","telefono","contacto_valido","urgencia"]
    ].copy()
    pendientes_df = pendientes_df.sort_values(["urgencia","fecha_display"], 
        key=lambda col: col.map({"Alta":0,"Media":1,"Baja":2}) if col.name=="urgencia" else col)
    pendientes_df.columns = ["Paciente","Especialidad","Fecha","Hora","Telefono","Contacto valido","Urgencia"]
    pendientes_df["Contacto valido"] = pendientes_df["Contacto valido"].map({True:"Si",False:"No"})

    if len(pendientes_df) > 0:
        st.dataframe(pendientes_df, use_container_width=True, hide_index=True)
        csv_pend = pendientes_df.to_csv(index=False).encode("utf-8")
        st.download_button("Descargar lista de llamadas (CSV)", csv_pend, "llamadas_proxima_semana.csv","text/csv")
    else:
        st.success("Todos los pacientes de la proxima semana ya tienen su cita confirmada.")



# ─────────────────────────────────────────────
# CALENDARIO ANUAL
# ─────────────────────────────────────────────
elif modulo == "calendario":
    import calendar as cal_lib
    st.markdown("<div style='padding:24px 8px;'>", unsafe_allow_html=True)
    st.markdown("<div class='hsg-section-title'>Calendario Anual de Citas</div>", unsafe_allow_html=True)
    st.markdown("<div class='hsg-section-sub'>Vista mensual — se actualiza automaticamente al agendar nuevas citas</div>", unsafe_allow_html=True)

    col_f1, col_f2, col_f3 = st.columns([1,2,2])
    anio_sel   = col_f1.selectbox("Año", [2026, 2027], key="cal_anio")
    esp_cal    = col_f2.selectbox("Especialidad", ["Todas"]+sorted(df_citas["especialidad"].unique().tolist()), key="cal_esp")
    estado_cal = col_f3.selectbox("Estado", ["Todos","Confirmada","Pendiente","Cancelada","Ausente"], key="cal_estado")

    # Filtrar citas
    citas_cal = df_citas.copy()
    citas_cal["anio"] = citas_cal["fecha"].str[:4].astype(int)
    citas_cal["mes"]  = citas_cal["fecha"].str[5:7].astype(int)
    citas_cal["dia"]  = citas_cal["fecha"].str[8:10].astype(int)
    citas_cal = citas_cal[citas_cal["anio"]==anio_sel]
    if esp_cal != "Todas":
        citas_cal = citas_cal[citas_cal["especialidad"]==esp_cal]
    if estado_cal != "Todos":
        citas_cal = citas_cal[citas_cal["estado"]==estado_cal]

    MESES = {
        1:"Enero", 2:"Febrero", 3:"Marzo", 4:"Abril",
        5:"Mayo", 6:"Junio", 7:"Julio", 8:"Agosto",
        9:"Septiembre", 10:"Octubre", 11:"Noviembre", 12:"Diciembre"
    }
    COLOR_ESTADO = {"Confirmada":"#34a853","Pendiente":"#f9ab00","Cancelada":"#ea4335","Ausente":"#9aa0a6"}
    hoy = datetime.today()

    st.divider()

    # Mostrar meses de 3 en 3
    for fila in range(4):
        cols = st.columns(3)
        for col_idx in range(3):
            mes_num = fila*3 + col_idx + 1
            with cols[col_idx]:
                citas_mes = citas_cal[citas_cal["mes"]==mes_num]
                total_mes = len(citas_mes)
                conf_mes  = len(citas_mes[citas_mes["estado"]=="Confirmada"])
                pend_mes  = len(citas_mes[citas_mes["estado"]=="Pendiente"])

                # Header
                st.markdown(f"""
                <div style="background:#1a3a6b;border-radius:8px 8px 0 0;padding:8px 14px;
                            display:flex;justify-content:space-between;align-items:center;margin-bottom:0;">
                    <span style="color:white;font-weight:700;font-size:14px;">{MESES[mes_num]}</span>
                    <span style="color:rgba(255,255,255,0.75);font-size:12px;">{total_mes} citas</span>
                </div>
                """, unsafe_allow_html=True)

                # Agrupar citas por dia
                citas_por_dia = citas_mes.groupby("dia").apply(
                    lambda x: x["estado"].value_counts().idxmax()
                ).to_dict() if len(citas_mes)>0 else {}
                conteo_por_dia = citas_mes.groupby("dia").size().to_dict() if len(citas_mes)>0 else {}

                # Construir matriz del mes (7 columnas = dias semana)
                matriz = cal_lib.monthcalendar(anio_sel, mes_num)
                dias_header = ["L","M","X","J","V","S","D"]

                # Usar dataframe estilizado
                rows = []
                for semana in matriz:
                    fila_data = {}
                    for i, dia in enumerate(semana):
                        if dia == 0:
                            fila_data[dias_header[i]] = ""
                        else:
                            n = conteo_por_dia.get(dia, 0)
                            if n > 0:
                                fila_data[dias_header[i]] = f"{dia}({n})"
                            else:
                                fila_data[dias_header[i]] = str(dia)
                    rows.append(fila_data)

                df_mes = pd.DataFrame(rows, columns=dias_header)

                def estilo_celda(val):
                    if val == "":
                        return "background-color:#f8f9fa;color:#f8f9fa;"
                    try:
                        if "(" in str(val):
                            dia_v = int(str(val).split("(")[0])
                            fecha_v = f"{anio_sel}-{mes_num:02d}-{dia_v:02d}"
                            citas_d = citas_mes[citas_mes["dia"]==dia_v]
                            if len(citas_d)>0:
                                estado_dom = citas_d["estado"].value_counts().idxmax()
                                color = COLOR_ESTADO.get(estado_dom,"#1a73e8")
                                return f"background-color:{color}22;color:{color};font-weight:700;border-radius:4px;"
                        dia_v = int(str(val))
                        if anio_sel==hoy.year and mes_num==hoy.month and dia_v==hoy.day:
                            return "background-color:#1a3a6b;color:white;font-weight:900;border-radius:4px;"
                    except:
                        pass
                    return "color:#333;"

                st.dataframe(
                    df_mes.style.map(estilo_celda),
                    use_container_width=True,
                    hide_index=True,
                    height=int(len(matriz)*35 + 38)
                )

                # Mini resumen
                if total_mes > 0:
                    st.markdown(f"""
                    <div style="display:flex;gap:6px;margin-top:2px;margin-bottom:12px;">
                        <span style="font-size:11px;background:#e6f4ea;color:#137333;padding:2px 8px;border-radius:10px;">{conf_mes} conf.</span>
                        <span style="font-size:11px;background:#fef7e0;color:#b06000;padding:2px 8px;border-radius:10px;">{pend_mes} pend.</span>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("<div style='margin-bottom:12px;'></div>", unsafe_allow_html=True)

    st.divider()

    # Grafico resumen anual
    st.markdown("**Resumen anual de citas por mes**")
    resumen_anual = []
    for mes_num in range(1,13):
        citas_m = citas_cal[citas_cal["mes"]==mes_num]
        resumen_anual.append({
            "Mes": MESES[mes_num][:3],
            "Confirmadas": len(citas_m[citas_m["estado"]=="Confirmada"]),
            "Pendientes":  len(citas_m[citas_m["estado"]=="Pendiente"]),
            "Canceladas":  len(citas_m[citas_m["estado"]=="Cancelada"]),
            "Ausentes":    len(citas_m[citas_m["estado"]=="Ausente"]),
        })
    df_res = pd.DataFrame(resumen_anual)
    fig_anual = px.bar(
        df_res.melt(id_vars="Mes", var_name="Estado", value_name="Citas"),
        x="Mes", y="Citas", color="Estado", barmode="stack",
        color_discrete_map={"Confirmadas":"#34a853","Pendientes":"#f9ab00",
                            "Canceladas":"#ea4335","Ausentes":"#9aa0a6"}
    )
    fig_anual.update_layout(
        margin=dict(l=0,r=0,t=10,b=0), height=280,
        plot_bgcolor="white", paper_bgcolor="white",
        legend=dict(orientation="h",y=-0.25)
    )
    st.plotly_chart(fig_anual, use_container_width=True)