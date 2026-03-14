import streamlit as st
import pandas as pd
import calendar
import random
from datetime import datetime

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="AOSR Train Manager Elite", layout="wide")

# --- CSS CUSTOM ---
st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; color: #ffffff; }
    .aosr-header {
        background: linear-gradient(135deg, #1a1f2c 0%, #0b0e14 100%);
        padding: 25px; border-radius: 15px; border: 2px solid #00c8ff;
        text-align: center; margin-bottom: 20px;
    }
    .aosr-title { font-family: 'Orbitron', sans-serif; color: #00c8ff; font-size: 2.2rem; letter-spacing: 3px; margin: 0; }
    
    /* Badge Giocatori */
    .p-box { padding: 6px 10px; border-radius: 6px; margin: 3px 0; font-size: 0.85rem; text-transform: uppercase; font-weight: bold; }
    .r5-r4-card { background: rgba(255, 71, 87, 0.2); border-left: 4px solid #ff4757; color: #ff4757; }
    .r3-card { background: rgba(46, 213, 115, 0.2); border-left: 4px solid #2ed573; color: #2ed573; }
    .r2-r1-card { background: rgba(162, 155, 254, 0.2); border-left: 4px solid #a29bfe; color: #a29bfe; }

    /* Stile Griglia Screenshot */
    .print-container {
        background-color: #000; padding: 30px; border-radius: 20px; border: 3px solid #00c8ff;
    }
    .summary-card {
        background: #111; border: 1px solid #333; padding: 12px; 
        text-align: center; border-radius: 10px; margin-bottom: 15px;
        min-height: 110px; box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    .day-label { color: #00c8ff; font-weight: 900; font-size: 0.9rem; border-bottom: 1px solid #222; margin-bottom: 8px; }
    
    /* Bottone Gigante Stampa */
    .stButton > button[kind="primary"] {
        width: 100%; height: 80px; font-size: 1.8rem !important; 
        background-color: #2ed573 !important; border: none !important;
        font-family: 'Orbitron', sans-serif; transition: 0.3s;
    }
    </style>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@700&display=swap" rel="stylesheet">
    """, unsafe_allow_html=True)

# --- DATABASE INIZIALE ---
if 'players_db' not in st.session_state:
    data = []
    leaders = ["Hool (R5)", "MASTER (R4)", "Le 12 Scimmie (R4)", "Sagittarius A1 (R4)", "Starbetty (R4)", "PEPPE (R4)", "Ricky Around (R4)", "uncle g (R4)", "09ALEX24 (R4)", "ShinyPasta (R4)", "Wall 7 (R4)"]
    for n in leaders: data.append({"Nome": n, "Grado": "R5/R4"})
    r3 = ["G Erry", "Uncle g brother", "Cane Avvoltoio", "Ghandal", "Aryron", "Tricheco", "Maメツ", "NOVEMBERGENZ", "Lalla 96", "Whale Panda", "GennaroM", "EchoZero", "EDDward", "AMY", "Resilienza", "Ana Bunny", "Giuseppec84", "Benito Muschiolini", "Pandino19", "xFlotchy", "MX63", "holdfast", "Ghost", "BadBigBoss", "Stefano00000", "PakII", "BANDOLERO26", "BlOOdyBlade", "Whale hunter Levve", "Aresxxx", "KingGruffalo", "Hulkspakka", "Joseone", "ImAde", "Nysbie", "LeFada13", "Skifetto", "SPio24", "TomEnergy", "Markus Defender", "Sho0t3r", "Wolf006", "Zokra", "perseusxxx", "Bendico", "Obbyy", "ArLes", "Fatz87", "cruel neve", "Trivellatore", "Osgh00", "Slowfia ABOH", "Pontatinatore", "27Francesco", "MissDrinks", "krompir", "MaledettO"]
    for n in r3: data.append({"Nome": n, "Grado": "R3"})
    r2 = ["teomadh", "Bossnico", "Valecit", "FarmerHool", "camiiiii 08", "Doctor team", "Yass081", "Nuorifleming", "Vergabrio", "Frenk70", "Comandante Maveric", "Thor9000", "MrBolly", "BustaMaki", "Ritardato", "StUnTmArK", "MONKEY D LUFFY 20", "CineSalentino", "Danylo98", "Ezechielefabianino", "BRNcommando", "LEONIDA", "elchicogyot", "erer1000", "Pupisnic", "Backfire1", "AnarchyBG", "Fabrizio1987", "JurdanS", "WiseR9", "Infinity8080"]
    for n in r2: data.append({"Nome": n, "Grado": "R2"})
    st.session_state['players_db'] = pd.DataFrame(data)

db = st.session_state['players_db']
all_names = db['Nome'].tolist()

# --- HEADER ---
if not st.session_state.get('print_mode', False):
    st.markdown('<div class="aosr-header"><div class="aosr-title">AOSR EXPRESS MANAGER</div></div>', unsafe_allow_html=True)

# --- MENU CONFIGURAZIONE (Nascosto in stampa) ---
if not st.session_state.get('print_mode', False):
    with st.expander("⚙️ CONFIGURAZIONE E PARTECIPANTI", expanded=True):
        c1, c2 = st.columns([1,2])
        mese_n = c1.selectbox("Seleziona Mese", list(calendar.month_name)[1:], index=datetime.now().month-1)
        anno_n = c1.number_input("Anno", 2024, 2030, 2026)
        meritevoli_list = db[db['Grado'] != "R5/R4"]['Nome'].tolist()
        sel_meritevoli = c2.multiselect("Partecipanti specifici (Lascia vuoto per TUTTI)", meritevoli_list)

    if st.button("🚀 GENERA NUOVO CALENDARIO", use_container_width=True):
        pool = sel_meritevoli if sel_meritevoli else meritevoli_list
        random.shuffle(pool)
        leaders = db[db['Grado']=="R5/R4"]['Nome'].tolist()
        num_gg = calendar.monthrange(anno_n, list(calendar.month_name).index(mese_n))[1]
        
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

# --- LOGICA DI VISUALIZZAZIONE ---
if 'master_cal' in st.session_state:
    
    # Sezione Modifica (Nascosta in stampa)
    if not st.session_state.get('print_mode', False):
        st.subheader("📝 Modifica e Revisione")
        for i, r in enumerate(st.session_state['master_cal']):
            col = st.columns([0.6, 2, 2, 0.5, 0.5])
            col[0].write(f"**G{r['Giorno']}**")
            
            for idx, role in enumerate(['Capo', 'Pass']):
                name = r[role]
                grado = db[db['Nome']==name]['Grado'].values[0] if name in all_names else "R3"
                s = "r5-r4-card" if grado == "R5/R4" else "r3-card" if grado == "R3" else "r2-r1-card"
                col[idx+1].markdown(f'<div class="p-box {s}">{name}</div>', unsafe_allow_html=True)
            
            if col[3].button("🔄", key=f"i_{i}"):
                st.session_state['master_cal'][i]['Capo'], st.session_state['master_cal'][i]['Pass'] = r['Pass'], r['Capo']
                st.rerun()
            if col[4].button("✏️", key=f"e_{i}"):
                st.session_state[f"edit_{i}"] = not st.session_state.get(f"edit_{i}", False)
            
            if st.session_state.get(f"edit_{i}", False):
                e1, e2, e3 = st.columns([3,3,1])
                nc = e1.selectbox("Capo", all_names, index=all_names.index(r['Capo']), key=f"nc_{i}")
                np = e2.selectbox("Pass", all_names, index=all_names.index(r['Pass']), key=f"np_{i}")
                if e3.button("✅", key=f"ok_{i}"):
                    st.session_state['master_cal'][i].update({"Capo": nc, "Pass": np})
                    st.session_state[f"edit_{i}"] = False
                    st.rerun()

    # --- VISIONE D'INSIEME (IL CALENDARIO) ---
    st.markdown("---")
    st.markdown(f"### 🖼️ CALENDARIO AOSR - {mese_n.upper()} {anno_n}")
    
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
                    <div class="day-label">GIORNO {r['Giorno']}</div>
                    <div style="color:{c_c}; font-size:0.8rem; font-weight:bold;">{r['Capo']}</div>
                    <div style="color:#444; font-size:0.5rem; margin:2px 0;">&</div>
                    <div style="color:{p_c}; font-size:0.8rem; font-weight:bold;">{r['Pass']}</div>
                </div>
                """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # --- BOTTONE FINALE DI STAMPA ---
    st.markdown("<br>", unsafe_allow_html=True)
    if not st.session_state.get('print_mode', False):
        if st.button("🖨️ STAMPA CALENDARIO (MODALITÀ FOTO)", type="primary"):
            st.session_state['print_mode'] = True
            st.rerun()
    else:
        if st.button("🔙 TORNA ALLA MODIFICA"):
            st.session_state['print_mode'] = False
            st.rerun()
        st.info("💡 Ora puoi fare uno screenshot pulito o premere CTRL+P per salvare in PDF/Immagine.")
