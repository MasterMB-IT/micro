import streamlit as st
import pandas as pd
import random
from datetime import datetime

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="AOSR Train Manager Elite", layout="wide")

MESI_ITA = ["Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno", 
            "Luglio", "Agosto", "Settembre", "Ottobre", "Novembre", "Dicembre"]

# --- CSS DEFINITIVO ---
st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; color: #ffffff; }

    /* Bottoni Principali Fluo */
    .btn-genera button { background: linear-gradient(90deg, #2ed573, #00ff85) !important; color: black !important; font-weight: bold; height: 60px !important; width: 100%; border: none !important; box-shadow: 0 0 15px rgba(46,213,115,0.4) !important; }
    .btn-resetta button { background: linear-gradient(90deg, #ff4757, #ff0055) !important; color: white !important; font-weight: bold; height: 60px !important; width: 100%; border: none !important; box-shadow: 0 0 15px rgba(255,71,87,0.4) !important; }

    /* Card Giorno */
    .summary-card {
        background: #111; border: 1px solid #333; padding: 12px; 
        border-radius: 12px; margin-bottom: 5px; min-height: 110px;
        position: relative; border-left: 4px solid #00c8ff;
    }
    .day-label { color: #00c8ff; font-weight: bold; font-size: 0.85rem; text-align: center; margin-bottom: 10px; }
    .name-text { font-size: 0.9rem; font-weight: bold; text-align: center; text-transform: uppercase; margin: 2px 0; }
    
    /* Rimuovi bordi e ombre dai popover per non sporcare */
    div[data-testid="stPopover"] > button {
        background: transparent !important; border: none !important; 
        padding: 0 !important; color: #444 !important; font-size: 0.8rem !important;
        position: absolute; top: 5px; right: 8px;
    }
    div[data-testid="stPopover"] > button:hover { color: #00c8ff !important; }
    </style>
    """, unsafe_allow_html=True)

# --- DATABASE ---
def init_db():
    data = []
    leaders = ["Hool (R5)", "MASTER (R4)", "Le 12 Scimmie (R4)", "Sagittarius A1 (R4)", "Starbetty (R4)", "PEPPE (R4)", "Ricky Around (R4)", "uncle g (R4)", "09ALEX24 (R4)", "ShinyPasta (R4)", "Wall 7 (R4)"]
    for n in leaders: data.append({"Nome": n, "Grado": "R5/R4"})
    # ... (Il resto del database rimane invariato come nelle versioni precedenti)
    r3 = ["G Erry", "Uncle g brother", "Cane Avvoltoio", "Ghandal", "Aryron", "Tricheco", "Maメツ", "NOVEMBERGENZ", "Lalla 96", "Whale Panda", "GennaroM", "EchoZero", "EDDward", "AMY", "Resilienza", "Ana Bunny", "Giuseppec84", "Benito Muschiolini", "Pandino19", "xFlotchy", "MX63", "holdfast", "Ghost", "BadBigBoss", "Stefano00000", "PakII", "BANDOLERO26", "BlOOdyBlade", "Whale hunter Levve", "Aresxxx", "KingGruffalo", "Hulkspakka", "Joseone", "ImAde", "Nysbie", "LeFada13", "Skifetto", "SPio24", "TomEnergy", "Markus Defender", "Sho0t3r", "Wolf006", "Zokra", "perseusxxx", "Bendico", "Obbyy", "ArLes", "Fatz87", "cruel neve", "Trivellatore", "Osgh00", "Slowfia ABOH", "Pontatinatore", "27Francesco", "MissDrinks", "krompir", "MaledettO"]
    for n in r3: data.append({"Nome": n, "Grado": "R3"})
    return pd.DataFrame(data)

if 'players_db' not in st.session_state:
    st.session_state['players_db'] = init_db()
    st.session_state['sel_mese'] = MESI_ITA[datetime.now().month - 1]
    st.session_state['sel_anno'] = 2026

db = st.session_state['players_db']
all_names = sorted(db['Nome'].tolist())

# --- HEADER ---
st.title("🚄 AOSR EXPRESS MANAGER")

# --- BOTTONI PRINCIPALI ---
col_b1, col_b2 = st.columns(2)
with col_b1:
    st.markdown('<div class="btn-genera">', unsafe_allow_html=True)
    if st.button("🚀 GENERA"):
        # Logica di generazione
        leaders = db[db['Grado']=="R5/R4"]['Nome'].tolist()
        others = db[db['Grado']!="R5/R4"]['Nome'].tolist()
        random.shuffle(others)
        m_idx = MESI_ITA.index(st.session_state['sel_mese']) + 1
        import calendar as cal_lib
        num_gg = cal_lib.monthrange(st.session_state['sel_anno'], m_idx)[1]
        cal = []
        p_idx = 0
        for g in range(1, num_gg + 1):
            if g <= 11: c, p = leaders[(g-1)%len(leaders)], leaders[g%len(leaders)]
            else: 
                c = others[p_idx % len(others)]; p = others[(p_idx+1) % len(others)]
                p_idx += 2
            cal.append({"Giorno": g, "Capo": c, "Pass": p})
        st.session_state['master_cal'] = cal
    st.markdown('</div>', unsafe_allow_html=True)

with col_b2:
    st.markdown('<div class="btn-resetta">', unsafe_allow_html=True)
    if st.button("🗑️ RESETTA"):
        if 'master_cal' in st.session_state: del st.session_state['master_cal']
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- CALENDARIO ---
if 'master_cal' in st.session_state:
    st.subheader(f"📅 {st.session_state['sel_mese'].upper()} {st.session_state['sel_anno']}")
    cols = st.columns(6)
    
    for i, r in enumerate(st.session_state['master_cal']):
        with cols[i % 6]:
            # Colori dinamici
            g_c = db[db['Nome']==r['Capo']]['Grado'].values[0] if r['Capo'] in all_names else "R3"
            g_p = db[db['Nome']==r['Pass']]['Grado'].values[0] if r['Pass'] in all_names else "R3"
            c_col = "#ff4757" if g_c == "R5/R4" else "#2ed573"
            p_col = "#ff4757" if g_p == "R5/R4" else "#2ed573"

            # Card visiva (HTML per lo screenshot)
            st.markdown(f"""
            <div class="summary-card">
                <div class="day-label">GG {r['Giorno']}</div>
                <div class="name-text" style="color:{c_col};">{r['Capo']}</div>
                <div style="color:#444; font-size:0.6rem; text-align:center;">TRAIN PASS</div>
                <div class="name-text" style="color:{p_col};">{r['Pass']}</div>
            </div>
            """, unsafe_allow_html=True)

            # MENU A TENDINA (Popover) - Posizionato sopra la card
            with st.popover("⚙️", use_container_width=False):
                st.write(f"Opzioni Giorno {r['Giorno']}")
                if st.button("🔄 Inverti Ruoli", key=f"inv_{i}"):
                    st.session_state['master_cal'][i]['Capo'], st.session_state['master_cal'][i]['Pass'] = r['Pass'], r['Capo']
                    st.rerun()
                
                new_c = st.selectbox("Cambia Capo", all_names, index=all_names.index(r['Capo']), key=f"nc_{i}")
                new_p = st.selectbox("Cambia Pass", all_names, index=all_names.index(r['Pass']), key=f"np_{i}")
                
                if st.button("✅ Salva", key=f"save_{i}"):
                    st.session_state['master_cal'][i].update({"Capo": new_c, "Pass": new_p})
                    st.rerun()

    st.success("✨ Suggerimento: Clicca sull'ingranaggio grigio in alto a destra di ogni casella per modificare i nomi o invertire i ruoli!")
