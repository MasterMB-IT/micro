import streamlit as st
import pandas as pd
import random
import json
import os
from datetime import datetime
import calendar
import streamlit.components.v1 as components

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="AOSR Train Manager - Snapshot Edition", layout="wide")

MESI_ITA = ["Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno", 
            "Luglio", "Agosto", "Settembre", "Ottobre", "Novembre", "Dicembre"]

GIORNI_SETTIMANA = ["Lunedì", "Martedì", "Mercoledì", "Giovedì", "Venerdì", "Sabato", "Domenica"]
GIORNI_ABBR = ["Lun", "Mar", "Mer", "Gio", "Ven", "Sab", "Dom"]

DB_FILE = "cronologia_treni.json"

# --- FUNZIONI DI PERSISTENZA ---
def save_history():
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(st.session_state['history'], f, ensure_ascii=False, indent=4)

def load_history():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    return []

if 'history' not in st.session_state:
    st.session_state['history'] = load_history()

# --- DATABASE ---
def init_db():
    leaders = ["Hool (R5)", "MASTER (R4)", "Le 12 Scimmie (R4)", "Sagittarius A1 (R4)", "Starbetty (R4)", "PEPPE (R4)", "Ricky Around (R4)", "Uncle g brother (R4)", "09ALEX24 (R4)", "ShinyPasta (R4)", "Wall 7 (R4)"]
    r3 = ["Uncle g", "G Erry", "Goz", "Ghandal", "Aryron", "Tricheco", "Maメツ", "NOVEMBERGENZ", "Lalla 96", "Whale Panda", "GennaroM", "EchoZero", "EDDward", "AMY", "Resilienza", "Ana Bunny", "Giuseppec84", "Benito Muschiolini", "Pandino19", "xFlotchy", "MX63", "holdfast", "Ghost", "BadBigBoss", "Stefano00000", "PakII", "BANDOLERO26", "BlOOdyBlade", "Whale hunter Levve", "Aresxxx", "KingGruffalo", "Hulkspakka", "Joseppone", "ImAde", "Nysbie", "LeFada13", "Skiteto", "SPio24", "TomEnergy", "Markus Defender", "Sho0t3r", "Wolf006", "Zokra", "perseusxxx", "Bendico", "Obbyy", "ArLes", "Fatz87", "cruel neve", "Trivellatore", "Osgh00", "Slowfia ABOH", "Pontatinatore", "27Francesco", "MissDrinks", "krompir", "MaledettO"]
    r2 = ["teomadh", "Bossnico", "Valecit", "FarmerHool", "camiiiii 08", "Doctor team", "Yass081", "Nuorifleming", "Vergabrio", "Frenk70", "Comandante Maveric", "Thor9000", "MrBolly", "BustaMaki", "S U C A", "StUnTmArK", "MONKEY D LUFFY 20", "CineSalentino", "Danylo98", "Ezechielefabianino", "BRNcommando", "LEONIDA", "elchicogyot", "erer1000", "Pupisnic", "Backfire1", "AnarchyBG", "Fabrizio1987", "JurdanS", "WiseR9", "Infinity8080"]
    data = [{"Nome": "---", "Grado": "Nessuno"}] + \
            [{"Nome": n, "Grado": "R5/R4"} for n in leaders] + \
            [{"Nome": n, "Grado": "R3"} for n in r3] + \
            [{"Nome": n, "Grado": "R2"} for n in r2]
    return pd.DataFrame(data)

if 'players_db' not in st.session_state: st.session_state['players_db'] = init_db()
db = st.session_state['players_db']
leaders_list = sorted(db[db['Grado'] == "R5/R4"]['Nome'].tolist())
all_names_list = sorted(db['Nome'].tolist())

# --- CSS E LOGICA SNAPSHOT ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Special+Elite&family=Rye&family=Montserrat:wght@700;900&display=swap');
    
    .stApp { background: linear-gradient(rgba(30, 20, 10, 0.8), rgba(15, 10, 5, 0.95)), url('https://www.transparenttextures.com/patterns/dark-matter.png'); background-attachment: fixed; }
    .train-title { font-family: 'Rye', cursive; text-align: center; color: #ffcc66; text-shadow: 4px 4px 0px #4b2e1b; font-size: 3.5rem; margin-bottom: 20px; }
    .sala-comando { background: rgba(25, 15, 5, 0.9); border: 2px solid #ffcc66; border-radius: 15px; padding: 20px; margin-bottom: 20px; }

    /* AREA CATTURA */
    #snapshot-area { background: #1e140a; padding: 20px; border-radius: 10px; }
    .cal-header-container { display: flex; align-items: center; justify-content: center; gap: 20px; margin-bottom: 15px; }
    .cal-header-text { font-family: 'Rye', cursive; color: #ffcc66; font-size: 2.2rem; margin: 0; text-transform: uppercase; }
    
    /* GRIGLIA COMPATTA ATTACCATA */
    .grid-container { display: grid; grid-template-columns: repeat(7, 1fr); gap: 0px; border: 2px solid #4b2e1b; }
    .calendar-cell { 
        background: #fdf5e6; border: 1px solid rgba(93, 64, 55, 0.3); 
        padding: 10px 5px; min-height: 180px; display: flex; flex-direction: column; 
        margin: 0px; background-image: url('https://www.transparenttextures.com/patterns/paper-fibers.png');
    }
    .day-badge { background: #8b0000; color: white; font-family: 'Montserrat'; font-weight: 900; padding: 2px 6px; font-size: 0.7rem; width: fit-content; margin-bottom: 5px; }
    .role-label { color: #5d4037; font-size: 0.55rem; font-family: 'Montserrat'; text-transform: uppercase; font-weight: 800; border-bottom: 1px solid rgba(93, 64, 55, 0.1); margin-top: 5px; }
    
    /* NOMI SEMPRE NERI */
    .name-text { font-family: 'Special Elite'; font-size: 0.85rem; font-weight: 900; color: #000000 !important; border-left: 3px solid #d4a373; padding-left: 5px; margin-top: 2px; }
    
    .stButton>button { border-radius: 4px !important; font-family: 'Rye' !important; }
    .snapshot-btn button { background-color: #ffcc66 !important; color: #2b1d0e !important; font-size: 1.2rem !important; height: 50px !important; }
    </style>
    """, unsafe_allow_html=True)

def trigger_snapshot():
    components.html("""
        <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
        <script>
            setTimeout(() => {
                const element = window.parent.document.getElementById('snapshot-area');
                html2canvas(element, { scale: 2, backgroundColor: "#1e140a" }).then(canvas => {
                    const link = document.createElement('a');
                    link.download = 'Calendario_AOSR_Express.png';
                    link.href = canvas.toDataURL("image/png");
                    link.click();
                });
            }, 500);
        </script>
    """, height=0)

# --- LOGICA CALENDARIO ---
def get_weekday_idx(day, month_name, year):
    return datetime(year, MESI_ITA.index(month_name) + 1, day).weekday()

# --- INTERFACCIA ---
st.markdown('<div class="train-title">🚂 AOSR EXPRESS MANAGER</div>', unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="sala-comando">', unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1, 1])
    with c1:
        sel_mese = st.selectbox("📅 MESE", MESI_ITA, index=datetime.now().month - 1)
        sel_anno = st.number_input("📆 ANNO", 2024, 2030, 2026)
    with c2:
        if st.button("⚒️ GENERA AUTO", use_container_width=True):
            num_gg = calendar.monthrange(sel_anno, MESI_ITA.index(sel_mese)+1)[1]
            st.session_state['master_cal'] = []
            for g in range(1, num_gg + 1):
                st.session_state['master_cal'].append({"Giorno": g, "Capo": random.choice(leaders_list), "Pass": random.choice(all_names_list)})
    with c3:
        st.markdown('<div class="snapshot-btn">', unsafe_allow_html=True)
        if st.button("📸 SCARICA FOTO", use_container_width=True):
            st.session_state['do_snapshot'] = True
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- VISUALIZZAZIONE AREA CATTURA ---
if 'master_cal' in st.session_state:
    st.markdown('<div id="snapshot-area">', unsafe_allow_html=True)
    
    # Intestazione con Treno
    st.markdown(f"""
        <div class="cal-header-container">
            <span style="font-size:3rem;">🚂</span>
            <h2 class="cal-header-text">AOSR - {sel_mese} {sel_anno}</h2>
            <span style="font-size:3rem;">🚂</span>
        </div>
    """, unsafe_allow_html=True)
    
    # Griglia Attaccata
    first_wd = get_weekday_idx(1, sel_mese, sel_anno)
    html_grid = '<div class="grid-container">'
    
    # Celle vuote iniziali
    for _ in range(first_wd):
        html_grid += '<div class="calendar-cell" style="background:rgba(0,0,0,0.1); border:none;"></div>'
    
    # Giorni del mese
    for r in st.session_state['master_cal']:
        wd_idx = get_weekday_idx(r['Giorno'], sel_mese, sel_anno)
        wd_name = GIORNI_ABBR[wd_idx]
        html_grid += f'''
            <div class="calendar-cell">
                <div class="day-badge">{wd_name} {r['Giorno']}</div>
                <div class="role-label">CAPO ⭐</div>
                <div class="name-text">{r['Capo']}</div>
                <div class="role-label">PASSEGGERO</div>
                <div class="name-text">{r['Pass']}</div>
            </div>
        '''
    html_grid += '</div></div>'
    st.markdown(html_grid, unsafe_allow_html=True)

# Trigger Snapshot
if st.session_state.get('do_snapshot'):
    trigger_snapshot()
    st.session_state['do_snapshot'] = False
