import streamlit as st
import pandas as pd
import calendar
import random
from datetime import datetime

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="AOSR Train Manager Elite", layout="wide")

# --- CSS CUSTOM COMPLETO (NEON + CANYON) ---
st.markdown("""
    <style>
    /* Sfondo Canyon scuro */
    .stApp {
        background-image: linear-gradient(rgba(11, 14, 20, 0.85), rgba(11, 14, 20, 0.95)), 
                          url('https://images.unsplash.com/photo-1506197361314-878513b4822a?q=80&w=1920&auto=format&fit=crop');
        background-size: cover;
        background-position: center;
        color: #ffffff;
    }

    /* Header stilizzato con icona treno e Glow */
    .aosr-header {
        background: linear-gradient(135deg, rgba(26, 31, 44, 0.95) 0%, rgba(11, 14, 20, 0.95) 100%);
        padding: 30px; 
        border-radius: 20px; 
        border: 2px solid #00c8ff;
        text-align: center; 
        margin-bottom: 30px;
        position: relative;
        box-shadow: 0 0 15px rgba(0, 200, 255, 0.4);
    }
    
    /* Titolo Orbitron con treni 🚄 */
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

    /* Badge Giocatori (Label) */
    .p-box { padding: 4px 8px; border-radius: 4px; margin: 2px 0; font-size: 0.8rem; text-transform: uppercase; font-weight: 600; }
    .r5-r4-card { background: rgba(255, 71, 87, 0.15); border-left: 3px solid #ff4757; color: #ff4757; }
    .r3-card { background: rgba(46, 213, 115, 0.15); border-left: 3px solid #2ed573; color: #2ed573; }
    .r2-r1-card { background: rgba(162, 155, 254, 0.15); border-left: 3px solid #a29bfe; color: #a29bfe; }

    /* Area Screenshot (Cornice Azzurra) */
    .print-container { 
        background-color: rgba(0, 0, 0, 0.9); 
        padding: 30px; 
        border-radius: 20px; 
        border: 3px solid #00c8ff;
        box-shadow: inset 0 0 20px rgba(0, 200, 255, 0.2);
    }

    /* CASELLA CALENDARIO CON EFFETTO HOVER FLUO */
    .summary-card {
        background: rgba(17, 17, 17, 0.9); 
        border: 1px solid #333; 
        padding: 12px; 
        text-align: center; 
        border-radius: 12px; 
        margin-bottom: 15px;
        min-height: 110px;
        transition: all 0.3s ease-in-out; /* Animazione fluida */
    }

    /* Effetto Hover (Mouse Sopra) */
    .summary-card:hover {
        transform: scale(1.05); /* Si ingrandisce leggermente */
        border-color: #00c8ff; /* Bordo azzurro fluo */
        box-shadow: 0 0 20px rgba(0, 200, 255, 0.8); /* Bagliore esterno */
        background: rgba(26, 26, 26, 0.95);
    }

    /* Giorno Label con Glow */
    .day-label { 
        color: #00c8ff; 
        font-weight: 900; 
        font-size: 0.9rem; 
        border-bottom: 1px solid #222; 
        margin-bottom: 8px;
        text-shadow: 0 0 5px rgba(0, 200, 255, 0.5);
    }
    
    /* Pulsante Genera Fluo Verde */
    .stButton > button[kind="primary"] {
        width: 100%; height: 80px; font-size: 1.8rem !important; 
        background: linear-gradient(45deg, #2ed573, #00ff85) !important;
        border: none !important;
        box-shadow: 0 0 20px rgba(46, 213, 115, 0.5);
        color: black !important;
        font-family: 'Orbitron', sans-serif;
        transition: 0.3s;
    }
    .stButton > button:hover {
        box-shadow: 0 0 40px rgba(46, 213, 115, 0.8) !important;
        transform: translateY(-2px);
    }
    </style>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@700&display=swap" rel="stylesheet">
    """, unsafe_allow_html=True)

# --- DATABASE INIZIALE ---
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

# --- HEADER CON TRENO 🚄 ---
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
    with st.expander("🛠️ CONFIGURAZIONE E PARTECIPANTI", expanded=True):
        col_time, col_players = st.columns([1,2])
        
        # Selezione Tempo
        st.session_state['sel_mese'] = col_time.selectbox("Mese", list(calendar.month_name)[1:], index=list(calendar.month_name).index(st.session_state['sel_mese'])-1)
        st.session_state['sel_anno'] = col_time.number_input("Anno", 2024, 2030, st.session_state['sel_anno'])
        
        # NOVIETÀ: Selezione Passeggeri divisi per Categoria
        st.markdown("### 👥 Selezione Passeggeri (Extra Leader)")
        
        # Lista R3
        meritevoli_r3 = db[db['Grado'] == "R3"]['Nome'].tolist()
        sel_r3 = col_players.multiselect("Seleziona R3 (Vuoto = TUTTI)", meritevoli_r3, help="Scegli quali R3 far entrare nel pool casuale dopo il giorno 11.")
        
        # Lista R2
        meritevoli_r2 = db[db['Grado'] == "R2"]['Nome'].tolist()
        sel_r2 = col_players.multiselect("Seleziona R2 (Vuoto = TUTTI)", meritevoli_r2, help="Scegli quali R2 far entrare nel pool casuale dopo il giorno 11.")

    # --- BOTTONI AZIONE ---
    b_col1, b_col2 = st.columns([3, 1])
    
    if b_col1.button("🚀 GENERA NUOVO CALENDARIO", use_container_width=True, type="primary"):
        # Crea pool passeggeri basato sulla selezione (o tutti se vuoto)
        pool_r3 = sel_r3 if sel_r3 else meritevoli_r3
        pool_r2 = sel_r2 if sel_r2 else meritevoli_r2
        
        # Unisce e mescola il pool finale
        final_pool = pool_r3 + pool_r2
        random.shuffle(final_pool)
        
        leaders = db[db['Grado']=="R5/R4"]['Nome'].tolist()
        num_gg = calendar.monthrange(st.session_state['sel_anno'], list(calendar.month_name).index(st.session_state['sel_mese']))[1]
        
        cal = []
        p_idx = 0
        for g in range(1, num_gg + 1):
            if g <= 11:
                # Turni Leader R4/R5
                c, p = leaders[(g-1)%len(leaders)], leaders[g%len(leaders)]
            else:
                # Turni Passeggeri R3/R2 (se il pool non è vuoto)
                if final_pool:
                    c = final_pool[p_idx % len(final_pool)]; p_idx += 1
                    p = final_pool[p_idx % len(final_pool)]; p_idx += 1
                else:
                    c, p = "DA ASSEGNARE", "DA ASSEGNARE"
            cal.append({"Giorno": g, "Capo": c, "Pass": p})
        st.session_state['master_cal'] = cal

    # --- PULSANTE RESET ---
    if b_col2.button("🗑️ RESETTA", use_container_width=True, help="Cancella il calendario attuale e ricomincia."):
        if 'master_cal' in st.session_state:
            del st.session_state['master_cal']
        st.rerun()

# --- VISUALIZZAZIONE GESTIONE ---
if 'master_cal' in st.session_state and not st.session_state.get('print_mode', False):
    st.subheader("📝 Modifica Giorni")
    for i, r in enumerate(st.session_state['master_cal']):
        col = st.columns([0.6, 2, 2, 0.5, 0.5])
        col[0].write(f"**G{r['Giorno']}**")
        for idx, role in enumerate(['Capo', 'Pass']):
            name = r[role]
            # Gestione nomi non presenti nel DB (es. DA ASSEGNARE)
            if name in all_names:
                grado = db[db['Nome']==name]['Grado'].values[0]
                s = "r5-r4-card" if grado == "R5/R4" else "r3-card" if grado == "R3" else "r2-r1-card"
            else:
                s = "" # Nessuno stile speciale
            col[idx+1].markdown(f'<div class="p-box {s}">{name}</div>', unsafe_allow_html=True)
        
        if col[3].button("🔄", key=f"inv_{i}"):
            st.session_state['master_cal'][i]['Capo'], st.session_state['master_cal'][i]['Pass'] = r['Pass'], r['Capo']
            st.rerun()
        if col[4].button("✏️", key=f"ed_{i}"):
            st.session_state[f"em_{i}"] = not st.session_state.get(f"em_{i}", False)
        
        if st.session_state.get(f"em_{i}", False):
            e1, e2, e3 = st.columns([3,3,1])
            try:
                # Cerca l'indice del nome attuale, usa 0 se non trovato
                idx_c = all_names.index(r['Capo']) if r['Capo'] in all_names else 0
                idx_p = all_names.index(r['Pass']) if r['Pass'] in all_names else 0
                nc = e1.selectbox("Capo", all_names, index=idx_c, key=f"selc_{i}")
                np = e2.selectbox("Pass", all_names, index=idx_p, key=f"selp_{i}")
                if e3.button("✅", key=f"save_{i}"):
                    st.session_state['master_cal'][i].update({"Capo": nc, "Pass": np})
                    st.session_state[f"em_{i}"] = False
                    st.rerun()
            except ValueError:
                e1.error("Errore nel caricamento dei nomi.")

# --- GRIGLIA FINALE (SCREENSHOT READY) ---
if 'master_cal' in st.session_state:
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
                    <div style="color:{c_c}; font-size:0.85rem; font-weight:bold; text-transform:uppercase;">{r['Capo']}</div>
                    <div style="color:#444; font-size:0.6rem; margin:2px 0;">TRAIN PASS</div>
                    <div style="color:{p_c}; font-size:0.85rem; font-weight:bold; text-transform:uppercase;">{r['Pass']}</div>
                </div>
                """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # --- BOTTONE FOTO ---
    st.markdown("<br>", unsafe_allow_html=True)
    if not st.session_state.get('print_mode', False):
        if st.button("🖨️ MODALITÀ FOTO (SCREENSHOT)", use_container_width=True):
            st.session_state['print_mode'] = True
            st.rerun()
    else:
        if st.button("🔙 TORNA ALLA MODIFICA", use_container_width=True):
            st.session_state['print_mode'] = False
            st.rerun()
