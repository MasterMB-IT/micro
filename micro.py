import streamlit as st
import pandas as pd
import random
from datetime import datetime

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="AOSR Train Manager - Deluxe Edition", layout="wide")

MESI_ITA = ["Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno", 
            "Luglio", "Agosto", "Settembre", "Ottobre", "Novembre", "Dicembre"]

# --- CSS DEFINITIVO ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Special+Elite&family=Rye&family=Montserrat:wght@900&display=swap');

    .stApp { 
        background: linear-gradient(rgba(30, 20, 10, 0.75), rgba(15, 10, 5, 0.92)), 
                    url('https://images.unsplash.com/photo-1510524527013-0393282436da?q=80&w=1920&auto=format&fit=crop');
        background-size: cover; background-attachment: fixed;
    }

    .train-title {
        font-family: 'Rye', cursive;
        text-align: center; color: #ffcc66;
        text-shadow: 4px 4px 0px #4b2e1b;
        font-size: 3rem; margin-bottom: 10px;
    }

    /* PULSANTI */
    .stButton>button {
        width: 100% !important; height: 55px !important;
        border-radius: 10px !important;
        font-family: 'Montserrat', sans-serif !important;
        font-weight: 900 !important; font-size: 1.1rem !important;
        text-transform: uppercase !important;
        border: 3px solid #2b1d0e !important;
        box-shadow: 0px 5px 0px #1a1108 !important;
    }
    .btn-genera button { background: linear-gradient(145deg, #d4a373, #b88655) !important; color: #2b1d0e !important; }
    .btn-resetta button { background: linear-gradient(145deg, #a44a3f, #7a3229) !important; color: white !important; }

    /* CARDS */
    .summary-card {
        background: #fdf5e6; border: 3px solid #5d4037;
        padding: 10px; border-radius: 8px; 
        box-shadow: 8px 8px 15px rgba(0,0,0,0.6);
        color: #2b1d0e; margin-bottom: 10px;
        height: 200px;
        background-image: url('https://www.transparenttextures.com/patterns/paper-fibers.png');
    }

    .compact-card {
        background: #fdf5e6; border: 2px solid #5d4037;
        padding: 6px 4px; border-radius: 5px; 
        box-shadow: 4px 4px 10px rgba(0,0,0,0.5);
        color: #2b1d0e; margin-bottom: 5px;
        height: 140px; 
        background-image: url('https://www.transparenttextures.com/patterns/paper-fibers.png');
    }

    .day-badge {
        background: #8b0000; color: white;
        font-family: 'Montserrat', sans-serif; font-weight: 900;
        padding: 2px 8px; border-radius: 4px; font-size: 0.8rem;
        display: inline-block; margin-bottom: 5px;
    }

    .role-label { 
        color: #5d4037; font-size: 0.6rem; letter-spacing: 1px;
        font-family: 'Montserrat', sans-serif; text-transform: uppercase; font-weight: 800;
        border-bottom: 1px solid rgba(93, 64, 55, 0.2);
    }

    .name-container { height: 32px; display: flex; align-items: center; overflow: hidden; }
    
    .name-text { 
        font-family: 'Special Elite', cursive; font-size: 0.85rem; font-weight: 900; 
        white-space: nowrap; overflow: hidden; text-overflow: ellipsis; width: 100%;
        border-left: 4px solid #d4a373; padding-left: 8px;
    }

    .compact-card .name-text { font-size: 0.75rem; border-left-width: 3px; }

    /* STILE REGISTRO TESTUALE */
    .registro-text {
        background: rgba(253, 245, 230, 0.95);
        padding: 20px;
        border-radius: 10px;
        font-family: 'Special Elite', cursive;
        color: #2b1d0e;
        border: 2px solid #5d4037;
        line-height: 1.6;
    }

    hr { border-top: 2px solid #ffcc66 !important; opacity: 0.6; }
    </style>
    """, unsafe_allow_html=True)

# --- DATABASE (Nomi immagini inclusi) ---
def init_db():
    leaders = ["Hool (R5)", "MASTER (R4)", "Le 12 Scimmie (R4)", "Sagittarius A1 (R4)", "Starbetty (R4)", "PEPPE (R4)", "Ricky Around (R4)", "uncle g (R4)", "09ALEX24 (R4)", "ShinyPasta (R4)", "Wall 7 (R4)"]
    r3 = ["G Erry", "Uncle g brother", "Goz", "Ghandal", "Aryron", "Tricheco", "Maメツ", "NOVEMBERGENZ", "Lalla 96", "Whale Panda", "GennaroM", "EchoZero", "EDDward", "AMY", "Resilienza", "Ana Bunny", "Giuseppec84", "Benito Muschiolini", "Pandino19", "xFlotchy", "MX63", "holdfast", "Ghost", "BadBigBoss", "Stefano00000", "PakII", "BANDOLERO26", "BlOOdyBlade", "Whale hunter Levve", "Aresxxx", "KingGruffalo", "Hulkspakka", "Joseppone", "ImAde", "Nysbie", "LeFada13", "Skiteto", "SPio24", "TomEnergy", "Markus Defender", "Sho0t3r", "Wolf006", "Zokra", "perseusxxx", "Bendico", "Obbyy", "ArLes", "Fatz87", "cruel neve", "Trivellatore", "Osgh00", "Slowfia ABOH", "Pontatinatore", "27Francesco", "MissDrinks", "krompir", "MaledettO"]
    r2 = ["teomadh", "Bossnico", "Valecit", "FarmerHool", "camiiiii 08", "Doctor team", "Yass081", "Nuorifleming", "Vergabrio", "Frenk70", "Comandante Maveric", "Thor9000", "MrBolly", "BustaMaki", "S U C A", "StUnTmArK", "MONKEY D LUFFY 20", "CineSalentino", "Danylo98", "Ezechielefabianino", "BRNcommando", "LEONIDA", "elchicogyot", "erer1000", "Pupisnic", "Backfire1", "AnarchyBG", "Fabrizio1987", "JurdanS", "WiseR9", "Infinity8080"]
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

# --- PANEL REGISTRO ---
with st.expander("📝 UFFICIO ASSEGNAZIONI", expanded=True):
    c1, c2, c3, c4 = st.columns([1, 1.2, 1.2, 1.2])
    with c1:
        st.session_state['sel_mese'] = st.selectbox("Mese", MESI_ITA, index=MESI_ITA.index(st.session_state['sel_mese']))
        st.session_state['sel_anno'] = st.number_input("Anno", 2024, 2030, st.session_state['sel_anno'])
    
    m_leaders = db[db['Grado'] == "R5/R4"]['Nome'].tolist()
    m_r3, m_r2 = db[db['Grado'] == "R3"]['Nome'].tolist(), db[db['Grado'] == "R2"]['Nome'].tolist()
    with c2: sel_leaders = st.multiselect("R5/R4", m_leaders)
    with c3: sel_r3 = st.multiselect("R3", m_r3)
    with c4: sel_r2 = st.multiselect("R2", m_r2)

    st.markdown("<br>", unsafe_allow_html=True)
    cb1, cb2, cb3 = st.columns([1, 1, 1.5])
    with cb1:
        st.markdown('<div class="btn-genera">', unsafe_allow_html=True)
        if st.button("⚒️ GENERA"):
            pool_leaders = sel_leaders if sel_leaders else m_leaders
            pool_others = (sel_r3 if sel_r3 else m_r3) + (sel_r2 if sel_r2 else m_r2)
            random.shuffle(pool_leaders)
            random.shuffle(pool_others)
            num_gg = (pd.Timestamp(year=st.session_state['sel_anno'], month=MESI_ITA.index(st.session_state['sel_mese'])+1, day=1) + pd.offsets.MonthEnd(0)).day
            st.session_state['master_cal'] = []
            p_idx = 0
            for g in range(1, num_gg + 1):
                if g <= 11:
                    c = pool_leaders[(g-1) % len(pool_leaders)]
                    p = pool_leaders[g % len(pool_leaders)]
                else:
                    c = pool_others[p_idx % len(pool_others)]
                    p = pool_others[(p_idx + 1) % len(pool_others)]
                    p_idx += 2
                st.session_state['master_cal'].append({"Giorno": g, "Capo": c, "Pass": p})
        st.markdown('</div>', unsafe_allow_html=True)
    with cb2:
        st.markdown('<div class="btn-resetta">', unsafe_allow_html=True)
        if st.button("🌵 RESET"):
            if 'master_cal' in st.session_state: del st.session_state['master_cal']
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with cb3:
        st.markdown("<br>", unsafe_allow_html=True)
        view_mode = st.toggle("🎞️ VISTA TOTALE (Tutto in una schermata)", value=False)

# --- VISUALIZZAZIONE ---
if 'master_cal' in st.session_state:
    st.markdown("<hr>", unsafe_allow_html=True)
    
    if not view_mode:
        tab_cards, tab_lista = st.tabs(["🎴 VISTA EDITABILE", "📜 REGISTRO"])
        
        with tab_cards:
            cols = st.columns(7)
            for i, r in enumerate(st.session_state['master_cal']):
                with cols[i % 7]:
                    c_col = "#8b0000" if any(db[(db['Nome'] == r['Capo']) & (db['Grado'] == "R5/R4")]['Nome']) else "#1b4d3e"
                    p_col = "#8b0000" if any(db[(db['Nome'] == r['Pass']) & (db['Grado'] == "R5/R4")]['Nome']) else "#1b4d3e"
                    st.markdown(f"""<div class="summary-card">
                        <div class="day-badge">GG {r['Giorno']}</div>
                        <div class="role-label">CAPOTRENO</div>
                        <div class="name-container"><div class="name-text" style="color:{c_col}; border-left-color:{c_col};">🤠 {r['Capo']}</div></div>
                        <div class="role-label">PASSEGGERO</div>
                        <div class="name-container"><div class="name-text" style="color:{p_col}; border-left-color:{p_col};">🐎 {r['Pass']}</div></div>
                    """, unsafe_allow_html=True)
                    with st.popover("⚙️"):
                        nc = st.selectbox("Capo", all_names, index=all_names.index(r['Capo']), key=f"c_{i}")
                        np = st.selectbox("Pass", all_names, index=all_names.index(r['Pass']), key=f"p_{i}")
                        if st.button("Salva", key=f"s_{i}"):
                            st.session_state['master_cal'][i].update({"Capo": nc, "Pass": np}); st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)
        
        with tab_lista:
            # --- QUI HO AGGIUNTO IL CODICE PER IL REGISTRO ---
            st.markdown('<div class="registro-text">', unsafe_allow_html=True)
            st.subheader(f"📋 ORDINE DI SERVIZIO - {st.session_state['sel_mese'].upper()} {st.session_state['sel_anno']}")
            for r in st.session_state['master_cal']:
                st.markdown(f"**Giorno {r['Giorno']}** | 🤠 Capo: `{r['Capo']}` ➔ 🐎 Pass: `{r['Pass']}`")
            st.markdown('</div>', unsafe_allow_html=True)

    else:
        # VISTA TOTALE: 8 Colonne
        cols = st.columns(8)
        for i, r in enumerate(st.session_state['master_cal']):
            with cols[i % 8]:
                c_col = "#8b0000" if any(db[(db['Nome'] == r['Capo']) & (db['Grado'] == "R5/R4")]['Nome']) else "#1b4d3e"
                p_col = "#8b0000" if any(db[(db['Nome'] == r['Pass']) & (db['Grado'] == "R5/R4")]['Nome']) else "#1b4d3e"
                st.markdown(f"""
                <div class="compact-card">
                    <div class="day-badge">GG {r['Giorno']}</div>
                    <div class="role-label">CAPOTRENO</div>
                    <div class="name-container"><div class="name-text" style="color:{c_col}; border-left-color:{c_col};">🤠 {r['Capo']}</div></div>
                    <div class="role-label">PASSEGGERO</div>
                    <div class="name-container"><div class="name-text" style="color:{p_col}; border-left-color:{p_col};">🐎 {r['Pass']}</div></div>
                </div>
                """, unsafe_allow_html=True)
