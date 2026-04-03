import streamlit as st
import pandas as pd
import random
import json
import os
from datetime import datetime
import calendar

# --- CONFIGURAZIONE PAGINA (WIDE MODE PER 16:9) ---
st.set_page_config(page_title="AOSR Train Manager - Cinema Edition", layout="wide")

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

# --- DATABASE (Con JOSEPPONE) ---
def init_db():
    leaders = ["Hool (R5)", "MASTER (R4)", "Le 12 Scimmie (R4)", "Sagittarius A1 (R4)", "Starbetty (R4)", "PEPPE (R4)", "Ricky Around (R4)", "Uncle g brother (R4)", "09ALEX24 (R4)", "ShinyPasta (R4)", "Wall 7 (R4)"]
    # Correzione: JOSEONE -> JOSEPPONE
    r3 = ["Uncle g", "G Erry", "Goz", "Ghandal", "Aryron", "Tricheco", "Maメツ", "NOVEMBERGENZ", "Lalla 96", "Whale Panda", "GennaroM", "EchoZero", "EDDward", "AMY", "Resilienza", "Ana Bunny", "Giuseppec84", "Benito Muschiolini", "Pandino19", "xFlotchy", "MX63", "holdfast", "Ghost", "BadBigBoss", "Stefano00000", "PakII", "BANDOLERO26", "BlOOdyBlade", "Whale hunter Levve", "Aresxxx", "KingGruffalo", "Hulkspakka", "JOSEPPONE", "ImAde", "Nysbie", "LeFada13", "Skiteto", "SPio24", "TomEnergy", "Markus Defender", "Sho0t3r", "Wolf006", "Zokra", "perseusxxx", "Bendico", "Obbyy", "ArLes", "Fatz87", "cruel neve", "Trivellatore", "Osgh00", "Slowfia ABOH", "Pontatinatore", "27Francesco", "MissDrinks", "krompir", "MaledettO"]
    r2 = ["teomadh", "Bossnico", "Valecit", "FarmerHool", "camiiiii 08", "Doctor team", "Yass081", "Nuorifleming", "Vergabrio", "Frenk70", "Comandante Maveric", "Thor9000", "MrBolly", "BustaMaki", "S U C A", "StUnTmArK", "MONKEY D LUFFY 20", "CineSalentino", "Danylo98", "Ezechielefabianino", "BRNcommando", "LEONIDA", "elchicogyot", "erer1000", "Pupisnic", "Backfire1", "AnarchyBG", "Fabrizio1987", "JurdanS", "WiseR9", "Infinity8080"]
    
    data = [{"Nome": "---", "Grado": "Nessuno"}] + \
           [{"Nome": n, "Grado": "R5/R4"} for n in leaders] + \
           [{"Nome": n, "Grado": "R3"} for n in r3] + \
           [{"Nome": n, "Grado": "R2"} for n in r2]
    return pd.DataFrame(data)

st.session_state['players_db'] = init_db()
db = st.session_state['players_db']
leaders_list = sorted(db[db['Grado'] == "R5/R4"]['Nome'].tolist())
all_names_list = sorted(db['Nome'].tolist())

# --- CSS INTEGRATO (Vintage + Layout 16:9) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Special+Elite&family=Rye&family=Montserrat:wght@800;900&display=swap');
    
    /* Espansione Totale Schermo */
    .block-container { padding: 1rem 1rem; max-width: 100% !important; }
    .stApp { background: linear-gradient(rgba(30, 20, 10, 0.85), rgba(15, 10, 5, 0.98)), url('https://images.unsplash.com/photo-1510524527013-0393282436da?q=80&w=1920&auto=format&fit=crop'); background-size: cover; background-attachment: fixed; }

    /* Testata Giorni Settimana */
    .week-header {
        background-color: rgba(93, 64, 55, 0.95);
        color: #ffcc66;
        text-align: center;
        padding: 10px;
        font-family: 'Rye', cursive;
        border: 1px solid #4b2e1b;
        font-size: 1.2rem;
        margin-bottom: -1px;
    }

    /* Griglia Senza Spazi */
    [data-testid="column"] { padding: 0px !important; margin: 0px !important; }
    div[data-testid="stHorizontalBlock"] { gap: 0px !important; }

    .calendar-cell { 
        background: #fdf5e6; 
        border: 1px solid rgba(93, 64, 55, 0.5); 
        padding: 10px; 
        color: #2b1d0e; 
        background-image: url('https://www.transparenttextures.com/patterns/paper-fibers.png'); 
        display: flex; 
        flex-direction: column; 
        height: 165px; 
        margin: -0.5px;
        transition: 0.2s;
    }
    .calendar-cell:hover { background-color: #fff9f0; z-index: 10; box-shadow: inset 0 0 15px rgba(0,0,0,0.15); }
    
    .cell-empty { background: rgba(0,0,0,0.3); border: 1px solid rgba(93, 64, 55, 0.2); height: 165px; margin: -0.5px; }

    .day-badge { 
        background: #8b0000; 
        color: white; 
        font-family: 'Montserrat', sans-serif; 
        padding: 2px 8px; 
        font-size: 0.9rem; 
        font-weight: 900;
        width: fit-content; 
        margin-bottom: 12px;
        border-radius: 2px;
    }

    .role-label { color: #5d4037; font-size: 0.65rem; font-family: 'Montserrat', sans-serif; font-weight: 800; text-transform: uppercase; opacity: 0.7; margin-top: 4px; }
    
    .name-text { 
        font-family: 'Special Elite', cursive; 
        font-size: 1.05rem; 
        font-weight: 900; 
        text-transform: uppercase; 
        border-left: 3px solid #d4a373; 
        padding-left: 6px; 
        margin-bottom: 2px;
        white-space: nowrap;
        overflow: hidden;
    }
    
    .main-title { font-family: 'Rye', cursive; text-align: center; color: #ffcc66; font-size: 3.5rem; text-shadow: 4px 4px 0px #4b2e1b; margin-bottom: 10px; }
    
    /* Popover button adjustment */
    div[data-testid="stPopover"] > button { 
        padding: 0px 5px !important; 
        height: 22px !important; 
        font-size: 0.6rem !important; 
        border: 1px solid #d4a373 !important;
        background: rgba(212, 163, 115, 0.1) !important;
    }
    </style>
    """, unsafe_allow_html=True)

def get_weekday_idx(day, month_name, year):
    month_idx = MESI_ITA.index(month_name) + 1
    return datetime(year, month_idx, day).weekday()

# --- LOGICA RENDERING ---
def draw_cinema_calendar(data):
    st.markdown(f"<div class='main-title'>🚂 {st.session_state['sel_mese'].upper()} {st.session_state['sel_anno']} 🚂</div>", unsafe_allow_html=True)
    
    # Header Giorni (Lunedì -> Domenica)
    h_cols = st.columns(7)
    for idx, day in enumerate(GIORNI_SETTIMANA):
        h_cols[idx].markdown(f"<div class='week-header'>{day}</div>", unsafe_allow_html=True)
    
    # Calcolo offset per iniziare il mese al giorno giusto
    first_wd = get_weekday_idx(1, st.session_state['sel_mese'], st.session_state['sel_anno'])
    full_list = [{"type": "empty"}] * first_wd + [{"type": "data", "content": d} for d in data]
    
    # Disegno righe (7 colonne fisse)
    for i in range(0, len(full_list), 7):
        cols = st.columns(7)
        chunk = full_list[i:i + 7]
        for j, item in enumerate(chunk):
            with cols[j]:
                if item["type"] == "empty":
                    st.markdown('<div class="cell-empty"></div>', unsafe_allow_html=True)
                else:
                    r = item["content"]
                    g = r['Giorno']
                    
                    # Colori dinamici
                    c_color = "#8b0000" if r['Capo'] != "---" else "#888"
                    p_color = "#1b4d3e" if r['Pass'] != "---" else "#888"
                    
                    st.markdown(f"""
                    <div class="calendar-cell">
                        <div class="day-badge">{g}</div>
                        <div class="role-label">CAPOTRENO {"⭐" if g <= 11 else ""}</div>
                        <div class="name-text" style="color:{c_color};">{r['Capo']}</div>
                        <div class="role-label">PASSEGGERO</div>
                        <div class="name-text" style="color:{p_color};">{r['Pass']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Popover di modifica rapida
                    with st.popover("📝", help="Modifica"):
                        opts_c = ["---"] + (leaders_list if g <= 11 else all_names_list)
                        opts_p = ["---"] + all_names_list
                        
                        # Fix indici sicuri per JOSEPPONE
                        idx_c = opts_c.index(r['Capo']) if r['Capo'] in opts_c else 0
                        idx_p = opts_p.index(r['Pass']) if r['Pass'] in opts_p else 0
                        
                        new_c = st.selectbox(f"Capo G{g}", opts_c, index=idx_c, key=f"sel_c_{g}")
                        new_p = st.selectbox(f"Pass G{g}", opts_p, index=idx_p, key=f"sel_p_{g}")
                        if st.button("AGGIORNA", key=f"btn_up_{g}"):
                            for idx, m in enumerate(st.session_state['master_cal']):
                                if m['Giorno'] == g:
                                    st.session_state['master_cal'][idx].update({"Capo": new_c, "Pass": new_p})
                                    st.rerun()

# --- INTERFACCIA COMANDI ---
with st.expander("🤠 SALA COMANDO (Configurazione)", expanded=False):
    c1, c2, c3, c4 = st.columns([1,1,1,1])
    with c1:
        st.session_state['sel_mese'] = st.selectbox("Mese", MESI_ITA, index=datetime.now().month - 1)
        st.session_state['sel_anno'] = st.number_input("Anno", 2024, 2030, 2026)
    with c2:
        if st.button("⚒️ GENERA AUTO", use_container_width=True):
            num_gg = calendar.monthrange(st.session_state['sel_anno'], MESI_ITA.index(st.session_state['sel_mese'])+1)[1]
            st.session_state['master_cal'] = []
            for g in range(1, num_gg + 1):
                st.session_state['master_cal'].append({
                    "Giorno": g, 
                    "Capo": random.choice(leaders_list) if g <= 11 else random.choice(all_names_list), 
                    "Pass": random.choice(all_names_list)
                })
            st.rerun()
    with c3:
        if st.button("🟩 SALVA TURNO", use_container_width=True):
            if 'master_cal' in st.session_state:
                st.session_state['history'].append({
                    "data": f"{st.session_state['sel_mese']} {st.session_state['sel_anno']}", 
                    "ts": datetime.now().strftime("%d/%m %H:%M"), 
                    "cal": st.session_state['master_cal']
                })
                save_history()
                st.success("Calendario archiviato!")
    with c4:
        if st.button("🏜️ RESET", use_container_width=True):
            if 'master_cal' in st.session_state: del st.session_state['master_cal']
            st.rerun()

# --- MAIN ---
if 'master_cal' in st.session_state:
    draw_cinema_calendar(st.session_state['master_cal'])
else:
    st.markdown("<div style='text-align:center; color:#ffcc66; font-family:Rye; font-size:2rem; margin-top:100px;'>🚂 Benvenuto Capotreno! Genera un nuovo calendario dal pannello in alto.</div>", unsafe_allow_html=True)

# Cronologia in fondo
if st.session_state['history']:
    st.markdown("---")
    with st.expander("📜 Cronologia Calendari"):
        for h in reversed(st.session_state['history']):
            st.write(f"📅 {h['data']} - Creato alle {h['ts']}")
