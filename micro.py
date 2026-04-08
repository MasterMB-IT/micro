import streamlit as st
import pandas as pd
import random
import json
import os
from datetime import datetime
import calendar
import streamlit.components.v1 as components

# --- CONFIGURAZIONE ---
st.set_page_config(page_title="AOSR Train Manager", layout="wide")

MESI_ITA = ["Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno", 
            "Luglio", "Agosto", "Settembre", "Ottobre", "Novembre", "Dicembre"]
GIORNI_ABBR = ["Lun", "Mar", "Mer", "Gio", "Ven", "Sab", "Dom"]

# --- DATABASE ---
def init_db():
    leaders = ["Hool (R5)", "MASTER (R4)", "Le 12 Scimmie (R4)", "Sagittarius A1 (R4)", "Starbetty (R4)", "PEPPE (R4)", "Ricky Around (R4)", "Uncle g brother (R4)", "09ALEX24 (R4)", "ShinyPasta (R4)", "Wall 7 (R4)"]
    r3 = ["Uncle g", "G Erry", "Goz", "Ghandal", "Aryron", "Tricheco", "Maメツ", "NOVEMBERGENZ", "Lalla 96", "Whale Panda", "GennaroM", "EchoZero", "EDDward", "AMY", "Resilienza", "Ana Bunny", "Giuseppec84", "Benito Muschiolini", "Pandino19", "xFlotchy", "MX63", "holdfast", "Ghost", "BadBigBoss", "Stefano00000", "PakII", "BANDOLERO26", "BlOOdyBlade", "Whale hunter Levve", "Aresxxx", "KingGruffalo", "Hulkspakka", "Joseppone", "ImAde", "Nysbie", "LeFada13", "Skiteto", "SPio24", "TomEnergy", "Markus Defender", "Sho0t3r", "Wolf006", "Zokra", "perseusxxx", "Bendico", "Obbyy", "ArLes", "Fatz87", "cruel neve", "Trivellatore", "Osgh00", "Slowfia ABOH", "Pontatinatore", "27Francesco", "MissDrinks", "krompir", "MaledettO"]
    r2 = ["teomadh", "Bossnico", "Valecit", "FarmerHool", "camiiiii 08", "Doctor team", "Yass081", "Nuorifleming", "Vergabrio", "Frenk70", "Comandante Maveric", "Thor9000", "MrBolly", "BustaMaki", "S U C A", "StUnTmArK", "MONKEY D LUFFY 20", "CineSalentino", "Danylo98", "Ezechielefabianino", "BRNcommando", "LEONIDA", "elchicogyot", "erer1000", "Pupisnic", "Backfire1", "AnarchyBG", "Fabrizio1987", "JurdanS", "WiseR9", "Infinity8080"]
    data = [{"Nome": n, "Grado": "R4/R5"} for n in leaders] + [{"Nome": n, "Grado": "R3"} for n in r3] + [{"Nome": n, "Grado": "R2"} for n in r2]
    return pd.DataFrame(data)

if 'players_db' not in st.session_state: st.session_state['players_db'] = init_db()
db = st.session_state['players_db']
names_list = sorted(db['Nome'].tolist())

# --- STILI CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Special+Elite&family=Rye&family=Montserrat:wght@900&display=swap');
    
    .stApp { background-color: #0e1117; }
    
    /* Area che verrà fotografata */
    #capture-zone { 
        background: #1e140a; 
        padding: 30px; 
        border-radius: 0px; 
        width: 100%;
        margin: 0 auto;
    }

    .header-aosr {
        display: flex; align-items: center; justify-content: center; gap: 20px;
        font-family: 'Rye', cursive; color: #ffcc66; font-size: 3rem; margin-bottom: 20px;
    }

    /* Griglia compatta senza spazi */
    .grid-container { 
        display: grid; 
        grid-template-columns: repeat(7, 1fr); 
        gap: 0px; 
        border: 4px solid #4b2e1b;
    }

    .cell { 
        background: #fdf5e6; 
        border: 1px solid rgba(75, 46, 27, 0.3); 
        padding: 10px; 
        min-height: 160px;
        display: flex; flex-direction: column;
        background-image: url('https://www.transparenttextures.com/patterns/paper-fibers.png');
    }

    .day-num { background: #8b0000; color: white; font-family: 'Montserrat'; padding: 2px 6px; font-size: 0.8rem; width: fit-content; margin-bottom: 8px; }
    .label { color: #5d4037; font-size: 0.6rem; font-family: 'Montserrat'; text-transform: uppercase; font-weight: bold; border-bottom: 1px solid rgba(75, 46, 27, 0.1); margin-top: 8px; }
    
    /* NOMI NERI */
    .name { font-family: 'Special Elite'; font-size: 0.9rem; font-weight: bold; color: #000000 !important; margin-top: 2px; }

    .empty-cell { background: #2b1d0e; border: 1px solid #4b2e1b; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNZIONE DOWNLOAD ---
def download_button():
    # Carichiamo la libreria html2canvas via CDN
    components.html("""
        <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
        <script>
        function doCapture() {
            const container = window.parent.document.getElementById('capture-zone');
            html2canvas(container, {
                scale: 2,
                backgroundColor: "#1e140a",
                useCORS: true
            }).then(canvas => {
                const link = document.createElement('a');
                link.download = 'Calendario_AOSR_Express.png';
                link.href = canvas.toDataURL("image/png");
                link.click();
            });
        }
        doCapture();
        </script>
    """, height=0)

# --- INTERFACCIA ---
st.title("🚂 AOSR EXPRESS MANAGER")

with st.sidebar:
    st.header("Comandi")
    mese = st.selectbox("Mese", MESI_ITA, index=datetime.now().month-1)
    anno = st.number_input("Anno", 2025, 2030, 2026)
    
    if st.button("⚒️ GENERA CALENDARIO", use_container_width=True):
        num_gg = calendar.monthrange(anno, MESI_ITA.index(mese)+1)[1]
        st.session_state['cal_data'] = []
        for g in range(1, num_gg + 1):
            st.session_state['cal_data'].append({
                "Giorno": g, 
                "Capo": random.choice(names_list), 
                "Pass": random.choice(names_list)
            })

    st.write("---")
    # PULSANTE ISTANTANEA
    if st.button("📸 SCARICA COME FOTO", type="primary", use_container_width=True):
        st.session_state['run_download'] = True

# --- RENDERING CALENDARIO ---
if 'cal_data' in st.session_state:
    # Contenitore ID per lo snapshot
    st.markdown('<div id="capture-zone">', unsafe_allow_html=True)
    
    # Intestazione con Treno
    st.markdown(f"""
        <div class="header-aosr">
            <span>🚂</span> AOSR EXPRESS - {mese.upper()} {anno} <span>🚂</span>
        </div>
    """, unsafe_allow_html=True)
    
    # Calcolo spazi vuoti iniziali
    first_wd = datetime(anno, MESI_ITA.index(mese)+1, 1).weekday()
    
    # Inizio Griglia
    html_code = '<div class="grid-container">'
    
    # Celle vuote
    for _ in range(first_wd):
        html_code += '<div class="cell empty-cell"></div>'
    
    # Celle giorni
    for r in st.session_state['cal_data']:
        wd_name = GIORNI_ABBR[datetime(anno, MESI_ITA.index(mese)+1, r['Giorno']).weekday()]
        html_code += f"""
            <div class="cell">
                <div class="day-num">{wd_name} {r['Giorno']}</div>
                <div class="label">CAPO ⭐</div>
                <div class="name">{r['Capo']}</div>
                <div class="label">PASSEGGERO</div>
                <div class="name">{r['Pass']}</div>
            </div>
        """
    
    html_code += '</div></div>'
    st.markdown(html_code, unsafe_allow_html=True)

# Esegui download se richiesto
if st.session_state.get('run_download'):
    download_button()
    st.session_state['run_download'] = False
