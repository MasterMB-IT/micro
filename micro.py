import streamlit as st
import pandas as pd
import random
import json
import os
from datetime import datetime
import calendar

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="AOSR Train Manager - Cinema Edition", layout="wide")

MESI_ITA = ["Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno", 
            "Luglio", "Agosto", "Settembre", "Ottobre", "Novembre", "Dicembre"]

GIORNI_SETTIMANA = ["Lunedì", "Martedì", "Mercoledì", "Giovedì", "Venerdì", "Sabato", "Domenica"]

DB_FILE = "cronologia_treni.json"

# --- PERSISTENZA ---
def save_history():
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(st.session_state['history'], f, ensure_ascii=False, indent=4)

def load_history():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f: return json.load(f)
        except: return []
    return []

if 'history' not in st.session_state: st.session_state['history'] = load_history()

# --- DATABASE ---
def init_db():
    leaders = ["Hool (R5)", "MASTER (R4)", "Le 12 Scimmie (R4)", "Sagittarius A1 (R4)", "Starbetty (R4)", "PEPPE (R4)", "Ricky Around (R4)", "Uncle g brother (R4)", "09ALEX24 (R4)", "ShinyPasta (R4)", "Wall 7 (R4)"]
    r3 = ["Uncle g", "G Erry", "Goz", "Ghandal", "Aryron", "Tricheco", "Maメツ", "NOVEMBERGENZ", "Lalla 96", "Whale Panda", "GennaroM", "EchoZero", "EDDward", "AMY", "Resilienza", "Ana Bunny", "Giuseppec84", "Benito Muschiolini", "Pandino19", "xFlotchy", "MX63", "holdfast", "Ghost", "BadBigBoss", "Stefano00000", "PakII", "BANDOLERO26", "BlOOdyBlade", "Whale hunter Levve", "Aresxxx", "KingGruffalo", "Hulkspakka", "JOSEPPONE", "ImAde", "Nysbie", "LeFada13", "Skiteto", "SPio24", "TomEnergy", "Markus Defender", "Sho0t3r", "Wolf006", "Zokra", "perseusxxx", "Bendico", "Obbyy", "ArLes", "Fatz87", "cruel neve", "Trivellatore", "Osgh00", "Slowfia ABOH", "Pontatinatore", "27Francesco", "MissDrinks", "krompir", "MaledettO"]
    r2 = ["teomadh", "Bossnico", "Valecit", "FarmerHool", "camiiiii 08", "Doctor team", "Yass081", "Nuorifleming", "Vergabrio", "Frenk70", "Comandante Maveric", "Thor9000", "MrBolly", "BustaMaki", "S U C A", "StUnTmArK", "MONKEY D LUFFY 20", "CineSalentino", "Danylo98", "Ezechielefabianino", "BRNcommando", "LEONIDA", "elchicogyot", "erer1000", "Pupisnic", "Backfire1", "AnarchyBG", "Fabrizio1987", "JurdanS", "WiseR9", "Infinity8080"]
    data = [{"Nome": "---", "Grado": "Nessuno"}] + [{"Nome": n, "Grado": "R5/R4"} for n in leaders] + [{"Nome": n, "Grado": "R3"} for n in r3] + [{"Nome": n, "Grado": "R2"} for n in r2]
    return pd.DataFrame(data)

st.session_state['players_db'] = init_db()
db = st.session_state['players_db']
leaders_list = sorted(db[db['Grado'] == "R5/R4"]['Nome'].tolist())
all_names_list = sorted(db['Nome'].tolist())

# --- CSS INTEGRATO ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Special+Elite&family=Rye&family=Montserrat:wght@800;900&display=swap');
    
    .main .block-container { max-width: 100% !important; padding: 1rem !important; }
    .stApp { background: #1a120b; background-image: linear-gradient(rgba(0,0,0,0.8), rgba(0,0,0,0.8)), url('https://www.transparenttextures.com/patterns/dark-leather.png'); }

    .main-title { font-family: 'Rye', cursive; color: #ffcc66; text-align: center; font-size: 3rem; margin-bottom: 20px; text-shadow: 3px 3px 0px #4b2e1b; }

    /* Header Settimana */
    .week-header-row { display: grid; grid-template-columns: repeat(7, 1fr); gap: 5px; margin-bottom: 5px; }
    .week-day-label { background: #5d4037; color: #ffcc66; font-family: 'Rye', cursive; text-align: center; padding: 12px; border: 1px solid #3e2723; font-size: 1.1rem; }

    /* Griglia Visione Insieme */
    .cinema-grid { display: grid; grid-template-columns: repeat(7, 1fr); gap: 5px; }
    .cinema-cell { 
        background: #fdf5e6; background-image: url('https://www.transparenttextures.com/patterns/paper-fibers.png');
        height: 160px; border: 1px solid #d7ccc8; padding: 10px; position: relative; transition: 0.3s;
    }
    .cinema-cell:hover { transform: scale(1.02); z-index: 5; box-shadow: 0 0 20px rgba(255,204,102,0.5); }
    .cinema-cell-empty { background: rgba(255,255,255,0.05); height: 160px; border: 1px solid rgba(255,255,255,0.1); }

    .day-num { background: #8b0000; color: white; font-family: 'Montserrat', sans-serif; font-weight: 900; padding: 2px 8px; width: fit-content; margin-bottom: 10px; border-radius: 2px; }
    .role-text { color: #5d4037; font-family: 'Montserrat', sans-serif; font-size: 0.65rem; font-weight: 800; text-transform: uppercase; margin-bottom: 2px; }
    .name-display { font-family: 'Special Elite', cursive; font-size: 1rem; font-weight: 900; text-transform: uppercase; border-left: 3px solid #d4a373; padding-left: 6px; margin-bottom: 5px; color: #2b1d0e; white-space: nowrap; overflow: hidden; }
    
    /* Toggle Style */
    .stCheckbox { background: rgba(255,204,102,0.1); padding: 10px; border-radius: 10px; border: 1px solid #ffcc66; color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNZIONE LOGICA CALENDARIO ---
def draw_calendar_view(data, overview_mode=True):
    st.markdown(f"<div class='main-title'>🚂 {st.session_state['sel_mese'].upper()} {st.session_state['sel_anno']} 🚂</div>", unsafe_allow_html=True)
    
    # Testata Giorni
    st.markdown("<div class='week-header-row'>" + "".join([f"<div class='week-day-label'>{d}</div>" for d in GIORNI_SETTIMANA]) + "</div>", unsafe_allow_html=True)
    
    first_wd = datetime(st.session_state['sel_anno'], MESI_ITA.index(st.session_state['sel_mese'])+1, 1).weekday()
    full_days = [{"type": "empty"}] * first_wd + [{"type": "data", "content": d} for d in data]

    # Griglia a 7 colonne
    for i in range(0, len(full_days), 7):
        cols = st.columns(7)
        chunk = full_days[i:i+7]
        for idx, item in enumerate(chunk):
            with cols[idx]:
                if item["type"] == "empty":
                    st.markdown('<div class="cinema-cell-empty"></div>', unsafe_allow_html=True)
                else:
                    r = item["content"]
                    g = r['Giorno']
                    
                    st.markdown(f"""
                        <div class="cinema-cell">
                            <div class="day-num">{g}</div>
                            <div class="role-text">CAPO {"⭐" if g <= 11 else ""}</div>
                            <div class="name-display" style="color:#8b0000;">{r['Capo']}</div>
                            <div class="role-text">PASSEGGERO</div>
                            <div class="name-display" style="color:#1b4d3e;">{r['Pass']}</div>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # Se NON siamo in sola visione, aggiungi il tasto modifica
                    if not overview_mode:
                        with st.popover("MODIFICA"):
                            opts_c = ["---"] + (leaders_list if g <= 11 else all_names_list)
                            nc = st.selectbox(f"C {g}", opts_c, index=opts_c.index(r['Capo']) if r['Capo'] in opts_c else 0, key=f"ec_{g}")
                            np = st.selectbox(f"P {g}", ["---"]+all_names_list, index=(["---"]+all_names_list).index(r['Pass']) if r['Pass'] in (["---"]+all_names_list) else 0, key=f"ep_{g}")
                            if st.button("OK", key=f"save_{g}"):
                                for i_m, m in enumerate(st.session_state['master_cal']):
                                    if m['Giorno'] == g:
                                        st.session_state['master_cal'][i_m].update({"Capo": nc, "Pass": np})
                                        st.rerun()

# --- SIDEBAR E COMANDI ---
with st.sidebar:
    st.markdown("<h2 style='color:#ffcc66; font-family:Rye;'>⚙️ PANNELLO</h2>", unsafe_allow_html=True)
    st.session_state['sel_mese'] = st.selectbox("Mese", MESI_ITA, index=datetime.now().month - 1)
    st.session_state['sel_anno'] = st.number_input("Anno", 2024, 2030, 2026)
    
    st.write("---")
    if st.button("⚒️ GENERA NUOVO", use_container_width=True):
        num_gg = calendar.monthrange(st.session_state['sel_anno'], MESI_ITA.index(st.session_state['sel_mese'])+1)[1]
        st.session_state['master_cal'] = [{"Giorno": g, "Capo": random.choice(leaders_list) if g <= 11 else "---", "Pass": "---"} for g in range(1, num_gg + 1)]
        st.rerun()
    
    if st.button("🟩 SALVA IN CRONOLOGIA", use_container_width=True):
        if 'master_cal' in st.session_state:
            st.session_state['history'].append({"data": f"{st.session_state['sel_mese']} {st.session_state['sel_anno']}", "ts": datetime.now().strftime("%H:%M"), "cal": st.session_state['master_cal']})
            save_history()
            st.success("Archiviato!")

# --- AREA PRINCIPALE ---
if 'master_cal' in st.session_state:
    # PULSANTE VISIONE D'INSIEME (Toggle)
    mode = st.toggle("🎞️ ATTIVA VISIONE D'INSIEME (Sola Lettura)", value=True)
    
    # Rendering del calendario basato sul toggle
    draw_calendar_view(st.session_state['master_cal'], overview_mode=mode)
else:
    st.markdown("<div style='text-align:center; margin-top:150px; color:#ffcc66; font-family:Rye; font-size:2rem;'>🚂 USA IL MENU A SINISTRA PER GENERARE IL TRENO</div>", unsafe_allow_html=True)
