import streamlit as st
import pandas as pd
import random
import json
import os
from datetime import datetime
import calendar
import streamlit.components.v1 as components

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="AOSR Train Manager - Deluxe Edition", layout="wide")

MESI_ITA = ["Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno", 
            "Luglio", "Agosto", "Settembre", "Ottobre", "Novembre", "Dicembre"]

GIORNI_ABBR = ["Lun", "Mar", "Mer", "Gio", "Ven", "Sab", "Dom"]
DB_FILE = "cronologia_treni.json"

# --- PERSISTENZA DATI ---
if 'history' not in st.session_state:
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f:
                st.session_state['history'] = json.load(f)
        except:
            st.session_state['history'] = []
    else:
        st.session_state['history'] = []

def save_history():
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(st.session_state['history'], f, ensure_ascii=False, indent=4)

# --- DATABASE GIOCATORI ---
def init_db():
    leaders = ["Hool (R5)", "MASTER (R4)", "Le 12 Scimmie (R4)", "Sagittarius A1 (R4)", "Starbetty (R4)", "PEPPE (R4)", "Ricky Around (R4)", "Uncle g brother (R4)", "09ALEX24 (R4)", "ShinyPasta (R4)", "Wall 7 (R4)"]
    # Corretto Joseppone
    r3 = ["Uncle g", "G Erry", "Goz", "Ghandal", "Aryron", "Tricheco", "Maメツ", "NOVEMBERGENZ", "Lalla 96", "Whale Panda", "GennaroM", "EchoZero", "EDDward", "AMY", "Resilienza", "Ana Bunny", "Giuseppec84", "Benito Muschiolini", "Pandino19", "xFlotchy", "MX63", "holdfast", "Ghost", "BadBigBoss", "Stefano00000", "PakII", "BANDOLERO26", "BlOOdyBlade", "Whale hunter Levve", "Aresxxx", "KingGruffalo", "Hulkspakka", "Joseppone", "ImAde", "Nysbie", "LeFada13", "Skiteto", "SPio24", "TomEnergy", "Markus Defender", "Sho0t3r", "Wolf006", "Zokra", "perseusxxx", "Bendico", "Obbyy", "ArLes", "Fatz87", "cruel neve", "Trivellatore", "Osgh00", "Slowfia ABOH", "Pontatinatore", "27Francesco", "MissDrinks", "krompir", "MaledettO"]
    r2 = ["teomadh", "Bossnico", "Valecit", "FarmerHool", "camiiiii 08", "Doctor team", "Yass081", "Nuorifleming", "Vergabrio", "Frenk70", "Comandante Maveric", "Thor9000", "MrBolly", "BustaMaki", "S U C A", "StUnTmArK", "MONKEY D LUFFY 20", "CineSalentino", "Danylo98", "Ezechielefabianino", "BRNcommando", "LEONIDA", "elchicogyot", "erer1000", "Pupisnic", "Backfire1", "AnarchyBG", "Fabrizio1987", "JurdanS", "WiseR9", "Infinity8080"]
    
    data = [{"Nome": "---", "Grado": "Nessuno"}] + \
           [{"Nome": n, "Grado": "R5/R4"} for n in leaders] + \
           [{"Nome": n, "Grado": "R3"} for n in r3] + \
           [{"Nome": n, "Grado": "R2"} for n in r2]
    return pd.DataFrame(data)

if 'players_db' not in st.session_state: st.session_state['players_db'] = init_db()
db = st.session_state['players_db']
early_leaders_list = sorted(db[db['Grado'].isin(["R5/R4", "R3"])]['Nome'].tolist())
all_names_list = sorted(db['Nome'].tolist())

# --- CSS E LOGICA JS PER ISTANTANEA ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Special+Elite&family=Rye&family=Montserrat:wght@900&display=swap');
    
    .stApp { background: linear-gradient(rgba(20, 15, 10, 0.9), rgba(10, 5, 0, 0.95)), url('https://www.transparenttextures.com/patterns/dark-matter.png'); }
    .train-title { font-family: 'Rye', cursive; text-align: center; color: #ffcc66; text-shadow: 3px 3px 0px #4b2e1b; font-size: 3.5rem; margin-bottom: 20px; }
    
    /* Contenitore Calendario per Export */
    #capture-area { 
        background: #fdf5e6; 
        padding: 25px; 
        border: 8px solid #4b2e1b; 
        border-radius: 15px; 
        display: grid; 
        grid-template-columns: repeat(7, 1fr); 
        gap: 2px;
        width: 100%;
    }

    .calendar-cell { 
        background: #fdf5e6; 
        border: 1px solid rgba(93, 64, 55, 0.3); 
        padding: 12px; 
        min-height: 180px; 
        display: flex; 
        flex-direction: column;
        background-image: url('https://www.transparenttextures.com/patterns/paper-fibers.png');
    }

    .day-badge { 
        background: #8b0000; 
        color: white; 
        font-family: 'Montserrat'; 
        padding: 2px 8px; 
        font-size: 0.8rem; 
        width: fit-content; 
        margin-bottom: 8px;
        border-radius: 2px;
    }

    .role-label { 
        font-size: 0.65rem; 
        color: #5d4037; 
        font-weight: bold; 
        text-transform: uppercase; 
        margin-top: 10px; 
        border-bottom: 1px solid rgba(93, 64, 55, 0.2); 
    }

    /* TUTTI I NOMI NERI */
    .name-text { 
        font-family: 'Special Elite'; 
        font-size: 0.95rem; 
        font-weight: bold; 
        color: #000000 !important; 
        margin-top: 3px; 
        word-break: break-all;
    }

    .sala-comando { 
        background: rgba(25, 15, 5, 0.85); 
        border: 2px solid #ffcc66; 
        border-radius: 15px; 
        padding: 20px; 
        margin-bottom: 30px; 
    }
    </style>
    """, unsafe_allow_html=True)

# --- COMPONENTE JS PER DOWNLOAD ---
def trigger_snapshot():
    components.html("""
        <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
        <script>
            setTimeout(() => {
                const element = window.parent.document.getElementById('capture-area');
                if (element) {
                    html2canvas(element, { 
                        scale: 2,
                        backgroundColor: "#4b2e1b",
                        logging: false,
                        useCORS: true
                    }).then(canvas => {
                        const link = window.parent.document.createElement('a');
                        link.download = 'Calendario_Treni_AOSR.png';
                        link.href = canvas.toDataURL("image/png");
                        link.click();
                    });
                }
            }, 500);
        </script>
    """, height=0)

# --- INTERFACCIA PRINCIPALE ---
st.markdown('<div class="train-title">🚂 AOSR EXPRESS</div>', unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="sala-comando">', unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1, 1])
    with c1:
        sel_mese = st.selectbox("📅 MESE", MESI_ITA, index=datetime.now().month-1)
    with c2:
        sel_anno = st.number_input("📆 ANNO", 2024, 2030, 2026)
    with c3:
        st.write("🛠️ AZIONI VELOCI")
        btn_col1, btn_col2 = st.columns(2)
        with btn_col1:
            if st.button("⚒️ GENERA AUTO", use_container_width=True):
                num_gg = calendar.monthrange(sel_anno, MESI_ITA.index(sel_mese)+1)[1]
                st.session_state['master_cal'] = []
                # Esempio generazione rapida
                for g in range(1, num_gg + 1):
                    st.session_state['master_cal'].append({
                        "Giorno": g, 
                        "Capo": random.choice(early_leaders_list), 
                        "Pass": random.choice(all_names_list)
                    })
        with btn_col2:
            if st.button("🏜️ RESET", use_container_width=True):
                if 'master_cal' in st.session_state: del st.session_state['master_cal']
                st.rerun()
    
    st.markdown("---")
    
    ca1, ca2, ca3 = st.columns(3)
    with ca1:
        if st.button("🟩 SALVA IN CRONOLOGIA", use_container_width=True):
            if 'master_cal' in st.session_state:
                st.session_state['history'].append({
                    "data": f"{sel_mese} {sel_anno}",
                    "ts": datetime.now().strftime("%d/%m/%Y %H:%M"),
                    "cal": [dict(d) for d in st.session_state['master_cal']]
                })
                save_history()
                st.toast("Salvato!")
    with ca2:
        if st.button("📸 SCARICA COME FOTO", type="primary", use_container_width=True):
            st.session_state['trigger_shot'] = True
    st.markdown('</div>', unsafe_allow_html=True)

# --- VISUALIZZAZIONE CALENDARIO ---
if 'master_cal' in st.session_state:
    st.markdown(f"<h2 style='text-align:center; color:#ffcc66; font-family:Rye;'>{sel_mese.upper()} {sel_anno}</h2>", unsafe_allow_html=True)
    
    # Costruzione HTML della griglia
    num_gg = len(st.session_state['master_cal'])
    first_wd = datetime(sel_anno, MESI_ITA.index(sel_mese)+1, 1).weekday()
    
    html_grid = '<div id="capture-area">'
    # Spazi vuoti
    for _ in range(first_wd):
        html_grid += '<div class="calendar-cell" style="opacity:0.3"></div>'
    
    # Giorni reali
    for r in st.session_state['master_cal']:
        wd_idx = datetime(sel_anno, MESI_ITA.index(sel_mese)+1, r['Giorno']).weekday()
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
    html_grid += '</div>'
    
    st.markdown(html_grid, unsafe_allow_html=True)

# --- GESTIONE CRONOLOGIA ---
if st.session_state['history']:
    st.markdown("<br><br><h2 style='color:#ffcc66; font-family:Rye; text-align:center;'>📜 CRONOLOGIA</h2>", unsafe_allow_html=True)
    for idx, item in enumerate(reversed(st.session_state['history'])):
        real_idx = len(st.session_state['history']) - 1 - idx
        with st.expander(f"📦 {item['data']} - Creato il {item['ts']}"):
            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"📝 CARICA E MODIFICA", key=f"edit_{real_idx}", use_container_width=True):
                    st.session_state['master_cal'] = [dict(d) for d in item['cal']]
                    st.rerun()
            with col2:
                if st.button(f"🗑️ ELIMINA", key=f"del_{real_idx}", use_container_width=True):
                    st.session_state['history'].pop(real_idx)
                    save_history()
                    st.rerun()

# Trigger Snapshot JS
if st.session_state.get('trigger_shot'):
    trigger_snapshot()
    st.session_state['trigger_shot'] = False
