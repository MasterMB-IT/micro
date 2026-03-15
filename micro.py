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
        width: 100% !important; height: 50px !important;
        border-radius: 10px !important;
        font-family: 'Montserrat', sans-serif !important;
        font-weight: 900 !important; font-size: 1rem !important;
        text-transform: uppercase !important;
        border: 2px solid #2b1d0e !important;
    }
    .btn-genera button { background: linear-gradient(145deg, #d4a373, #b88655) !important; color: #2b1d0e !important; }
    .btn-resetta button { background: linear-gradient(145deg, #a44a3f, #7a3229) !important; color: white !important; }
    .btn-verifica button { background: #5bc0de !important; color: white !important; }
    .btn-assegna button { background: #28a745 !important; color: white !important; border: 3px solid #1e7e34 !important; }

    /* CARDS */
    .summary-card, .compact-card {
        background: #fdf5e6; border: 2px solid #5d4037;
        padding: 10px; border-radius: 8px; 
        color: #2b1d0e; margin-bottom: 10px;
        background-image: url('https://www.transparenttextures.com/patterns/paper-fibers.png');
    }
    .summary-card { height: 210px; }
    .compact-card { height: 140px; padding: 6px 4px; }

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

    .history-box {
        background: rgba(43, 29, 14, 0.8);
        border: 2px dashed #ffcc66;
        padding: 15px; border-radius: 10px;
        margin-top: 20px;
    }

    hr { border-top: 2px solid #ffcc66 !important; opacity: 0.6; }
    </style>
    """, unsafe_allow_html=True)

# --- DATABASE INIZIALE ---
def init_db():
    leaders = ["Hool (R5)", "MASTER (R4)", "Le 12 Scimmie (R4)", "Sagittarius A1 (R4)", "Starbetty (R4)", "PEPPE (R4)", "Ricky Around (R4)", "uncle g (R4)", "09ALEX24 (R4)", "ShinyPasta (R4)", "Wall 7 (R4)"]
    r3 = ["G Erry", "Uncle g brother", "Goz", "Ghandal", "Aryron", "Tricheco", "Maメツ", "NOVEMBERGENZ", "Lalla 96", "Whale Panda", "GennaroM", "EchoZero", "EDDward", "AMY", "Resilienza", "Ana Bunny", "Giuseppec84", "Benito Muschiolini", "Pandino19", "xFlotchy", "MX63", "holdfast", "Ghost", "BadBigBoss", "Stefano00000", "PakII", "BANDOLERO26", "BlOOdyBlade", "Whale hunter Levve", "Aresxxx", "KingGruffalo", "Hulkspakka", "Joseppone", "ImAde", "Nysbie", "LeFada13", "Skiteto", "SPio24", "TomEnergy", "Markus Defender", "Sho0t3r", "Wolf006", "Zokra", "perseusxxx", "Bendico", "Obbyy", "ArLes", "Fatz87", "cruel neve", "Trivellatore", "Osgh00", "Slowfia ABOH", "Pontatinatore", "27Francesco", "MissDrinks", "krompir", "MaledettO"]
    r2 = ["teomadh", "Bossnico", "Valecit", "FarmerHool", "camiiiii 08", "Doctor team", "Yass081", "Nuorifleming", "Vergabrio", "Frenk70", "Comandante Maveric", "Thor9000", "MrBolly", "BustaMaki", "S U C A", "StUnTmArK", "MONKEY D LUFFY 20", "CineSalentino", "Danylo98", "Ezechielefabianino", "BRNcommando", "LEONIDA", "elchicogyot", "erer1000", "Pupisnic", "Backfire1", "AnarchyBG", "Fabrizio1987", "JurdanS", "WiseR9", "Infinity8080"]
    data = [{"Nome": n, "Grado": "R5/R4"} for n in leaders] + [{"Nome": n, "Grado": "R3"} for n in r3] + [{"Nome": n, "Grado": "R2"} for n in r2]
    return pd.DataFrame(data)

# --- INIZIALIZZAZIONE SESSIONE ---
if 'players_db' not in st.session_state: st.session_state['players_db'] = init_db()
if 'history' not in st.session_state: st.session_state['history'] = []
if 'sel_mese' not in st.session_state: st.session_state['sel_mese'] = MESI_ITA[datetime.now().month - 1]
if 'sel_anno' not in st.session_state: st.session_state['sel_anno'] = 2026

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
    b1, b2, b3, b4 = st.columns(4)
    
    with b1:
        st.markdown('<div class="btn-genera">', unsafe_allow_html=True)
        if st.button("⚒️ GENERA"):
            pool_leaders = sel_leaders if sel_leaders else m_leaders
            pool_others = (sel_r3 if sel_r3 else m_r3) + (sel_r2 if sel_r2 else m_r2)
            random.shuffle(pool_leaders); random.shuffle(pool_others)
            num_gg = (pd.Timestamp(year=st.session_state['sel_anno'], month=MESI_ITA.index(st.session_state['sel_mese'])+1, day=1) + pd.offsets.MonthEnd(0)).day
            st.session_state['master_cal'] = []
            p_idx = 0
            for g in range(1, num_gg + 1):
                if g <= 11:
                    c, p = pool_leaders[(g-1)%len(pool_leaders)], pool_leaders[g%len(pool_leaders)]
                else:
                    c, p = pool_others[p_idx % len(pool_others)], pool_others[(p_idx + 1) % len(pool_others)]
                    p_idx += 2
                st.session_state['master_cal'].append({"Giorno": g, "Capo": c, "Pass": p})
        st.markdown('</div>', unsafe_allow_html=True)

    with b2:
        st.markdown('<div class="btn-verifica">', unsafe_allow_html=True)
        if st.button("🔍 VERIFICA DOPPIONI"):
            if 'master_cal' in st.session_state:
                doppioni = []
                for r in st.session_state['master_cal']:
                    if r['Capo'] == r['Pass']: doppioni.append(f"GG {r['Giorno']}: {r['Capo']} è sia Capo che Pass!")
                if doppioni: st.error("⚠️ DOPPIONI TROVATI:\n" + "\n".join(doppioni))
                else: st.success("✅ Tutto in regola! Nessun passeggero guida il proprio vagone.")
        st.markdown('</div>', unsafe_allow_html=True)

    with b3:
        st.markdown('<div class="btn-assegna">', unsafe_allow_html=True)
        if st.button("✅ ASSEGNAZIONE"):
            if 'master_cal' in st.session_state:
                entry = {
                    "data": f"{st.session_state['sel_mese']} {st.session_state['sel_anno']}",
                    "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M"),
                    "calendario": list(st.session_state['master_cal'])
                }
                st.session_state['history'].append(entry)
                st.success("📦 CALENDARIO CONGELATO IN CRONOLOGIA!")
        st.markdown('</div>', unsafe_allow_html=True)

    with b4:
        st.markdown('<div class="btn-resetta">', unsafe_allow_html=True)
        if st.button("🌵 RESET"):
            if 'master_cal' in st.session_state: del st.session_state['master_cal']
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    view_mode = st.toggle("🎞️ VISTA TOTALE (Diapositiva)", value=False)

# --- VISUALIZZAZIONE CALENDARIO ATTUALE ---
if 'master_cal' in st.session_state:
    st.markdown("<hr>", unsafe_allow_html=True)
    if not view_mode:
        t1, t2 = st.tabs(["🎴 VISTA EDITABILE", "📜 REGISTRO TESTUALE"])
        with t1:
            cols = st.columns(7)
            for i, r in enumerate(st.session_state['master_cal']):
                with cols[i % 7]:
                    c_col = "#8b0000" if any(db[(db['Nome'] == r['Capo']) & (db['Grado'] == "R5/R4")]['Nome']) else "#1b4d3e"
                    p_col = "#8b0000" if any(db[(db['Nome'] == r['Pass']) & (db['Grado'] == "R5/R4")]['Nome']) else "#1b4d3e"
                    st.markdown(f"""<div class="summary-card"><div class="day-badge">GG {r['Giorno']}</div>
                        <div class="role-label">CAPOTRENO</div><div class="name-container"><div class="name-text" style="color:{c_col};">🤠 {r['Capo']}</div></div>
                        <div class="role-label">PASSEGGERO</div><div class="name-container"><div class="name-text" style="color:{p_col};">🐎 {r['Pass']}</div></div>
                    """, unsafe_allow_html=True)
                    with st.popover("⚙️"):
                        nc = st.selectbox("Capo", all_names, index=all_names.index(r['Capo']), key=f"c_{i}")
                        np = st.selectbox("Pass", all_names, index=all_names.index(r['Pass']), key=f"p_{i}")
                        if st.button("Salva", key=f"s_{i}"):
                            st.session_state['master_cal'][i].update({"Capo": nc, "Pass": np}); st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)
        with t2:
            st.code("\n".join([f"GG {r['Giorno']}: {r['Capo']} -> {r['Pass']}" for r in st.session_state['master_cal']]))
    else:
        cols = st.columns(8)
        for i, r in enumerate(st.session_state['master_cal']):
            with cols[i % 8]:
                c_col = "#8b0000" if any(db[(db['Nome'] == r['Capo']) & (db['Grado'] == "R5/R4")]['Nome']) else "#1b4d3e"
                st.markdown(f"""<div class="compact-card"><div class="day-badge">GG {r['Giorno']}</div>
                    <div class="role-label">CAPOTRENO</div><div class="name-container"><div class="name-text" style="color:{c_col};">🤠 {r['Capo']}</div></div>
                    <div class="role-label">PASSEGGERO</div><div class="name-container"><div class="name-text">🐎 {r['Pass']}</div></div></div>
                """, unsafe_allow_html=True)

# --- SEZIONE CRONOLOGIA ---
if st.session_state['history']:
    st.markdown("<br><h2 style='color:#ffcc66; font-family:Rye;'>📜 CRONOLOGIA ASSEGNAZIONI</h2>", unsafe_allow_html=True)
    for idx, item in enumerate(reversed(st.session_state['history'])):
        with st.expander(f"📦 CALENDARIO: {item['data']} (Assegnato il {item['timestamp']})"):
            h_cols = st.columns(10)
            for j, hr in enumerate(item['calendario']):
                with h_cols[j % 10]:
                    st.markdown(f"<small><b>GG {hr['Giorno']}</b><br>{hr['Capo']}<br>↓<br>{hr['Pass']}</small>", unsafe_allow_html=True)
            if st.button(f"Elimina questo record", key=f"del_{idx}"):
                st.session_state['history'].pop(-(idx+1)); st.rerun()
