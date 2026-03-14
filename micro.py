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
        text-align: center; margin-bottom: 30px;
    }
    .aosr-title { font-family: 'Orbitron', sans-serif; color: #00c8ff; font-size: 2.5rem; letter-spacing: 4px; margin: 0; }
    
    /* Griglia Calendario Principale */
    .calendar-grid {
        display: grid; grid-template-columns: repeat(7, 1fr);
        gap: 15px; margin-top: 20px;
    }
    .day-card {
        background: #161b25; border-radius: 10px; padding: 12px;
        border: 1px solid #2d343f; min-height: 140px;
    }
    .day-number { font-size: 1.2rem; font-weight: 900; color: #444; margin-bottom: 8px; display: block;}
    
    /* Badge Giocatori */
    .p-box { padding: 4px 8px; border-radius: 4px; margin: 2px 0; font-size: 0.8rem; text-transform: uppercase; }
    .label { font-size: 0.6rem; opacity: 0.7; display: block; }
    .r5-r4-card { background: rgba(255, 71, 87, 0.15); border-left: 3px solid #ff4757; color: #ff4757; }
    .r3-card { background: rgba(46, 213, 115, 0.15); border-left: 3px solid #2ed573; color: #2ed573; }
    .r2-r1-card { background: rgba(162, 155, 254, 0.15); border-left: 3px solid #a29bfe; color: #a29bfe; }

    /* Visione d'Insieme Compatta */
    .summary-container {
        display: grid; grid-template-columns: repeat(auto-fill, minmax(110px, 1fr));
        gap: 8px; background: #000; padding: 15px; border-radius: 10px; border: 1px solid #00c8ff;
    }
    .summary-item {
        background: #111; border: 1px solid #333; padding: 5px; text-align: center; border-radius: 4px;
    }
    .summary-day-num { font-size: 0.7rem; color: #00c8ff; font-weight: bold; }
    .summary-name { font-size: 0.75rem; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
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
        anno_n = st.number_input("Anno", 2024, 2030, 2024)
    with col_b:
        default_sel = db[db['Grado'] != "R5/R4"]['Nome'].tolist()
        meritevoli = st.multiselect("Partecipanti (R3, R2)", default_sel, default_sel)

# --- GENERAZIONE ---
if st.button("🚄 GENERA CALENDARIO COMPLETO", use_container_width=True):
    random.shuffle(meritevoli)
    leaders = db[db['Grado']=="R5/R4"]['Nome'].tolist()
    num_gg = calendar.monthrange(anno_n, list(calendar.month_name).index(mese_n))[1]
    
    res_cal = []
    pool_idx = 0
    for g in range(1, num_gg + 1):
        if g <= 11:
            c, p = leaders[(g-1) % len(leaders)], leaders[g % len(leaders)]
        else:
            # Riempimento randomico continuo (loop sui meritevoli)
            c = meritevoli[pool_idx % len(meritevoli)]
            pool_idx += 1
            p = meritevoli[pool_idx % len(meritevoli)]
            pool_idx += 1
        res_cal.append({"Giorno": g, "Capotreno": c, "Passeggero": p})
    st.session_state['master_cal'] = res_cal

# --- FUNZIONI HELPER ---
def get_p_style(nome):
    grado = db[db['Nome']==nome]['Grado'].values[0] if nome in all_names else "R3"
    return "r5-r4-card" if grado == "R5/R4" else "r3-card" if grado == "R3" else "r2-r1-card"

def is_dup(nome):
    if nome in ["DA ASSEGNARE", "VUOTO"]: return False
    grado = db[db['Nome']==nome]['Grado'].values[0] if nome in all_names else "R3"
    if grado == "R5/R4": return False
    return sum(1 for d in st.session_state['master_cal'] if d['Capotreno']==nome or d['Passeggero']==nome) > 1

# --- VISUALIZZAZIONE ---
if 'master_cal' in st.session_state:
    st.markdown("### 📅 Calendario Dettagliato")
    
    primo_gg_sett = calendar.weekday(anno_n, list(calendar.month_name).index(mese_n), 1)
    st.markdown('<div class="calendar-grid">', unsafe_allow_html=True)
    for _ in range(primo_gg_sett):
        st.markdown('<div style="opacity: 0.1;">.</div>', unsafe_allow_html=True)
    
    for r in st.session_state['master_cal']:
        c_s, p_s = get_p_style(r['Capotreno']), get_p_style(r['Passeggero'])
        warn_c = "⚠️" if is_dup(r['Capotreno']) else ""
        warn_p = "⚠️" if is_dup(r['Passeggero']) else ""
        
        st.markdown(f"""
            <div class="day-card">
                <span class="day-number">{r['Giorno']}</span>
                <div class="p-box {c_s}"><span class="label">CAPO {warn_c}</span>{r['Capotreno']}</div>
                <div class="p-box {p_s}"><span class="label">PASS {warn_p}</span>{r['Passeggero']}</div>
            </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # --- VISIONE D'INSIEME (SCREENSHOT READY) ---
    st.markdown("---")
    st.markdown("### 🖼️ VISIONE D'INSIEME (Screenshot Ready)")
    
    summary_html = '<div class="summary-container">'
    for r in st.session_state['master_cal']:
        c_style = "color:#ff4757" if "R5/R4" in (db[db['Nome']==r['Capotreno']]['Grado'].values[0] if r['Capotreno'] in all_names else "") else "color:#2ed573"
        p_style = "color:#ff4757" if "R5/R4" in (db[db['Nome']==r['Passeggero']]['Grado'].values[0] if r['Passeggero'] in all_names else "") else "color:#a29bfe"
        
        summary_html += f"""
        <div class="summary-item">
            <div class="summary-day-num">GG {r['Giorno']}</div>
            <div class="summary-name" style="{c_style}">{r['Capotreno']}</div>
            <div style="font-size:0.5rem; color:#444;">&</div>
            <div class="summary-name" style="{p_style}">{r['Passeggero']}</div>
        </div>
        """
    summary_html += '</div>'
    st.markdown(summary_html, unsafe_allow_html=True)

    # Modifica rapida
    with st.expander("📝 MODIFICA GIORNO SPECIFICO"):
        day_to_edit = st.number_input("Giorno", 1, 31, 1)
        col1, col2 = st.columns(2)
        new_c = col1.selectbox("Nuovo Capo", all_names, key="nc", index=all_names.index(st.session_state['master_cal'][day_to_edit-1]['Capotreno']))
        new_p = col2.selectbox("Nuovo Pass", all_names, key="np", index=all_names.index(st.session_state['master_cal'][day_to_edit-1]['Passeggero']))
        if st.button("Applica Modifica"):
            st.session_state['master_cal'][day_to_edit-1]['Capotreno'] = new_c
            st.session_state['master_cal'][day_to_edit-1]['Passeggero'] = new_p
            st.rerun()
