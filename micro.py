import streamlit as st
import pandas as pd
import calendar
import random
from datetime import datetime

# --- CONFIGURAZIONE ---
st.set_page_config(page_title="AOSR Train Manager Pro", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .main-header { background: linear-gradient(90deg, #00c8ff, #0072ff); padding: 15px; border-radius: 10px; text-align: center; margin-bottom: 20px; }
    .warning-box { background-color: #ff9f4322; border-left: 5px solid #ff9f43; padding: 5px; margin: 2px 0; border-radius: 3px; color: #ff9f43; font-size: 0.75rem; }
    
    .r5-r4-text { color: #ff4757; font-weight: bold; }
    .r3-text { color: #2ed573; font-weight: bold; }
    .r2-text { color: #a29bfe; font-weight: bold; }
    
    .summary-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(130px, 1fr));
        gap: 12px;
        background: #161b22;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #30363d;
        margin-top: 20px;
    }
    .summary-day {
        background: #0d1117;
        padding: 12px;
        border-radius: 8px;
        border: 1px solid #30363d;
        text-align: center;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.3);
    }
    .day-label { font-size: 0.75rem; color: #8b949e; border-bottom: 1px solid #30363d; margin-bottom: 8px; display: block; font-weight: bold; }
    .name-line { font-size: 0.85rem; margin: 2px 0; text-transform: uppercase; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
    .separator { color: #444; font-size: 0.7rem; margin: 2px 0; }
    </style>
    """, unsafe_allow_html=True)

# --- DATABASE ---
if 'players_db' not in st.session_state:
    data = []
    # Leader
    leaders_list = ["Hool (R5)", "MASTER (R4)", "Le 12 Scimmie (R4)", "Sagittarius A1 (R4)", "Starbetty (R4)", "PEPPE (R4)", "Ricky Around (R4)", "uncle g (R4)", "09ALEX24 (R4)", "ShinyPasta (R4)", "Wall 7 (R4)"]
    for n in leaders_list: data.append({"Nome": n, "Grado": "R5/R4"})
    # R3
    r3_l = ["G Erry", "Uncle g brother", "Cane Avvoltoio", "Ghandal", "Aryron", "Tricheco", "Maメツ", "NOVEMBERGENZ", "Lalla 96", "Whale Panda", "GennaroM", "EchoZero", "EDDward", "AMY", "Resilienza", "Ana Bunny", "Giuseppec84", "Benito Muschiolini", "Pandino19", "xFlotchy", "MX63", "holdfast", "Ghost", "BadBigBoss", "Stefano00000", "PakII", "BANDOLERO26", "BlOOdyBlade", "Whale hunter Levve", "Aresxxx", "KingGruffalo", "Hulkspakka", "Joseone", "ImAde", "Nysbie", "LeFada13", "Skifetto", "SPio24", "TomEnergy", "Markus Defender", "Sho0t3r", "Wolf006", "Zokra", "perseusxxx", "Bendico", "Obbyy", "ArLes", "Fatz87", "cruel neve", "Trivellatore", "Osgh00", "Slowfia ABOH", "Pontatinatore", "27Francesco", "MissDrinks", "krompir", "MaledettO"]
    for n in r3_l: data.append({"Nome": n, "Grado": "R3"})
    # R2
    r2_l = ["teomadh", "Bossnico", "Valecit", "FarmerHool", "camiiiii 08", "Doctor team", "Yass081", "Nuorifleming", "Vergabrio", "Frenk70", "Comandante Maveric", "Thor9000", "MrBolly", "BustaMaki", "Ritardato", "StUnTmArK", "MONKEY D LUFFY 20", "CineSalentino", "Danylo98", "Ezechielefabianino", "BRNcommando", "LEONIDA", "elchicogyot", "erer1000", "Pupisnic", "Backfire1", "AnarchyBG", "Fabrizio1987", "JurdanS", "WiseR9", "Infinity8080"]
    for n in r2_l: data.append({"Nome": n, "Grado": "R2"})
    st.session_state['players_db'] = pd.DataFrame(data)

db = st.session_state['players_db']
all_names = db['Nome'].tolist()

# --- HEADER ---
st.markdown('<div class="main-header"><h1>AOSR TRAIN MANAGEMENT SYSTEM</h1></div>', unsafe_allow_html=True)

# --- CONTROLLI ---
with st.container():
    c1, c2, c3 = st.columns([1, 1, 2])
    mese_n = c1.selectbox("Mese", list(calendar.month_name)[1:], index=datetime.now().month-1)
    anno_n = c2.number_input("Anno", 2024, 2030, 2024)
    # Di default selezioniamo tutti i meritevoli (R3, R2) per evitare celle vuote
    default_merit = db[db['Grado'] != "R5/R4"]['Nome'].tolist()
    sel_meritevoli = c3.multiselect("Seleziona Partecipanti Mensili", default_merit, default_merit)

# --- GENERAZIONE ---
if st.button("🚀 GENERA CALENDARIO COMPLETO", use_container_width=True):
    if not sel_meritevoli:
        st.error("Seleziona almeno un giocatore per i giorni dopo l'11!")
    else:
        random.shuffle(sel_meritevoli)
        leaders = db[db['Grado']=="R5/R4"]['Nome'].tolist()
        num_gg = calendar.monthrange(anno_n, list(calendar.month_name).index(mese_n))[1]
        
        cal = []
        pool_idx = 0
        
        for g in range(1, num_gg + 1):
            if g <= 11:
                # Rotazione fissa Leader
                c, p = leaders[(g-1)%len(leaders)], leaders[g%len(leaders)]
            else:
                # Riempimento randomico continuo dai selezionati
                c = sel_meritevoli[pool_idx % len(sel_meritevoli)]
                pool_idx += 1
                p = sel_meritevoli[pool_idx % len(sel_meritevoli)]
                pool_idx += 1
            
            cal.append({"Giorno": g, "Capotreno": c, "Passeggero": p})
        st.session_state['master_cal'] = cal

# --- LOGICA DUPLICATI (Esclusi R5/R4) ---
def is_duplicate(nome):
    if nome in ["DA ASSEGNARE", "VUOTO"]: return False
    grado = db[db['Nome'] == nome]['Grado'].values[0] if nome in all_names else ""
    if grado == "R5/R4": return False
    count = sum(1 for r in st.session_state.get('master_cal', []) if r['Capotreno'] == nome or r['Passeggero'] == nome)
    return count > 1

# --- VISUALIZZAZIONE ---
if 'master_cal' in st.session_state:
    with st.expander("📝 MODIFICA SINGOLI GIORNI"):
        for i, r in enumerate(st.session_state['master_cal']):
            cols = st.columns([1, 3, 3, 1])
            with cols[0]: st.write(f"**Giorno {r['Giorno']}**")
            
            for idx, role in enumerate(['Capotreno', 'Passeggero']):
                name = r[role]
                g = db[db['Nome'] == name]['Grado'].values[0] if name in all_names else "R3"
                cl = "r5-r4-text" if g == "R5/R4" else "r3-text" if g == "R3" else "r2-text"
                with cols[idx+1]:
                    st.markdown(f'<span class="{cl}">{name}</span>', unsafe_allow_html=True)
                    if is_duplicate(name): st.markdown('<span style="color:#ff9f43;font-size:0.7rem;">⚠️ Duplicato</span>', unsafe_allow_html=True)

            if cols[3].button("Edit", key=f"btn_{i}"):
                st.session_state[f"active_{i}"] = not st.session_state.get(f"active_{i}", False)
            
            if st.session_state.get(f"active_{i}", False):
                ec1, ec2, ec3 = st.columns([4, 4, 2])
                nc = ec1.selectbox(f"Capo G{r['Giorno']}", all_names, index=all_names.index(r['Capotreno']), key=f"nc_{i}")
                np = ec2.selectbox(f"Pass G{r['Giorno']}", all_names, index=all_names.index(r['Passeggero']), key=f"np_{i}")
                if ec3.button("Salva", key=f"sv_{i}"):
                    st.session_state['master_cal'][i]['Capotreno'], st.session_state['master_cal'][i]['Passeggero'] = nc, np
                    st.session_state[f"active_{i}"] = False
                    st.rerun()

    # --- VISIONE D'INSIEME ---
    st.markdown("### 🖼️ VISIONE D'INSIEME (Screenshot Ready)")
    grid_html = '<div class="summary-grid">'
    for r in st.session_state['master_cal']:
        g_c = db[db['Nome'] == r['Capotreno']]['Grado'].values[0] if r['Capotreno'] in all_names else "R3"
        g_p = db[db['Nome'] == r['Passeggero']]['Grado'].values[0] if r['Passeggero'] in all_names else "R3"
        cl_c = "r5-r4-text" if g_c == "R5/R4" else "r3-text" if g_c == "R3" else "r2-text"
        cl_p = "r5-r4-text" if g_p == "R5/R4" else "r3-text" if g_p == "R3" else "r2-text"
        
        grid_html += f"""
        <div class="summary-day">
            <span class="day-label">GG {r['Giorno']}</span>
            <div class="name-line {cl_c}">{r['Capotreno']}</div>
            <div class="separator">/</div>
            <div class="name-line {cl_p}">{r['Passeggero']}</div>
        </div>
        """
    grid_html += '</div>'
    st.markdown(grid_html, unsafe_allow_html=True)
