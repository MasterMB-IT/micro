import streamlit as st
import pandas as pd
import calendar
import random
from datetime import datetime

# --- CONFIGURAZIONE ---
st.set_page_config(page_title="AOSR Master Calendar", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #f4f7f9; color: #1e272e; }
    
    /* Header Stiloso */
    .header-container {
        background: #1e272e; padding: 20px; border-radius: 15px;
        text-align: center; margin-bottom: 30px; border-bottom: 5px solid #00d8ff;
    }
    .header-title { color: #00d8ff; font-family: 'Arial Black'; font-size: 2.5rem; margin: 0; }
    .header-subtitle { color: #ffd32a; font-size: 1rem; letter-spacing: 2px; }

    /* Griglia Calendario Classica */
    .calendar-wrapper {
        display: grid;
        grid-template-columns: repeat(7, 1fr);
        gap: 2px;
        background-color: #d1d8e0;
        border: 2px solid #485e74;
    }
    .weekday-header {
        background-color: #485e74; color: white;
        text-align: center; padding: 10px; font-weight: bold;
        text-transform: uppercase; font-size: 0.9rem;
    }
    .day-cell {
        background-color: white; min-height: 120px; padding: 10px;
        border: 1px solid #d1d8e0; position: relative;
    }
    .empty-cell { background-color: #f1f2f6; }
    
    /* Contenuto Cella */
    .day-num {
        font-size: 1.1rem; font-weight: bold; color: #7f8c8d;
        margin-bottom: 8px; display: block;
    }
    .player-slot {
        font-family: 'Verdana'; font-size: 0.85rem; line-height: 1.4;
        text-transform: uppercase; margin-bottom: 4px;
    }
    .capo-name { color: #2c3e50; font-weight: 800; display: block; }
    .pass-name { color: #27ae60; font-weight: 600; display: block; }
    .r4-free { color: #e67e22; font-style: italic; font-size: 0.75rem; }

    /* Alert */
    .warning-dot { color: #eb4d4b; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- DATABASE INVARIATO ---
if 'players_db' not in st.session_state:
    # (Mantengo i tuoi 100 nomi caricati in precedenza...)
    data = []
    for n in ["Hool (R5)", "MASTER (R4)", "Le 12 Scimmie (R4)", "Sagittarius A1 (R4)", "Starbetty (R4)", "PEPPE (R4)", "Ricky Around (R4)", "uncle g (R4)", "09ALEX24 (R4)", "ShinyPasta (R4)", "Wall 7 (R4)"]:
        data.append({"Nome": n, "Grado": "R5/R4"})
    r3_list = ["G Erry", "Uncle g brother", "Cane Avvoltoio", "Ghandal", "Aryron", "Tricheco", "Maメツ", "NOVEMBERGENZ", "Lalla 96", "Whale Panda", "GennaroM", "EchoZero", "EDDward", "AMY", "Resilienza", "Ana Bunny", "Giuseppec84", "Benito Muschiolini", "Pandino19", "xFlotchy", "MX63", "holdfast", "Ghost", "BadBigBoss", "Stefano00000", "PakII", "BANDOLERO26", "BlOOdyBlade", "Whale hunter Levve", "Aresxxx", "KingGruffalo", "Hulkspakka", "Joseone", "ImAde", "Nysbie", "LeFada13", "Skifetto", "SPio24", "TomEnergy", "Markus Defender", "Sho0t3r", "Wolf006", "Zokra", "perseusxxx", "Bendico", "Obbyy", "ArLes", "Fatz87", "cruel neve", "Trivellatore", "Osgh00", "Slowfia ABOH", "Pontatinatore", "27Francesco", "MissDrinks", "krompir", "MaledettO"]
    for n in r3_list: data.append({"Nome": n, "Grado": "R3"})
    # ... resto del DB ...
    st.session_state['players_db'] = pd.DataFrame(data)

# --- UI DI COMANDO ---
st.markdown('<div class="header-container"><p class="header-title">TRAIN CALENDAR AOSR</p><p class="header-subtitle">PIANIFICAZIONE MENSILE CAPITRENI</p></div>', unsafe_allow_html=True)

col1, col2 = st.columns([1,3])
with col1:
    mese_str = st.selectbox("Seleziona Mese", list(calendar.month_name)[1:], index=datetime.now().month-1)
    anno = st.number_input("Anno", 2024, 2030, 2026)
    mese_idx = list(calendar.month_name).index(mese_str)

with col2:
    meritevoli = st.multiselect("Partecipanti Attivi", st.session_state['players_db'][st.session_state['players_db']['Grado'] != "R5/R4"]['Nome'].tolist())

if st.button("🔄 GENERA CALENDARIO SETTIMANALE", use_container_width=True):
    # Logica di generazione (Leader primi 11gg, poi meritevoli)
    random.shuffle(meritevoli)
    pool = list(meritevoli)
    leaders = st.session_state['players_db'][st.session_state['players_db']['Grado']=="R5/R4"]['Nome'].tolist()
    num_gg = calendar.monthrange(anno, mese_idx)[1]
    
    cal_data = []
    for g in range(1, num_gg + 1):
        if g <= 11:
            c, p = leaders[(g-1)%len(leaders)], "VUOTO"
        else:
            c = pool.pop(0) if pool else "DA ASSEGNARE"
            p = pool.pop(0) if pool else "VUOTO"
        cal_data.append({"giorno": g, "capo": c, "pass": p})
    st.session_state['current_cal'] = cal_data

# --- RENDERING CALENDARIO ---
if 'current_cal' in st.session_state:
    # Header Giorni
    days_abbr = ["Lunedì", "Martedì", "Mercoledì", "Giovedì", "Venerdì", "Sabato", "Domenica"]
    st.markdown('<div class="calendar-wrapper">', unsafe_allow_html=True)
    for d in days_abbr:
        st.markdown(f'<div class="weekday-header">{d}</div>', unsafe_allow_html=True)
    
    # Calcolo offset (0=Lunedì, 6=Domenica)
    primo_gg = calendar.weekday(anno, mese_idx, 1)
    
    # Celle vuote iniziali
    for _ in range(primo_gg):
        st.markdown('<div class="day-cell empty-cell"></div>', unsafe_allow_html=True)
        
    # Giorni del mese
    for d_info in st.session_state['current_cal']:
        pass_html = f'<span class="pass-name">{d_info["pass"]}</span>' if d_info["pass"] != "VUOTO" else ""
        r4_free = '<span class="r4-free">R4-free</span>' if d_info["giorno"] > 11 and d_info["pass"] == "VUOTO" else ""
        
        st.markdown(f"""
            <div class="day-cell">
                <span class="day-num">{d_info['giorno']}</span>
                <div class="player-slot">
                    <span class="capo-name">{d_info['capo']}</span>
                    {pass_html}
                    {r4_free}
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

    st.info("💡 Suggerimento: Per stampare o salvare, usa la funzione 'Stampa' del browser (Ctrl+P) impostando il layout su Orizzontale.")
