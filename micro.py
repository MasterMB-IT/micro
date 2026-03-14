import streamlit as st
import pandas as pd
import calendar
import random
from datetime import datetime

# --- CONFIGURAZIONE PAGINA A TUTTO SCHERMO ---
st.set_page_config(page_title="Alliance Train Manager Ultra", layout="wide")

# CSS per layout orizzontale e stile "Gaming Pro"
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .main-header { 
        background: linear-gradient(90deg, #00c8ff, #0072ff); 
        padding: 15px; border-radius: 10px; text-align: center; margin-bottom: 20px;
    }
    .calendar-row { 
        background-color: #1e2229; border-radius: 8px; padding: 10px; 
        margin-bottom: 5px; display: flex; align-items: center; border: 1px solid #333;
    }
    .day-num { width: 50px; font-weight: bold; color: #00c8ff; font-size: 1.2rem; }
    .role-box { flex: 1; padding: 0 15px; border-right: 1px solid #444; }
    .btn-col { width: 100px; text-align: center; }
    .r5-r4-text { color: #ff4757; font-weight: bold; }
    .r3-text { color: #2ed573; font-weight: bold; }
    .other-text { color: #a29bfe; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- INIZIALIZZAZIONE DATABASE ---
if 'players_db' not in st.session_state:
    data = []
    # Leader
    leaders = ["Hool (R5)", "MASTER (R4)", "Le 12 Scimmie (R4)", "Sagittarius A1 (R4)", "Starbetty (R4)", "PEPPE (R4)", "Ricky Around (R4)", "uncle g (R4)", "09ALEX24 (R4)", "ShinyPasta (R4)", "Wall 7 (R4)"]
    for n in leaders: data.append({"Nome": n, "Grado": "R5/R4"})
    # R3
    r3_init = ["G Erry", "Uncle g brother", "Cane Avvoltoio", "Ghandal", "Aryron", "Tricheco", "Maメツ", "NOVEMBERGENZ", "Lalla 96", "Whale Panda", "GennaroM", "EchoZero", "EDDward", "AMY", "Resilienza", "Ana Bunny", "Giuseppec84", "Benito Muschiolini", "Pandino19", "xFlotchy", "MX63", "holdfast", "Ghost", "BadBigBoss", "Stefano00000", "PakII", "BANDOLERO26", "BlOOdyBlade", "Whale hunter Levve", "Aresxxx", "KingGruffalo", "Hulkspakka", "Joseone", "ImAde", "Nysbie", "LeFada13", "Skifetto", "SPio24", "TomEnergy", "Markus Defender", "Sho0t3r", "Wolf006", "Zokra", "perseusxxx", "Bendico", "Obbyy", "ArLes", "Fatz87", "cruel neve", "Trivellatore", "Osgh00", "Slowfia ABOH", "Pontatinatore", "27Francesco", "MissDrinks", "krompir", "MaledettO"]
    for n in r3_init: data.append({"Nome": n, "Grado": "R3"})
    # R2/R1 filler
    for i in range(1, 33): data.append({"Nome": f"Soldato_{i}", "Grado": "R2" if i < 16 else "R1"})
    st.session_state['players_db'] = pd.DataFrame(data)

# --- HEADER E SELEZIONI IN ALTO (FULL WIDTH) ---
st.markdown('<div class="main-header"><h1>MANAGEMENT TRENI ALLEANZA - CONTROLLO TOTALE</h1></div>', unsafe_allow_html=True)

# SEZIONE 1: GESTIONE ROSTER (Spostamenti tra categorie)
with st.expander("👥 GESTIONE CATEGORIE E GRADI (Clicca per spostare i giocatori)", expanded=False):
    st.session_state['players_db'] = st.data_editor(
        st.session_state['players_db'],
        column_config={"Grado": st.column_config.SelectboxColumn("Cambia Grado", options=["R5/R4", "R3", "R2", "R1"])},
        hide_index=True, use_container_width=True
    )

# SEZIONE 2: FILTRI DI GENERAZIONE (Orizzontali)
col_m, col_a, col_gen = st.columns([2, 1, 2])
with col_m:
    mese_nome = st.selectbox("📅 Seleziona Mese", list(calendar.month_name)[1:], index=datetime.now().month-1)
with col_a:
    anno = st.number_input("Year", 2024, 2030, 2024)
with col_gen:
    st.write("") # Spacer
    btn_genera = st.button("🚀 GENERA CALENDARIO RANDOMIZZATO", use_container_width=True)

# SEZIONE 3: SELEZIONE MERITEVOLI (Ricerca inclusa)
st.markdown("### 🌟 Seleziona i partecipanti per questo mese")
db = st.session_state['players_db']
sel_r3 = st.multiselect("Seleziona da R3 (Search active)", db[db['Grado']=="R3"]['Nome'].tolist())
sel_r2_r1 = st.multiselect("Seleziona da R2/R1 (Search active)", db[db['Grado'].isin(["R2", "R1"])]['Nome'].tolist())
meritevoli_totali = sel_r3 + sel_r2_r1

# --- LOGICA DI GENERAZIONE ---
mese_idx = list(calendar.month_name).index(mese_nome)
num_giorni = calendar.monthrange(anno, mese_idx)[1]

if btn_genera:
    random.shuffle(meritevoli_totali)
    pool = list(meritevoli_totali)
    leaders = db[db['Grado']=="R5/R4"]['Nome'].tolist()
    
    new_cal = []
    for g in range(1, num_giorni + 1):
        if g <= 11:
            # Leader a rotazione fissa per i primi 11
            c = leaders[g-1 % len(leaders)]
            p = leaders[(g) % len(leaders)]
        else:
            # Random per gli altri
            c = pool.pop(0) if pool else "DA ASSEGNARE"
            p = pool.pop(0) if pool else "DA ASSEGNARE"
        new_cal.append({"Giorno": g, "Capotreno": c, "Passeggero": p})
    st.session_state['master_cal'] = new_cal

# --- CALENDARIO A TUTTO SCHERMO CON MODIFICA SINGOLA RIGA ---
if 'master_cal' in st.session_state:
    st.markdown("---")
    st.subheader(f"📅 Programma di {mese_nome}")
    
    all_names = db['Nome'].tolist()
    
    # Intestazione Tabella Custom
    st.markdown("""
        <div style="display: flex; font-weight: bold; padding: 10px; background: #333; border-radius: 5px;">
            <div style="width: 50px;">Giorno</div>
            <div style="flex: 1; padding-left: 15px;">Capotreno</div>
            <div style="flex: 1; padding-left: 15px;">Passeggero</div>
            <div style="width: 150px; text-align: center;">Azioni</div>
        </div>
    """, unsafe_allow_html=True)

    for i, row in enumerate(st.session_state['master_cal']):
        cols = st.columns([0.5, 3, 3, 1.5])
        
        with cols[0]:
            st.markdown(f"**{row['Giorno']:02d}**")
        
        with cols[1]:
            # Identificazione colore per grado
            g_c = db[db['Nome'] == row['Capotreno']]['Grado'].values[0] if row['Capotreno'] in all_names else "N/A"
            style_c = "r5-r4-text" if g_c == "R5/R4" else "r3-text" if g_c == "R3" else "other-text"
            st.markdown(f'<span class="{style_c}">{row["Capotreno"]}</span>', unsafe_allow_html=True)
            
        with cols[2]:
            g_p = db[db['Nome'] == row['Passeggero']]['Grado'].values[0] if row['Passeggero'] in all_names else "N/A"
            style_p = "r5-r4-text" if g_p == "R5/R4" else "r3-text" if g_p == "R3" else "other-text"
            st.markdown(f'<span class="{style_p}">{row["Passeggero"]}</span>', unsafe_allow_html=True)
            
        with cols[3]:
            # Tasto Modifica Riga
            if st.button(f"📝 Modifica", key=f"edit_{i}"):
                st.session_state[f"editing_row_{i}"] = True
        
        # Se il tasto modifica è attivo, apre un mini menu sotto la riga
        if st.session_state.get(f"editing_row_{i}", False):
            with st.container():
                edit_c1, edit_c2, edit_btn = st.columns([3, 3, 1])
                new_c = edit_c1.selectbox(f"Nuovo Capo G{row['Giorno']}", all_names, index=all_names.index(row['Capotreno']), key=f"sel_c_{i}")
                new_p = edit_c2.selectbox(f"Nuovo Pass G{row['Giorno']}", all_names, index=all_names.index(row['Passeggero']), key=f"sel_p_{i}")
                if edit_btn.button("✅ Salva", key=f"save_{i}"):
                    st.session_state['master_cal'][i]['Capotreno'] = new_c
                    st.session_state['master_cal'][i]['Passeggero'] = new_p
                    st.session_state[f"editing_row_{i}"] = False
                    st.rerun()

    # Esportazione Finale
    st.markdown("---")
    if st.download_button("📥 SCARICA CALENDARIO COMPLETO (CSV)", pd.DataFrame(st.session_state['master_cal']).to_csv(index=False).encode('utf-8'), f"Treni_{mese_nome}.csv"):
        st.success("Download avviato!")
