import streamlit as st
import pandas as pd
import calendar
import random
from datetime import datetime

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="AOSR Train Manager Elite", layout="wide")

# CSS CUSTOM
st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; color: #ffffff; }
    .aosr-header {
        background: linear-gradient(135deg, #1a1f2c 0%, #0b0e14 100%);
        padding: 30px; border-radius: 20px; border: 2px solid #00c8ff;
        text-align: center; margin-bottom: 30px; position: relative;
    }
    .aosr-title { font-family: 'Orbitron', sans-serif; color: #00c8ff; font-size: 2.5rem; letter-spacing: 4px; margin: 0; }
    
    /* Griglia Calendario Principale */
    .calendar-grid {
        display: grid; grid-template-columns: repeat(7, 1fr);
        gap: 15px; margin-top: 20px;
    }
    .day-card {
        background: #161b25; border-radius: 10px; padding: 12px;
        border: 1px solid #2d343f; min-height: 150px;
    }
    .day-number { font-size: 1.2rem; font-weight: 900; color: #555; margin-bottom: 8px; display: block;}
    
    /* Badge Giocatori */
    .p-box { padding: 4px 8px; border-radius: 4px; margin: 2px 0; font-size: 0.8rem; text-transform: uppercase; }
    .label { font-size: 0.6rem; opacity: 0.7; display: block; }
    .r5-r4-card { background: rgba(255, 71, 87, 0.15); border-left: 3px solid #ff4757; color: #ff4757; }
    .r3-card { background: rgba(46, 213, 115, 0.15); border-left: 3px solid #2ed573; color: #2ed573; }
    .r2-r1-card { background: rgba(162, 155, 254, 0.15); border-left: 3px solid #a29bfe; color: #a29bfe; }

    /* Visione d'Insieme Compatta */
    .summary-section {
        background: linear-gradient(180deg, #0b0e14 0%, #1a1f2c 100%);
        padding: 25px; border-radius: 15px; border: 1px solid #00c8ff; margin-top: 30px;
    }
    .summary-container {
        display: grid; grid-template-columns: repeat(auto-fill, minmax(130px, 1fr));
        gap: 10px;
    }
    .summary-item {
        background: rgba(0,0,0,0.6); border: 1px solid #333; padding: 8px; text-align: center; border-radius: 6px;
    }
    .summary-day-num { font-size: 0.75rem; color: #00c8ff; font-weight: bold; margin-bottom: 5px; border-bottom: 1px solid #222;}
    .summary-name { font-size: 0.8rem; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; font-weight: 600; }
    
    /* Edit Buttons Style */
    .stButton>button { border-radius: 5px; font-size: 0.7rem; height: 1.8rem; padding: 0 10px; }
    </style>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@700&display=swap" rel="stylesheet">
    """, unsafe_allow_html=True)

# --- DATABASE ---
if 'players_db' not in st.session_state:
    data = []
    leaders = ["Hool (R5)", "MASTER (R4)", "Le 12 Scimmie (R4)", "Sagittarius A1 (R4)", "Starbetty (R4)", "PEPPE (R4)", "Ricky Around (R4)", "uncle g (R4)", "09ALEX24 (R4)", "ShinyPasta (R4)", "Wall 7 (R4)"]
    for n in leaders: data.append({"Nome": n, "Grado": "R5/R4"})
    r3_list = ["G Erry", "Uncle g brother", "Cane Avvoltoio", "Ghandal", "Aryron", "Tricheco", "Maメツ", "NOVEMBERGENZ", "Lalla 96", "Whale Panda", "GennaroM", "EchoZero", "EDDward", "AMY", "Resilienza", "Ana Bunny", "Giuseppec84", "Benito Muschiolini", "Pandino19", "xFlotchy", "MX63", "holdfast", "Ghost", "BadBigBoss", "Stefano00000", "PakII", "BANDOLERO26", "BlOOdyBlade", "Whale hunter Levve", "Aresxxx", "KingGruffalo", "Hulkspakka", "Joseone", "ImAde", "Nysbie", "LeFada13", "Skifetto", "SPio24", "TomEnergy", "Markus Defender", "Sho0t3r", "Wolf006", "Zokra", "perseusxxx", "Bendico", "Obbyy", "ArLes", "Fatz87", "cruel neve", "Trivellatore", "Osgh00", "Slowfia ABOH", "Pontatinatore", "27Francesco", "MissDrinks", "krompir", "MaledettO"]
    for n in r3_list: data.append({"Nome": n, "Grado": "R3"})
    r2_list = ["teomadh", "Bossnico", "Valecit", "FarmerHool", "camiiiii 08", "Doctor team", "Yass081", "Nuorifleming", "Vergabrio", "Frenk70", "Comandante Maveric", "Thor9000", "MrBolly", "BustaMaki", "Ritardato", "StUnTmArK", "MONKEY D LUFFY 20", "CineSalentino", "Danylo98", "Ezechielefabianino", "BRNcommando", "LEONIDA", "elchicogyot", "erer1000", "Pupisnic", "Backfire1", "AnarchyBG", "Fabrizio1987", "JurdanS", "WiseR9", "Infinity8080"]
    for n in r2_list: data.append({"Nome": n, "Grado": "R2"})
    st.session_state['players_db'] = pd.DataFrame(data)

db = st.session_state['players_db']
all_names = db['Nome'].tolist()

# --- HEADER ---
st.markdown('<div class="aosr-header"><div class="aosr-title">AOSR EXPRESS</div></div>', unsafe_allow_html=True)

# --- CONTROLLI ---
with st.expander("🛠️ CONFIGURAZIONE", expanded=True):
    col_a, col_b = st.columns([1,3])
    with col_a:
        mese_n = st.selectbox("Mese", list(calendar.month_name)[1:], index=datetime.now().month-1)
        anno_n = st.number_input("Anno", 2024, 2030, 2026)
    with col_b:
        meritevoli_opzioni = db[db['Grado'] != "R5/R4"]['Nome'].tolist()
        sel_meritevoli = st.multiselect("Seleziona Partecipanti (Vuoto per TUTTI)", meritevoli_opzioni, default=[])

# --- GENERAZIONE ---
if st.button("🚀 GENERA CALENDARIO AOSR", use_container_width=True):
    pool_giocatori = sel_meritevoli if sel_meritevoli else db[db['Grado'] != "R5/R4"]['Nome'].tolist()
    random.shuffle(pool_giocatori)
    leaders = db[db['Grado']=="R5/R4"]['Nome'].tolist()
    num_gg = calendar.monthrange(anno_n, list(calendar.month_name).index(mese_n))[1]
    
    res_cal = []
    pool_idx = 0
    for g in range(1, num_gg + 1):
        if g <= 11:
            c, p = leaders[(g-1) % len(leaders)], leaders[g % len(leaders)]
        else:
            c = pool_giocatori[pool_idx % len(pool_giocatori)]
            pool_idx += 1
            p = pool_giocatori[pool_idx % len(pool_giocatori)]
            pool_idx += 1
        res_cal.append({"Giorno": g, "Capotreno": c, "Passeggero": p})
    st.session_state['master_cal'] = res_cal

# --- HELPER FUNZIONI ---
def is_dup(nome):
    if not st.session_state.get('master_cal'): return False
    grado = db[db['Nome']==nome]['Grado'].values[0] if nome in all_names else "R3"
    if grado == "R5/R4": return False
    return sum(1 for d in st.session_state['master_cal'] if d['Capotreno']==nome or d['Passeggero']==nome) > 1

# --- VISUALIZZAZIONE ---
if 'master_cal' in st.session_state:
    st.markdown("### 📅 Gestione Dettagliata")
    
    # LISTA EDITABILE CON INVERTI E MODIFICA
    for i, r in enumerate(st.session_state['master_cal']):
        cols = st.columns([0.6, 2, 2, 0.8, 0.8])
        cols[0].markdown(f"**G{r['Giorno']}**")
        
        # Capo e Pass con stili
        for idx, role in enumerate(['Capotreno', 'Passeggero']):
            name = r[role]
            grado = db[db['Nome']==name]['Grado'].values[0] if name in all_names else "R3"
            style = "r5-r4-card" if grado == "R5/R4" else "r3-card" if grado == "R3" else "r2-r1-card"
            warn = "⚠️" if is_dup(name) else ""
            cols[idx+1].markdown(f'<div class="p-box {style}">{role}: {name} {warn}</div>', unsafe_allow_html=True)
        
        # Tasto Inverti
        if cols[3].button("🔄", key=f"inv_{i}", help="Inverti Capo/Pass"):
            st.session_state['master_cal'][i]['Capotreno'], st.session_state['master_cal'][i]['Passeggero'] = r['Passeggero'], r['Capotreno']
            st.rerun()
            
        # Tasto Modifica
        if cols[4].button("✏️", key=f"edit_{i}", help="Cambia Giocatori"):
            st.session_state[f"show_edit_{i}"] = not st.session_state.get(f"show_edit_{i}", False)
        
        # Pannello Modifica (Scompare/Appare)
        if st.session_state.get(f"show_edit_{i}", False):
            ec1, ec2, ec3 = st.columns([3, 3, 1])
            new_c = ec1.selectbox("Nuovo Capo", all_names, index=all_names.index(r['Capotreno']), key=f"sel_c_{i}")
            new_p = ec2.selectbox("Nuovo Pass", all_names, index=all_names.index(r['Passeggero']), key=f"sel_p_{i}")
            if ec3.button("✅", key=f"save_{i}"):
                st.session_state['master_cal'][i]['Capotreno'] = new_c
                st.session_state['master_cal'][i]['Passeggero'] = new_p
                st.session_state[f"show_edit_{i}"] = False
                st.rerun()
        st.markdown('<hr style="margin:5px 0; opacity:0.1">', unsafe_allow_html=True)

    # --- VISIONE D'INSIEME (SCREENSHOT READY) ---
    st.markdown('<div class="summary-section">', unsafe_allow_html=True)
    st.markdown("### 🖼️ VISIONE D'INSIEME (Screenshot Ready)")
    summary_html = '<div class="summary-container">'
    for r in st.session_state['master_cal']:
        g_c = db[db['Nome']==r['Capotreno']]['Grado'].values[0] if r['Capotreno'] in all_names else "R3"
        g_p = db[db['Nome']==r['Passeggero']]['Grado'].values[0] if r['Passeggero'] in all_names else "R3"
        c_color = "#ff4757" if g_c == "R5/R4" else "#2ed573"
        p_color = "#ff4757" if g_p == "R5/R4" else "#a29bfe"
        
        summary_html += f"""
        <div class="summary-item">
            <div class="summary-day-num">GG {r['Giorno']}</div>
            <div class="summary-name" style="color:{c_color};">{r['Capotreno']}</div>
            <div style="font-size:0.5rem; color:#444; margin:2px 0;">&</div>
            <div class="summary-name" style="color:{p_color};">{r['Passeggero']}</div>
        </div>
        """
    summary_html += '</div></div>'
    st.markdown(summary_html, unsafe_allow_html=True)
