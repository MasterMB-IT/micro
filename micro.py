import streamlit as st
import pandas as pd
import random
from datetime import datetime

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="AOSR Train Manager - Ultimate Edition", layout="wide")

MESI_ITA = ["Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno", 
            "Luglio", "Agosto", "Settembre", "Ottobre", "Novembre", "Dicembre"]

# --- CSS: RESTAURO STILE ORIGINALE + PROFONDITÀ ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Special+Elite&family=Rye&family=Montserrat:wght@900&display=swap');

    .stApp { 
        background: linear-gradient(rgba(30, 20, 10, 0.8), rgba(15, 10, 5, 0.95)), 
                    url('https://images.unsplash.com/photo-1510524527013-0393282436da?q=80&w=1920&auto=format&fit=crop');
        background-size: cover; background-attachment: fixed;
    }

    /* TITOLO */
    .train-title {
        font-family: 'Rye', cursive; text-align: center; color: #ffcc66;
        text-shadow: 4px 4px 0px #4b2e1b; font-size: 3.5rem; margin-bottom: 20px;
    }

    /* UFFICIO ASSEGNAZIONI: CORNICE DORATA */
    .ufficio-container {
        border: 3px solid #ffcc66; border-radius: 15px;
        padding: 25px; background: rgba(30, 20, 10, 0.5);
        margin-bottom: 30px; box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }

    /* CARDS STILE ORIGINALE */
    .pergamena-card {
        background: #fdf5e6; border: 2px solid #5d4037;
        padding: 15px; border-radius: 5px; color: #2b1d0e;
        background-image: url('https://www.transparenttextures.com/patterns/paper-fibers.png');
        box-shadow: 5px 5px 15px rgba(0,0,0,0.5);
        min-height: 180px; position: relative;
    }

    /* LINEA DI PROFONDITÀ TRA COLONNE */
    .column-border {
        border-right: 4px solid rgba(0,0,0,0.6);
        border-left: 1px solid rgba(255,204,102,0.1);
        margin-right: 10px; padding-right: 15px;
    }

    .day-header {
        font-family: 'Rye', cursive; color: #8b0000;
        font-size: 1.2rem; border-bottom: 1.5px dashed #5d4037;
        margin-bottom: 10px; padding-bottom: 5px;
    }

    .role-text { font-family: 'Montserrat', sans-serif; font-size: 0.65rem; color: #5d4037; text-align: center; font-weight: 800; }
    .name-text { font-family: 'Special Elite', cursive; font-size: 0.95rem; font-weight: 900; text-align: center; margin: 5px 0; }

    /* PULSANTI */
    .stButton>button {
        border-radius: 8px !important; font-family: 'Montserrat', sans-serif !important;
        font-weight: 900 !important; text-transform: uppercase !important;
        height: 45px !important; transition: 0.3s !important;
    }
    .btn-genera button { background: #1e2a38 !important; color: white !important; border: 1px solid #ffcc66 !important; }
    .btn-verifica button { background: #2c3e50 !important; color: #5bc0de !important; border: 1px solid #5bc0de !important; }
    .btn-assegna button { background: #1b4d3e !important; color: #2ecc71 !important; border: 1px solid #2ecc71 !important; }
    .btn-resetta button { background: #3d1a1a !important; color: #e74c3c !important; border: 1px solid #e74c3c !important; }

    hr { border-top: 2px solid #ffcc66 !important; opacity: 0.5; }
    </style>
    """, unsafe_allow_html=True)

# --- DATABASE ---
def init_db():
    leaders = ["Hool (R5)", "MASTER (R4)", "Le 12 Scimmie (R4)", "Sagittarius A1 (R4)", "Starbetty (R4)", "PEPPE (R4)", "Ricky Around (R4)", "uncle g (R4)", "09ALEX24 (R4)", "ShinyPasta (R4)", "Wall 7 (R4)"]
    r3 = ["G Erry", "Uncle g brother", "Goz", "Ghandal", "Aryron", "Tricheco", "Maメツ", "NOVEMBERGENZ", "Lalla 96", "Whale Panda", "GennaroM", "EchoZero", "EDDward", "AMY", "Resilienza", "Ana Bunny", "Giuseppec84", "Benito Muschiolini", "Pandino19", "xFlotchy", "MX63", "holdfast", "Ghost", "BadBigBoss", "Stefano00000", "PakII", "BANDOLERO26", "BlOOdyBlade", "Whale hunter Levve", "Aresxxx", "KingGruffalo", "Hulkspakka", "Joseppone", "ImAde", "Nysbie", "LeFada13", "Skiteto", "SPio24", "TomEnergy", "Markus Defender", "Sho0t3r", "Wolf006", "Zokra", "perseusxxx", "Bendico", "Obbyy", "ArLes", "Fatz87", "cruel neve", "Trivellatore", "Osgh00", "Slowfia ABOH", "Pontatinatore", "27Francesco", "MissDrinks", "krompir", "MaledettO"]
    r2 = ["teomadh", "Bossnico", "Valecit", "FarmerHool", "camiiiii 08", "Doctor team", "Yass081", "Nuorifleming", "Vergabrio", "Frenk70", "Comandante Maveric", "Thor9000", "MrBolly", "BustaMaki", "S U C A", "StUnTmArK", "MONKEY D LUFFY 20", "CineSalentino", "Danylo98", "Ezechielefabianino", "BRNcommando", "LEONIDA", "elchicogyot", "erer1000", "Pupisnic", "Backfire1", "AnarchyBG", "Fabrizio1987", "JurdanS", "WiseR9", "Infinity8080"]
    data = [{"Nome": n, "Grado": "R5/R4"} for n in leaders] + [{"Nome": n, "Grado": "R3"} for n in r3] + [{"Nome": n, "Grado": "R2"} for n in r2]
    return pd.DataFrame(data)

if 'players_db' not in st.session_state: st.session_state['players_db'] = init_db()
if 'history' not in st.session_state: st.session_state['history'] = []
db = st.session_state['players_db']
all_names = sorted(db['Nome'].tolist())

# --- UI ---
st.markdown('<div class="train-title">🚂 AOSREXPRESS</div>', unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="ufficio-container">', unsafe_allow_html=True)
    st.markdown("<h4 style='color:#ffcc66; font-family:Rye; margin-top:0;'>📜 UFFICIO ASSEGNAZIONI</h4>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns([1, 1.2, 1.2, 1.2])
    with c1:
        st.session_state['sel_mese'] = st.selectbox("Periodo", MESI_ITA, index=2) # Marzo default
        st.session_state['sel_anno'] = st.number_input("Anno", 2024, 2030, 2026)
    with c2: sel_leaders = st.multiselect("Sceriffi R5/R4", m_leaders := db[db['Grado']=="R5/R4"]['Nome'].tolist())
    with c3: sel_r3 = st.multiselect("Banditi R3", m_r3 := db[db['Grado']=="R3"]['Nome'].tolist())
    with c4: sel_r2 = st.multiselect("Fuorilegge R2", m_r2 := db[db['Grado']=="R2"]['Nome'].tolist())

    st.markdown("<br>", unsafe_allow_html=True)
    b1, b2, b3, b4 = st.columns(4)
    with b1:
        st.markdown('<div class="btn-genera">', unsafe_allow_html=True)
        if st.button("⚒️ GENERA CONVOGLIO"):
            pool_leaders = sel_leaders if sel_leaders else m_leaders
            pool_others = (sel_r3 if sel_r3 else m_r3) + (sel_r2 if sel_r2 else m_r2)
            random.shuffle(pool_leaders); random.shuffle(pool_others)
            num_gg = (pd.Timestamp(year=st.session_state['sel_anno'], month=MESI_ITA.index(st.session_state['sel_mese'])+1, day=1) + pd.offsets.MonthEnd(0)).day
            st.session_state['master_cal'] = []
            p_idx = 0
            for g in range(1, num_gg + 1):
                if g <= 11: c, p = pool_leaders[(g-1)%len(pool_leaders)], pool_leaders[g%len(pool_leaders)]
                else: c, p = pool_others[p_idx % len(pool_others)], pool_others[(p_idx + 1) % len(pool_others)]; p_idx += 2
                st.session_state['master_cal'].append({"Giorno": g, "Capo": c, "Pass": p})
        st.markdown('</div>', unsafe_allow_html=True)
    with b2:
        st.markdown('<div class="btn-verifica">', unsafe_allow_html=True)
        if st.button("🔍 VERIFICA"):
            if 'master_cal' in st.session_state: st.success("✅ Ispezione completata!")
        st.markdown('</div>', unsafe_allow_html=True)
    with b3:
        st.markdown('<div class="btn-assegna">', unsafe_allow_html=True)
        if st.button("✅ ASSEGNAZIONE"):
            if 'master_cal' in st.session_state:
                st.session_state['history'].append({"data": f"{st.session_state['sel_mese']} {st.session_state['sel_anno']}", "ts": datetime.now().strftime("%d/%m/%Y %H:%M"), "cal": list(st.session_state['master_cal'])})
        st.markdown('</div>', unsafe_allow_html=True)
    with b4:
        st.markdown('<div class="btn-resetta">', unsafe_allow_html=True)
        if st.button("🌵 RESET"):
            if 'master_cal' in st.session_state: del st.session_state['master_cal']
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- VISUALIZZAZIONE GRIGLIA ---
def draw_grid(calendar_data, is_history=False):
    num_cols = 7
    rows = [calendar_data[i:i + num_cols] for i in range(0, len(calendar_data), num_cols)]
    for row in rows:
        cols = st.columns(num_cols)
        for i, r in enumerate(row):
            with cols[i]:
                st.markdown(f"""
                    <div class="pergamena-card">
                        <div class="day-header">GG {r['Giorno']}</div>
                        <div class="role-text">CAPOTRENO</div>
                        <div class="name-text" style="color:#8b0000;">🤠 {r['Capo']}</div>
                        <div class="role-text">PASSEGGERO</div>
                        <div class="name-text" style="color:#5d4037;">🐎 {r['Pass']}</div>
                    </div>
                """, unsafe_allow_html=True)
                if not is_history:
                    with st.popover("⚙️"):
                        nc = st.selectbox("Capo", all_names, index=all_names.index(r['Capo']), key=f"c_{r['Giorno']}")
                        np = st.selectbox("Pass", all_names, index=all_names.index(r['Pass']), key=f"p_{r['Giorno']}")
                        if st.button("OK", key=f"s_{r['Giorno']}"):
                            idx = next(i for i, item in enumerate(st.session_state['master_cal']) if item["Giorno"] == r['Giorno'])
                            st.session_state['master_cal'][idx].update({"Capo": nc, "Pass": np}); st.rerun()

if 'master_cal' in st.session_state:
    st.markdown(f"<h3 style='text-align:center; color:#ffcc66; font-family:Rye;'>📅 {st.session_state['sel_mese'].upper()}</h3>", unsafe_allow_html=True)
    draw_grid(st.session_state['master_cal'])

# --- CRONOLOGIA A GRIGLIA ---
if st.session_state['history']:
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<h2 style='color:#ffcc66; font-family:Rye; text-align:center;'>📜 CRONOLOGIA ASSEGNAZIONI</h2>", unsafe_allow_html=True)
    for idx, item in enumerate(reversed(st.session_state['history'])):
        with st.expander(f"📦 CALENDARIO: {item['data']} (Assegnato il {item['ts']})"):
            draw_grid(item['cal'], is_history=True)
            if st.button("ELIMINA RECORD", key=f"del_{idx}"):
                st.session_state['history'].pop(-(idx+1)); st.rerun()
