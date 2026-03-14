import streamlit as st
import pandas as pd
import random
from datetime import datetime

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="AOSR Train Manager Elite", layout="wide")

MESI_ITA = ["Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno", 
            "Luglio", "Agosto", "Settembre", "Ottobre", "Novembre", "Dicembre"]

# --- CSS CUSTOM PER PULSANTI INTERNI ---
st.markdown("""
    <style>
    .stApp {
        background-color: #0b0e14;
        color: #ffffff;
    }

    /* Header e Titolo */
    .aosr-header {
        background: rgba(26, 31, 44, 0.95); padding: 20px; border-radius: 20px; 
        border: 2px solid #00c8ff; text-align: center; margin-bottom: 25px;
    }
    .aosr-title { font-family: 'Orbitron', sans-serif; color: #00c8ff; font-size: 2rem; }

    /* Container Calendario */
    .print-container { 
        background-color: #000000; padding: 20px; border-radius: 15px; border: 2px solid #00c8ff;
    }
    
    /* CARD DEL GIORNO */
    .summary-card {
        background: #111; border: 1px solid #333; padding: 10px; 
        border-radius: 10px; margin-bottom: 10px; position: relative;
        min-height: 120px; display: flex; flex-direction: column; justify-content: center;
    }

    .day-label { color: #00c8ff; font-weight: bold; font-size: 0.8rem; margin-bottom: 8px; text-align: center; }

    /* CONTROLLI DENTRO LA CARD */
    .inner-controls {
        position: absolute; top: 10px; right: 8px;
        display: flex; flex-direction: column; gap: 4px;
    }

    /* Stile micro-pulsanti */
    .stButton > button { border-radius: 5px !important; transition: 0.2s; }
    
    /* Pulsanti Grandi Fluo */
    .btn-genera button { background: linear-gradient(90deg, #2ed573, #00ff85) !important; color: black !important; font-weight: bold; height: 60px !important; width: 100%; border: none; }
    .btn-resetta button { background: linear-gradient(90deg, #ff4757, #ff0055) !important; color: white !important; font-weight: bold; height: 60px !important; width: 100%; border: none; }

    /* Micro pulsanti interni */
    .card-btn button {
        width: 24px !important; height: 24px !important; padding: 0 !important;
        font-size: 0.7rem !important; background: #222 !important; border: 1px solid #444 !important;
        color: #00c8ff !important;
    }
    .card-btn button:hover { border-color: #00c8ff !important; background: #333 !important; }

    /* Nomi */
    .name-text { font-size: 0.85rem; font-weight: bold; text-align: center; text-transform: uppercase; }
    </style>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@700&display=swap" rel="stylesheet">
    """, unsafe_allow_html=True)

# --- DATABASE ---
def init_db():
    data = []
    leaders = ["Hool (R5)", "MASTER (R4)", "Le 12 Scimmie (R4)", "Sagittarius A1 (R4)", "Starbetty (R4)", "PEPPE (R4)", "Ricky Around (R4)", "uncle g (R4)", "09ALEX24 (R4)", "ShinyPasta (R4)", "Wall 7 (R4)"]
    for n in leaders: data.append({"Nome": n, "Grado": "R5/R4"})
    r3 = ["G Erry", "Uncle g brother", "Cane Avvoltoio", "Ghandal", "Aryron", "Tricheco", "Maメツ", "NOVEMBERGENZ", "Lalla 96", "Whale Panda", "GennaroM", "EchoZero", "EDDward", "AMY", "Resilienza", "Ana Bunny", "Giuseppec84", "Benito Muschiolini", "Pandino19", "xFlotchy", "MX63", "holdfast", "Ghost", "BadBigBoss", "Stefano00000", "PakII", "BANDOLERO26", "BlOOdyBlade", "Whale hunter Levve", "Aresxxx", "KingGruffalo", "Hulkspakka", "Joseone", "ImAde", "Nysbie", "LeFada13", "Skifetto", "SPio24", "TomEnergy", "Markus Defender", "Sho0t3r", "Wolf006", "Zokra", "perseusxxx", "Bendico", "Obbyy", "ArLes", "Fatz87", "cruel neve", "Trivellatore", "Osgh00", "Slowfia ABOH", "Pontatinatore", "27Francesco", "MissDrinks", "krompir", "MaledettO"]
    for n in r3: data.append({"Nome": n, "Grado": "R3"})
    r2 = ["teomadh", "Bossnico", "Valecit", "FarmerHool", "camiiiii 08", "Doctor team", "Yass081", "Nuorifleming", "Vergabrio", "Frenk70", "Comandante Maveric", "Thor9000", "MrBolly", "BustaMaki", "Ritardato", "StUnTmArK", "MONKEY D LUFFY 20", "CineSalentino", "Danylo98", "Ezechielefabianino", "BRNcommando", "LEONIDA", "elchicogyot", "erer1000", "Pupisnic", "Backfire1", "AnarchyBG", "Fabrizio1987", "JurdanS", "WiseR9", "Infinity8080"]
    for n in r2: data.append({"Nome": n, "Grado": "R2"})
    return pd.DataFrame(data)

if 'players_db' not in st.session_state:
    st.session_state['players_db'] = init_db()
    st.session_state['sel_mese_ita'] = MESI_ITA[datetime.now().month - 1]
    st.session_state['sel_anno'] = 2026

db = st.session_state['players_db']
all_names = sorted(db['Nome'].tolist())

# --- HEADER ---
st.markdown('<div class="aosr-header"><div class="aosr-title">🚄 AOSR EXPRESS MANAGER 🚄</div></div>', unsafe_allow_html=True)

# --- BOTTONI FLUO ---
col_b1, col_b2 = st.columns(2)
with col_b1:
    st.markdown('<div class="btn-genera">', unsafe_allow_html=True)
    if st.button("🚀 GENERA CALENDARIO"):
        leaders = db[db['Grado']=="R5/R4"]['Nome'].tolist()
        others = db[db['Grado']!="R5/R4"]['Nome'].tolist()
        random.shuffle(others)
        
        m_idx = MESI_ITA.index(st.session_state['sel_mese_ita']) + 1
        import calendar as cal_lib
        num_gg = cal_lib.monthrange(st.session_state['sel_anno'], m_idx)[1]
        
        new_cal = []
        p_idx = 0
        for g in range(1, num_gg + 1):
            if g <= 11:
                c, p = leaders[(g-1)%len(leaders)], leaders[g%len(leaders)]
            else:
                c, p = others[p_idx % len(others)], others[(p_idx+1) % len(others)]
                p_idx += 2
            new_cal.append({"Giorno": g, "Capo": c, "Pass": p})
        st.session_state['master_cal'] = new_cal
    st.markdown('</div>', unsafe_allow_html=True)

with col_b2:
    st.markdown('<div class="btn-resetta">', unsafe_allow_html=True)
    if st.button("🗑️ RESETTA"):
        if 'master_cal' in st.session_state: del st.session_state['master_cal']
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- VISUALIZZAZIONE ---
if 'master_cal' in st.session_state:
    st.markdown(f"### 🖼️ CALENDARIO {st.session_state['sel_mese_ita'].upper()} {st.session_state['sel_anno']}")
    
    st.markdown('<div class="print-container">', unsafe_allow_html=True)
    cols = st.columns(6)
    
    for i, r in enumerate(st.session_state['master_cal']):
        with cols[i % 6]:
            # Colori nomi
            g_c = db[db['Nome']==r['Capo']]['Grado'].values[0] if r['Capo'] in all_names else "R3"
            g_p = db[db['Nome']==r['Pass']]['Grado'].values[0] if r['Pass'] in all_names else "R3"
            c_color = "#ff4757" if g_c == "R5/R4" else "#2ed573"
            p_color = "#ff4757" if g_p == "R5/R4" else "#2ed573"

            # Inizio Card
            st.markdown(f"""
            <div class="summary-card">
                <div class="day-label">GG {r['Giorno']}</div>
                <div class="name-text" style="color:{c_color};">{r['Capo']}</div>
                <div style="color:#444; font-size:0.5rem; text-align:center; margin:2px 0;">&</div>
                <div class="name-text" style="color:{p_color};">{r['Pass']}</div>
            """, unsafe_allow_html=True)
            
            # Pulsanti interni alla card
            st.markdown('<div class="inner-controls">', unsafe_allow_html=True)
            col_mini1, col_mini2 = st.columns(2)
            with col_mini1:
                st.markdown('<div class="card-btn">', unsafe_allow_html=True)
                if st.button("🔄", key=f"inv_{i}"):
                    st.session_state['master_cal'][i]['Capo'], st.session_state['master_cal'][i]['Pass'] = r['Pass'], r['Capo']
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
            with col_mini2:
                st.markdown('<div class="card-btn">', unsafe_allow_html=True)
                if st.button("✏️", key=f"ed_{i}"):
                    st.session_state[f"edit_{i}"] = not st.session_state.get(f"edit_{i}", False)
                st.markdown('</div>', unsafe_allow_html=True)
            st.markdown('</div></div>', unsafe_allow_html=True) # Chiude inner-controls e summary-card

            # Form modifica (appare sotto se cliccato edit)
            if st.session_state.get(f"edit_{i}", False):
                nc = st.selectbox("C", all_names, index=all_names.index(r['Capo']), key=f"selc_{i}")
                np = st.selectbox("P", all_names, index=all_names.index(r['Pass']), key=f"selp_{i}")
                if st.button("OK", key=f"ok_{i}"):
                    st.session_state['master_cal'][i].update({"Capo": nc, "Pass": np})
                    st.session_state[f"edit_{i}"] = False
                    st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
