import streamlit as st
import pandas as pd
import random
from datetime import datetime

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="AOSR Train Manager Elite", layout="wide")

MESI_ITA = ["Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno", 
            "Luglio", "Agosto", "Settembre", "Ottobre", "Novembre", "Dicembre"]

# --- CSS DEFINITIVO: POSIZIONAMENTO E STILE ---
st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; color: #ffffff; }

    /* Pannello Configurazione */
    .stExpander { background-color: rgba(26, 31, 44, 0.5) !important; border: 1px solid #00c8ff !important; border-radius: 15px !important; }

    /* Bottoni Principali Fluo */
    .btn-genera button { background: linear-gradient(90deg, #2ed573, #00ff85) !important; color: black !important; font-weight: bold; height: 70px !important; width: 100%; border: none !important; box-shadow: 0 0 15px rgba(46,213,115,0.4) !important; margin-bottom: 20px; }
    .btn-resetta button { background: linear-gradient(90deg, #ff4757, #ff0055) !important; color: white !important; font-weight: bold; height: 70px !important; width: 100%; border: none !important; box-shadow: 0 0 15px rgba(255,71,87,0.4) !important; margin-bottom: 20px; }

    /* Card Giorno con posizionamento relativo */
    .summary-card {
        background: #111; border: 1px solid #333; padding: 15px; 
        border-radius: 12px; margin-bottom: 5px; min-height: 120px;
        position: relative; /* Necessario per l'ingranaggio */
        border-top: 2px solid #00c8ff;
    }
    
    .day-label { color: #00c8ff; font-weight: bold; font-size: 0.9rem; text-align: center; margin-bottom: 10px; }
    .name-text { font-size: 0.9rem; font-weight: bold; text-align: center; text-transform: uppercase; margin: 3px 0; }
    
    /* FORZATURA INGRANAGGIO IN ALTO A DESTRA */
    .popover-container {
        position: absolute;
        top: 5px;
        right: 5px;
        z-index: 100;
    }
    
    /* Stile pulito per il tasto ingranaggio */
    div[data-testid="stPopover"] > button {
        background: transparent !important; border: none !important; 
        padding: 0 !important; color: #555 !important; font-size: 1rem !important;
        box-shadow: none !important;
    }
    div[data-testid="stPopover"] > button:hover { color: #00c8ff !important; transform: rotate(45deg); transition: 0.3s; }
    
    </style>
    """, unsafe_allow_html=True)

# --- DATABASE ---
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
    st.session_state['sel_mese'] = MESI_ITA[datetime.now().month - 1]
    st.session_state['sel_anno'] = 2026

db = st.session_state['players_db']
all_names = sorted(db['Nome'].tolist())

# --- HEADER ---
st.markdown("<h1 style='text-align: center; color: #00c8ff; font-family: Orbitron;'>AOSR TRAIN MANAGER ELITE</h1>", unsafe_allow_html=True)

# --- 🛠️ CONFIGURAZIONE RIPRISTINATA ---
with st.expander("🛠️ CONFIGURAZIONE PASSEGGERI", expanded=True):
    c1, c2, c3 = st.columns([1, 1.5, 1.5])
    st.session_state['sel_mese'] = c1.selectbox("Mese", MESI_ITA, index=MESI_ITA.index(st.session_state['sel_mese']))
    st.session_state['sel_anno'] = c1.number_input("Anno", 2024, 2030, st.session_state['sel_anno'])
    
    m_r3 = db[db['Grado'] == "R3"]['Nome'].tolist()
    m_r2 = db[db['Grado'] == "R2"]['Nome'].tolist()
    sel_r3 = c2.multiselect("Filtra R3 (Vuoto = Tutti)", m_r3)
    sel_r2 = c3.multiselect("Filtra R2 (Vuoto = Tutti)", m_r2)

# --- BOTTONI PRINCIPALI ALLINEATI ---
col_b1, col_b2 = st.columns(2)
with col_b1:
    st.markdown('<div class="btn-genera">', unsafe_allow_html=True)
    if st.button("🚀 GENERA NUOVO CALENDARIO"):
        pool = (sel_r3 if sel_r3 else m_r3) + (sel_r2 if sel_r2 else m_r2)
        random.shuffle(pool)
        leaders = db[db['Grado']=="R5/R4"]['Nome'].tolist()
        m_idx = MESI_ITA.index(st.session_state['sel_mese']) + 1
        import calendar as cal_lib
        num_gg = cal_lib.monthrange(st.session_state['sel_anno'], m_idx)[1]
        
        new_cal = []
        p_idx = 0
        for g in range(1, num_gg + 1):
            if g <= 11:
                c, p = leaders[(g-1)%len(leaders)], leaders[g%len(leaders)]
            else:
                c = pool[p_idx % len(pool)]; p_idx += 1
                p = pool[p_idx % len(pool)]; p_idx += 1
            new_cal.append({"Giorno": g, "Capo": c, "Pass": p})
        st.session_state['master_cal'] = new_cal
    st.markdown('</div>', unsafe_allow_html=True)

with col_b2:
    st.markdown('<div class="btn-resetta">', unsafe_allow_html=True)
    if st.button("🗑️ RESETTA"):
        if 'master_cal' in st.session_state: del st.session_state['master_cal']
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- CALENDARIO ---
if 'master_cal' in st.session_state:
    st.markdown(f"<h3 style='text-align: center; color: white;'>📅 {st.session_state['sel_mese'].upper()} {st.session_state['sel_anno']}</h3>", unsafe_allow_html=True)
    
    cols = st.columns(6)
    for i, r in enumerate(st.session_state['master_cal']):
        with cols[i % 6]:
            # Colori in base al grado
            g_c = db[db['Nome']==r['Capo']]['Grado'].values[0] if r['Capo'] in all_names else "R3"
            g_p = db[db['Nome']==r['Pass']]['Grado'].values[0] if r['Pass'] in all_names else "R3"
            c_col = "#ff4757" if g_c == "R5/R4" else "#2ed573"
            p_col = "#ff4757" if g_p == "R5/R4" else "#2ed573"

            # Container della Card
            st.markdown(f"""
            <div class="summary-card">
                <div class="day-label">GG {r['Giorno']}</div>
                <div class="name-text" style="color:{c_col};">{r['Capo']}</div>
                <div style="color:#444; font-size:0.6rem; text-align:center;">TRAIN PASS</div>
                <div class="name-text" style="color:{p_col};">{r['Pass']}</div>
            """, unsafe_allow_html=True)
            
            # INGRANAGGIO IN ALTO A DESTRA (DENTRO LA CARD)
            st.markdown('<div class="popover-container">', unsafe_allow_html=True)
            with st.popover("⚙️"):
                st.write(f"Modifica Giorno {r['Giorno']}")
                if st.button("🔄 Inverti Ruoli", key=f"inv_{i}"):
                    st.session_state['master_cal'][i]['Capo'], st.session_state['master_cal'][i]['Pass'] = r['Pass'], r['Capo']
                    st.rerun()
                
                new_c = st.selectbox("Capo", all_names, index=all_names.index(r['Capo']), key=f"selc_{i}")
                new_p = st.selectbox("Pass", all_names, index=all_names.index(r['Pass']), key=f"selp_{i}")
                
                if st.button("✅ Salva", key=f"ok_{i}"):
                    st.session_state['master_cal'][i].update({"Capo": new_c, "Pass": new_p})
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True) # Chiude popover-container
            st.markdown('</div>', unsafe_allow_html=True) # Chiude summary-card

    st.info("💡 Usa l'ingranaggio in alto a destra di ogni casella per scambiare i ruoli o cambiare i nomi.")
