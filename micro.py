import streamlit as st
import pandas as pd
import calendar
import random
from datetime import datetime

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="AOSR Train Manager Elite", layout="wide")

# CSS CUSTOM PER IL TRENO AOSR
st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; color: #ffffff; }
    
    /* Header AOSR Style */
    .aosr-header {
        background: linear-gradient(135deg, #1a1f2c 0%, #0b0e14 100%);
        padding: 40px; border-radius: 20px; border: 2px solid #00c8ff;
        text-align: center; margin-bottom: 40px;
        box-shadow: 0 10px 30px rgba(0,200,255,0.2);
    }
    .aosr-title { font-family: 'Orbitron', sans-serif; color: #00c8ff; font-size: 3rem; letter-spacing: 5px; margin: 0; }
    .aosr-subtitle { color: #ffd700; font-size: 1.2rem; text-transform: uppercase; margin-top: 10px; }

    /* Griglia Calendario */
    .calendar-grid {
        display: grid;
        grid-template-columns: repeat(7, 1fr);
        gap: 15px;
        margin-top: 20px;
    }
    .day-card {
        background: #161b25;
        border-radius: 12px;
        padding: 15px;
        border: 1px solid #2d343f;
        transition: transform 0.3s;
        min-height: 160px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    .day-card:hover { border-color: #00c8ff; transform: translateY(-5px); }
    
    .day-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }
    .day-number { font-size: 1.4rem; font-weight: 900; color: #555; }
    .today-marker { color: #00c8ff !important; }

    /* Badge Giocatori */
    .p-box { padding: 5px 8px; border-radius: 6px; margin: 2px 0; font-size: 0.85rem; }
    .label { font-size: 0.65rem; text-transform: uppercase; color: #888; display: block; }
    
    .r5-r4-card { background: rgba(255, 71, 87, 0.15); border-left: 3px solid #ff4757; color: #ff4757; font-weight: bold; }
    .r3-card { background: rgba(46, 213, 115, 0.15); border-left: 3px solid #2ed573; color: #2ed573; }
    .r2-r1-card { background: rgba(162, 155, 254, 0.15); border-left: 3px solid #a29bfe; color: #a29bfe; }
    
    .warning-icon { color: #ff9f43; font-size: 0.8rem; margin-top: 5px; }
    </style>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@700&display=swap" rel="stylesheet">
    """, unsafe_allow_html=True)

# --- DATABASE ---
if 'players_db' not in st.session_state:
    data = []
    # Leader
    for n in ["Hool (R5)", "MASTER (R4)", "Le 12 Scimmie (R4)", "Sagittarius A1 (R4)", "Starbetty (R4)", "PEPPE (R4)", "Ricky Around (R4)", "uncle g (R4)", "09ALEX24 (R4)", "ShinyPasta (R4)", "Wall 7 (R4)"]:
        data.append({"Nome": n, "Grado": "R5/R4"})
    # R3
    r3_list = ["G Erry", "Uncle g brother", "Cane Avvoltoio", "Ghandal", "Aryron", "Tricheco", "Maメツ", "NOVEMBERGENZ", "Lalla 96", "Whale Panda", "GennaroM", "EchoZero", "EDDward", "AMY", "Resilienza", "Ana Bunny", "Giuseppec84", "Benito Muschiolini", "Pandino19", "xFlotchy", "MX63", "holdfast", "Ghost", "BadBigBoss", "Stefano00000", "PakII", "BANDOLERO26", "BlOOdyBlade", "Whale hunter Levve", "Aresxxx", "KingGruffalo", "Hulkspakka", "Joseone", "ImAde", "Nysbie", "LeFada13", "Skifetto", "SPio24", "TomEnergy", "Markus Defender", "Sho0t3r", "Wolf006", "Zokra", "perseusxxx", "Bendico", "Obbyy", "ArLes", "Fatz87", "cruel neve", "Trivellatore", "Osgh00", "Slowfia ABOH", "Pontatinatore", "27Francesco", "MissDrinks", "krompir", "MaledettO"]
    for n in r3_list: data.append({"Nome": n, "Grado": "R3"})
    # R2
    r2_list = ["teomadh", "Bossnico", "Valecit", "FarmerHool", "camiiiii 08", "Doctor team", "Yass081", "Nuorifleming", "Vergabrio", "Frenk70", "Comandante Maveric", "Thor9000", "MrBolly", "BustaMaki", "Ritardato", "StUnTmArK", "MONKEY D LUFFY 20", "CineSalentino", "Danylo98", "Ezechielefabianino", "BRNcommando", "LEONIDA", "elchicogyot", "erer1000", "Pupisnic", "Backfire1", "AnarchyBG", "Fabrizio1987", "JurdanS", "WiseR9", "Infinity8080"]
    for n in r2_list: data.append({"Nome": n, "Grado": "R2"})
    st.session_state['players_db'] = pd.DataFrame(data)

db = st.session_state['players_db']

# --- HEADER STILIZZATO ---
st.markdown("""
    <div class="aosr-header">
        <div class="aosr-title">AOSR EXPRESS</div>
        <div class="aosr-subtitle">Alliance Official Strategic Railway • Management System</div>
    </div>
    """, unsafe_allow_html=True)

# --- CONTROLLI ---
with st.expander("🛠️ CONFIGURAZIONE E SELEZIONI", expanded=False):
    col_a, col_b = st.columns([1,3])
    with col_a:
        mese_n = st.selectbox("Mese", list(calendar.month_name)[1:], index=datetime.now().month-1)
        anno_n = st.number_input("Anno", 2024, 2030, 2024)
    with col_b:
        meritevoli = st.multiselect("Seleziona Partecipanti (R3, R2, R1)", db[db['Grado'] != "R5/R4"]['Nome'].tolist())

# --- GENERAZIONE ---
if st.button("🚄 GENERA NUOVO PERCORSO AOSR", use_container_width=True):
    random.shuffle(meritevoli)
    pool = list(meritevoli)
    leaders = db[db['Grado']=="R5/R4"]['Nome'].tolist()
    num_gg = calendar.monthrange(anno_n, list(calendar.month_name).index(mese_n))[1]
    
    res_cal = []
    for g in range(1, num_gg + 1):
        if g <= 11:
            c, p = leaders[(g-1) % len(leaders)], leaders[g % len(leaders)]
        else:
            c = pool.pop(0) if pool else "DA ASSEGNARE"
            p = pool.pop(0) if pool else "DA ASSEGNARE"
        res_cal.append({"Giorno": g, "Capotreno": c, "Passeggero": p})
    st.session_state['master_cal'] = res_cal

# --- VISUALIZZAZIONE A GRIGLIA ---
if 'master_cal' in st.session_state:
    st.markdown(f"### 📅 Tabellone Marce: {mese_n} {anno_n}")
    
    # Calcolo spazi vuoti per inizio mese
    primo_gg_sett = calendar.weekday(anno_n, list(calendar.month_name).index(mese_n), 1)
    
    all_names = db['Nome'].tolist()
    
    # Helper stile badge
    def get_p_style(nome):
        grado = db[db['Nome']==nome]['Grado'].values[0] if nome in all_names else "R3"
        if grado == "R5/R4": return "r5-r4-card"
        if grado == "R3": return "r3-card"
        return "r2-r1-card"

    # Helper duplicati
    def is_dup(nome):
        if nome in ["DA ASSEGNARE", "VUOTO"]: return False
        grado = db[db['Nome']==nome]['Grado'].values[0] if nome in all_names else "R3"
        if grado == "R5/R4": return False
        count = sum(1 for d in st.session_state['master_cal'] if d['Capotreno']==nome or d['Passeggero']==nome)
        return count > 1

    # Inizio Griglia
    st.markdown('<div class="calendar-grid">', unsafe_allow_html=True)
    
    # Giorni vuoti
    for _ in range(primo_gg_sett):
        st.markdown('<div style="opacity: 0.2;">.</div>', unsafe_allow_html=True)
        
    # Giorni effettivi
    for i, r in enumerate(st.session_state['master_cal']):
        c_style = get_p_style(r['Capotreno'])
        p_style = get_p_style(r['Passeggero'])
        
        warn_c = "⚠️" if is_dup(r['Capotreno']) else ""
        warn_p = "⚠️" if is_dup(r['Passeggero']) else ""
        
        st.markdown(f"""
            <div class="day-card">
                <div class="day-header">
                    <span class="day-number">{r['Giorno']}</span>
                    <span style="font-size:0.6rem; color:#444;">AOSR_LINE</span>
                </div>
                <div class="p-box {c_style}">
                    <span class="label">Capotreno {warn_c}</span>
                    {r['Capotreno']}
                </div>
                <div class="p-box {p_style}">
                    <span class="label">Passeggero {warn_p}</span>
                    {r['Passeggero']}
                </div>
            </div>
        """, unsafe_allow_html=True)
        
    st.markdown('</div>', unsafe_allow_html=True)

    # Pulsante modifica riga (veloce, sotto la griglia)
    st.markdown("---")
    with st.expander("📝 MODIFICA VELOCE RIGHE"):
        edit_idx = st.number_input("Inserisci Giorno da modificare", 1, 31, 1)
        ec1, ec2 = st.columns(2)
        new_c = ec1.selectbox("Nuovo Capo", all_names, key="nc")
        new_p = ec2.selectbox("Nuovo Pass", all_names, key="np")
        if st.button("Aggiorna Giorno"):
            st.session_state['master_cal'][edit_idx-1]['Capotreno'] = new_c
            st.session_state['master_cal'][edit_idx-1]['Passeggero'] = new_p
            st.rerun()

    st.download_button("📥 ESPORTA TABELLONE AOSR", pd.DataFrame(st.session_state['master_cal']).to_csv(index=False).encode('utf-8'), f"AOSR_{mese_n}.csv")
