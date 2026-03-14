import streamlit as st
import pandas as pd
import random
from datetime import datetime

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="AOSR Train Manager Elite", layout="wide")

MESI_ITA = ["Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno", 
            "Luglio", "Agosto", "Settembre", "Ottobre", "Novembre", "Dicembre"]

# --- CSS ELITE ANIMATO (IL TUO STANDARD) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap');

    .stApp { 
        background-color: #0b0e14;
        background-image: linear-gradient(rgba(11, 14, 20, 0.9), rgba(11, 14, 20, 0.95)), 
                          url('https://images.unsplash.com/photo-1550751827-4bd374c3f58b?q=80&w=1920&auto=format&fit=crop');
        background-size: cover; color: #ffffff; 
    }

    .train-title {
        font-family: 'Orbitron', sans-serif; font-weight: 900; text-align: center;
        color: #00c8ff; text-shadow: 0 0 20px rgba(0, 200, 255, 0.6);
        font-size: 2.5rem; margin-bottom: 30px; letter-spacing: 5px;
    }

    /* Bottoni Fluo */
    .btn-genera button { 
        background: linear-gradient(45deg, #2ed573, #7bed9f) !important; 
        color: black !important; font-family: 'Orbitron', sans-serif; font-weight: 900; 
        height: 70px !important; width: 100%; border: none !important; 
        box-shadow: 0 4px 15px rgba(46,213,115,0.4) !important; transition: 0.3s all !important;
    }
    .btn-genera button:hover { transform: translateY(-3px); box-shadow: 0 8px 25px rgba(46,213,115,0.6) !important; }

    .btn-resetta button { 
        background: linear-gradient(45deg, #ff4757, #ff6b81) !important; 
        color: white !important; font-family: 'Orbitron', sans-serif; font-weight: 900; 
        height: 70px !important; width: 100%; border: none !important; 
        box-shadow: 0 4px 15px rgba(255,71,87,0.4) !important; transition: 0.3s all !important;
    }
    .btn-resetta button:hover { transform: translateY(-3px); box-shadow: 0 8px 25px rgba(255,71,87,0.6) !important; }

    /* Card Animata */
    .summary-card {
        background: rgba(17, 17, 17, 0.9); border: 1px solid #333; padding: 20px; 
        border-radius: 15px; position: relative; border-top: 3px solid #00c8ff;
        transition: 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    .summary-card:hover {
        transform: scale(1.05); border-color: #00c8ff;
        box-shadow: 0 10px 30px rgba(0, 200, 255, 0.4);
    }
    
    .day-label { color: #00c8ff; font-family: 'Orbitron', sans-serif; font-weight: bold; font-size: 1rem; text-align: center; margin-bottom: 12px; }
    .name-text { font-size: 0.95rem; font-weight: 800; text-align: center; text-transform: uppercase; margin: 4px 0; }

    /* Ingranaggio in alto a destra */
    .popover-container { position: absolute; top: 10px; right: 10px; z-index: 100; }
    div[data-testid="stPopover"] > button {
        background: transparent !important; border: none !important; 
        padding: 0 !important; color: rgba(255,255,255,0.3) !important; font-size: 1.2rem !important;
    }
    div[data-testid="stPopover"] > button:hover { color: #00c8ff !important; transform: rotate(90deg); transition: 0.3s; }
    </style>
    """, unsafe_allow_html=True)

# --- DATABASE ---
def init_db():
    leaders = ["Hool (R5)", "MASTER (R4)", "Le 12 Scimmie (R4)", "Sagittarius A1 (R4)", "Starbetty (R4)", "PEPPE (R4)", "Ricky Around (R4)", "uncle g (R4)", "09ALEX24 (R4)", "ShinyPasta (R4)", "Wall 7 (R4)"]
    r3 = ["G Erry", "Uncle g brother", "Cane Avvoltoio", "Ghandal", "Aryron", "Tricheco", "Maメツ", "NOVEMBERGENZ", "Lalla 96", "Whale Panda", "GennaroM", "EchoZero", "EDDward", "AMY", "Resilienza", "Ana Bunny", "Giuseppec84", "Benito Muschiolini", "Pandino19", "xFlotchy", "MX63", "holdfast", "Ghost", "BadBigBoss", "Stefano00000", "PakII", "BANDOLERO26", "BlOOdyBlade", "Whale hunter Levve", "Aresxxx", "KingGruffalo", "Hulkspakka", "Joseone", "ImAde", "Nysbie", "LeFada13", "Skifetto", "SPio24", "TomEnergy", "Markus Defender", "Sho0t3r", "Wolf006", "Zokra", "perseusxxx", "Bendico", "Obbyy", "ArLes", "Fatz87", "cruel neve", "Trivellatore", "Osgh00", "Slowfia ABOH", "Pontatinatore", "27Francesco", "MissDrinks", "krompir", "MaledettO"]
    r2 = ["teomadh", "Bossnico", "Valecit", "FarmerHool", "camiiiii 08", "Doctor team", "Yass081", "Nuorifleming", "Vergabrio", "Frenk70", "Comandante Maveric", "Thor9000", "MrBolly", "BustaMaki", "Ritardato", "StUnTmArK", "MONKEY D LUFFY 20", "CineSalentino", "Danylo98", "Ezechielefabianino", "BRNcommando", "LEONIDA", "elchicogyot", "erer1000", "Pupisnic", "Backfire1", "AnarchyBG", "Fabrizio1987", "JurdanS", "WiseR9", "Infinity8080"]
    
    data = [{"Nome": n, "Grado": "R5/R4"} for n in leaders] + \
           [{"Nome": n, "Grado": "R3"} for n in r3] + \
           [{"Nome": n, "Grado": "R2"} for n in r2]
    return pd.DataFrame(data)

if 'players_db' not in st.session_state:
    st.session_state['players_db'] = init_db()
    st.session_state['sel_mese'] = MESI_ITA[datetime.now().month - 1]
    st.session_state['sel_anno'] = 2026

db = st.session_state['players_db']
all_names = sorted(db['Nome'].tolist())

# --- TITOLO ---
st.markdown('<div class="train-title">🚄 AOSR EXPRESS ELITE</div>', unsafe_allow_html=True)

# --- CONFIGURAZIONE ---
with st.expander("🛠️ CONFIGURAZIONE TRENO", expanded=True):
    c1, c2, c3 = st.columns([1, 1.5, 1.5])
    st.session_state['sel_mese'] = c1.selectbox("Seleziona Mese", MESI_ITA, index=MESI_ITA.index(st.session_state['sel_mese']))
    st.session_state['sel_anno'] = c1.number_input("Anno", 2024, 2030, st.session_state['sel_anno'])
    
    m_r3 = db[db['Grado'] == "R3"]['Nome'].tolist()
    m_r2 = db[db['Grado'] == "R2"]['Nome'].tolist()
    sel_r3 = c2.multiselect("Filtra R3", m_r3)
    sel_r2 = c3.multiselect("Filtra R2", m_r2)

# --- BOTTONI PRINCIPALI ---
st.markdown("<br>", unsafe_allow_html=True)
col_b1, col_b2 = st.columns(2)
with col_b1:
    st.markdown('<div class="btn-genera">', unsafe_allow_html=True)
    if st.button("🚀 GENERA NUOVO CALENDARIO"):
        pool = (sel_r3 if sel_r3 else m_r3) + (sel_r2 if sel_r2 else m_r2)
        random.shuffle(pool)
        leaders = db[db['Grado']=="R5/R4"]['Nome'].tolist()
        import calendar as cal_lib
        num_gg = cal_lib.monthrange(st.session_state['sel_anno'], MESI_ITA.index(st.session_state['sel_mese']) + 1)[1]
        
        st.session_state['master_cal'] = []
        p_idx = 0
        for g in range(1, num_gg + 1):
            if g <= 11:
                c, p = leaders[(g-1)%len(leaders)], leaders[g%len(leaders)]
            else:
                c, p = pool[p_idx % len(pool)], pool[(p_idx+1) % len(pool)]
                p_idx += 2
            st.session_state['master_cal'].append({"Giorno": g, "Capo": c, "Pass": p})
    st.markdown('</div>', unsafe_allow_html=True)

with col_b2:
    st.markdown('<div class="btn-resetta">', unsafe_allow_html=True)
    if st.button("🗑️ RESETTA SISTEMA"):
        if 'master_cal' in st.session_state: del st.session_state['master_cal']
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- CALENDARIO ---
if 'master_cal' in st.session_state:
    st.markdown(f"<h2 style='text-align: center; font-family: Orbitron;'>{st.session_state['sel_mese'].upper()} {st.session_state['sel_anno']}</h2>", unsafe_allow_html=True)
    cols = st.columns(6)
    
    for i, r in enumerate(st.session_state['master_cal']):
        with cols[i % 6]:
            # Colori gradi
            g_c = db[db['Nome']==r['Capo']]['Grado'].values[0] if r['Capo'] in all_names else "R3"
            g_p = db[db['Nome']==r['Pass']]['Grado'].values[0] if r['Pass'] in all_names else "R3"
            c_col = "#ff4757" if g_c == "R5/R4" else "#2ed573"
            p_col = "#ff4757" if g_p == "R5/R4" else "#2ed573"

            # Card HTML
            st.markdown(f"""
            <div class="summary-card">
                <div class="day-label">GG {r['Giorno']}</div>
                <div class="name-text" style="color:{c_col};">{r['Capo']}</div>
                <div style="color:#555; font-size:0.6rem; text-align:center; margin: 5px 0;">TRAIN PASS</div>
                <div class="name-text" style="color:{p_col};">{r['Pass']}</div>
            """, unsafe_allow_html=True)
            
            # Ingranaggio Popover
            st.markdown('<div class="popover-container">', unsafe_allow_html=True)
            with st.popover("⚙️"):
                # --- LOGICA SCAMBIO FIXATA ---
                if st.button("🔄 Scambia Ruoli", key=f"swap_{i}"):
                    # Scambio diretto nello state
                    old_capo = st.session_state['master_cal'][i]['Capo']
                    st.session_state['master_cal'][i]['Capo'] = st.session_state['master_cal'][i]['Pass']
                    st.session_state['master_cal'][i]['Pass'] = old_capo
                    st.rerun() # Forza il refresh per mostrare il cambio
                
                new_c = st.selectbox("Capo", all_names, index=all_names.index(r['Capo']), key=f"selc_{i}")
                new_p = st.selectbox("Pass", all_names, index=all_names.index(r['Pass']), key=f"selp_{i}")
                
                if st.button("💾 Applica Nomi", key=f"save_{i}"):
                    st.session_state['master_cal'][i]['Capo'] = new_c
                    st.session_state['master_cal'][i]['Pass'] = new_p
                    st.rerun()
            st.markdown('</div></div>', unsafe_allow_html=True)

    st.caption("✨ Grafica Elite Attiva: i riquadri sono animati al passaggio del mouse.")
