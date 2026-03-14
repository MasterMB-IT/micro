import streamlit as st
import pandas as pd
import calendar
import random
from datetime import datetime

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="Alliance Train Manager Ultra", layout="wide")

# CSS Gaming Style & Layout Full-Width
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .main-header { 
        background: linear-gradient(90deg, #00c8ff, #0072ff); 
        padding: 15px; border-radius: 10px; text-align: center; margin-bottom: 20px;
    }
    .r5-r4-text { color: #ff4757; font-weight: bold; }
    .r3-text { color: #2ed573; font-weight: bold; }
    .r2-text { color: #a29bfe; font-weight: bold; }
    .r1-text { color: #eccc68; font-weight: bold; }
    .calendar-row { background: #1e2229; padding: 10px; border-radius: 5px; margin-bottom: 5px; border-left: 5px solid #444; }
    </style>
    """, unsafe_allow_html=True)

# --- DATABASE GIOCATORI AGGIORNATO ---
if 'players_db' not in st.session_state:
    data = []
    # R5 & R4
    for n in ["Hool (R5)", "MASTER (R4)", "Le 12 Scimmie (R4)", "Sagittarius A1 (R4)", "Starbetty (R4)", "PEPPE (R4)", "Ricky Around (R4)", "uncle g (R4)", "09ALEX24 (R4)", "ShinyPasta (R4)", "Wall 7 (R4)"]:
        data.append({"Nome": n, "Grado": "R5/R4"})
    
    # R3 (Dalle immagini precedenti)
    r3_list = ["G Erry", "Uncle g brother", "Cane Avvoltoio", "Ghandal", "Aryron", "Tricheco", "Maメツ", "NOVEMBERGENZ", "Lalla 96", "Whale Panda", "GennaroM", "EchoZero", "EDDward", "AMY", "Resilienza", "Ana Bunny", "Giuseppec84", "Benito Muschiolini", "Pandino19", "xFlotchy", "MX63", "holdfast", "Ghost", "BadBigBoss", "Stefano00000", "PakII", "BANDOLERO26", "BlOOdyBlade", "Whale hunter Levve", "Aresxxx", "KingGruffalo", "Hulkspakka", "Joseone", "ImAde", "Nysbie", "LeFada13", "Skifetto", "SPio24", "TomEnergy", "Markus Defender", "Sho0t3r", "Wolf006", "Zokra", "perseusxxx", "Bendico", "Obbyy", "ArLes", "Fatz87", "cruel neve", "Trivellatore", "Osgh00", "Slowfia ABOH", "Pontatinatore", "27Francesco", "MissDrinks", "krompir", "MaledettO"]
    for n in r3_list: data.append({"Nome": n, "Grado": "R3"})
    
    # R2 (Inseriti dai nuovi screenshot forniti)
    r2_new = [
        "teomadh", "Bossnico", "Valecit", "FarmerHool", "camiiiii 08", "Doctor team", 
        "Yass081", "Nuorifleming", "Vergabrio", "Frenk70", "Comandante Maveric", "Thor9000",
        "MrBolly", "BustaMaki", "Ritardato", "StUnTmArK", "MONKEY D LUFFY 20", "CineSalentino",
        "Danylo98", "Ezechielefabianino", "BRNcommando", "LEONIDA", "elchicogyot", "erer1000",
        "Pupisnic", "Backfire1", "AnarchyBG", "Fabrizio1987", "JurdanS", "WiseR9", "Infinity8080"
    ]
    for n in r2_new: data.append({"Nome": n, "Grado": "R2"})
    
    # Slot R1 (Esempio per completare il roster)
    for i in range(1, 11): data.append({"Nome": f"Cadetto_R1_{i}", "Grado": "R1"})
    
    st.session_state['players_db'] = pd.DataFrame(data)

# --- INTERFACCIA SUPERIORE ---
st.markdown('<div class="main-header"><h1>MANAGEMENT TRENI ALLEANZA</h1></div>', unsafe_allow_html=True)

# GESTIONE ROSTER (Spostamenti rapidi)
with st.expander("🔄 GESTIONE ROSTER E TRASFERIMENTI (Tutto Schermo)", expanded=False):
    st.session_state['players_db'] = st.data_editor(
        st.session_state['players_db'],
        column_config={"Grado": st.column_config.SelectboxColumn("Grado", options=["R5/R4", "R3", "R2", "R1"])},
        hide_index=True, use_container_width=True
    )

# SELEZIONE MERITEVOLI E DATA
st.markdown("### 🚂 Configurazione Treni Mensili")
c1, c2, c3 = st.columns([1, 1, 3])
with c1:
    mese_n = st.selectbox("Mese", list(calendar.month_name)[1:], index=datetime.now().month-1)
with c2:
    anno_n = st.number_input("Anno", 2024, 2030, 2024)

db = st.session_state['players_db']
sel_r3 = st.multiselect("🌟 Meritevoli R3", db[db['Grado']=="R3"]['Nome'].tolist())
sel_r2 = st.multiselect("🎖️ Meritevoli R2", db[db['Grado']=="R2"]['Nome'].tolist())
sel_r1 = st.multiselect("🔰 Meritevoli R1", db[db['Grado']=="R1"]['Nome'].tolist())

meritevoli = sel_r3 + sel_r2 + sel_r1

# --- GENERAZIONE ---
if st.button("🚀 GENERA CALENDARIO RANDOM", use_container_width=True):
    random.shuffle(meritevoli)
    pool = list(meritevoli)
    leaders = db[db['Grado']=="R5/R4"]['Nome'].tolist()
    
    num_gg = calendar.monthrange(anno_n, list(calendar.month_name).index(mese_n))[1]
    nuovo_cal = []
    for g in range(1, num_gg + 1):
        if g <= 11:
            c, p = leaders[g-1 % len(leaders)], leaders[(g) % len(leaders)]
        else:
            c = pool.pop(0) if pool else "DA ASSEGNARE"
            p = pool.pop(0) if pool else "DA ASSEGNARE"
        nuovo_cal.append({"Giorno": g, "Capotreno": c, "Passeggero": p})
    st.session_state['master_cal'] = nuovo_cal

# --- CALENDARIO E MODIFICA RIGA ---
if 'master_cal' in st.session_state:
    st.markdown("---")
    all_names = db['Nome'].tolist()
    
    # Intestazione Colonne
    st.markdown("""<div style="display:flex; font-weight:bold; background:#333; padding:10px; border-radius:5px;">
        <div style="width:10%;">Giorno</div><div style="width:35%;">Capotreno</div><div style="width:35%;">Passeggero</div><div style="width:20%; text-align:center;">Azioni</div>
    </div>""", unsafe_allow_html=True)

    for i, r in enumerate(st.session_state['master_cal']):
        cols = st.columns([1, 3.5, 3.5, 2])
        
        # Colore basato sul grado attuale nel DB
        def get_style(nome):
            grado = db[db['Nome']==nome]['Grado'].values[0] if nome in all_names else ""
            if grado == "R5/R4": return "r5-r4-text"
            if grado == "R3": return "r3-text"
            if grado == "R2": return "r2-text"
            return "r1-text"

        with cols[0]: st.markdown(f"**{r['Giorno']:02d}**")
        with cols[1]: st.markdown(f'<span class="{get_style(r["Capotreno"])}">{r["Capotreno"]}</span>', unsafe_allow_html=True)
        with cols[2]: st.markdown(f'<span class="{get_style(r["Passeggero"])}">{r["Passeggero"]}</span>', unsafe_allow_html=True)
        
        with cols[3]:
            if st.button(f"📝 Modifica", key=f"btn_{i}"):
                st.session_state[f"edit_active_{i}"] = not st.session_state.get(f"edit_active_{i}", False)

        # Pannello di modifica inline
        if st.session_state.get(f"edit_active_{i}", False):
            with st.container():
                ec1, ec2, ec3 = st.columns([4, 4, 2])
                new_c = ec1.selectbox("Capo", all_names, index=all_names.index(r['Capotreno']) if r['Capotreno'] in all_names else 0, key=f"sel_c{i}")
                new_p = ec2.selectbox("Pass", all_names, index=all_names.index(r['Passeggero']) if r['Passeggero'] in all_names else 0, key=f"sel_p{i}")
                if ec3.button("💾 OK", key=f"save_{i}"):
                    st.session_state['master_cal'][i]['Capotreno'] = new_c
                    st.session_state['master_cal'][i]['Passeggero'] = new_p
                    st.session_state[f"edit_active_{i}"] = False
                    st.rerun()

    st.download_button("📥 Scarica Tabella CSV", pd.DataFrame(st.session_state['master_cal']).to_csv(index=False).encode('utf-8'), "Calendario_Treni.csv")
