import streamlit as st
import pandas as pd
import random
from datetime import datetime

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="AOSR Train Manager - Deluxe Edition", layout="wide")

MESI_ITA = ["Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno", 
            "Luglio", "Agosto", "Settembre", "Ottobre", "Novembre", "Dicembre"]

# --- CSS AVANZATO: BOLD & HARMONIOUS WEST ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Special+Elite&family=Rye&family=Montserrat:wght@700;900&display=swap');

    .stApp { 
        background: linear-gradient(rgba(30, 20, 10, 0.75), rgba(15, 10, 5, 0.92)), 
                    url('https://images.unsplash.com/photo-1510524527013-0393282436da?q=80&w=1920&auto=format&fit=crop');
        background-size: cover; background-attachment: fixed;
    }

    /* TITOLO TITANICO */
    .train-title {
        font-family: 'Rye', cursive;
        text-align: center; color: #ffcc66;
        text-shadow: 5px 5px 0px #4b2e1b;
        font-size: 4rem; margin-bottom: 20px;
    }

    /* RIQUADRO ASSEGNAZIONI ARMONIOSO */
    .stExpander {
        background: rgba(43, 29, 14, 0.9) !important;
        border: 4px solid #ffcc66 !important;
        border-radius: 15px !important;
        box-shadow: 0px 10px 30px rgba(0,0,0,0.8) !important;
    }
    
    .stExpander details summary {
        font-family: 'Rye', cursive !important;
        color: #ffcc66 !important;
        font-size: 1.5rem !important;
        padding: 10px !important;
    }

    /* CARD WANTED (VISTA CARDS) */
    .summary-card {
        background: #fdf5e6; 
        border: 4px solid #5d4037; /* Bordo più pieno */
        padding: 15px 10px; 
        border-radius: 8px; 
        box-shadow: 10px 10px 20px rgba(0,0,0,0.6);
        color: #2b1d0e; 
        margin-bottom: 15px;
        height: 220px;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        background-image: url('https://www.transparenttextures.com/patterns/paper-fibers.png'); /* Texture carta */
    }

    .day-badge {
        background: #8b0000; color: white;
        font-family: 'Montserrat', sans-serif; font-weight: 900;
        padding: 4px 12px; border-radius: 4px; font-size: 1rem;
        align-self: flex-start; margin-bottom: 10px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.3);
    }

    .role-label { 
        color: #5d4037; font-size: 0.75rem; letter-spacing: 1.5px;
        font-family: 'Montserrat', sans-serif; text-transform: uppercase; font-weight: 800;
        margin-top: 6px; border-bottom: 2px solid rgba(93, 64, 55, 0.2);
    }

    .name-container {
        height: 45px; 
        display: flex;
        align-items: center;
        margin-bottom: 5px;
    }

    .name-text { 
        font-family: 'Special Elite', cursive; font-size: 1rem; font-weight: 900; 
        text-transform: uppercase; line-height: 1.1;
        border-left: 5px solid #d4a373; padding-left: 10px;
    }

    /* BOTTONI PIÙ "PIENI" */
    .stButton>button {
        border-radius: 8px !important;
        font-family: 'Rye', cursive !important;
        font-size: 1.3rem !important;
        height: 55px !important;
        border: 3px solid #2b1d0e !important;
        box-shadow: 0px 4px 0px #2b1d0e !important;
        transition: all 0.1s !important;
    }
    
    .stButton>button:active {
        transform: translateY(4px) !important;
        box-shadow: 0px 0px 0px !important;
    }

    .btn-genera button { background: #d4a373 !important; color: #2b1d0e !important; }
    .btn-resetta button { background: #a44a3f !important; color: white !important; }
    
    /* Input Form Labels */
    label p {
        font-family: 'Montserrat', sans-serif !important;
        color: #ffcc66 !important;
        font-weight: 800 !important;
        font-size: 1.1rem !important;
    }

    hr { border-top: 3px solid #ffcc66 !important; opacity: 0.8; margin: 30px 0; }
    </style>
    """, unsafe_allow_html=True)

# --- DATABASE ---
def init_db():
    leaders = ["Hool (R5)", "MASTER (R4)", "Le 12 Scimmie (R4)", "Sagittarius A1 (R4)", "Starbetty (R4)", "PEPPE (R4)", "Ricky Around (R4)", "uncle g (R4)", "09ALEX24 (R4)", "ShinyPasta (R4)", "Wall 7 (R4)"]
    r3 = ["G Erry", "Uncle g brother", "Cane Avvoltoio", "Ghandal", "Aryron", "Tricheco", "Maメツ", "NOVEMBERGENZ", "Lalla 96", "Whale Panda", "GennaroM", "EchoZero", "EDDward", "AMY", "Resilienza", "Ana Bunny", "Giuseppec84", "Benito Muschiolini", "Pandino19", "xFlotchy", "MX63", "holdfast", "Ghost", "BadBigBoss", "Stefano00000", "PakII", "BANDOLERO26", "BlOOdyBlade", "Whale hunter Levve", "Aresxxx", "KingGruffalo", "Hulkspakka", "Joseone", "ImAde", "Nysbie", "LeFada13", "Skifetto", "SPio24", "TomEnergy", "Markus Defender", "Sho0t3r", "Wolf006", "Zokra", "perseusxxx", "Bendico", "Obbyy", "ArLes", "Fatz87", "cruel neve", "Trivellatore", "Osgh00", "Slowfia ABOH", "Pontatinatore", "27Francesco", "MissDrinks", "krompir", "MaledettO"]
    r2 = ["teomadh", "Bossnico", "Valecit", "FarmerHool", "camiiiii 08", "Doctor team", "Yass081", "Nuorifleming", "Vergabrio", "Frenk70", "Comandante Maveric", "Thor9000", "MrBolly", "BustaMaki", "Ritardato", "StUnTmArK", "MONKEY D LUFFY 20", "CineSalentino", "Danylo98", "Ezechielefabianino", "BRNcommando", "LEONIDA", "elchicogyot", "erer1000", "Pupisnic", "Backfire1", "AnarchyBG", "Fabrizio1987", "JurdanS", "WiseR9", "Infinity8080"]
    data = [{"Nome": n, "Grado": "R5/R4"} for n in leaders] + [{"Nome": n, "Grado": "R3"} for n in r3] + [{"Nome": n, "Grado": "R2"} for n in r2]
    return pd.DataFrame(data)

if 'players_db' not in st.session_state:
    st.session_state['players_db'] = init_db()
    st.session_state['sel_mese'] = MESI_ITA[datetime.now().month - 1]
    st.session_state['sel_anno'] = 2026

db = st.session_state['players_db']
all_names = sorted(db['Nome'].tolist())

# --- TITOLO ---
st.markdown('<div class="train-title">🚂 AOSR EXPRESS</div>', unsafe_allow_html=True)

# --- PANEL REGISTRO (RIQUADRO ARMONIOSO) ---
with st.expander("📝 UFFICIO ASSEGNAZIONI", expanded=True):
    # Layout più arioso
    c1, c2, c3, c4 = st.columns([1, 1.2, 1.2, 1.2])
    with c1:
        st.session_state['sel_mese'] = st.selectbox("Mese", MESI_ITA, index=MESI_ITA.index(st.session_state['sel_mese']))
        st.session_state['sel_anno'] = st.number_input("Anno", 2024, 2030, st.session_state['sel_anno'])
    
    m_leaders = db[db['Grado'] == "R5/R4"]['Nome'].tolist()
    m_r3, m_r2 = db[db['Grado'] == "R3"]['Nome'].tolist(), db[db['Grado'] == "R2"]['Nome'].tolist()
    
    with c2: sel_leaders = st.multiselect("Sceriffi R5/R4", m_leaders)
    with c3: sel_r3 = st.multiselect("Banditi R3", m_r3)
    with c4: sel_r2 = st.multiselect("Fuorilegge R2", m_r2)

    st.markdown("<br>", unsafe_allow_html=True)
    cb1, cb2 = st.columns(2)
    with cb1:
        st.markdown('<div class="btn-genera">', unsafe_allow_html=True)
        if st.button("⚒️ GENERA CONVOGLIO"):
            pool_leaders = sel_leaders if sel_leaders else m_leaders
            pool_others = (sel_r3 if sel_r3 else m_r3) + (sel_r2 if sel_r2 else m_r2)
            random.shuffle(pool_others)
            num_gg = (pd.Timestamp(year=st.session_state['sel_anno'], month=MESI_ITA.index(st.session_state['sel_mese'])+1, day=1) + pd.offsets.MonthEnd(0)).day
            st.session_state['master_cal'] = []
            p_idx = 0
            for g in range(1, num_gg + 1):
                if g <= 11:
                    c = pool_leaders[(g-1)%len(pool_leaders)]; p = pool_leaders[g%len(pool_leaders)]
                else:
                    c = pool_others[p_idx % len(pool_others)]; p = pool_others[(p_idx+1) % len(pool_others)]
                    p_idx += 2
                st.session_state['master_cal'].append({"Giorno": g, "Capo": c, "Pass": p})
        st.markdown('</div>', unsafe_allow_html=True)
    with cb2:
        st.markdown('<div class="btn-resetta">', unsafe_allow_html=True)
        if st.button("🏜️ RESET"):
            if 'master_cal' in st.session_state: del st.session_state['master_cal']
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# --- VISUALIZZAZIONE ---
if 'master_cal' in st.session_state:
    st.markdown("<hr>", unsafe_allow_html=True)
    tab_cards, tab_lista = st.tabs(["🎴 VISTA CARDS", "📜 REGISTRO SEQUENZIALE"])

    with tab_cards:
        cols = st.columns(7)
        for i, r in enumerate(st.session_state['master_cal']):
            with cols[i % 7]:
                c_col = "#8b0000" if any(db[(db['Nome'] == r['Capo']) & (db['Grado'] == "R5/R4")]['Nome']) else "#1b4d3e"
                p_col = "#8b0000" if any(db[(db['Nome'] == r['Pass']) & (db['Grado'] == "R5/R4")]['Nome']) else "#1b4d3e"
                st.markdown(f"""
                <div class="summary-card">
                    <div class="day-badge">GG {r['Giorno']}</div>
                    <div class="role-label">CAPOTRENO</div>
                    <div class="name-container">
                        <div class="name-text" style="color:{c_col};">{r['Capo']}</div>
                    </div>
                    <div class="role-label">PASSEGGERO</div>
                    <div class="name-container">
                        <div class="name-text" style="color:{p_col};">{r['Pass']}</div>
                    </div>
                """, unsafe_allow_html=True)
                with st.popover("⚙️"):
                    nc = st.selectbox("Capotreno", all_names, index=all_names.index(r['Capo']), key=f"c_{i}")
                    np = st.selectbox("Passeggero", all_names, index=all_names.index(r['Pass']), key=f"p_{i}")
                    if st.button("💾 Salva", key=f"s_{i}"):
                        st.session_state['master_cal'][i].update({"Capo": nc, "Pass": np}); st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

    with tab_lista:
        st.markdown('<div class="registro-box">', unsafe_allow_html=True)
        for r in st.session_state['master_cal']:
            st.markdown(f"**Giorno {r['Giorno']}:** {r['Capo']} (Capotreno) ➔ {r['Pass']} (Passeggero)")
        st.markdown('</div>', unsafe_allow_html=True)
