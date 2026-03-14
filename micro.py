import streamlit as st
import pandas as pd
import random
from datetime import datetime
import io

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="AOSR Train Manager Elite", layout="wide")

# --- TRADUZIONE MESI ---
MESI_ITA = ["Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno", 
            "Luglio", "Agosto", "Settembre", "Ottobre", "Novembre", "Dicembre"]

# --- CSS CUSTOM COMPLETO ---
st.markdown("""
    <style>
    .stApp {
        background-image: linear-gradient(rgba(11, 14, 20, 0.9), rgba(11, 14, 20, 0.95)), 
                          url('https://images.unsplash.com/photo-1506197361314-878513b4822a?q=80&w=1920&auto=format&fit=crop');
        background-size: cover; background-position: center; color: #ffffff;
    }

    .aosr-header {
        background: rgba(26, 31, 44, 0.95); padding: 20px; border-radius: 20px; 
        border: 2px solid #00c8ff; text-align: center; margin-bottom: 25px;
        box-shadow: 0 0 20px rgba(0, 200, 255, 0.3);
    }
    
    .aosr-title {
        font-family: 'Orbitron', sans-serif; color: #00c8ff; font-size: 2rem;
        display: flex; align-items: center; justify-content: center; gap: 15px;
    }

    /* --- BOTTONI FLUO ALLINEATI --- */
    .stButton > button {
        width: 100% !important; height: 70px !important;
        font-family: 'Orbitron', sans-serif !important; border: none !important;
        transition: 0.3s all !important; text-transform: uppercase !important;
        font-weight: 900 !important; letter-spacing: 4px !important;
        border-radius: 12px !important; margin-bottom: 15px !important;
    }

    /* Genera (Verde Fluo) */
    div[data-testid="stHorizontalBlock"] div:nth-child(1) button {
        background: linear-gradient(90deg, #2ed573, #00ff85) !important;
        box-shadow: 0 0 20px rgba(46, 213, 115, 0.6) !important; color: #000 !important;
    }
    div[data-testid="stHorizontalBlock"] div:nth-child(1) button:hover {
        box-shadow: 0 0 35px rgba(46, 213, 115, 0.9) !important; transform: scale(1.02);
    }

    /* Resetta (Viola Fluo) */
    div[data-testid="stHorizontalBlock"] div:nth-child(2) button {
        background: linear-gradient(90deg, #a29bfe, #6c5ce7) !important;
        box-shadow: 0 0 20px rgba(108, 92, 231, 0.6) !important; color: #fff !important;
    }
    div[data-testid="stHorizontalBlock"] div:nth-child(2) button:hover {
        box-shadow: 0 0 35px rgba(108, 92, 231, 0.9) !important; transform: scale(1.02);
    }

    /* --- CARDS CALENDARIO ED EDITING --- */
    .print-container { 
        background-color: rgba(0, 0, 0, 0.8); padding: 25px; border-radius: 20px; 
        border: 2px solid #00c8ff;
    }
    
    .summary-card {
        background: rgba(25, 25, 25, 0.9); border: 1px solid #444; padding: 10px; 
        text-align: center; border-radius: 12px; margin-bottom: 10px;
        position: relative; transition: 0.3s;
    }
    
    .summary-card:hover { border-color: #00c8ff; box-shadow: 0 0 15px rgba(0, 200, 255, 0.5); }

    .day-label { color: #00c8ff; font-weight: 900; font-size: 0.8rem; margin-bottom: 5px; border-bottom: 1px solid #333; }
    
    /* Micro-bottoni INTERNI alla card */
    .card-edit-controls {
        position: absolute; top: 5px; right: 5px;
        display: flex; flex-direction: column; gap: 2px;
    }

    /* Sovrascrive lo stile Streamlit per i micro-bottoni */
    .card-edit-controls .stButton > button {
        width: 20px !important; height: 20px !important;
        padding: 0 !important; min-width: 20px !important;
        font-size: 0.6rem !important; background: rgba(50, 50, 50, 0.8) !important;
        border: 1px solid #444 !important; border-radius: 4px !important;
        box-shadow: none !important; color: #aaa !important; margin: 0 !important;
    }
    .card-edit-controls .stButton > button:hover {
        background: rgba(100, 100, 100, 0.9) !important; color: #fff !important;
        border-color: #00c8ff !important;
    }

    .p-box { padding: 3px 6px; border-radius: 4px; font-size: 0.75rem; font-weight: 600; text-transform: uppercase; }
    .r5-r4-card { background: rgba(255, 71, 87, 0.15); border-left: 3px solid #ff4757; color: #ff4757; }
    .r3-card { background: rgba(46, 213, 115, 0.15); border-left: 3px solid #2ed573; color: #2ed573; }
    .r2-r1-card { background: rgba(162, 155, 254, 0.15); border-left: 3px solid #a29bfe; color: #a29bfe; }
    
    /* Input di modifica rapidi */
    .quick-edit-form { margin-top: 10px; padding: 5px; border-top: 1px solid #333; }
    .quick-edit-form div[data-baseweb="select"] { font-size: 0.7rem !important; }
    </style>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&display=swap" rel="stylesheet">
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
    st.session_state['sel_mese_ita'] = MESI_ITA[datetime.now().month - 1]
    st.session_state['sel_anno'] = 2026

db = st.session_state['players_db']
all_names = sorted(db['Nome'].tolist())

# --- HEADER ---
st.markdown('<div class="aosr-header"><div class="aosr-title">🚄 AOSR EXPRESS MANAGER 🚄</div></div>', unsafe_allow_html=True)

# --- CONFIGURAZIONE ---
with st.expander("🛠️ IMPOSTAZIONI TRENO", expanded=True):
    c_time, c_r3, c_r2 = st.columns([1,1.5,1.5])
    st.session_state['sel_mese_ita'] = c_time.selectbox("Mese", MESI_ITA, index=MESI_ITA.index(st.session_state['sel_mese_ita']))
    st.session_state['sel_anno'] = c_time.number_input("Anno", 2024, 2030, st.session_state['sel_anno'])
    
    m_r3 = db[db['Grado'] == "R3"]['Nome'].tolist()
    m_r2 = db[db['Grado'] == "R2"]['Nome'].tolist()
    sel_r3 = c_r3.multiselect("Filtra R3", m_r3)
    sel_r2 = c_r2.multiselect("Filtra R2", m_r2)

# --- BOTTONI FLUO ALLINEATI (STESSA RIGA) ---
col_btn1, col_btn2 = st.columns(2)

if col_btn1.button("🚀 GENERA NUOVO CALENDARIO"):
    pool = (sel_r3 if sel_r3 else m_r3) + (sel_r2 if sel_r2 else m_r2)
    random.shuffle(pool)
    leaders = db[db['Grado']=="R5/R4"]['Nome'].tolist()
    # Calcolo giorni del mese
    m_idx = MESI_ITA.index(st.session_state['sel_mese_ita']) + 1
    import calendar as cal_lib
    num_gg = cal_lib.monthrange(st.session_state['sel_anno'], m_idx)[1]
    
    cal_data = []
    p_idx = 0
    for g in range(1, num_gg + 1):
        if g <= 11:
            c, p = leaders[(g-1)%len(leaders)], leaders[g%len(leaders)]
        else:
            c = pool[p_idx % len(pool)]; p_idx += 1
            p = pool[p_idx % len(pool)]; p_idx += 1
        cal_data.append({"Giorno": g, "Capo": c, "Pass": p})
    st.session_state['master_cal'] = cal_data

if col_btn2.button("🗑️ RESETTA TUTTO"):
    if 'master_cal' in st.session_state: del st.session_state['master_cal']
    st.rerun()

# --- VISUALIZZAZIONE CALENDARIO ---
if 'master_cal' in st.session_state:
    st.markdown(f"### 🖼️ CALENDARIO {st.session_state['sel_mese_ita'].upper()} {st.session_state['sel_anno']}")
    
    with st.container():
        st.markdown('<div class="print-container">', unsafe_allow_html=True)
        # Usiamo markdown puro per la griglia per inserire i bottoni all'interno
        cols = st.columns(6)
        
        for i, r in enumerate(st.session_state['master_cal']):
            with cols[i % 6]:
                # Colori basati sul grado
                g_c = db[db['Nome']==r['Capo']]['Grado'].values[0] if r['Capo'] in all_names else "R3"
                g_p = db[db['Nome']==r['Pass']]['Grado'].values[0] if r['Pass'] in all_names else "R3"
                c_c = "#ff4757" if g_c == "R5/R4" else "#2ed573" if g_c == "R3" else "#a29bfe"
                p_c = "#ff4757" if g_p == "R5/R4" else "#2ed573" if g_p == "R3" else "#a29bfe"
                
                # Card Visiva
                st.markdown(f"""
                <div class="summary-card">
                    <div class="day-label">GG {r['Giorno']}</div>
                    <div style="color:{c_c}; font-size:0.8rem; font-weight:bold;">{r['Capo']}</div>
                    <div style="color:#666; font-size:0.5rem;">&</div>
                    <div style="color:{p_c}; font-size:0.8rem; font-weight:bold;">{r['Pass']}</div>
                </div>
                """, unsafe_allow_html=True)
                
                # Sovrapponiamo i micro-bottoni INTERNI alla card usando st.markdown e posizionamento CSS
                # Questo richiede un trucco: posizioniamo dei bottoni streamlit trasparenti sopra la card
                st.markdown('<div class="card-edit-controls">', unsafe_allow_html=True)
                # Bottone Inverti 🔄
                if st.button("🔄", key=f"inv_{i}", help="Inverti ruoli"):
                    st.session_state['master_cal'][i]['Capo'], st.session_state['master_cal'][i]['Pass'] = r['Pass'], r['Capo']
                    st.rerun()
                # Bottone Modifica ✏️
                if st.button("✏️", key=f"ed_{i}", help="Modifica nomi"):
                    st.session_state[f"edit_mode_{i}"] = not st.session_state.get(f"edit_mode_{i}", False)
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Sezione di modifica rapida se attiva (sotto la card)
                if st.session_state.get(f"edit_mode_{i}", False):
                    st.markdown('<div class="quick-edit-form">', unsafe_allow_html=True)
                    nc = st.selectbox("C", all_names, index=all_names.index(r['Capo']), key=f"sc_{i}", label_visibility="collapsed")
                    np = st.selectbox("P", all_names, index=all_names.index(r['Pass']), key=f"sp_{i}", label_visibility="collapsed")
                    if st.button("OK", key=f"ok_{i}"):
                        st.session_state['master_cal'][i].update({"Capo": nc, "Pass": np})
                        st.session_state[f"edit_mode_{i}"] = False
                        st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)
                    
        st.markdown('</div>', unsafe_allow_html=True)

    # --- EXPORT ---
    st.divider()
    st.subheader("📥 Esporta Dati")
    df_export = pd.DataFrame(st.session_state['master_cal'])
    
    # Export CSV
    csv = df_export.to_csv(index=False).encode('utf-8')
    st.download_button(label="💾 Scarica Calendario (CSV)", data=csv, file_name=f"calendario_aosr_{st.session_state['sel_mese_ita']}.csv", mime='text/csv')
