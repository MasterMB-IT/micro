import streamlit as st
import pandas as pd
import random
import json
import os
from datetime import datetime
import calendar

# --- CONFIGURAZIONE PAGINA (MODALITÀ CINEMA) ---
st.set_page_config(page_title="AOSR Train Manager - 16:9 Vision", layout="wide")

MESI_ITA = ["Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno", 
            "Luglio", "Agosto", "Settembre", "Ottobre", "Novembre", "Dicembre"]

GIORNI_SETTIMANA = ["LUNEDÌ", "MARTEDÌ", "MERCOLEDÌ", "GIOVEDÌ", "VENERDÌ", "SABATO", "DOMENICA"]

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

# --- DATABASE (Con JOSEPPONE aggiornato) ---
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

# --- CSS DEFINITIVO VISIONE D'INSIEME ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Special+Elite&family=Rye&family=Montserrat:wght@800;900&display=swap');
    
    /* Forza l'app a usare il 100% della larghezza e rimuovi padding */
    .main .block-container { max-width: 100% !important; padding: 0.5rem 1rem !important; }
    
    .stApp { background: #1a120b; background-image: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), url('https://www.transparenttextures.com/patterns/dark-leather.png'); }

    /* Titolo Grande */
    .title-banner { font-family: 'Rye', cursive; color: #ffcc66; text-align: center; font-size: 3.5rem; text-shadow: 3px 3px 0px #4b2e1b; margin-bottom: 5px; }

    /* Testata Settimana */
    .week-grid { display: grid; grid-template-columns: repeat(7, 1fr); gap: 2px; margin-bottom: 2px; }
    .week-day { background: #5d4037; color: #ffcc66; font-family: 'Rye', cursive; text-align: center; padding: 10px; border: 1px solid #3e2723; font-size: 1rem; }

    /* Celle Calendario */
    .cal-grid { display: grid; grid-template-columns: repeat(7, 1fr); gap: 2px; }
    .cal-cell { 
        background: #fdf5e6; background-image: url('https://www.transparenttextures.com/patterns/paper-fibers.png');
        height: 140px; border: 1px solid #d7ccc8; padding: 8px; position: relative; overflow: hidden;
    }
    .cal-cell:hover { background-color: #ffffff; z-index: 2; box-shadow: 0 0 15px rgba(255,204,102,0.4); }
    .cell-empty { background: rgba(255,255,255,0.05); height: 140px; border: 1px solid rgba(255,255,255,0.1); }

    .day-num { background: #8b0000; color: white; font-family: 'Montserrat', sans-serif; font-weight: 900; font-size: 0.8rem; padding: 2px 6px; width: fit-content; margin-bottom: 10px; border-radius: 2px; }
    .role { color: #5d4037; font-family: 'Montserrat', sans-serif; font-size: 0.6rem; font-weight: 800; text-transform: uppercase; margin-bottom: 0px; }
    .name { font-family: 'Special Elite', cursive; font-size: 0.95rem; font-weight: 900; text-transform: uppercase; line-height: 1.1; margin-bottom: 5px; border-left: 3px solid #d4a373; padding-left: 5px; }
    
    /* Popover */
    div[data-testid="stPopover"] > button { position: absolute; bottom: 5px; right: 5px; height: 20px !important; font-size: 0.6rem !important; opacity: 0.6; }
    </style>
    """, unsafe_allow_html=True)

# --- RENDERING ---
def draw_overview(data):
    st.markdown(f"<div class='title-banner'>🚂 {st.session_state['sel_mese'].upper()} {st.session_state['sel_anno']} 🚂</div>", unsafe_allow_html=True)
    
    # Testata giorni
    st.markdown("<div class='week-grid'>" + "".join([f"<div class='week-day'>{d}</div>" for d in GIORNI_SETTIMANA]) + "</div>", unsafe_allow_html=True)
    
    # Calcolo Logica Griglia
    first_wd = datetime(st.session_state['sel_anno'], MESI_ITA.index(st.session_state['sel_mese'])+1, 1).weekday()
    
    # Inizio Griglia
    st.markdown("<div class='cal-grid'>", unsafe_allow_html=True)
    
    # Colonne Streamlit per gestire i popover (purtroppo i popover richiedono contenitori Streamlit)
    full_days = [{"type": "empty"}] * first_wd + [{"type": "data", "content": d} for d in data]
    
    # Dividiamo in righe da 7
    for i in range(0, len(full_days), 7):
        cols = st.columns(7)
        chunk = full_days[i:i+7]
        for idx, item in enumerate(chunk):
            with cols[idx]:
                if item["type"] == "empty":
                    st.markdown('<div class="cell-empty"></div>', unsafe_allow_html=True)
                else:
                    r = item["content"]
                    g = r['Giorno']
                    capo = r['Capo']
                    passg = r['Pass']
                    
                    st.markdown(f"""
                        <div class="cal-cell">
                            <div class="day-num">{g}</div>
                            <div class="role">CAPOTRENO {"⭐" if g <= 11 else ""}</div>
                            <div class="name" style="color:#8b0000;">{capo}</div>
                            <div class="role">PASSEGGERO</div>
                            <div class="name" style="color:#1b4d3e;">{passg}</div>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    with st.popover("⚙️"):
                        opts_c = ["---"] + (leaders_list if g <= 11 else all_names_list)
                        new_c = st.selectbox(f"Capo G{g}", opts_c, index=opts_c.index(capo) if capo in opts_c else 0, key=f"c_{g}")
                        new_p = st.selectbox(f"Pass G{g}", ["---"]+all_names_list, index=(["---"]+all_names_list).index(passg) if passg in (["---"]+all_names_list) else 0, key=f"p_{g}")
                        if st.button("OK", key=f"b_{g}"):
                            for i_m, m in enumerate(st.session_state['master_cal']):
                                if m['Giorno'] == g:
                                    st.session_state['master_cal'][i_m].update({"Capo": new_c, "Pass": new_p})
                                    st.rerun()

# --- COMANDI ---
with st.sidebar:
    st.title("🤠 COMANDI")
    st.session_state['sel_mese'] = st.selectbox("Mese", MESI_ITA, index=datetime.now().month - 1)
    st.session_state['sel_anno'] = st.number_input("Anno", 2024, 2030, 2026)
    
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

    if st.button("🟩 SALVA E ARCHIVIA", use_container_width=True):
        if 'master_cal' in st.session_state:
            st.session_state['history'].append({"data": f"{st.session_state['sel_mese']} {st.session_state['sel_anno']}", "ts": datetime.now().strftime("%d/%m %H:%M"), "cal": st.session_state['master_cal']})
            save_history()
            st.toast("Salvato!")

# --- DISPLAY ---
if 'master_cal' in st.session_state:
    draw_overview(st.session_state['master_cal'])
else:
    st.markdown("<h2 style='text-align:center; color:#ffcc66; margin-top:20%; font-family:Rye;'>🚂 BENVENUTO CAPOTRENO!<br>Usa i comandi a sinistra per iniziare.</h2>", unsafe_allow_html=True)
