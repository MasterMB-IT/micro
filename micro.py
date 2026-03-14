import streamlit as st
import pandas as pd
import calendar
import random
from datetime import datetime

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="AOSR Train Manager Elite", layout="wide")

# --- CSS CUSTOM: PULSANTI ALLUNGATI E FLUO ---
st.markdown("""
    <style>
    .stApp {
        background-image: linear-gradient(rgba(11, 14, 20, 0.85), rgba(11, 14, 20, 0.95)), 
                          url('https://images.unsplash.com/photo-1506197361314-878513b4822a?q=80&w=1920&auto=format&fit=crop');
        background-size: cover;
        background-position: center;
        color: #ffffff;
    }

    .aosr-header {
        background: linear-gradient(135deg, rgba(26, 31, 44, 0.95) 0%, rgba(11, 14, 20, 0.95) 100%);
        padding: 30px; border-radius: 20px; border: 2px solid #00c8ff;
        text-align: center; margin-bottom: 30px;
        box-shadow: 0 0 20px rgba(0, 200, 255, 0.4);
    }
    
    .aosr-title {
        font-family: 'Orbitron', sans-serif; color: #00c8ff; font-size: 2.5rem;
        display: flex; align-items: center; justify-content: center; gap: 15px;
        text-shadow: 0 0 10px rgba(0, 200, 255, 0.5);
    }

    /* --- BOTTONI ALLUNGATI E POTENTI --- */
    .stButton > button {
        width: 100% !important; 
        height: 90px !important; /* Molto più alti */
        font-size: 1.6rem !important; /* Testo più grande */
        font-family: 'Orbitron', sans-serif !important; 
        border: none !important;
        transition: 0.3s all ease-in-out !important; 
        text-transform: uppercase !important; 
        font-weight: 900 !important;
        letter-spacing: 5px !important; /* Testo distanziato per allungare visivamente */
        border-radius: 15px !important;
    }

    /* Bottone Genera (Verde Cyber) */
    div[data-testid="stHorizontalBlock"] div:nth-child(1) button {
        background: linear-gradient(90deg, #2ed573, #00ff85) !important;
        box-shadow: 0 0 25px rgba(46, 213, 115, 0.5) !important;
        color: #000 !important;
    }
    div[data-testid="stHorizontalBlock"] div:nth-child(1) button:hover {
        box-shadow: 0 0 45px rgba(46, 213, 115, 0.9) !important;
        transform: scale(1.03) translateY(-2px);
    }

    /* Bottone Resetta (Rosso Neon) */
    div[data-testid="stHorizontalBlock"] div:nth-child(2) button {
        background: linear-gradient(90deg, #ff4757, #ff0055) !important;
        box-shadow: 0 0 25px rgba(255, 71, 87, 0.5) !important;
        color: #fff !important;
    }
    div[data-testid="stHorizontalBlock"] div:nth-child(2) button:hover {
        box-shadow: 0 0 45px rgba(255, 71, 87, 0.9) !important;
        transform: scale(1.03) translateY(-2px);
    }

    /* Cards e Layout */
    .print-container { 
        background-color: rgba(0, 0, 0, 0.9); padding: 30px; border-radius: 20px; 
        border: 3px solid #00c8ff; box-shadow: inset 0 0 20px rgba(0, 200, 255, 0.2);
    }
    .summary-card {
        background: rgba(17, 17, 17, 0.9); border: 1px solid #333; padding: 12px; 
        text-align: center; border-radius: 12px; margin-bottom: 15px;
        min-height: 110px; transition: 0.3s;
    }
    .summary-card:hover {
        transform: translateY(-5px); border-color: #00c8ff;
        box-shadow: 0 5px 20px rgba(0, 200, 255, 0.6);
    }
    .day-label { color: #00c8ff; font-weight: 900; border-bottom: 1px solid #222; margin-bottom: 8px; }
    .p-box { padding: 4px 8px; border-radius: 4px; margin: 2px 0; font-size: 0.8rem; font-weight: 600; text-transform: uppercase; }
    .r5-r4-card { background: rgba(255, 71, 87, 0.15); border-left: 3px solid #ff4757; color: #ff4757; }
    .r3-card { background: rgba(46, 213, 115, 0.15); border-left: 3px solid #2ed573; color: #2ed573; }
    .r2-r1-card { background: rgba(162, 155, 254, 0.15); border-left: 3px solid #a29bfe; color: #a29bfe; }
    </style>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&display=swap" rel="stylesheet">
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
    st.session_state['sel_mese'] = list(calendar.month_name)[datetime.now().month]
    st.session_state['sel_anno'] = 2026

db = st.session_state['players_db']
all_names = db['Nome'].tolist()

# --- HEADER ---
st.markdown('<div class="aosr-header"><div class="aosr-title">🚄 AOSR EXPRESS MANAGER 🚄</div></div>', unsafe_allow_html=True)

# --- CONFIGURAZIONE ---
if not st.session_state.get('print_mode', False):
    with st.expander("🛠️ CONFIGURAZIONE PASSEGGERI", expanded=True):
        c_time, c_r3, c_r2 = st.columns([1,1.5,1.5])
        st.session_state['sel_mese'] = c_time.selectbox("Mese", list(calendar.month_name)[1:], index=list(calendar.month_name).index(st.session_state['sel_mese'])-1)
        st.session_state['sel_anno'] = c_time.number_input("Anno", 2024, 2030, st.session_state['sel_anno'])
        
        m_r3 = db[db['Grado'] == "R3"]['Nome'].tolist()
        m_r2 = db[db['Grado'] == "R2"]['Nome'].tolist()
        sel_r3 = c_r3.multiselect("Filtra R3 (Vuoto=TUTTI)", m_r3)
        sel_r2 = c_r2.multiselect("Filtra R2 (Vuoto=TUTTI)", m_r2)

    # --- BOTTONI AZIONE AFFIANCATI (VERSIONE XL) ---
    col_btn1, col_btn2 = st.columns(2)
    
    if col_btn1.button("🚀 GENERA"):
        pool = (sel_r3 if sel_r3 else m_r3) + (sel_r2 if sel_r2 else m_r2)
        random.shuffle(pool)
        leaders = db[db['Grado']=="R5/R4"]['Nome'].tolist()
        num_gg = calendar.monthrange(st.session_state['sel_anno'], list(calendar.month_name).index(st.session_state['sel_mese']))[1]
        
        cal = []
        p_idx = 0
        for g in range(1, num_gg + 1):
            if g <= 11:
                c, p = leaders[(g-1)%len(leaders)], leaders[g%len(leaders)]
            else:
                c = pool[p_idx % len(pool)]; p_idx += 1
                p = pool[p_idx % len(pool)]; p_idx += 1
            cal.append({"Giorno": g, "Capo": c, "Pass": p})
        st.session_state['master_cal'] = cal

    if col_btn2.button("🗑️ RESETTA"):
        if 'master_cal' in st.session_state:
            del st.session_state['master_cal']
        st.rerun()

# --- VISUALIZZAZIONE ---
if 'master_cal' in st.session_state:
    if not st.session_state.get('print_mode', False):
        st.subheader("📝 Modifica Rapida")
        for i, r in enumerate(st.session_state['master_cal']):
            col = st.columns([0.6, 2, 2, 0.5, 0.5])
            col[0].write(f"**G{r['Giorno']}**")
            for idx, role in enumerate(['Capo', 'Pass']):
                name = r[role]
                grado = db[db['Nome']==name]['Grado'].values[0] if name in all_names else "R3"
                s = "r5-r4-card" if grado == "R5/R4" else "r3-card" if grado == "R3" else "r2-r1-card"
                col[idx+1].markdown(f'<div class="p-box {s}">{name}</div>', unsafe_allow_html=True)
            if col[3].button("🔄", key=f"inv_{i}"):
                st.session_state['master_cal'][i]['Capo'], st.session_state['master_cal'][i]['Pass'] = r['Pass'], r['Capo']
                st.rerun()
            if col[4].button("✏️", key=f"ed_{i}"):
                st.session_state[f"em_{i}"] = not st.session_state.get(f"em_{i}", False)
            if st.session_state.get(f"em_{i}", False):
                e1, e2, e3 = st.columns([3,3,1])
                nc = e1.selectbox("Capo", all_names, index=all_names.index(r['Capo']), key=f"selc_{i}")
                np = e2.selectbox("Pass", all_names, index=all_names.index(r['Pass']), key=f"selp_{i}")
                if e3.button("✅", key=f"save_{i}"):
                    st.session_state['master_cal'][i].update({"Capo": nc, "Pass": np})
                    st.session_state[f"em_{i}"] = False
                    st.rerun()

    # --- GRIGLIA FINALE ---
    st.markdown(f"### 🖼️ CALENDARIO {st.session_state['sel_mese'].upper()}")
    with st.container():
        st.markdown('<div class="print-container">', unsafe_allow_html=True)
        cols_per_row = 6
        for i in range(0, len(st.session_state['master_cal']), cols_per_row):
            row_data = st.session_state['master_cal'][i : i + cols_per_row]
            grid = st.columns(cols_per_row)
            for idx, r in enumerate(row_data):
                g_c = db[db['Nome']==r['Capo']]['Grado'].values[0] if r['Capo'] in all_names else "R3"
                g_p = db[db['Nome']==r['Pass']]['Grado'].values[0] if r['Pass'] in all_names else "R3"
                c_c = "#ff4757" if g_c == "R5/R4" else "#2ed573" if g_c == "R3" else "#a29bfe"
                p_c = "#ff4757" if g_p == "R5/R4" else "#2ed573" if g_p == "R3" else "#a29bfe"
                grid[idx].markdown(f"""
                <div class="summary-card">
                    <div class="day-label">GG {r['Giorno']}</div>
                    <div style="color:{c_c}; font-size:0.85rem; font-weight:bold;">{r['Capo']}</div>
                    <div style="color:#444; font-size:0.55rem; margin:2px 0;">&</div>
                    <div style="color:{p_c}; font-size:0.85rem; font-weight:bold;">{r['Pass']}</div>
                </div>
                """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # --- BOTTONE FOTO ---
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("📸 MODALITÀ SCREENSHOT", use_container_width=True):
        st.session_state['print_mode'] = not st.session_state.get('print_mode', False)
        st.rerun()
