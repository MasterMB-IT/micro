import streamlit as st
import pandas as pd
import calendar
import random
from datetime import datetime

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="AOSR Train Manager Elite", layout="wide")

# --- CSS CUSTOM CON IMMAGINE DI SFONDO ---
# Ho aggiunto un'immagine di sfondo di un canyon scuro e sfocato per l'atmosfera.
st.markdown("""
    <style>
    /* Sfondo dell'intera app con immagine Canyon */
    .stApp {
        background-image: linear-gradient(rgba(11, 14, 20, 0.8), rgba(11, 14, 20, 0.9)), 
                          url('https://images.unsplash.com/photo-1506197361314-878513b4822a?q=80&w=1920&auto=format&fit=crop');
        background-size: cover;
        background-position: center;
        color: #ffffff;
    }

    /* Header stilizzato con icona treno */
    .aosr-header {
        background: linear-gradient(135deg, rgba(26, 31, 44, 0.95) 0%, rgba(11, 14, 20, 0.95) 100%);
        padding: 30px; 
        border-radius: 20px; 
        border: 2px solid #00c8ff;
        text-align: center; 
        margin-bottom: 30px;
        position: relative;
    }
    
    /* Titolo con icona treno */
    .aosr-title {
        font-family: 'Orbitron', sans-serif;
        color: #00c8ff;
        font-size: 2.5rem;
        letter-spacing: 4px;
        margin: 0;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 15px;
    }
    .train-icon { font-size: 3rem; }

    /* Griglia Calendario Principale */
    .calendar-grid {
        display: grid; 
        grid-template-columns: repeat(7, 1fr);
        gap: 15px; 
        margin-top: 20px;
    }
    .day-card {
        background: rgba(22, 27, 37, 0.9); 
        border-radius: 10px; 
        padding: 12px;
        border: 1px solid #2d343f; 
        min-height: 140px;
    }
    .day-number { font-size: 1.2rem; font-weight: 900; color: #555; margin-bottom: 8px; display: block;}
    
    /* Badge Giocatori */
    .p-box { padding: 4px 8px; border-radius: 4px; margin: 2px 0; font-size: 0.8rem; text-transform: uppercase; font-weight: 600; }
    .label { font-size: 0.6rem; opacity: 0.7; display: block; }
    .r5-r4-card { background: rgba(255, 71, 87, 0.15); border-left: 3px solid #ff4757; color: #ff4757; }
    .r3-card { background: rgba(46, 213, 115, 0.15); border-left: 3px solid #2ed573; color: #2ed573; }
    .r2-r1-card { background: rgba(162, 155, 254, 0.15); border-left: 3px solid #a29bfe; color: #a29bfe; }
    </style>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@700&display=swap" rel="stylesheet">
    """, unsafe_allow_html=True)

# --- DATABASE AGGIORNATO CON R2 ---
if 'players_db' not in st.session_state:
    data = []
    leaders = ["Hool (R5)", "MASTER (R4)", "Le 12 Scimmie (R4)", "Sagittarius A1 (R4)", "Starbetty (R4)", "PEPPE (R4)", "Ricky Around (R4)", "uncle g (R4)", "09ALEX24 (R4)", "ShinyPasta (R4)", "Wall 7 (R4)"]
    for n in leaders: data.append({"Nome": n, "Grado": "R5/R4"})
    
    r3 = ["G Erry", "Uncle g brother", "Cane Avvoltoio", "Ghandal", "Aryron", "Tricheco", "Maメツ", "NOVEMBERGENZ", "Lalla 96", "Whale Panda", "GennaroM", "EchoZero", "EDDward", "AMY", "Resilienza", "Ana Bunny", "Giuseppec84", "Benito Muschiolini", "Pandino19", "xFlotchy", "MX63", "holdfast", "Ghost", "BadBigBoss", "Stefano00000", "PakII", "BANDOLERO26", "BlOOdyBlade", "Whale hunter Levve", "Aresxxx", "KingGruffalo", "Hulkspakka", "Joseone", "ImAde", "Nysbie", "LeFada13", "Skifetto", "SPio24", "TomEnergy", "Markus Defender", "Sho0t3r", "Wolf006", "Zokra", "perseusxxx", "Bendico", "Obbyy", "ArLes", "Fatz87", "cruel neve", "Trivellatore", "Osgh00", "Slowfia ABOH", "Pontatinatore", "27Francesco", "MissDrinks", "krompir", "MaledettO"]
    for n in r3: data.append({"Nome": n, "Grado": "R3"})
    
    # Lista R2 estrapolata dai tuoi screenshot
    r2 = ["teomadh", "Bossnico", "Valecit", "FarmerHool", "camiiiii 08", "Doctor team", "Yass081", "Nuorifleming", "Vergabrio", "Frenk70", "Comandante Maveric", "Thor9000", "MrBolly", "BustaMaki", "Ritardato", "StUnTmArK", "MONKEY D LUFFY 20", "CineSalentino", "Danylo98", "Ezechielefabianino", "BRNcommando", "LEONIDA", "elchicogyot", "erer1000", "Pupisnic", "Backfire1", "AnarchyBG", "Fabrizio1987", "JurdanS", "WiseR9", "Infinity8080"]
    for n in r2: data.append({"Nome": n, "Grado": "R2"})
    
    st.session_state['players_db'] = pd.DataFrame(data)
    st.session_state['sel_mese'] = list(calendar.month_name)[datetime.now().month]
    st.session_state['sel_anno'] = 2026

db = st.session_state['players_db']
all_names = db['Nome'].tolist()

# --- HEADER CON ICONA TRENO ---
# Ho aggiunto un emoji stilizzato di un treno ad alta velocità 🚄 accanto al titolo.
st.markdown("""
    <div class="aosr-header">
        <div class="aosr-title">
            <span class="train-icon">🚄</span>
            <span>AOSR EXPRESS MANAGER</span>
            <span class="train-icon">🚄</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- CONFIGURAZIONE ---
if not st.session_state.get('print_mode', False):
    with st.expander("⚙️ CONFIGURAZIONE E PARTECIPANTI", expanded=True):
        c1, c2 = st.columns([1,2])
        st.session_state['sel_mese'] = c1.selectbox("Mese", list(calendar.month_name)[1:], index=list(calendar.month_name).index(st.session_state['sel_mese'])-1)
        st.session_state['sel_anno'] = c1.number_input("Anno", 2024, 2030, st.session_state['sel_anno'])
        meritevoli = db[db['Grado'] != "R5/R4"]['Nome'].tolist()
        sel_meritevoli = c2.multiselect("Seleziona Partecipanti (Vuoto = TUTTI)", meritevoli)

    if st.button("🚀 GENERA / AGGIORNA CALENDARIO", use_container_width=True):
        pool = sel_meritevoli if sel_meritevoli else meritevoli
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

# --- VISUALIZZAZIONE ---
if 'master_cal' in st.session_state:
    if not st.session_state.get('print_mode', False):
        st.subheader("📝 Modifica Giorni")
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

    # --- TITOLO CALENDARIO ---
    m_titolo = st.session_state['sel_mese'].upper()
    a_titolo = st.session_state['sel_anno']
    st.markdown(f"### 🖼️ CALENDARIO AOSR - {m_titolo} {a_titolo}")
    
    # --- GRIGLIA FINALE (Screenshot Ready) ---
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

    # --- BOTTONE STAMPA ---
    st.markdown("<br>", unsafe_allow_html=True)
    if not st.session_state.get('print_mode', False):
        if st.button("🖨️ STAMPA CALENDARIO (MODALITÀ FOTO)", type="primary"):
            st.session_state['print_mode'] = True
            st.rerun()
    else:
        if st.button("🔙 TORNA ALLA MODIFICA"):
            st.session_state['print_mode'] = False
            st.rerun()
