import streamlit as st
import pandas as pd
import calendar
import random
from datetime import datetime

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="AOSR Train Manager Elite", layout="wide")

# --- CSS CUSTOM PER EFFETTO "FOTO" ---
st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; color: #ffffff; }
    
    /* Container che simula la foto finale */
    .photo-canvas {
        background-color: #000000;
        padding: 40px;
        border: 4px solid #00c8ff;
        border-radius: 20px;
        box-shadow: 0px 0px 30px rgba(0, 200, 255, 0.3);
        margin-bottom: 20px;
    }

    .summary-card {
        background: #111;
        border: 1px solid #333;
        padding: 15px;
        text-align: center;
        border-radius: 12px;
        margin-bottom: 15px;
        min-height: 120px;
    }

    .day-label { color: #00c8ff; font-weight: 900; font-size: 1rem; border-bottom: 1px solid #222; margin-bottom: 10px; }
    
    /* Bottone Gigante */
    .stButton > button[kind="primary"] {
        width: 100%;
        height: 100px;
        font-size: 2rem !important;
        background: linear-gradient(90deg, #2ed573, #7bed9f) !important;
        border: none !important;
        color: black !important;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# --- DATABASE (Incluso aggiornamento R2 dai file) ---
if 'players_db' not in st.session_state:
    data = []
    # R5/R4
    leaders = ["Hool (R5)", "MASTER (R4)", "Le 12 Scimmie (R4)", "Sagittarius A1 (R4)", "Starbetty (R4)", "PEPPE (R4)", "Ricky Around (R4)", "uncle g (R4)", "09ALEX24 (R4)", "ShinyPasta (R4)", "Wall 7 (R4)"]
    for n in leaders: data.append({"Nome": n, "Grado": "R5/R4"})
    # R3
    r3 = ["G Erry", "Uncle g brother", "Cane Avvoltoio", "Ghandal", "Aryron", "Tricheco", "Maメツ", "NOVEMBERGENZ", "Lalla 96", "Whale Panda", "GennaroM", "EchoZero", "EDDward", "AMY", "Resilienza", "Ana Bunny", "Giuseppec84", "Benito Muschiolini", "Pandino19", "xFlotchy", "MX63", "holdfast", "Ghost", "BadBigBoss", "Stefano00000", "PakII", "BANDOLERO26", "BlOOdyBlade", "Whale hunter Levve", "Aresxxx", "KingGruffalo", "Hulkspakka", "Joseone", "ImAde", "Nysbie", "LeFada13", "Skifetto", "SPio24", "TomEnergy", "Markus Defender", "Sho0t3r", "Wolf006", "Zokra", "perseusxxx", "Bendico", "Obbyy", "ArLes", "Fatz87", "cruel neve", "Trivellatore", "Osgh00", "Slowfia ABOH", "Pontatinatore", "27Francesco", "MissDrinks", "krompir", "MaledettO"]
    for n in r3: data.append({"Nome": n, "Grado": "R3"})
    # R2 (Aggiornato dai file caricati)
    r2 = ["teomadh", "Bossnico", "Valecit", "FarmerHool", "camiiiii 08", "Doctor team", "Yass081", "Nuorifleming", "Vergabrio", "Frenk70", "Comandante Maveric", "Thor9000", "MrBolly", "BustaMaki", "Ritardato", "StUnTmArK", "MONKEY D LUFFY 20", "CineSalentino", "Danylo98", "Ezechielefabianino", "BRNcommando", "LEONIDA", "elchicogyot", "erer1000", "Pupisnic", "Backfire1", "AnarchyBG", "Fabrizio1987", "JurdanS", "WiseR9", "Infinity8080"]
    for n in r2: data.append({"Nome": n, "Grado": "R2"})
    st.session_state['players_db'] = pd.DataFrame(data)
    st.session_state['sel_mese'] = "Marzo"
    st.session_state['sel_anno'] = 2026

db = st.session_state['players_db']
all_names = db['Nome'].tolist()

# --- HEADER ---
if not st.session_state.get('print_mode', False):
    st.title("🚂 AOSR EXPRESS MANAGER")

# --- CONFIGURAZIONE ---
if not st.session_state.get('print_mode', False):
    with st.expander("⚙️ IMPOSTAZIONI"):
        c1, c2 = st.columns([1,2])
        st.session_state['sel_mese'] = c1.selectbox("Mese", list(calendar.month_name)[1:], index=2)
        st.session_state['sel_anno'] = c1.number_input("Anno", 2024, 2030, 2026)
        
    if st.button("🚀 GENERA CALENDARIO", use_container_width=True):
        leaders = db[db['Grado']=="R5/R4"]['Nome'].tolist()
        pool = db[db['Grado'] != "R5/R4"]['Nome'].tolist()
        random.shuffle(pool)
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

# --- DISPLAY ---
if 'master_cal' in st.session_state:
    if not st.session_state.get('print_mode', False):
        st.subheader("📝 Revisione")
        # Logica Modifica/Inverti qui (omessa per brevità ma presente nel tuo sistema)
        # ... (stessi bottoni inverti/modifica precedenti)

    # --- TITOLO FOTO ---
    st.markdown(f"<h1 style='text-align:center; color:#00c8ff;'>CALENDARIO {st.session_state['sel_mese'].upper()} {st.session_state['sel_anno']}</h1>", unsafe_allow_html=True)
    
    # --- IL CALENDARIO (CANVAS PER SCREENSHOT) ---
    st.markdown('<div class="photo-canvas">', unsafe_allow_html=True)
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
                <div style="color:{c_c}; font-size:0.9rem; font-weight:bold;">{r['Capo']}</div>
                <div style="color:#555; font-size:0.6rem;">&</div>
                <div style="color:{p_c}; font-size:0.9rem; font-weight:bold;">{r['Pass']}</div>
            </div>
            """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # --- AZIONI FINALI ---
    if not st.session_state.get('print_mode', False):
        if st.button("📸 PREPARA FOTO PER SALVATAGGIO", type="primary"):
            st.session_state['print_mode'] = True
            st.rerun()
    else:
        st.success("✅ MODALITÀ FOTO ATTIVA: Fai uno screenshot o usa 'Salva con nome' dal browser.")
        if st.button("🔙 ESCI DALLA MODALITÀ FOTO"):
            st.session_state['print_mode'] = False
            st.rerun()
        
        # Pulsante per scaricare i dati (come backup)
        df_export = pd.DataFrame(st.session_state['master_cal'])
        csv = df_export.to_csv(index=False).encode('utf-8')
        st.download_button("💾 Scarica Tabella Dati (CSV)", data=csv, file_name=f"calendario_{st.session_state['sel_mese']}.csv")
