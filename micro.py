import streamlit as st
import pandas as pd
import calendar
import random
from datetime import datetime

# --- CONFIGURAZIONE ---
st.set_page_config(page_title="Alliance Train Manager Ultra v7", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .main-header { background: linear-gradient(90deg, #00c8ff, #0072ff); padding: 15px; border-radius: 10px; text-align: center; margin-bottom: 20px; }
    .counter-badge { background: #333; padding: 2px 8px; border-radius: 10px; font-size: 0.9rem; color: #00c8ff; margin-left: 10px; border: 1px solid #00c8ff; }
    .warning-box { background-color: #ff9f4322; border-left: 5px solid #ff9f43; padding: 10px; margin: 5px 0; border-radius: 5px; color: #ff9f43; font-weight: bold; }
    .r5-r4-text { color: #ff4757; font-weight: bold; }
    .r3-text { color: #2ed573; font-weight: bold; }
    .r2-text { color: #a29bfe; font-weight: bold; }
    .r1-text { color: #eccc68; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- DATABASE ---
if 'players_db' not in st.session_state:
    data = []
    # Leader (11)
    for n in ["Hool (R5)", "MASTER (R4)", "Le 12 Scimmie (R4)", "Sagittarius A1 (R4)", "Starbetty (R4)", "PEPPE (R4)", "Ricky Around (R4)", "uncle g (R4)", "09ALEX24 (R4)", "ShinyPasta (R4)", "Wall 7 (R4)"]:
        data.append({"Nome": n, "Grado": "R5/R4"})
    # R3 (57)
    r3_list = ["G Erry", "Uncle g brother", "Cane Avvoltoio", "Ghandal", "Aryron", "Tricheco", "Maメツ", "NOVEMBERGENZ", "Lalla 96", "Whale Panda", "GennaroM", "EchoZero", "EDDward", "AMY", "Resilienza", "Ana Bunny", "Giuseppec84", "Benito Muschiolini", "Pandino19", "xFlotchy", "MX63", "holdfast", "Ghost", "BadBigBoss", "Stefano00000", "PakII", "BANDOLERO26", "BlOOdyBlade", "Whale hunter Levve", "Aresxxx", "KingGruffalo", "Hulkspakka", "Joseone", "ImAde", "Nysbie", "LeFada13", "Skifetto", "SPio24", "TomEnergy", "Markus Defender", "Sho0t3r", "Wolf006", "Zokra", "perseusxxx", "Bendico", "Obbyy", "ArLes", "Fatz87", "cruel neve", "Trivellatore", "Osgh00", "Slowfia ABOH", "Pontatinatore", "27Francesco", "MissDrinks", "krompir", "MaledettO"]
    for n in r3_list: data.append({"Nome": n, "Grado": "R3"})
    # R2 (31 dai tuoi screenshot)
    r2_list = ["teomadh", "Bossnico", "Valecit", "FarmerHool", "camiiiii 08", "Doctor team", "Yass081", "Nuorifleming", "Vergabrio", "Frenk70", "Comandante Maveric", "Thor9000", "MrBolly", "BustaMaki", "Ritardato", "StUnTmArK", "MONKEY D LUFFY 20", "CineSalentino", "Danylo98", "Ezechielefabianino", "BRNcommando", "LEONIDA", "elchicogyot", "erer1000", "Pupisnic", "Backfire1", "AnarchyBG", "Fabrizio1987", "JurdanS", "WiseR9", "Infinity8080"]
    for n in r2_list: data.append({"Nome": n, "Grado": "R2"})
    # R1 filler per arrivare a 100
    for i in range(1, 2): data.append({"Nome": f"Cadetto_R1_{i}", "Grado": "R1"})
    st.session_state['players_db'] = pd.DataFrame(data)

db = st.session_state['players_db']

# --- CONTEGGI ---
count_r4 = len(db[db['Grado'] == "R5/R4"])
count_r3 = len(db[db['Grado'] == "R3"])
count_r2 = len(db[db['Grado'] == "R2"])
count_r1 = len(db[db['Grado'] == "R1"])
total_p = len(db)

st.markdown(f'<div class="main-header"><h1>MANAGEMENT TRENI - {total_p}/100 GIOCATORI</h1></div>', unsafe_allow_html=True)

# --- GESTIONE ROSTER CON CONTATORI ---
with st.expander("🔄 GESTIONE ROSTER E TRASFERIMENTI", expanded=False):
    st.write(f"R5/R4: {count_r4} | R3: {count_r3} | R2: {count_r2} | R1: {count_r1}")
    st.session_state['players_db'] = st.data_editor(db, hide_index=True, use_container_width=True)

# --- SELEZIONE MERITEVOLI ---
st.markdown("### 📋 Selezione Partecipanti Mensili")
col1, col2 = st.columns([1, 4])
with col1:
    mese_n = st.selectbox("Mese", list(calendar.month_name)[1:], index=datetime.now().month-1)
    anno_n = st.number_input("Anno", 2024, 2030, 2024)

with col2:
    sel_r3 = st.multiselect(f"🌟 R3 Meritevoli ({len(db[db['Grado']=='R3'])})", db[db['Grado']=="R3"]['Nome'].tolist())
    sel_r2 = st.multiselect(f"🎖️ R2 Meritevoli ({len(db[db['Grado']=='R2'])})", db[db['Grado']=="R2"]['Nome'].tolist())
    sel_r1 = st.multiselect(f"🔰 R1 Meritevoli ({len(db[db['Grado']=='R1'])})", db[db['Grado']=="R1"]['Nome'].tolist())

meritevoli = sel_r3 + sel_r2 + sel_r1

# --- GENERAZIONE ---
if st.button("🚀 GENERA CALENDARIO RANDOM", use_container_width=True):
    random.shuffle(meritevoli)
    pool = list(meritevoli)
    leaders = db[db['Grado']=="R5/R4"]['Nome'].tolist()
    num_gg = calendar.monthrange(anno_n, list(calendar.month_name).index(mese_n))[1]
    
    res_cal = []
    for g in range(1, num_gg + 1):
        if g <= 11:
            c, p = leaders[g-1 % len(leaders)], leaders[(g) % len(leaders)]
        else:
            c = pool.pop(0) if pool else "DA ASSEGNARE"
            p = pool.pop(0) if pool else "DA ASSEGNARE"
        res_cal.append({"Giorno": g, "Capotreno": c, "Passeggero": p})
    st.session_state['master_cal'] = res_cal

# --- CALENDARIO CON ALERT DUPLICATI ---
if 'master_cal' in st.session_state:
    st.markdown("---")
    all_names = db['Nome'].tolist()
    
    # Helper per trovare duplicati in tutto il calendario
    def check_duplicate(nome, current_index):
        if nome == "DA ASSEGNARE" or nome == "VUOTO": return False
        count = 0
        for idx, entry in enumerate(st.session_state['master_cal']):
            if entry['Capotreno'] == nome: count += 1
            if entry['Passeggero'] == nome: count += 1
        return count > 1

    for i, r in enumerate(st.session_state['master_cal']):
        # Rilevamento duplicati
        dup_capo = check_duplicate(r['Capotreno'], i)
        dup_pass = check_duplicate(r['Passeggero'], i)

        cols = st.columns([1, 3, 3, 1.5])
        with cols[0]: st.markdown(f"**Giorno {r['Giorno']:02d}**")
        
        # Colonna Capotreno
        with cols[1]:
            st.markdown(f"Capo: **{r['Capotreno']}**")
            if dup_capo: st.markdown('<div class="warning-box">⚠️ Giocatore già presente nel mese!</div>', unsafe_allow_html=True)
            
        # Colonna Passeggero
        with cols[2]:
            st.markdown(f"Pass: **{r['Passeggero']}**")
            if dup_pass: st.markdown('<div class="warning-box">⚠️ Giocatore già presente nel mese!</div>', unsafe_allow_html=True)

        with cols[3]:
            if st.button(f"📝 Modifica", key=f"edit_btn_{i}"):
                st.session_state[f"active_edit_{i}"] = not st.session_state.get(f"active_edit_{i}", False)

        # Editor di riga
        if st.session_state.get(f"active_edit_{i}", False):
            with st.container():
                ec1, ec2, ec3 = st.columns([4, 4, 2])
                new_c = ec1.selectbox("Cambia Capotreno", all_names, index=all_names.index(r['Capotreno']) if r['Capotreno'] in all_names else 0, key=f"ec_{i}")
                new_p = ec2.selectbox("Cambia Passeggero", all_names, index=all_names.index(r['Passeggero']) if r['Passeggero'] in all_names else 0, key=f"ep_{i}")
                
                if ec3.button("✅ Salva e Verifica", key=f"sv_{i}"):
                    st.session_state['master_cal'][i]['Capotreno'] = new_c
                    st.session_state['master_cal'][i]['Passeggero'] = new_p
                    st.session_state[f"active_edit_{i}"] = False
                    st.rerun()
        st.markdown("---")

    st.download_button("📥 Scarica Calendario Finale", pd.DataFrame(st.session_state['master_cal']).to_csv(index=False).encode('utf-8'), "Calendario_Treni.csv")
