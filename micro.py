import streamlit as st
import pandas as pd
import random
import json
import os
from datetime import datetime
import calendar

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="AOSR Train Manager - Vintage Grid", layout="wide")

MESI_ITA = ["Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno", 
            "Luglio", "Agosto", "Settembre", "Ottobre", "Novembre", "Dicembre"]

GIORNI_SETTIMANA = ["Lunedì", "Martedì", "Mercoledì", "Giovedì", "Venerdì", "Sabato", "Domenica"]

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
        except: return []
    return []

if 'history' not in st.session_state:
    st.session_state['history'] = load_history()

# --- DATABASE ---
def init_db():
    leaders = ["Hool (R5)", "MASTER (R4)", "Le 12 Scimmie (R4)", "Sagittarius A1 (R4)", "Starbetty (R4)", "PEPPE (R4)", "Ricky Around (R4)", "Uncle g brother (R4)", "09ALEX24 (R4)", "ShinyPasta (R4)", "Wall 7 (R4)"]
    r3 = ["Uncle g", "G Erry", "Goz", "Ghandal", "Aryron", "Tricheco", "Maメツ", "NOVEMBERGENZ", "Lalla 96", "Whale Panda", "GennaroM", "EchoZero", "EDDward", "AMY", "Resilienza", "Ana Bunny", "Giuseppec84", "Benito Muschiolini", "Pandino19", "xFlotchy", "MX63", "holdfast", "Ghost", "BadBigBoss", "Stefano00000", "PakII", "BANDOLERO26", "BlOOdyBlade", "Whale hunter Levve", "Aresxxx", "KingGruffalo", "Hulkspakka", "Joseone", "ImAde", "Nysbie", "LeFada13", "Skiteto", "SPio24", "TomEnergy", "Markus Defender", "Sho0t3r", "Wolf006", "Zokra", "perseusxxx", "Bendico", "Obbyy", "ArLes", "Fatz87", "cruel neve", "Trivellatore", "Osgh00", "Slowfia ABOH", "Pontatinatore", "27Francesco", "MissDrinks", "krompir", "MaledettO"]
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

# --- CSS INTEGRATO (Stile Vintage + Griglia Compatta) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Special+Elite&family=Rye&family=Montserrat:wght@700;900&display=swap');
    
    .stApp { background: linear-gradient(rgba(30, 20, 10, 0.8), rgba(15, 10, 5, 0.95)), url('https://images.unsplash.com/photo-1510524527013-0393282436da?q=80&w=1920&auto=format&fit=crop'); background-size: cover; background-attachment: fixed; }
    
    /* Intestazione Giorni della Settimana */
    .week-header {
        background-color: rgba(93, 64, 55, 0.9);
        color: #ffcc66;
        text-align: center;
        padding: 12px;
        font-family: 'Rye', cursive;
        border: 1px solid #4b2e1b;
        font-size: 1.2rem;
    }
    
    /* Cella del Calendario (Vintage) */
    .calendar-cell {
        background-color: #fdf5e6;
        background-image: url('https://www.transparenttextures.com/patterns/paper-fibers.png');
        border: 1px solid rgba(93, 64, 55, 0.4);
        height: 180px;
        padding: 10px;
        display: flex;
        flex-direction: column;
        margin: -0.5px; /* Sovrapposizione bordi */
        transition: 0.2s;
    }
    .calendar-cell:hover { background-color: #fff9f0; z-index: 5; box-shadow: inset 0 0 15px rgba(0,0,0,0.1); }
    
    .cell-empty {
        background-color: rgba(0,0,0,0.2);
        border: 1px solid rgba(93, 64, 55, 0.2);
        height: 180px;
        margin: -0.5px;
    }

    .day-badge {
        background: #8b0000;
        color: white;
        font-family: 'Montserrat', sans-serif;
        font-weight: 900;
        padding: 3px 10px;
        border-radius: 3px;
        font-size: 0.85rem;
        width: fit-content;
        margin-bottom: 10px;
    }

    .role-label {
        color: #5d4037;
        font-size: 0.65rem;
        font-family: 'Montserrat', sans-serif;
        text-transform: uppercase;
        font-weight: 800;
        margin-top: 5px;
    }

    .name-display {
        font-family: 'Special Elite', cursive;
        font-size: 0.95rem;
        font-weight: bold;
        text-transform: uppercase;
        border-left: 4px solid #d4a373;
        padding-left: 8px;
        color: #2b1d0e;
        overflow: hidden;
        white-space: nowrap;
    }

    /* Rimuove spazi Streamlit */
    [data-testid="column"] { padding: 0px !important; }
    div[data-testid="stHorizontalBlock"] { gap: 0px !important; }
    
    .main-title {
        font-family: 'Rye', cursive;
        text-align: center;
        color: #ffcc66;
        text-shadow: 4px 4px 0px #4b2e1b;
        font-size: 3.5rem;
        margin-bottom: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

def get_weekday_idx(day, month_name, year):
    month_idx = MESI_ITA.index(month_name) + 1
    return datetime(year, month_idx, day).weekday()

# --- RENDERING GRIGLIA ---
def draw_vintage_calendar(data):
    # Titolo Mese
    st.markdown(f"<div class='main-title'>🚂 {st.session_state['sel_mese'].upper()} {st.session_state['sel_anno']} 🚂</div>", unsafe_allow_html=True)
    
    # Header Lun-Dom
    h_cols = st.columns(7)
    for idx, name in enumerate(GIORNI_SETTIMANA):
        h_cols[idx].markdown(f"<div class='week-header'>{name}</div>", unsafe_allow_html=True)
    
    # Logica Offset
    first_day_wd = get_weekday_idx(1, st.session_state['sel_mese'], st.session_state['sel_anno'])
    full_display_list = [{"type": "empty"}] * first_day_wd
    for item in data:
        full_display_list.append({"type": "data", "content": item})
    
    # Riempimento righe
    for i in range(0, len(full_display_list), 7):
        cols = st.columns(7)
        chunk = full_display_list[i:i + 7]
        for j, item in enumerate(chunk):
            with cols[j]:
                if item["type"] == "empty":
                    st.markdown('<div class="cell-empty"></div>', unsafe_allow_html=True)
                else:
                    r = item["content"]
                    g = r['Giorno']
                    st.markdown(f"""
                        <div class="calendar-cell">
                            <div class="day-badge">{g}</div>
                            <div class="role-label">CAPOTRENO {"⭐" if g <= 11 else ""}</div>
                            <div class="name-display" style="color:#8b0000;">{r['Capo']}</div>
                            <div class="role-label">PASSEGGERO</div>
                            <div class="name-display" style="color:#1b4d3e;">{r['Pass']}</div>
                        </div>
                    """, unsafe_allow_html=True)

# --- PANEL COMANDI ---
with st.sidebar:
    st.title("🤠 Train Control")
    st.session_state['sel_mese'] = st.selectbox("Seleziona Mese", MESI_ITA, index=datetime.now().month - 1)
    st.session_state['sel_anno'] = st.number_input("Seleziona Anno", 2024, 2030, 2026)
    
    if st.button("⚒️ GENERA TURNI"):
        num_gg = calendar.monthrange(st.session_state['sel_anno'], MESI_ITA.index(st.session_state['sel_mese'])+1)[1]
        st.session_state['master_cal'] = []
        for g in range(1, num_gg + 1):
            st.session_state['master_cal'].append({
                "Giorno": g, 
                "Capo": random.choice(leaders_list) if g <= 11 else random.choice(all_names_list), 
                "Pass": random.choice(all_names_list)
            })

    if st.button("🟩 SALVA"):
        if 'master_cal' in st.session_state:
            st.session_state['history'].append({"data": f"{st.session_state['sel_mese']} {st.session_state['sel_anno']}", "ts": datetime.now().strftime("%d/%m %H:%M"), "cal": st.session_state['master_cal']})
            save_history()
            st.toast("Salvato!")

# --- MAIN ---
if 'master_cal' in st.session_state:
    draw_vintage_calendar(st.session_state['master_cal'])
else:
    st.markdown("<div style='text-align:center; color:#ffcc66; margin-top:100px; font-family:Rye; font-size:2rem;'>Pronto per il viaggio? Genera un calendario!</div>", unsafe_allow_html=True)
